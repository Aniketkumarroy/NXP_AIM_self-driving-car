#!/usr/bin/env python3
# import os
# import sys
import copy
import os
from time import time
# import re
# import importlib
import numpy as np
import rclpy
from rclpy.executors import MultiThreadedExecutor
from example_interfaces.srv import AddTwoInts
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import Parameter
from rcl_interfaces.msg import ParameterType
from rcl_interfaces.msg import ParameterDescriptor
import sensor_msgs.msg
from std_msgs.msg import String, Float32 # will be used in creating a publisher
import nxp_cup_interfaces.msg
from nxp_cup_vision.detector import yolov5s, AvoidObstacles
from datetime import datetime
from cv_bridge import CvBridge
# from rclpy.qos import QoSProfile
import cv2
if cv2.__version__ < "4.0.0":
    raise ImportError("Requires opencv >= 4.0, "
                      "but found {:s}".format(cv2.__version__))

class NXPTrackVision(Node):

    def __init__(self):
        
        super().__init__("nxp_track_vision")

        # Get paramaters or defaults
        pyramid_down_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_INTEGER,
            description='Number of times to pyramid image down.')

        camera_image_topic_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Camera image topic.')
        
        debug_image_topic_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Run in debug mode and publish to debug image topic')

        namespace_topic_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_STRING,
            description='Namespaceing if needed.')

        mask_ratio_array_descriptor = ParameterDescriptor(
            type=ParameterType.PARAMETER_DOUBLE_ARRAY,
            description='Array for mask ratio')
        
        self.declare_parameter("pyramid_down", 2, 
            pyramid_down_descriptor)
        
        self.declare_parameter("camera_image", "Pixy2CMUcam5_sensor", 
            camera_image_topic_descriptor)
        
        self.declare_parameter("debug_image", "", 
            debug_image_topic_descriptor)

        self.declare_parameter("namespace", "", 
            namespace_topic_descriptor)

        self.declare_parameter("mask_ratio_array", [1.0, 0.5], 
            mask_ratio_array_descriptor)

        self.pyrDown = self.get_parameter("pyramid_down").value

        self.cameraImageTopic = self.get_parameter("camera_image").value

        self.debugImageTopic = self.get_parameter("debug_image").value

        self.namespaceTopic = self.get_parameter("namespace").value

        self.mask_ratio_array = self.get_parameter("mask_ratio_array").value


        # self.model = yolov5s("/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/best.pt", "/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/classes.txt")
        self.imgshape = (936,1296) # size of the image as defined in nxp_cupcar.sdf.jinja
        self.smallsize = (self.imgshape[0]//2,self.imgshape[1]//2) # reducinng image size since we are not processing such large image
        self.widthratio = int(0.35*self.smallsize[1]) # this is the sidewise width to be taken from the image to know the sidewise background(whether its road or not)
        self.lower = np.array([43,137,120]) # array of lower end values of hue, sat and val for white colour segmantation
        self.upper = np.array([62,222,255]) # array of higher end values of hue, sat and val for white colour segmantation
        self.lower1 = np.array([15,77,60]) # for bumpy road
        self.upper1 = np.array([40,178,185]) # for bumpy road
        self.lower2 = np.array([130,177,208]) # for overbridge
        self.upper2 = np.array([147,201,255]) # for overbridge
        self.lower3 = np.array([95,165,145]) # for loop overbridge
        self.upper3 = np.array([154,210,200]) # for loop overbridge
        (self.h,self.w) = self.smallsize
        pts1 = np.array([[0,268],[self.w,268],[514,0],[142,0]],np.float32) # this are the points of the road boundary as viewed by pixy camera(which will be trapezium)
        pts2 = np.array([  [0,self.h], [self.w,self.h],  [self.w,0],  [0,0]],  np.float32)
        self.mat=cv2.getPerspectiveTransform(pts1,pts2) # this is the transformation matrix to transform our image to bird's eye view
        

        #setup CvBridge
        self.bridge = CvBridge()
        
        #Rectangualr area to remove from image calculation to 
        # eliminate the vehicle. Used as ratio of overall image width and height
        # "width ratio,height ratio"
        self.maskRectRatioWidthHeight = np.array([float(self.mask_ratio_array[0]),float(self.mask_ratio_array[1])])
        
        #Bool for generating and publishing the debug image evaluation
        self.debug = False
        
        if self.debugImageTopic != "":
            self.debug = True

        self.timeStamp = self.get_clock().now().nanoseconds
        
        #Pixy image size parameters
        self.pixyImageWidth = 72
        self.pixyImageHeight = 52
        
        #Subscribers
        self.imageSub = self.create_subscription(sensor_msgs.msg.Image, 
            '/{:s}/image_raw'.format(self.cameraImageTopic), 
            self.pixyImageCallback, 
            qos_profile_sensor_data)

        # self.frontcam = self.create_subscription(sensor_msgs.msg.Image, 
        #     '/frontcam/image_raw', 
        #     self.FrontCamCallback, 
        #     qos_profile_sensor_data)

        #Publishers
        self.debugDetectionImagePub = self.create_publisher(sensor_msgs.msg.Image,
            '/{:s}'.format(self.debugImageTopic), 0)

        self.imageshape = self.create_publisher(String,"/middle",0) # our subscriber
        self.string = String() # this variable will store our message for subscribing
        
        self.PixyVectorPub = self.create_publisher(nxp_cup_interfaces.msg.PixyVector,
            '{:s}/PixyVector'.format(self.namespaceTopic), 0)
        
        #Only used for debugging line finding issues
        self.lineFindPrintDebug = False
        self.lineMethodsUsedCount = [0, 0, 0, 0, 0, 0, 0]
        self.lineMethodUsed = 0

        (self.pX0, self.pY0, self.pX1, self.pY1) = (0,1,2,3)
        
        #Testing
        self.useBogusData=False
        self.publishSecondVector=True
        self.sortRightToLeft=False
        self.switchVectorPoints=True
        self.stage=0
        self.startTime=0
        self.testAllConfigs=False

        self.bogusOffsetNumber = 3
          
        if self.sortRightToLeft:
            self.bogusDataTest=[[int((self.pixyImageWidth*0.8)+
                self.bogusOffsetNumber),0,
                int(self.pixyImageWidth*0.8),self.pixyImageHeight],
                [int((self.pixyImageWidth*0.2)-self.bogusOffsetNumber),0,
                int(self.pixyImageWidth*0.2),self.pixyImageHeight]]
        else:
            self.bogusDataTest=[[int((self.pixyImageWidth*0.2)+
                self.bogusOffsetNumber),0,
                int(self.pixyImageWidth*0.2),self.pixyImageHeight],
                [int((self.pixyImageWidth*0.8)-self.bogusOffsetNumber),0,
                int(self.pixyImageWidth*0.8),self.pixyImageHeight]]

        if self.switchVectorPoints:
            (self.pX0, self.pY0, self.pX1, self.pY1) = (2,3,0,1)

    def findLines(self, passedImage):
        
        self.timeStamp = self.get_clock().now().nanoseconds
        
        #Testing
        if self.testAllConfigs:
            if self.stage == 0:
                self.get_logger().info("\nPublishing lines Left to Right, points NOT switched")
                self.sortRightToLeft=False
                self.switchVectorPoints=False
                self.startTime = self.timeStamp
                self.stage = 1
            elif (((self.timeStamp - self.startTime) > 30*1e6) and (self.stage == 1)):
                self.sortRightToLeft=False
                self.switchVectorPoints=True
                self.stage = 2
                self.get_logger().info("\nPublishing lines Left to Right, points ARE switched")
            elif (((self.timeStamp - self.startTime) > 40*1e6) and (self.stage == 2)):
                self.sortRightToLeft=True
                self.switchVectorPoints=False
                self.stage = 3
                self.get_logger().info("\nPublishing lines Right to Left, points NOT switched")
            elif (((self.timeStamp - self.startTime) > 50*1e6) and (self.stage == 3)):
                self.sortRightToLeft=True
                self.switchVectorPoints=True
                self.stage = 4
                self.get_logger().info("\nPublishing lines Right to Left, points ARE switched")

        
        #convert image to grayscale
        # passedImageGray = cv2.cvtColor(passedImage,cv2.COLOR_BGR2GRAY)
        
        #Image dimensions
        imageHeight, imageWidth = passedImage.shape[:2]
        
        #Threshold image black and white
        HSV = cv2.cvtColor(passedImage,cv2.COLOR_BGR2HSV)
        passedImageGrayThresh = cv2.inRange(HSV,np.array([0, 0, 46]),np.array([179, 1, 55]))
        
        #Create image mask background
        maskWhite = np.ones(passedImageGrayThresh.shape[:2], dtype="uint8") * 255
        
        #calculate points to be masked based on provided ratio
        maskVehicleBoxTopLeftXY = (int(imageWidth*(1.0-self.maskRectRatioWidthHeight[0])/2.0), 
            int(imageHeight*(1.0-self.maskRectRatioWidthHeight[1])))
        
        #calculate points to be masked based on provided ratio
        maskVehicleBoxBottomRightXY = (int(imageWidth*(1.0+self.maskRectRatioWidthHeight[0])/2.0), 
            int(imageHeight))
        
        maskVehicle = cv2.rectangle(maskWhite,maskVehicleBoxTopLeftXY,
            maskVehicleBoxBottomRightXY,color=0,thickness=-1)
        
        #Mask out the area of the vehicle
        passedImageGrayThreshMasked = cv2.bitwise_and(passedImageGrayThresh, 
            passedImageGrayThresh, mask=maskVehicle)
        
        #Find contours
        cnts, hierarchy = cv2.findContours(passedImageGrayThreshMasked.copy(),
            cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        returnedImageDebug=passedImage

        #Max number of found contours to process based on area of return, largest returned first
        maxCnt = 2
        if len (cnts) < maxCnt:
            maxCnt = len(cnts)
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0:maxCnt]

        #Take largest contours and sort left to right
        if len (cnts) > 1:
            boundingBoxes = [cv2.boundingRect(c) for c in cnt]
            (cnt, boundingBoxes) = zip(*sorted(zip(cnt, boundingBoxes),
                key=lambda b:b[1][0], reverse=self.sortRightToLeft))

        #Initialize and/or clear existing found line vector array
        pixyScaledVectorArray = np.empty([0,4], int)

        #Used to determine what line is mapped in message from debug image
        lineNumber=0

        #Loop through contours
        for cn in cnt:

            if self.debug:
                #Paint all the areas found in the contour
                cv2.fillPoly(returnedImageDebug,pts=[cn],color=(0,0,255))
            
            #Find lines from contours using least square method
            [vectorX,vectorY,linePointX,linePointY] = cv2.fitLine(cn,cv2.DIST_L2,0,0.01,0.01)
            
            if (linePointX >= 1.0) and (linePointY >= 1.0):
                #Easy avoid divide by zero
                if vectorY == 0:
                    vectorY = 1e-4
                if vectorX == 0:
                    vectorX = 1e-4

                #Calculate line points to see if they exceeds any bounds of the image, correct if they do
                topLeftX = int((-linePointY*vectorX/vectorY)+linePointX)
                bottomRightX = int(((imageHeight-linePointY)*vectorX/vectorY)+linePointX)
                topLeftY = 0
                bottomRightY = imageHeight
                self.lineMethodUsed = 0
                
                if (topLeftX <= 0) and (bottomRightX > imageWidth):
                    self.lineMethodUsed = 1
                    topLeftY = int(((-linePointX)*vectorY/vectorX)+linePointY)
                    bottomRightY = int(((imageWidth-linePointX)*vectorY/vectorX)+linePointY)
                    topLeftX = 0
                    bottomRightX = imageWidth

                elif (topLeftX > imageWidth) and (bottomRightX < 0):
                    self.lineMethodUsed = 2
                    topLeftY = int(((imageWidth-linePointX)*vectorY/vectorX)+linePointY)
                    bottomRightY = int(((-linePointX)*vectorY/vectorX)+linePointY)
                    topLeftX = imageWidth
                    bottomRightX = 0

                elif (topLeftX <= 0) and (bottomRightX < imageWidth):
                    self.lineMethodUsed = 3
                    topLeftY = int(((-linePointX)*vectorY/vectorX)+linePointY)
                    bottomRightY = imageHeight
                    topLeftX = 0
                    bottomRightX = int(((imageHeight-linePointY)*vectorX/vectorY)+linePointX)

                elif (topLeftX > 0) and (bottomRightX > imageWidth):
                    self.lineMethodUsed = 4
                    topLeftY = 0
                    bottomRightY = int(((imageWidth-linePointX)*vectorY/vectorX)+linePointY)
                    topLeftX = int((-linePointY*vectorX/vectorY)+linePointX)
                    bottomRightX = imageWidth

                elif (topLeftX > imageWidth) and (bottomRightX > 0):
                    self.lineMethodUsed = 5
                    topLeftY = imageHeight
                    bottomRightY = int(((imageWidth-linePointX)*vectorY/vectorX)+linePointY)
                    topLeftX = int(((imageHeight-linePointY)*vectorX/vectorY)+linePointX)
                    bottomRightX = imageWidth

                elif (topLeftX < imageWidth) and (bottomRightX < 0):
                    self.lineMethodUsed = 6
                    topLeftY = int((-linePointX*vectorY/vectorX)+linePointY)
                    bottomRightY = 0
                    topLeftX = 0
                    bottomRightX = int((linePointY)*(-vectorX/vectorY)+linePointX)
                
                
                #Extra safety
                if topLeftX < 0:
                    topLeftX=0
                elif topLeftX > imageWidth:
                    topLeftX=imageWidth
                if bottomRightX < 0:
                    bottomRightX=0
                elif bottomRightX > imageWidth:
                    bottomRightX=imageWidth
                if topLeftY < 0:
                    topLeftY=0
                elif topLeftY > imageHeight:
                    topLeftY=imageHeight
                if bottomRightY < 0:
                    bottomRightY=0
                elif bottomRightY > imageHeight:
                    bottomRightY=imageHeight

                #Add line method used to array count
                self.lineMethodsUsedCount[self.lineMethodUsed]+=1
                
                #Scale into Pixy camera units
                topLeftXScaled = int(topLeftX*(self.pixyImageWidth/imageWidth))
                bottomRightXScaled = int(bottomRightX*(self.pixyImageWidth/imageWidth))
                topLeftYScaled = int(topLeftY*(self.pixyImageWidth/imageWidth))
                bottomRightYScaled = int(bottomRightY*(self.pixyImageWidth/imageWidth))

                if self.lineFindPrintDebug:
                    self.get_logger().info('\n\nlineMethodUsed:{:d},lineMethodsUsedCount:{:s}'.format(
                        self.lineMethodUsed,str(self.lineMethodsUsedCount)))
                    self.get_logger().info('vectorX:{:f},vectorY:{:f},linePointX:{:f},linePointY:{:f}'.format(
                        float(vectorX),float(vectorY),float(linePointX),float(linePointY)))
                    self.get_logger().info('topLeftX:{:d},topLeftY:{:d},bottomRightX:{:d},bottomRightY:{:d}'.format(
                        topLeftX,topLeftY,bottomRightX,bottomRightY))
                    returnedImageDebug = cv2.line(returnedImageDebug,(topLeftX,topLeftY),
                        (bottomRightX,bottomRightY),(255,128,128),2)

                #Append found line points to pixy found line vector array
                pixyScaledVectorArray = np.append(pixyScaledVectorArray,
                    np.array([[topLeftXScaled,topLeftYScaled,bottomRightXScaled,bottomRightYScaled]]),axis=0)
                #Increment line number
                lineNumber += 1
        
        #Testing
        if self.useBogusData:
            if self.sortRightToLeft:
                self.bogusDataTest=[[int((self.pixyImageWidth*0.8)+
                    self.bogusOffsetNumber),0,
                    int(self.pixyImageWidth*0.8),self.pixyImageHeight],
                    [int((self.pixyImageWidth*0.2)-self.bogusOffsetNumber),0,
                    int(self.pixyImageWidth*0.2),self.pixyImageHeight]]
            else:
                self.bogusDataTest=[[int((self.pixyImageWidth*0.2)+
                    self.bogusOffsetNumber),0,
                    int(self.pixyImageWidth*0.2),self.pixyImageHeight],
                    [int((self.pixyImageWidth*0.8)-self.bogusOffsetNumber),0,
                    int(self.pixyImageWidth*0.8),self.pixyImageHeight]]

            if self.switchVectorPoints:
                (self.pX0, self.pY0, self.pX1, self.pY1) = (2,3,0,1)
            else:
                (self.pX0, self.pY0, self.pX1, self.pY1) = (0,1,2,3)

            pixyScaledVectorArray = np.array(self.bogusDataTest)

        if self.debug:
            #Border for vehicle mask
            returnedImageDebug = cv2.rectangle(returnedImageDebug,maskVehicleBoxTopLeftXY,
                maskVehicleBoxBottomRightXY, color=(128,128,0),thickness=3)

            #Calcualte background for pixy image space
            debugPixyMessageTopLeftXY = (int((imageWidth/2)-(self.pixyImageWidth/2)),
                int((imageHeight/2)-(self.pixyImageHeight/2)))

            #Create background for pixy image space
            returnedImageDebug = cv2.rectangle(returnedImageDebug,debugPixyMessageTopLeftXY,
                ((debugPixyMessageTopLeftXY[0]+self.pixyImageWidth),
                (debugPixyMessageTopLeftXY[1]+self.pixyImageHeight)),(0,255,0),-1)
            
            for lineNumber in range(len(pixyScaledVectorArray)):
                #Draw the found line in image space
                returnedImageDebug = cv2.line(returnedImageDebug,
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][0],
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][1]),
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][2],
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][3]),
                    (255,128,128),1)
                
                #Draw box point for top left XY for Pixy space debug image
                returnedImageDebug = cv2.rectangle(returnedImageDebug,
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][0]-1, 
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][1]-1),
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][0]+1, 
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][1]+1),
                    (0,0,255),-1)
                
                #Draw box point for bottom right XY for Pixy space debug image
                returnedImageDebug = cv2.rectangle(returnedImageDebug,
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][2]-1,
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][3]-1),
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][2]+1, 
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][3]+1),
                    (0,0,255),-1)
                
                #Write text for top left XY for Pixy space debug image
                returnedImageDebug = cv2.putText(
                    returnedImageDebug, '{:d},{:d}'.format(
                    pixyScaledVectorArray[lineNumber][0],pixyScaledVectorArray[lineNumber][1]), 
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][0]-20+(20*lineNumber), 
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255,0,0), 1, cv2.LINE_AA)
                
                #Write text for bottom right XY for Pixy space debug image
                returnedImageDebug = cv2.putText(returnedImageDebug, '{:d},{:d}'.format(
                    pixyScaledVectorArray[lineNumber][2],pixyScaledVectorArray[lineNumber][3]),
                    (debugPixyMessageTopLeftXY[0]+pixyScaledVectorArray[lineNumber][2]-20+(20*lineNumber), 
                    debugPixyMessageTopLeftXY[1]+pixyScaledVectorArray[lineNumber][3]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255,0,0), 1, cv2.LINE_AA)

                #Write the line number for message
                returnedImageDebug = cv2.putText(returnedImageDebug, 'm{:d}'.format(
                    lineNumber),
                    (int((pixyScaledVectorArray[lineNumber][0]+
                    pixyScaledVectorArray[lineNumber][2])/2.0+
                    debugPixyMessageTopLeftXY[0]-20+(20*lineNumber)),
                    int((pixyScaledVectorArray[lineNumber][1]+
                    pixyScaledVectorArray[lineNumber][3])/2.0+
                    debugPixyMessageTopLeftXY[1])), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,255), 1, cv2.LINE_AA)

        #Pixy message for publication
        if (len(pixyScaledVectorArray) == 0):
            PixyVector_msg = nxp_cup_interfaces.msg.PixyVector()
            PixyVector_msg.timestamp = int(self.timeStamp)
            PixyVector_msg.m0_x0 = int(0)
            PixyVector_msg.m0_y0 = int(0)
            PixyVector_msg.m0_x1 = int(0)
            PixyVector_msg.m0_y1 = int(0)
            PixyVector_msg.m1_x0 = int(0)
            PixyVector_msg.m1_y0 = int(0)
            PixyVector_msg.m1_x1 = int(0)
            PixyVector_msg.m1_y1 = int(0)
            self.PixyVectorPub.publish(PixyVector_msg)
        if (len(pixyScaledVectorArray) > 0):
            PixyVector_msg = nxp_cup_interfaces.msg.PixyVector()
            PixyVector_msg.timestamp = int(self.timeStamp)
            PixyVector_msg.m0_x0 = int(pixyScaledVectorArray[0][self.pX0])
            PixyVector_msg.m0_y0 = int(pixyScaledVectorArray[0][self.pY0])
            PixyVector_msg.m0_x1 = int(pixyScaledVectorArray[0][self.pX1])
            PixyVector_msg.m0_y1 = int(pixyScaledVectorArray[0][self.pY1])
            PixyVector_msg.m1_x0 = int(0)
            PixyVector_msg.m1_y0 = int(0)
            PixyVector_msg.m1_x1 = int(0)
            PixyVector_msg.m1_y1 = int(0)
            if (len(pixyScaledVectorArray) > 1) and self.publishSecondVector:
                PixyVector_msg.m1_x0 = int(pixyScaledVectorArray[1][self.pX0])
                PixyVector_msg.m1_y0 = int(pixyScaledVectorArray[1][self.pY0])
                PixyVector_msg.m1_x1 = int(pixyScaledVectorArray[1][self.pX1])
                PixyVector_msg.m1_y1 = int(pixyScaledVectorArray[1][self.pY1])
            self.PixyVectorPub.publish(PixyVector_msg)

        return(returnedImageDebug)
      
    
    def pixyImageCallback(self, data):
        
        # Scene from subscription callback
        scene = self.bridge.imgmsg_to_cv2(data, "bgr8")

        #deep copy and pyramid down image to reduce resolution
        scenePyr = copy.deepcopy(scene)
        if self.pyrDown > 0:
            for i in range(self.pyrDown):
                scenePyr = cv2.pyrDown(scenePyr)
        sceneDetect = copy.deepcopy(scenePyr)

        #find lines function
        sceneDetected = self.findLines(sceneDetect)
        
        if self.debug:
            #publish debug image
            msg = self.bridge.cv2_to_imgmsg(sceneDetected, "bgr8")
            msg.header.stamp = data.header.stamp
            self.debugDetectionImagePub.publish(msg)
        threshold = 210
        smallimage = cv2.resize(scene,(self.smallsize[1],self.smallsize[0])) # grabbing our image(resizing it since will not use that large image)
        hsv = cv2.cvtColor(smallimage,cv2.COLOR_BGR2HSV) # converting to hsv
        mask1 = cv2.inRange(hsv,self.lower,self.upper) # creating mask of our image for white colour(road segmentation)
        mask2 = cv2.inRange(hsv,self.lower1,self.upper1)
        mask3 = cv2.inRange(hsv,self.lower2,self.upper2)
        mask4 = cv2.inRange(hsv,self.lower3,self.upper3)
        mask = cv2.addWeighted(mask1, 1.0, mask2, 1.0, 0)
        mask = cv2.addWeighted(mask, 1.0, mask3, 1.0, 0)
        mask = cv2.addWeighted(mask, 1.0, mask4, 1.0, 0)
        transform=cv2.warpPerspective(mask,self.mat,(self.w,self.h)) # transforming to bird's eye view
        left = transform[:,:self.widthratio] # grabbing left most region of our image
        right = transform[:,self.smallsize[1]-self.widthratio:] # grabbing right most region of our image

        img2 = transform[317:418,289:359]
        img2 = img2/255
        count = int(np.sum(img2==0)>0)


        img_left = transform[338:398, 184:224]
        img_left = img_left/255
        left_count = int(np.sum(img_left==0))
        img_right = transform[338:398, 424:464]
        img_right = img_right/255
        right_count = int(np.sum(img_right==0))
        move = 0
        if (right_count>left_count):
            move = 1
        else:
            move = -1
        # self._logger.info(str(count))
        # avoid_cones_tranform = transform[100:, 230:470]
        # avoid_cones_tranform_left = avoid_cones_tranform[:,:int(avoid_cones_tranform.shape[1]/2)] 
        # avoid_cones_tranform_right = avoid_cones_tranform[:,int(avoid_cones_tranform.shape[1]/2):] 
        # cones_left = np.where(avoid_cones_tranform_left <= threshold, 0, 1) # we want to know how many white pixels are there(how much area is under road)
        # cones_right = np.where(avoid_cones_tranform_right <= threshold, 0, 1)
        # cones_s = (cones_left.shape[0])*(cones_left.shape[1])
        # left_pid_send = np.sum(cones_left)/cones_s
        # right_pid_send = np.sum(cones_right)/cones_s

        # cv2.imshow("mask",mask)
        # cv2.imshow("avoid_cones_tranform",avoid_cones_tranform)

        # cv2.imshow("tranform",transform)
        # cv2.waitKey(1)

        #For bumpy Road

        bumpy_road_transform = cv2.warpPerspective(mask2,self.mat,(self.w,self.h))
        is_bumpy_road = int(np.sum(bumpy_road_transform==255)>50000)
        steer_according_to_black_on_bumpy = count*move*is_bumpy_road

        avoid_cones_tranform = transform[268:, 224:424]
        # gray = cv2.cvtColor(avoid_cones_tranform, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(avoid_cones_tranform, 50, 255, cv2.THRESH_BINARY_INV)

        cont,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        right_pid_send = 0
        left_pid_send = 0
        for cnt in cont:

            M = cv2.moments(cnt)
            cx, cy = int(M["m10"]/(M["m00"] + 1e-7)), int(M["m01"]/(M["m00"] + 1e-7))
            l = cv2.arcLength(cnt, True)
            corners = cv2.approxPolyDP(cnt, 0.01*l, True)

            if len(corners) >= 6:
                if cx<avoid_cones_tranform.shape[1]/2:
                    left_pid_send += 1
                else:
                    right_pid_send += 1


        # avoid_cones_tranform_left = avoid_cones_tranform[:,:int(avoid_cones_tranform.shape[1]/2)] 
        # avoid_cones_tranform_right = avoid_cones_tranform[:,int(avoid_cones_tranform.shape[1]/2):] 
        # cones_left = np.where(avoid_cones_tranform_left <= threshold, 0, 1) # we want to know how many white pixels are there(how much area is under road)
        # cones_right = np.where(avoid_cones_tranform_right <= threshold, 0, 1)
        # cones_s = (cones_left.shape[0])*(cones_left.shape[1])
        # left_pid_send = np.sum(cones_left)/cones_s
        # right_pid_send = np.sum(cones_right)/cones_s
        # cv2.imshow("avoid_cones_tranform",avoid_cones_tranform)
        # cv2.imshow("transform_SELF_NOW",mask)
       
        # cv2.imshow("transform_the_image", transform)
        # cv2.imshow("transform",transform)

        img22 = transform[370:440,200:400]
        img22 = img22/255
        count2 = int(np.sum(img22==0)>0)


        img_left2 = transform[370:440, 170:200]
        img_left2 = img_left2/255
        left_count2 = int(np.sum(img_left2==0))
        img_right2 = transform[370:440, 400:430]
        img_right2 = img_right2/255
        right_count2 = int(np.sum(img_right2==0))
        move2 = 0
        if (right_count2>left_count2):
            move2 = 1
        else:
            move2 = -1
        

        left = np.where(left <= threshold, 0, 1) # we want to know how many white pixels are there(how much area is under road)
        right = np.where(right <= threshold, 0, 1) # we want to know how many white pixels are there(how much area is under road)
        s = (left.shape[0])*(left.shape[1]) # total no. of pixels
        self.string.data = f"{np.sum(left)/s}%{np.sum(right)/s}%{left_pid_send}%{right_pid_send}%{count}%{move}%{steer_according_to_black_on_bumpy}%{is_bumpy_road}%{count2*move2}" # encripting the average white pixel density of left and right side to our message
        self.imageshape.publish(self.string) # publishing message

    # def avoid_cones(self)


