#!python3
import cv2
from math import exp
import torch
import numpy as np
from time import time, sleep

class yolov5s():

    def __init__(self, weights_path, labels, confidence_threshold=0.25, NMS_threshold=0.45):
        
        yolov5_model = 'ultralytics/yolov5'  # loading model architecture from ultralytics/yolov5 repository
        self.model = torch.hub.load(yolov5_model, 'custom', weights_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device) 
        print(f"using device {self.device}")
        self.model.conf = confidence_threshold
        self.model.iou = NMS_threshold
        with open(labels, "r") as f:
            self.labels = f.read().strip().split("\n")
            f.close()
        np.random.seed(40)
        self.colours = np.random.randint(0, 255, size=(len(self.labels), 3),dtype="uint8")
        self.detections = []

    def detect(self, img):
        self.detections = []
        self.initial = time()
        # self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.results = self.model(img) # change self.gray to img if you want to detect on colour rgb image
        self.t = time() - self.initial
        h, w = img.shape[:2]
        for pred in self.results.xyxyn[0]:
            lx, ly = pred[0].item()*w, pred[1].item()*h
            rx, ry = pred[2].item()*w, pred[3].item()*h
            conf = pred[4].item()
            obj_class = self.labels[int(pred[5].item())]
            self.detections.append([obj_class, conf, lx, ly, rx, ry])

    def show_on_image(self, img, fps = -1):
        if len(self.detections) > 0:
            h,w = img.shape[:2]
            for object in self.detections:
                col = [int(c) for c in self.colours[self.labels.index(object[0])]]
                top_left = (int(object[2]), int(object[3]))
                bottom_right = (int(object[4]), int(object[5]))
                ratio = abs(object[3] - object[5])/h
                cv2.rectangle(img, top_left, bottom_right, col, 2)
                cv2.rectangle(img, (int(object[2]), int(object[3] - 15)), (int(object[2] + len(object[0]*10) + 100), int(object[3])), col, -1)
                cv2.putText(img, f"{object[0]}: {round(object[1], 2)}  {round(ratio,3)}", (int(object[2]), int(object[3] - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                if fps > 0:
                    cv2.putText(img, f"{round(self.t,4)}/frame", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    fps = 1/self.t
                    cv2.putText(img, f"{round(fps,4)} fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                else:
                    cv2.putText(img, f"{round(1/fps,4)}/frame", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    fps = 1/self.t
                    cv2.putText(img, f"{round(fps,4)} fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        return img


class AvoidObstacles():

    def __init__(self, avoid_threshhold_file, labels):
        with open(avoid_threshhold_file, "r") as f:
            self.avoiding_ratio = f.read().strip().split("\n")
            self.avoiding_ratio = [float(i) for i in self.avoiding_ratio]
            f.close()
        with open(labels, "r") as f:
            self.labels = f.read().strip().split("\n")
            f.close()

    def steer(self, img, detections):

        h, w = img.shape[:2]
        SteerLeft = []
        SteerRight = []
        traffic_light_steer = 0
        a = 0.3
        b = 1
        # all_steer_values = []
        for detect in detections:

            index, lx, ly, rx, ry = self.labels.index(detect[0]), detect[2], detect[3], detect[4], detect[5]
            
            ratio = (abs(ly - ry)/h)
            ratio = 1.0 if ratio >= self.avoiding_ratio[index] else ratio
            if detect[0] != "left" or detect[0] != "right":
                cx = (rx + lx)/2
                if detect[0] != "trafficlight":
                    if (cx - w/2) > 0: # the obstacle is at right
                        SteerLeft.append(-a*exp(-(lx - w/2)*b*ratio/(w/2)))
                        # SteerLeft.append(-a*(w-cx)*ratio)
                    else:
                        SteerRight.append(a*exp((rx - w/2)*b*ratio/(w/2)))
                    # SteerRight.append(a*cx*ratio)
                else:
                    traffic_light_steer = (w/2 - cx)/(w/2)

        if len(SteerLeft) > 0:
            l = min(SteerLeft)
        else:
            l = 0
        if len(SteerRight) > 0:
            r = max(SteerRight)
        else:
            r = 0
        return 0#-(l + r) + traffic_light_steer*1.2
            



if __name__ == "__main__":


    cap = cv2.VideoCapture("nxp_car.avi")
    model = yolov5s("best.pt", "classes.txt")

    avoid = AvoidObstacles("avoid_threshold.txt", "classes.txt")
    # result = cv2.VideoWriter('filename2.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10,(int(cap.get(3)), int(cap.get(4))))

    initial = 0

    while True:
        ret, img = cap.read()
        if ret:
            # result.write(img)
            model.detect(img)
            img = model.show_on_image(img)

            if hasattr(model, "detections") == True:
                print(avoid.steer(img, model.detections))
            cv2.imshow("output",img)
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
            if key == ord("l"):
                sleep(7)
        else:
            print("ERROR")
            break

    cap.release()
    # result.release()

    cv2.destroyAllWindows()