#! /usr/bin/env python
__author__ ='Jacques Saraydaryan'
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
from openpose_ros_srvs.srv import DetectPeoplePoseFromImg
import numpy as np
import json

import rospkg
import argparse

parser = argparse.ArgumentParser(description='Read images and convert into json file with OpenPose positions')
parser.add_argument('pathInput',type=str,default = './../datasetPN',help='Enter input path with images')
parser.add_argument('pathOutput',type=str,default = './../openPoseDataset',help='Enter output path to save json files')


def ConvertRes(res):
	results_list = []
	for i in range(len(res)):
		body_part = [ {'part_id': res[i].body_part[j].part_id,
				'x': res[i].body_part[j].x,
				'y': res[i].body_part[j].y,
				'confidence': res[i].body_part[j].confidence } for j in range(len(res[i].body_part))]
		results_list.append({'body_part': body_part, 'face_landmark': res[i].face_landmark})
	return results_list

def LoadImg(pathOutput, _bridge):
 #Load Image
    print('Loading images...')
    for im in os.listdir(pathOutput.replace('openPoseDataset', 'datasetPN')):
	im_path=os.path.join(pathOutput.replace('openPoseDataset', 'datasetPN'), im)
	if (os.path.isfile(im_path)):
    		img_loaded2 = cv2.imread(im_path)
		msg_im2 = _bridge.cv2_to_imgmsg(img_loaded2, encoding="bgr8")

	        #call service to learn people
	        rospy.wait_for_service('people_pose_from_img')

	        try:
			detect_from_img_srv = rospy.ServiceProxy('people_pose_from_img', DetectPeoplePoseFromImg)
			resp3 = detect_from_img_srv(msg_im2)

			#write json file
			json_name = os.path.splitext(pathOutput+'/'+str(im))[0]+'.json'
			print(json_name)
			res = ConvertRes(resp3.personList.persons)
			with open(json_name, 'w') as f:
				f.write(json.dumps(res))
				f.close()

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e


def LoadImgAndPublish(pathInput,pathOutput):
    # get an instance of RosPack with the default search paths
    rospack = rospkg.RosPack()

    # get the file path for rospy_tutorials
    package_path=rospack.get_path('openpose_ros_examples')

    _bridge = CvBridge()
    rospy.loginfo("media_folder:"+str(pathInput))

    rospy.init_node('LoadAndPublishImg', anonymous=True)
    result_folders = []
    #get hierarchy of input path to copy on output path
    for folder in [x[0] for x in os.walk(pathInput)]:
	    if (folder.endswith('distract') or folder.endswith('focus')):
		    splitted = folder.split("/")[-2:]
		    separator = '/'
		    result_folder = pathOutput + separator.join(splitted)

    #create folder if it does not exist
		    if not(os.path.exists(result_folder)):
			first_folder = separator.join(result_folder.split("/")[:-1])
			if not(os.path.exists(first_folder)):
				os.mkdir(first_folder)
			os.mkdir(result_folder)
		    LoadImg(result_folder, _bridge)

       # spin
    rospy.spin()






if __name__ == '__main__':
    args = parser.parse_args()
    pathInput = args.pathInput
    pathOutput = args.pathOutput
    try:
        LoadImgAndPublish(pathInput,pathOutput)
    except rospy.ROSInterruptException:
        pass