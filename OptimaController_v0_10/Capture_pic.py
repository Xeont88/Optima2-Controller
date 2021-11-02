import cv2
import threading

command = None

def process():
    global command
    while True:
        command = input('Enter command')

thread = threading.Thread(target=process)
thread.daemon = True
thread.start()

cap = cv2.VideoCapture(0)
reqCommand = 'Capture_pic'

def camera_on():
    while True:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.IMREAD_COLOR)

        cv2.imshow('frame', frame)
        if command == reqCommand:
            out = cv2.imwrite('capture.jpg', frame)
            thread.terminate()
            break

        k = cv2.waitKey(1)
        if k == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

thread_cam = threading.Thread(target=camera_on)
thread_cam.start()