class YoloNode(Node):

    def __init__(self):

        super().__init__("YoloNode")
        self.model = yolov5s("/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/best (1).pt", "/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/classes.txt", confidence_threshold=0.5)
        self.avoid = AvoidObstacles("/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/avoid_threshold.txt", "/home/pranay/ros2ws/src/nxp_cup_vision/nxp_cup_vision/classes.txt")
        self.bridge = CvBridge()
        self.frontcam = self.create_subscription(sensor_msgs.msg.Image, '/frontcam/image_raw', self.FrontCamCallback, qos_profile_sensor_data)
        self.YoloV5Steer = self.create_publisher(Float32,'/yolov5_steer', 0)
        self.TrafficSign = self.create_publisher(Float32,'/traffic_sign', 0)

        self.vounter = 0
        # self.turn_clint = self.create_client(AddTwoInts, "/turn")
        # while not self.turn_clint.wait_for_service(timeout_sec=1.0):
            # self.get_logger().info("waiting for /turn service")
        # self.req = AddTwoInts.Request()
        self.Traffic = Float32()
        self.yolo_steer = Float32()


        self.pick = lambda X, y: [i[y] for i in X]
        self.min_no_of_frame = 5
        self.max_no_of_frames_to_avoid = 5

        self.no_of_frames_right = 0
        self.no_of_frames_left = 0
        self.no_of_frames_not_right = 0
        self.no_of_frames_not_left = 0
        self.max_no_of_pings = 10
        self.c = 0 # traffic sign
        self.c1 = 0 # traffic light

        self.traffic_sign = 10 # [-1, 0, 1, 10, -5, 5, -10] <==> [right, stop, left, move, stop due to trafficlight, move due to trafficlight, no of barricades >= 2]
        self.start_time = datetime.now().timestamp()

        self.detected_objects = []

        self.no_of_barricades = 0
        self.c2 = 0 # barricades >= 2

        self.no_of_cones = 0
        self.c3 = 0



        self.stop_frames = 0
        self.not_stop_frames = 0
        self.min_no_stop_frames = 3
        self.stop_car = False
        self.stop_sign_ratio = 0


    # def turn_request(self, a, b):

    #     self.req.a = a
    #     self.req.b = b
    #     self.future = self.turn_clint.call_async(self.req)
    #     rclpy.spin_until_future_complete(self, self.future)
    #     return self.future.result()



    def FrontCamCallback(self, data):

        self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.img = cv2.resize(self.img, None,fx=0.5, fy=0.5)
        # self.traffic_sign = 10



        initial = time()

        # cv2.imwrite(f"/home/pranay/green_loght/Green_Light_{self.vounter}.jpg", self.img)
        # self.vounter += 1
        self.model.detect(self.img)
        self.detected_objects = self.pick(self.model.detections, 0)
        steer = self.avoid.steer(self.img, self.model.detections)
        # self.get_logger().info(f"{-round(steer,3)}")
        self.yolo_steer.data = float(steer)
        self.YoloV5Steer.publish(self.yolo_steer)





        # this code is for traffic sign detection
        self.traffic_sign_frame_counter()
        self.barricade_counter()
        self.cones_counter()

        if self.no_of_barricades >= 2:
            self.traffic_sign = -10
        
        if self.traffic_sign == -10:
            self.c2 += 1
            if self.c2 >= self.max_no_of_pings:
                self.traffic_sign = 10

        if self.no_of_cones >= 3:
            self.traffic_sign = -20
        # else:
        #     self.traffic_sign = 10
        
        if self.traffic_sign == -20:
            if self.no_of_cones <= 0:
                self.traffic_sign = 10

        

        # self.get_logger().info(f"{self.no_of_frames_left}  {self.no_of_frames_right}  {self.traffic_sign}")
        if self.traffic_sign == 1 or self.traffic_sign == -1:
            self.c += 1
            if self.c >= self.max_no_of_pings:
                self.traffic_sign = 10
                self.c = 0
                self.no_of_frames_left = 0
                self.no_of_frames_right = 0
                self.no_of_frames_not_left = 0
                self.no_of_frames_not_right = 0
        # end of traffic sign detection code

        msg = self.traffic_light()

        if len(msg) > 0 and (self.traffic_sign != 5 and self.traffic_sign != -5):
            if msg == "stop":
                self.traffic_sign = -5
                self.get_logger().info("ooooooooooooooooooooooooooooooooooooooooo")
            if msg == "go":
                self.traffic_sign = 5

        if self.traffic_sign == 5:# or self.traffic_sign == -5:
            self.c1 += 1
            if self.c1 >= self.max_no_of_pings:
                self.traffic_sign = 10
                self.c1 = 0

        if self.traffic_sign == -5:
            if not self.red():
                self.traffic_sign = 5
                self.get_logger().info("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")


        if not self.stop_car:
            self.stop_frames_counter()
            self.stop()
        else:
            self.traffic_sign = 0


        if not self.stop_car:
            self.stop_frames_counter()
            self.stop()
        else:
            self.traffic_sign = 0


        self.Traffic.data = float(self.traffic_sign)
        self.TrafficSign.publish(self.Traffic)
        # self.avoid_moving_obstacles()

        # self.traffic_light()
        
        # self._logger.info(str(self.traffic_sign))
        
        
        t = time() - initial
        self.detected_img = self.model.show_on_image(self.img, 1/t)
        cv2.imshow("output", self.img)
        cv2.waitKey(1)

        # self.get_logger().info(f"{self.no_of_frames_left}  {self.no_of_frames_not_left}  {self.no_of_frames_right}  {self.no_of_frames_not_right}")


    def traffic_sign_frame_counter(self):

        if datetime.now().timestamp() - self.start_time > 20:
            # detected_objects = self.pick(self.model.detections, 0)
            if "right" in self.detected_objects:
                self.no_of_frames_right += 1
            else:
                self.no_of_frames_not_right += 1
            if "left" in self.detected_objects:
                self.no_of_frames_left += 1
            else:
                self.no_of_frames_not_left += 1

        if self.no_of_frames_left > 0 or self.no_of_frames_right > 0:
            if self.traffic_sign != 1 or self.traffic_sign != -1:
                if self.no_of_frames_right >= self.min_no_of_frame:
                    self.traffic_sign = -1
                    self.no_of_frames_left = 0
                if self.no_of_frames_left >= self.min_no_of_frame:
                    self.traffic_sign = 1
                    self.no_of_frames_right = 0

                if self.no_of_frames_not_right >= self.max_no_of_frames_to_avoid:
                    self.no_of_frames_right = 0
                    self.no_of_frames_not_right = 0
                if self.no_of_frames_not_left >= self.max_no_of_frames_to_avoid:
                    self.no_of_frames_left = 0
                    self.no_of_frames_not_left = 0
        else:
            self.no_of_frames_not_left = 0
            self.no_of_frames_not_right = 0

    def traffic_light(self):

        # self.detected_objects = self.pick(self.model.detections,0)
        Area_thresh = 50

        if "trafficlight" in self.detected_objects:

            f = lambda x: [obj for obj in x if obj[0] == "trafficlight"]
            all_detected_traffic_lights = f(self.model.detections)
            traffic_light = max(all_detected_traffic_lights, key = lambda x: abs((x[2] - x[4])*(x[3] - x[5])))

            x1, y1, x2, y2 = traffic_light[2], traffic_light[3], traffic_light[4], traffic_light[5]

            light_region = self.img[int(y1):int(y2),int(x1):int(self.img.shape[1])]
            hsv = cv2.cvtColor(light_region,cv2.COLOR_BGR2HSV)
            greenmask = cv2.inRange(hsv, np.array([48, 200, 110]),np.array([75, 255, 150]))
            redmask = cv2.inRange(hsv, np.array([0, 200, 110]),np.array([10, 255, 145]))
            GreenContours, hierarchy = cv2.findContours(greenmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            RedContours, hierarchy = cv2.findContours(redmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


               
            # self.get_logger().info("705")
            
            # self.get_logger().info("707")

            if len(GreenContours) > 0:
                GreenCnt = max(GreenContours, key = cv2.contourArea) 
                if cv2.contourArea(GreenCnt) > Area_thresh:
                    return "go"
                else:
                    if len(RedContours) > 0:
                        RedCnt = max(RedContours, key = cv2.contourArea)
                        if cv2.contourArea(RedCnt) > Area_thresh:
                            return "stop"
                        else:
                            return "traffic light"
                    return "traffic light"
            else:
                if len(RedContours) > 0:
                    RedCnt = max(RedContours, key = cv2.contourArea)
                    if cv2.contourArea(RedCnt) > Area_thresh:
                        return "stop"
                    else:
                        return "traffic light"
                return "traffic light"
        else:
            return ""


    def red(self):
        Area_thresh = 50
        hsv = cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
        redmask = cv2.inRange(hsv, np.array([0, 200, 110]),np.array([10, 255, 145]))
        conts, hier = cv2.findContours(redmask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(conts) > 0:
            max_Area = cv2.contourArea(max(conts, key = cv2.contourArea))
            if max_Area > Area_thresh:
                return True
        return False

    def barricade_counter(self):

        self.no_of_barricades = self.detected_objects.count("barricade")
    
    def cones_counter(self):

        self.no_of_cones = self.detected_objects.count("cone")


    def stop_frames_counter(self):

        threshold = 0.7
        density = []
        stop_signs = [i for i in self.model.detections if i[0] == "stop"]

        if len(stop_signs) > 0:

            s = stop_signs[0]
            self.stop_sign_ratio = abs(s[3] - s[5])/(self.img.shape[0])
            for sign in stop_signs:
                slice = self.img[int(sign[3]):int(sign[5]), int(sign[2]):int(sign[4])]
                hsv = cv2.cvtColor(slice,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, np.array([0, 140, 70]), np.array([20, 255, 255]))

                mask = np.where(mask > 220, 1, 0)
                density.append(np.sum(mask)/(mask.shape[0]*mask.shape[1]))

            if max(density) >= threshold:
                self.stop_frames += 1
            else:
                self.not_stop_frames += 1

        else:
            self.not_stop_frames += 1

    def stop(self):

        if self.stop_frames >= self.min_no_stop_frames and self.stop_sign_ratio > 0.21:
            self.stop_car = True
            self.not_stop_frames = 0
        else:
            self.stop_car = False
        if self.not_stop_frames >= self.min_no_stop_frames:
            self.not_stop_frames = 0
            self.not_stop_frames = 0


def main(args=None):
    rclpy.init(args=args)

    multithreading_on = True

    if (multithreading_on):
        try:
            node1 = NXPTrackVision()
            node2 = YoloNode()
        except:
            print("failed to create nodes")

        try:
            executor = MultiThreadedExecutor()
            executor.add_node(node2)
            executor.add_node(node1)
        except:
            print("could not add nodes to MultiThreadedExecutor")
        
        try:
            executor.spin()
        except:
            print("can't run MultiThreadedExecutor for the nodes")
        
        finally:
            executor.shutdown()
            node1.destroy_node()
            node2.destroy_node()
            rclpy.shutdown()

    else:
        node = NXPTrackVision()
        
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
