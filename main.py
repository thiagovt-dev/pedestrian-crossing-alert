import cv2
import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
time.sleep(2)
print("Connection to Arduino established.")

pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
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

        if traffic_light_status in ["Green light", "Yellow light"]:
            print("Traffic light is green/yellow to cars. Monitoring for pedestrians...")

            if len(pedestrians) > 0:
                print("Pedestrian detected!")
                arduino.write(b'1')  
            else:
                arduino.write(b'0')  

    cv2.imshow('Pedestrian Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()