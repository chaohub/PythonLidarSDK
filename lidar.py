# Copyright 2018 MicroVision, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Written by Chao Chen
import cv2 as cv
import numpy as np

# Capture from camera at location 1. The number could change depending on how many cameras are connected to this computer.
foundLidar = False
for i in range (0, 3) :
    cam = cv.VideoCapture(i)
    if cam :
        width = cam.get(3)
        height = cam.get(4)
        if (width == 120 or width == 160 or width = 240) and height == 720 :
            # cam.set(cv.cv.CV_CAP_PROP_FOURCC, cv.cv.CV_FOURCC('B', 'G', 'R', '3'))		#This line is needed for OpenCV2.*
            cam.set(3, 160)    # set the width cv.cv.CV_CAP_PROP_FRAME_WIDTH 160
            cam.set(4, 720)    # set the height cv.cv.CV_CAP_PROP_FRAME_HEIGHT 720
            foundLidar = True
            break;
        cam.release()

if foundLidar :
    print "Start Lidar camera. Hit Esc key to quit"
else :
    print "Couldn't detect MicroVision Lidar camera. Exit..."

# grab camera frames and display
while foundLidar:
    ret, img = cam.read()
    # Our depth sensing camera output format has 120*720 pixels. Each pixel has 4 byes, 2 for depth, 2 for amplitude.
    # Since python OpenCV only support BRG3 format, our lidar will report 160*720 BGR3 format with 3 bytes/pixel. 
    # Reshaped img from 720*160*3 to 720*120*4 format
    img = np.reshape(img, [720, 120, 4])
    # img[:, :, 0:1] are depth data. Squeeze to 8 bits for gray scale display. The real depth data could be out of displayed range.
    depth0 = img[:, :, 0]
    depth1 = img[:, :, 1]
    depth= (depth1 & 0x01)*128 + depth0/2
    depthImg = np.dstack((depth, depth, depth))
    # img[:, :, 2:3] are amplitude data. Squeeze to 8 bits for gray scale display. The real amp data could be out of displayed range.
    amp0 = img[:, :, 2]
    amp1 = img[:, :, 3]
    amp = amp1*16 + amp0/16
    ampImg = np.dstack((amp, amp, amp))
    # stack depth image on top of amplitude image
    combined = np.vstack((depthImg, ampImg))
    rimg = cv.resize(combined, (960, 720), interpolation = cv.INTER_CUBIC)
    cv.imshow("Lidar Camera", rimg)
    key = cv.waitKey(10)
    if key == 27:   # Esc key
        break

cv.destroyAllWindows() 
cam.release()
