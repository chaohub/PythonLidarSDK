# Copyright [2018] [MicroVision]
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
# Written by Chao Chen
import cv2 as cv
import numpy as np

# Capture from camera at location 1. The number could change depending on how many cameras are connected to this computer.
cam = cv.VideoCapture(0)
# our depth sensing camera output format has 120*720 pixels. Each pixel has 4 byes, 2 for depth, 2 for amplitude.
# Since python OpenCV only support BRG3 format, our lidar will report 160*720 BGR3 format with 3 bytes/pixel. 
cam.set(cv.cv.CV_CAP_PROP_FOURCC, cv.cv.CV_FOURCC('B', 'G', 'R', '3'))		#This line is only used on Linux platform
cam.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 160)     # set the width 160
cam.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)    # set the height 720

# grab camera frames and display
print "Hit Esc key to quit"
while True:
    ret, img = cam.read()
    # Reshaped img to 720*120*4 format
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
    cv.imshow("Depth Camera", rimg)
    key = cv.waitKey(10)
    if key == 27:   # Esc key
        break

cv.destroyAllWindows() 
cam.release()
