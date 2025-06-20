import cv2
import time
# import serial  # Enable when using Arduino

# Load stop sign classifier
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')

# Start video capture
cap = cv2.VideoCapture(0)

sending_stop = False
stop_start_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stops = stop_cascade.detectMultiScale(gray, 1.3, 5)

    if len(stops) > 0 and not sending_stop:
        print("[INFO] Stop sign detected!")
        sending_stop = True
        stop_start_time = time.time()

    if sending_stop:
        print("Sending: 1")
        # ser.write(b'1')
        if time.time() - stop_start_time > 3:
            sending_stop = False
    else:
        print("Sending: 0")
        # ser.write(b'0')

    for (x, y, w, h) in stops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('Stop Sign Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# ser.close()
