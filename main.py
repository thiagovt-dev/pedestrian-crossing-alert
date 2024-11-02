import cv2
import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
time.sleep(2)
print("Connection to Arduino established.")

pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

while True:
    if arduino.in_waiting > 0:
        traffic_light_status = arduino.readline().decode().strip()
        print("Traffic light status: ", traffic_light_status)

        if traffic_light_status == "Red light":
            print("Traffic light is red. Starting pedestrian monitoring...")

            ret, frame = cap.read()
            if not ret:
                print("Error capturing video.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            pedestrians = pedestrian_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
            
            if len(pedestrians) > 0:
                for (x, y, w, h) in pedestrians:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print("Pedestrian detected at red light!")
                    arduino.write(b'1')
            else:
                print("No pedestrians detected at red light.")
                arduino.write(b'0')
            cv2.imshow('Pedestrian Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Traffic light is green or yellow. Waiting for it to turn red.")

cap.release()
cv2.destroyAllWindows()
arduino.close()
