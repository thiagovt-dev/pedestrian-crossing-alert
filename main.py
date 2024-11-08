import cv2
import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
time.sleep(2)
print("Connection to Arduino established.")

pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0) # change to your video source 
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error capturing video.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in pedestrians:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if arduino.in_waiting > 0:
        traffic_light_status = arduino.readline().decode('utf-8', errors='replace').strip()
        print("Traffic light status:", traffic_light_status)

        while traffic_light_status in ["Green light", "Yellow light"]:
            if len(pedestrians) > 0:
                arduino.write(b'1') 
                print("Pedestrian detected! Alarm ON")
            else:
                arduino.write(b'0') 
                print("No pedestrian detected. Alarm OFF")

            ret, frame = cap.read()
            if not ret:
                print("Error capturing video.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pedestrians = pedestrian_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in pedestrians:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Pedestrian Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if arduino.in_waiting > 0:
                traffic_light_status = arduino.readline().decode('utf-8', errors='replace').strip()
                print("Traffic light status:", traffic_light_status)

    cv2.imshow('Pedestrian Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()