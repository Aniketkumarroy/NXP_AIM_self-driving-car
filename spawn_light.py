from time import sleep
import os

spawn_green="gz model --spawn-file=/home/pranay/ros2ws/nxp_gazebo/models/traffic_light_green/model.sdf --model-name=lightGreen -x 1.883040 -y 7.477359 -z 0.785598 -R 3.132084 -P -0.000383 -Y 1.615736"
del_green="gz model -m lightGreen -d"

while(True):	
	sleep(10)
	os.system(spawn_green)
	sleep(10)
	os.system(del_green)	
