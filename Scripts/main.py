import numpy as np
import cv2
from pprint import pprint
import json
from convertSVG import convertSVG

#__init__ dicts to store coordinates

objDict = {}

#__init__ image and grayscale image

img = cv2.imread('images1.png')
cv2.resize(img, None, fx=1.4, fy=1.4)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(gray, (3,3), 0) 
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection

cv2.imshow('Canny Edge Detection', edges)
cv2.imwrite('edges.png', edges)  
cv2.waitKey(0)

#Function to find circles22
def findCircle():
    minDist = 100           #
    param1 = 700            #
    param2 = 50             #parameters __init__
    minRadius = 5           #
    maxRadius = 100         #
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius) #get all circles
    if circles is not None:
        circles = np.uint16(np.around(circles))# convrt values of circles to nearby int
        k = 1
        for i in circles[0]:
            str1 = 'CIRCLE '
            name = str1+str(k) # naming the circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 2) # highlighting the circles
            cv2.putText(img, name, (i[0]-35, i[1]-35), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255/2), 2) # naming the highlight box
            # print(f"x = {i[0]}, y = {i[1]} , rad = {i[2]}")
            x = int(i[0]) #x of circle
            y = int(i[1]) #y of circle
            rad =int(i[2]) #radius of circle
            objDict[name] = {'x':x,'y':y,'rad':rad} #pushing value of circle
            k+=1
           
#Function to find objects
def findObject(path,num):
    k = 1
    while num>0:
        method = cv2.TM_SQDIFF_NORMED
        small_image = cv2.imread(path) #load reference image to search
        result = cv2.matchTemplate(small_image, img, method) # finding similar images
        mn,_,minLoc,_ = cv2.minMaxLoc(result) #getting the x1,y1 coordinates 
        MPx,MPy = minLoc
        MPx,MPy = MPx+10,MPy+10 

        trows,tcols = small_image.shape[:2] #getting the x2,y2 coordinates
        trows,tcols = trows-15,tcols-15

        name = path.replace(".png","") # naming the obj
        name+= f" {k}"
        cv2.rectangle(img, (MPx,MPy),(MPx+tcols,MPy+trows),(0,255),2) #highlighting the object
        cv2.putText(img, name, (MPx, MPy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255/2), 2) #naming the highlightbox
        num-=1
        k+=1
        x1 = MPx #x1 of object
        y1 = MPy #y1 of object
        x2 = MPx+tcols #x2 of object
        y2 = MPy+trows #y2 of object
        objDict[name] = {'x1':x1,'y1':y1,'x2':x2,'y2':y2} #pushing value of object

# def findLines():
#     # Apply edge detection method on the image
#     threshold1 = 200
#     threshold2 = 750
#     edges = cv2.Canny(gray, threshold1=threshold1, threshold2=threshold2, apertureSize=3)
    
#     # This returns an array of r and theta values
#     lines = cv2.HoughLines(edges, 1, np.pi/180, 250)
    
#     # The below for loop runs till r and theta values
#     # are in the range of the 2d array
#     for r_theta in lines:
#         arr = np.array(r_theta[0], dtype=np.float64)
#         r, theta = arr
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*r
#         y0 = b*r
#         x1 = int(x0 + 1000*(-b))
#         y1 = int(y0 + 1000*(a))
#         x2 = int(x0 - 1000*(-b))
#         y2 = int(y0 - 1000*(a))
#         cv2.line(img, (x1, y1), (x2, y2), (255, 0,0), 1)


if __name__ == '__main__':
    findCircle()
    findObject('CL.png',3)# large chandlier
    findObject('CS.png',2)# small chandlier
    findObject('DL.png',3)# dim light
    findObject('DL2.png',1)# dim light
    findObject('Pl2.png',1)# panel light
    findObject('Pl3.png',1)# panel light
    pprint(objDict)
    with open("data.json", "w") as outfile:
        json.dump(objDict, outfile,indent= 4)
    convertSVG('D:hackahton//Mlsmartapp//edges.png')
    cv2.imshow('img', img)# show new image with highlights
    cv2.waitKey(0)
