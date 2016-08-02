__author__ = 'kanurminen'

import os
import cv2
import logging
import datetime
import time

#Globals
#Minimum position of tolerance slider
toleranceMin = 140000
#Maximum position of tolerance slider
toleranceMax = 160000
#Tolerance to be adjusted 
tolerance = 140000



def adjustTolerance(x):
    tolerance = x
    print "Tolerance set as %s" % tolerance


# compare two frames and return their difference
def detectMotionDiff(img0, img1, img2):
    frame1 = cv2.absdiff(img2, img1)
    frame2 = cv2.absdiff(img1, img0)
    return cv2.bitwise_and(frame1, frame2)

#function to check whether a folder exists. If it doesn't, it will be created. Returns current date to be used as the folder name.
def checkIfFolderExists():
    currentDate = datetime.datetime.now().strftime('%d%m%Y')
    dirName = os.path.join(os.getcwd(), currentDate)
    try: 
    	os.makedirs(dirName)
    except OSError:
    	if not os.path.isdir(dirName):
            raise
    return dirName


def startCamera():

   # initialize logging
    logger = logging.getLogger('blinkbright')
    hdlr = logging.FileHandler('blinkbright.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info('Blinkbright started.')

    #initialize camera (use system default device, change value on next line if needed)
    cam = cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)

   

    #initialize grayscale feeds for diff calculation
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    # create window for live display
    cv2.namedWindow("Blinkbright",1)
    #add trackbar for tolerance
    cv2.createTrackbar('Tolerance', "Blinkbright", toleranceMin, toleranceMax, adjustTolerance)
    # initiate camera read
    ret, colordisplay = cam.read()
    print "Welcome to Blinkbright! Use 'c' to take a snapshot. Use 'q' to quit the program. To display the instructions again, press 'h'."
    

    # main loop 	
    while True:
        try:
            #enable next line and disable the one after it to see grayscale diff output (for debugging/ tolerance adjustment purposes)
            #cv2.imshow('Blinkbright Live Display', detectMotionDiff(t_minus, t, t_plus))
            cv2.imshow("Blinkbright", colordisplay)
            ret, colordisplay = cam.read()
            #Timestamp
            cv2.putText(colordisplay, datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S"),
            (10, colordisplay.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 162), 1)

            #setting frames for comparison
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

            # Motion detection. If there's enough difference (white pixels), save the image.
            # Enable next "print" line to show calculated values (for debug & adjustment purposes)

            
            if cv2.countNonZero(detectMotionDiff(t_minus, t, t_plus)) > tolerance:
		currentDate = checkIfFolderExists()	
		frame = datetime.datetime.now().strftime('%d%m%Y_%H.%M.%S') + '.jpg'
		print "Motion detected. Frame saved as %s" % frame
                cv2.imwrite(os.path.join(currentDate, frame), colordisplay)
                #logger.info('Motion shot taken.')
        # enable/adjust following line to reduce rate of images taken         
		# time.sleep(1)

       # basic keyboard functionality; replace with more responsive interface later. C saves frame manually, H displays "help", Q quits the application.
            if cv2.waitKey(15) & 0xFF == ord('c'):
		name = datetime.datetime.now().strftime('%d%m%Y_%H.%M.%S') + '.jpg'
		print "Manual screenshot taken. Filename: %s" % name
		cv2.imwrite(name, colordisplay)
                #logger.info('Manual user screenshot taken.')
            if cv2.waitKey(15) == ord('h'):
                print " Use 'c' to take a snapshot. Use 'q' to quit the program. To display the instructions again, press 'h'."
            if cv2.waitKey(15) & 0xFF == ord('q'):
                print('Quitting program. Thank you for using Blinkbright.')
                cam.release()
                cv2.destroyAllWindows()
                logger.info('Blinkbright clean shutdown.')
                break
        except Exception, e:
            logger.info('It hurts, have an error')
            logger.exception(e)
            break



if __name__ == '__main__':
    print "Blinkbright Camera has been started as a main method. Please run from Blinkbright_Main. "
