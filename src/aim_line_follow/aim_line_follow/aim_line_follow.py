from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from example_interfaces.srv import AddTwoInts
from math import exp,sqrt
# from rclpy.exceptions import ParameterNotDeclaredException
# from rcl_interfaces.msg import Parameter
# from rcl_interfaces.msg import ParameterType
# from rcl_interfaces.msg import ParameterDescriptor
from math import atan2
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import String, Float32
from nav_msgs.msg import Odometry
from nxp_cup_interfaces.msg import PixyVector
from time import sleep
from datetime import datetime
import numpy as np


class LineFollow(Node):

    def __init__(self):
        super().__init__('aim_line_follow')

        self.state1_current_time = 0		#last time on the overbridge

        self.initial = 0 # it will be used in calculating dt in our PID function
        self.pid_error = [0,0] # it will be used in storing previous error in our PID function
        self.pid_sum = [0,0] # it will be used in storing error sum in our PID function

        self.yolo_t = 0
        self.yolo_error = 0
        
        self.start_delay = 15.0
        
        self.camera_vector_topic = "/cupcar0/PixyVector"

        self.default_linear_velocity = 0.8
        
        self.linear_velocity = 0.6

        self.a = 1.0 # our exponential decay term for our speed control function during steer
        
        self.angular_velocity = 0.6
        
        self.single_line_steer_scale = 1.0 	#steer scale when one end-track detected 

        self.double_line_steer_scale = 1.0 	#steer scale when two end-tracks detected 

        self.start_cone_detection = 0

        self.speed_threshold = 0.1

        self.center_obst = 0 

        self.last_cone_steer = 0

        self.taotal_steer_add = 0

        self.last_is_bumpy_road = 0

        self.ruk_ja_be = 0

        self.ruk_ja_be_delay = delay(6)


        
        # Time to wait before running
        self.get_logger().info('Waiting to start for {:s}'.format(str(self.start_delay)))
        sleep(self.start_delay)
        self.get_logger().info('Started')

        self.start_time = datetime.now().timestamp()
        self.restart_time = True

        # Subscribers
        self.pixy_subscriber = self.create_subscription(
            PixyVector,
            self.camera_vector_topic,
            self.listener_callback,
            10)
        self.middlesub = self.create_subscription(String,"/middle",self.middle,10) # get the message of average white pixel densities on left and right of car
        self.yolo = self.create_subscription(Float32,"/yolov5_steer",self.YoloSteer,10)
        

        # Publishers
        self.vel_publisher = self.create_publisher(Twist, '/cupcar0/vel', 10)
		#publisher of velocity
		
        self.speed_vector = Vector3()
        self.steer_vector = Vector3()
        self.vel = Twist()

    def get_num_vectors(self, msg):
        num_vectors = 0
        if(not(msg.m0_x0 == 0 and msg.m0_x1 == 0 and msg.m0_y0 == 0 and msg.m0_y1 == 0)):
            num_vectors = num_vectors + 1
        if(not(msg.m1_x0 == 0 and msg.m1_x1 == 0 and msg.m1_y0 == 0 and msg.m1_y1 == 0)):
            num_vectors = num_vectors + 1
        return num_vectors

    # def timer_callback(self):
    #     #TODO

    def listener_callback(self, msg):
        #TODO
        current_time = datetime.now().timestamp()
        frame_width = 79
        frame_height = 52
        window_center = (frame_width / 2)
        x = 0
        y = 0
        steer = 0
        speed = 0
        num_vectors = self.get_num_vectors(msg)

        if(num_vectors == 0):
            if self.restart_time:
                self.start_time = datetime.now().timestamp()
                self.restart_time = False
            if (self.start_time+4.0) > current_time:
                speed = self.linear_velocity * (4.0-(current_time-self.start_time))/4.0
            if (self.start_time+4.0) <= current_time:
                speed = 0.6
            steer = 0
        
        if(num_vectors == 2):
            if not self.restart_time:
                self.start_time = datetime.now().timestamp()
                self.restart_time = True

            # if (not (msg.m0_y0-msg.m0_y1<9 and msg.m1_y0-msg.m1_y1<9) and (msg.m0_y0-msg.m0_y1<9) or (msg.m1_y0-msg.m1_y1<9)):
            #     if msg.m1_y0-msg.m1_y1<9:
            #             num_vectors = 1
            #     else:
            #         msg.m0_x0 = msg.m1_x0
            #         msg.m0_x1 = msg.m1_x1
            #         msg.m0_y0 = msg.m1_y0
            #         msg.m0_y1 = msg.m1_y1
            #         num_vectors = 1
                    
        #else:
            m_x1 = (msg.m0_x1 + msg.m1_x1) / 2
            steer = -(self.angular_velocity)*(m_x1 - window_center) * (self.double_line_steer_scale) / frame_width
        
            if (self.start_time+4.0) > current_time:
                speed = (self.linear_velocity) * ((current_time-self.start_time)/4.0)
            if (self.start_time+4.0) <= current_time:
                speed = (self.linear_velocity)
            if (msg.m0_x0<window_center and msg.m1_x0<window_center):	
                steer=-0.3		 #if both num_vectors are on the left side from the center
            if (msg.m0_x0>window_center and msg.m1_x0>window_center):
                steer=0.3   		#if both num_vectors are on the right side from the center

        if(num_vectors == 1):
            
            if not self.restart_time:
                self.start_time = datetime.now().timestamp()
                self.restart_time = True
            if(msg.m0_x1 > msg.m0_x0):
                x = (msg.m0_x1 - msg.m0_x0) / frame_width
                y = (msg.m0_y1 - msg.m0_y0) / frame_height
            else:
                x = (msg.m0_x0 - msg.m0_x1) / frame_width
                y = (msg.m0_y0 - msg.m0_y1) / frame_height
            if(msg.m0_x0 != msg.m0_x1 and y != 0):
                steer = (self.angular_velocity) * (x / y) * (self.single_line_steer_scale)
                if (self.start_time+4.0) > current_time:
                    speed = (self.linear_velocity) * ((current_time-self.start_time)/4.0)
                if (self.start_time+4.0) <= current_time:
                    speed = self.linear_velocity
            else:
                steer = 0
                if (self.start_time+4.0) > current_time:
                    speed = (self.linear_velocity) * ((current_time-self.start_time)/4.0)*0.9
                if (self.start_time+4.0) <= current_time:
                    speed = (self.linear_velocity)
    
            

        
        self.speed_vector.x = min(float(speed*exp(-self.a*np.abs(steer))),self.linear_velocity) # our speed control function using steer
        self.steer_vector.z = float(steer)

        if abs(self.speed_vector.x)<self.speed_threshold and self.speed_vector.x!=0:
            self.speed_vector.x = float(self.speed_threshold)
        
    def middle(self,data):
        # this function will add an additional steer to the car based on the white pixel densities on left and right. a high density compared to other means
        # that the road is on that way and the car should steer towards it
        ##CODE TO AVOID OBSTACLE FROM THE CENTER SLICE OF TRANSFORM
        # last_cone_steers = [0,0,0,0,0,0]
        
        self.start_cone_detection=0
        d = data.data.split("%")
        l = float(d[0]) # density at left
        r = float(d[1]) # density at right
        self.center_obst = int(d[4])
        steer_according_to_black_on_bumpy = float(d[6])
        is_bumpy_road = int(d[7])
        # self.center_obst = int(d[2])

        # if self.start_cone_detection==1:
        #     l = float(d[2]) # density at left
        #     r = float(d[3]) # density at right
        #     self.linear_velocity = 0.5
        pid = self.PID((l,r),0.8,0.4,0) # using pid function for stable performance
        

        # if self.start_cone_detection==1:
        #     # now = last_cone_steers.pop(0)
            

        #     self.steer_vector.z = self.steer_vector.z + 12*(pid[0] - pid[1])# - self.taotal_steer_add/2 #+ self.partial_black_factor

        #     # self.last_cone_steer = 
        #     self.taotal_steer_add += pid[0] - pid[1] 
        #     # last_cone_steers.append()
        #     # self._logger.info("Doing This")
        #     # self._logger.info(str(10*(pid[0] - pid[1])))
        # else:
        #     self.steer_vector.z = self.steer_vector.z + (pid[0] - pid[1])/2.0 #+ #self.partial_black_factor#
        #     self._logger.info("not Doing This")

        self.steer_vector.z = self.steer_vector.z + (pid[0] - pid[1]) #+ 3.5*self.center_obst*float(d[5])#+ 2*steer_according_to_black_on_bumpy + 2.5*self.center_obst*float(d[5])  # if density at left is higher, car should move anticlockwise and therefore steer should
        # be +ve and hence it is added. for right steer should be negative and hence it is subtracted
        # if self.center_obst:
        #     self.linear_velocity *= 0.8
        # else:
        #     self.linear_velocity = self.default_linear_velocity

        if self.last_is_bumpy_road == 1 and is_bumpy_road==0:
            self.ruk_ja_be=1
            self.ruk_ja_be_delay.reset()
        self.last_is_bumpy_road = is_bumpy_road
        # self._logger.info(str(is_bumpy_road))

    def PID(self, X,kp,kd,ki):
        dt = datetime.now().timestamp() - self.initial # smal time interval
        output = [0,0] # since 2 pid will be calculated on the go, one for left density and one for right density
        for i,x in enumerate(X):
            self.pid_sum[i] = self.pid_sum[i] + x*dt # integral sum
            output[i] = kp*x + kd*(x - self.pid_error[i])/dt + ki*self.pid_sum[i] # output for each density
            self.pid_error[i] = x # storing error for next time
        self.initial = datetime.now().timestamp() # storing time for next
        return output

    def YoloSteer(self, data):

        kp = 0.8
        kd = 0.3
        steer = data.data#*(1+self.center_obst)
        dt = datetime.now().timestamp() - self.yolo_t
        output = steer*kp + kd*(steer - self.yolo_error)/dt
        # self.get_logger().info(f"{output/2}")
        self.steer_vector.z = self.steer_vector.z + output/2
        if self.ruk_ja_be==1 and (not self.ruk_ja_be_delay.wait()):
            self.speed_vector.x = float(0.2)
            self.steer_vector.z = -float(0.4)
            self._logger.info("bupy road end")
        self.vel.linear = self.speed_vector
        self.vel.angular = self.steer_vector
        
        self.vel_publisher.publish(self.vel) # publishing speed
        self.yolo_t = datetime.now().timestamp()
        self.yolo_error = steer


        

        # self._logger.info(str(yaw))


