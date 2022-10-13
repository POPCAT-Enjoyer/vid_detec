import cv2
import numpy as np
from sympy import *


dimensions = 2
max_iterations = 50
max_contours_iter = 10

class key:
    def __init__(self, key1, key2):
        self.keys[0] = key1
        self.keys[1] = key2

class item:
    def __init__(self, key1, key2, empty, img):
        self.keys[1] = key1
        self.keys[2] = key2
        self.isEmpty = empty
        self.img = img

class node:
    def __init__(self, itm, node1, node2):
        self.itm = itm
        self.node1 = node1
        self.node2 = node2

def find_color(color, img, img_key):
    contours = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if contours:
        return True, contours
    else:
        return False, contours

def run_the_tree(img):
    max_x, max_y= img.shape[:2]
    #for i in range(max_iterations):
        

object_color = "orange"

color_dist = {'red': {'Lower': np.array([0, 60, 60], dtype=np.uint8), 'Upper': np.array([6, 255, 255], dtype=np.uint8)},
              'blue': {'Lower': np.array([100,30,30], dtype=np.uint8), 'Upper': np.array([140, 255, 255], dtype=np.uint8)},
              'green': {'Lower': np.array([35, 43, 35], dtype=np.uint8), 'Upper': np.array([90, 255, 255], dtype=np.uint8)},
              'orange': {'Lower':np.array([5, 50, 50], dtype=np.uint8), 'Upper': np.array([24, 255, 255], dtype=np.uint8)}
              }

cum = cv2.VideoCapture(0)
mouse_x = 0
mouse_y = 0

def text_render(pos, color, img):
    cv2.putText(img, color, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

def mouse_pos(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y= y

def findColor(color, frame, outline):
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=2)
    #cv2.imshow("HELP", erode_hsv)
    inRange_hsv = cv2.inRange(erode_hsv, color_dist[color]['Lower'], color_dist[color]['Upper'])
    contours = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    #cv2.drawContours(frame, contours, 0, (255, 255, 255), 2)
    if contours:
        iter = len(contours)
        if(iter > max_contours_iter):
            iter = max_contours_iter
        for i in range(0, iter, 2):
            c = max(contours[i:i+1], key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            if(rect[1][0] * rect[1][1] > 100):
                box_center = (int(rect[0][0]), int(rect[0][1]))
                text_render(box_center, color, frame)
                #print(rect[-1], " ~ ", rect[2])
                #print(hsv[mouse_x, mouse_y])
                box = cv2.boxPoints(rect)
                cv2.drawContours(frame, [np.int0(box)], 0, outline, 2)

while cum.isOpened():
    cv2.namedWindow('colros')
    cv2.setMouseCallback('colros', mouse_pos)
    ret, frame = cum.read()
    if ret:
        if frame is not None:
            findColor("blue",  frame, (255, 0, 0))
            findColor("orange", frame, (10, 120, 250))

            #cv2.imshow('camera', frame)
            cv2.imshow('colros', frame)
            #cv2.imshow('GS', gs_frame)
            #cv2.imshow('HSV', hsv)
            #cv2.imshow('ERoDE', erode_hsv)
            cv2.waitKey(1)
        else:
            print("ur dumb")
    else:
        print("pc dumb")

cum.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
