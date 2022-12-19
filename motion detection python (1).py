import cv2
import datetime
import pywhatkit
motion = 0
b = 0
main_frame = None
video = cv2.VideoCapture(0)
while True:
    (check, frame) = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.medianBlur(gray_frame, 5)
    if main_frame is None:
        main_frame = gray_frame
        continue
    difference_frame = cv2.absdiff(main_frame, gray_frame)
    threshold_frame = cv2.threshold(difference_frame, 50, 255,cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
    (cnts, _) = cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < 8000:
            continue
        motion = 1
        b += 1      
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (255, 0, 0), 2)
    cv2.imshow('Difference Frame', difference_frame)
    cv2.imshow('Color Frame', frame)
    cv2.imshow('threshold Frame',threshold_frame)
    if 2 > b > 0:
        print('motion detected')
        hour = int(datetime.datetime.now().hour)
        minute = int(datetime.datetime.now().minute)
        minutes = minute + 1
        try:
            pywhatkit.sendwhatmsg('+91_mobile_number','alert! motion detected', hour,minutes)
            print ('Successfully Sent!')
        except:
            print ('An Unexpected Error!')
    key = cv2.waitKey(1)
    if key == ord('a'):
        break

video.release()
cv2.destroyAllWindows()