class Traffic(Node):

    def __init__(self):
        super().__init__('Traffic_decision')


        self.command = "Velocity"
        # self.pre_turning = False
        self.turning = False
        self.left_track  = 0
        self.right_track  = 0

        self.cmd_vel_publisher = self.create_publisher(Twist, '/cupcar0/cmd_vel', 10)
        self.vel_sub = self.create_subscription(Twist,"/cupcar0/vel",self.Velocity,10)
        self.Traffic_sub = self.create_subscription(Float32,"/traffic_sign",self.right_and_left,10)
        self.odom_sub = self.create_subscription(Odometry, "/cupcar0/odom", self.Odometry_handler, 10)
        self.middlesub = self.create_subscription(String,"/middle",self.middle,10)


        # self.turn_service = self.create_service(AddTwoInts, "/turn", self.turn_car)
        self.cmd_vel = Twist()
        self.target_vel = 0
        self.target_ang = 0
        self.last_traffic_sign_detected_time = 0
        self.is_right = False
        self.is_left = False
        self.is_bumpy_road = 0
        self.is_trafficlight_detected = False

        self.height_change_sampler_delay = delay(2)
        self.pass_traffic_light_delay = delay(1)
        self.pre_turn_delay = delay(1.5)
        self.pre_turn_delay2 = delay(3)
        self.is_2_barricade_delay = delay(15)
        self.backward_delay = 0
        self.no_backward_delay = 0
        self.Back = delay(2)
        self.Back_Forward = delay(2)

        self.yaw_value_center = 3.1
        self.turn_counter = 0
        self.deviation_from_ceneter_yaw = 0

        self.dstance_from_center =  0      

        self.initial_Z = 0
        self.z = 0
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0
        self.delta_height = 0
        self.last_steer_angle = 0
        self.is_2_barricade = False
        self.steer_due_to_barricade = 0

        self.steer_2_left = 0
        self.steer_3_right = 0

        self.is_cone = 0
        self.move_to_after_backward = 0

        self.target_orientation = 1.5

    # def turn_car(self, request, response):

    #     response.sum = request.a + request.b

    #     return response


    def middle(self, data):

        d = data.data.split("%")
        self.left_track = float(d[0])
        self.right_track = float(d[1])
        self.is_bumpy_road = int(d[7])
        
        # if (len(d))
        self.steer_due_to_barricade = float(d[8])

        self.steer_2_left = float(d[2])
        self.steer_3_right = float(d[3])

        self.move_to_after_backward = float(d[5])
        

    def Odometry_handler(self, data):
        pos = data.pose.pose.position
        self.x = pos.x
        self.y = pos.y
        self.z = pos.z
        orientation = data.pose.pose.orientation
        ori_x = orientation.x
        ori_y = orientation.y
        ori_z = orientation.z
        ori_w = orientation.w
        self.vel_x = float(data.twist.twist.linear.x)
        self.vel_y = float(data.twist.twist.linear.y)
        self.vel_z = float(data.twist.twist.linear.z)
        linear_twist_x = self.vel_x

        self.yaw = float(atan2(2.0 * (ori_z * ori_w + ori_x * ori_y) , - 1.0 + 2.0 * (ori_w* ori_w + ori_x * ori_x)))
        # self._logger.info(str(self.yaw))        

        if self.height_change_sampler_delay.wait():
            self.delta_height = self.z - self.initial_Z
            self.initial_Z = self.z
            self.height_change_sampler_delay.reset()
        
        if (self.yaw>0):
            self.deviation_from_ceneter_yaw =  self.yaw - self.yaw_value_center     #right - negative left - positive 
        if (self.yaw<0):
            self.deviation_from_ceneter_yaw = 3.14+ self.yaw

        self.dstance_from_center += self.deviation_from_ceneter_yaw*linear_twist_x*10
        # self._logger.info(str(self.z))        




    def Velocity(self, data):

        self.target_vel = data.linear.x
        self.target_ang = data.angular.z

        if self.command == "Velocity":
            self.cmd_vel = data
            # self.speed_control(5.0)

        if self.command == "trafficlight stop":
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0
        
        if self.command == "trafficlight go":
            self.cmd_vel.linear.x = data.linear.x
            self.cmd_vel.angular.z = 0.0
            if self.pass_traffic_light_delay.wait():
                self.command = "Velocity"
                self.is_trafficlight_detected = False
    

        if self.command == "turn":
            if self.turning:
                self.cmd_vel.angular.z = 0.4*(-1 if self.is_right else 1)
                self.cmd_vel.linear.x = 0.4
            else:
                self.cmd_vel.linear.x = 0.5
                self.cmd_vel.angular.z = data.angular.z*(0.6)

        if self.command == "stop":
            self.cmd_vel.linear.x = 0.0
            self.cmd_vel.angular.z = 0.0


        if self.z < 0.45:
            speed_accelerated_scale = 1.5
            speed_deaccelerated_scale = 1.5
            if self.up_down_bridge() == "up overbridge" and self.is_bumpy_road == 0:
                self.cmd_vel.linear.x = self.cmd_vel.linear.x*speed_accelerated_scale
                # self.get_logger().info(f"{round(self.delta_height,5)}  {round(self.z,3)}")
            if self.up_down_bridge() == "down overbridge":
                self.cmd_vel.linear.x = self.cmd_vel.linear.x*0/speed_deaccelerated_scale
                # self.get_logger().info(f"{round(self.delta_height,5)}  {round(self.z,3)}")

        if self.is_2_barricade:
            self.cmd_vel.linear.x = 0.45
            self.cmd_vel.angular.z += 1.5*self.steer_due_to_barricade
            self.get_logger().info(f"{datetime.now().timestamp() - self.is_2_barricade_delay.initial_time}")
            # self.get_logger().info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")

        if self.is_2_barricade_delay.wait():
            self.is_2_barricade = False

        if self.is_cone:
            self.cmd_vel.linear.x = 0.4
            self.cmd_vel.angular.z += -2*(self.steer_2_left-self.steer_3_right)

        if self.command == "backward":
            # self.get_logger().info(f"{self.command}")
            if self.Back.wait():
                self.Back.reset()
                self.command = "backward_forward"
                self.Back_Forward.reset()
                self.backward_delay = 0
                self.no_backward_delay = 0
            else:
                self.cmd_vel.linear.x = -0.3
                self.cmd_vel.angular.z = -self.move_to_after_backward/5


        if self.command == "backward_forward":

            self.cmd_vel.linear.x = 0.3
            self.cmd_vel.angular.z = self.move_to_after_backward/2.5
            # self.get_logger().info(f"{self.command}")
            if self.Back_Forward.wait():
                self.command = "Velocity"

        self.check_collision()


        if self.command != "backward":
            self.speed_control(4.8)

        # self.get_logger().info(f"{self.z}")
        # self.get_logger().info(f"{sqrt(self.vel_x**2 + self.vel_y**2)}")
        

        self.cmd_vel_publisher.publish(self.cmd_vel)
        # self.get_logger().info(f"{round(self.target_vel,3)}   {round(self.cmd_vel.linear.x,3)}    {round(self.error)}")

    def right_and_left(self,data):
        
        turn = data.data
        # self.get_logger().info(str(turn))

        if int(turn) == 0:
            self.command = "stop"
        if int(turn) == 1:
            self.is_left = True
            self.is_right = False
            self.pre_turn_delay.reset()
            self.pre_turn_delay2.reset()
        if int(turn) == -1:
            self.is_right = True
            self.is_left = False
            self.pre_turn_delay.reset()
            self.pre_turn_delay2.reset()


        if (turn==-20):
            self.is_cone = True
        else:
            self.is_cone = False

        if int(turn) == -10:
            self.is_2_barricade = True
            self.is_2_barricade_delay.reset()

        if int(turn) == -5 and not self.is_trafficlight_detected:
            self.command = "trafficlight stop"
            self.is_trafficlight_detected = True

        if int(turn) == 5:
            self.command = "trafficlight go"
            self.pass_traffic_light_delay.reset()
            
        
        if self.is_left or self.is_right:
            self.command = "turn"
            # self.get_logger().info(str(round(datetime.now().timestamp() - self.pre_turn_delay.initial_time, 3)) + f"   {self.command}  {self.turning}")
            # flag = self.right_track if self.is_right else self.left_track
            if self.right_track > 0.8 and self.left_track > 0.8 and not self.turning:
                if self.turn_counter == 0 or self.turn_counter == 1 or self.turn_counter == 2:
                    if self.pre_turn_delay.wait():
                        self.turning = True
                        self.last_steer_angle = self.yaw

                elif self.turn_counter == 4:
                    if self.pre_turn_delay2.wait():
                        self.turning = True
                        self.last_steer_angle = self.yaw
                else:
                    self.turning = True
                    self.last_steer_angle = self.yaw
                # self.get_logger().info(f"{self.command}  {self.turning}")

        # self.get_logger().info(f"{self.is_cone}   {turn}")


        # if self.turning and (self.right_track < 0.7 or self.left_track < 0.7):
        #     self.command = "Velocity"
        #     self.turning = False
        #     self.is_right = False
        #     self.is_left = False
        #     self.pre_turn_delay.reset()

        if (self.turn_counter==3):
            self.target_orientation = 0.8

        if self.turning:
            if abs(self.yaw - self.last_steer_angle)>3.14:
                if (self.last_steer_angle>0):
                    if abs(self.yaw + 3.14 + 3.14-self.last_steer_angle)>self.target_orientation:
                        # self.last_traffic_sign_detected_time = datetime.now().timestamp()
                        self.last_steer_angle = self.yaw
                        self.command = "Velocity"
                        self.turn_counter += 1
                        self.turning = False
                        self.is_right = False
                        self.is_left = False
                        self.pre_turn_delay.reset()
                        self.pre_turn_delay2.reset()
                        self._logger.info("HERE 1")

                else:
                    if abs(self.yaw - (3.14) - 3.14 - (self.last_steer_angle))>self.target_orientation:
                        # self.last_traffic_sign_detected_time = datetime.now().timestamp()
                        self.last_steer_angle = self.yaw
                        self.command = "Velocity"
                        self.turn_counter += 1
                        self.turning = False
                        self.is_right = False
                        self.is_left = False
                        self.pre_turn_delay.reset()
                        self.pre_turn_delay2.reset()
                        self._logger.info("HERE 2 ")


            elif abs(self.yaw - self.last_steer_angle)>self.target_orientation:
                # self.last_traffic_sign_detected_time = datetime.now().timestamp()
                self.last_steer_angle = self.yaw
                self.command = "Velocity"
                self.turn_counter += 1
                self.turning = False
                self.is_right = False
                self.is_left = False
                self.pre_turn_delay.reset()
                self.pre_turn_delay2.reset()
                self._logger.info("HERE 3")


        

        # self.get_logger().info(f"{self.turning}  {self.command}")

    # def up_down_bridge(self):

    #     if self.z >= 0.2 and self.delta_height > 0.01:
    #         return "up overbridge"
    #     if self.z >= 0.05 and self.delta_height < -0.01:
    #         return "down overbridge"

    def up_down_bridge(self):

        if self.z >= 0.1 and self.delta_height > 0.01:
            return "up overbridge"
        if self.z >= 0.05 and self.delta_height < -0.01:
            return "down overbridge"

    def speed_control(self, max_height):

        self.error = self.target_vel - sqrt(self.vel_x**2 + self.vel_y**2 + self.vel_z**2)

        if self.z >= 0.07 and self.z <= max_height and self.delta_height >= 0.01:
            self.cmd_vel.linear.x = self.target_vel + self.error*0.5
            self.cmd_vel.angular.z = self.target_ang
        if self.z >= 0.07 and self.delta_height <= -0.005:
            self.cmd_vel.linear.x = self.target_vel/5 + (self.target_vel/2 - sqrt(self.vel_x**2 + self.vel_y**2 + self.vel_z**2))*0.5
            self.cmd_vel.angular.z = self.target_ang/5

    def check_collision(self):

        if self.command == "Velocity" or self.command == "turn":

            if sqrt(self.vel_x**2 + self.vel_y**2)<0.006:
                self.backward_delay += 1
            else:
                self.no_backward_delay += 1

            if self.no_backward_delay >= 50:
                self.no_backward_delay = 0
                self.backward_delay = 0

            if self.backward_delay >= 50:
                self.no_backward_delay = 0
                self.command = "backward"
                self.Back.reset_once()
            # self.get_logger().info(f"{self.backward_delay}  {self.vel_x**2 + self.vel_y**2}")

        
        
class delay():

    def __init__(self,delay_time):

        self.delay = delay_time
        self.initial_time = 0
        self.one_time_reset = False

    def wait(self):
        if (datetime.now().timestamp() - self.initial_time >= self.delay):
            return True 
        else:
            return False

    def reset(self):
        self.initial_time = datetime.now().timestamp()
        self.one_time_reset = False

    def reset_once(self):

        if not self.one_time_reset:
            self.initial_time = datetime.now().timestamp()
            self.one_time_reset = True


        
def main(args=None):
    rclpy.init(args=args)

    multithreading_on = True

    if (multithreading_on):
        try:
            node1 = LineFollow()
            node2 = Traffic()
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
        node = LineFollow()
        
        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
