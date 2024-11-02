import cv2

pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

cap = cv2.VideoCapture(2)  

traffic_light_status = "red"

while True:
    if traffic_light_status == "red":
        print("Traffic light is red. Starting pedestrian monitoring...")

        ret, frame = cap.read()
        if not ret:
            print("Error capturing video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        pedestrians = pedestrian_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in pedestrians:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("Pedestrian detected at red light!")

        cv2.imshow('Pedestrian Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Traffic light is green or yellow. Waiting for it to turn red.")

cap.release()
cv2.destroyAllWindows()
