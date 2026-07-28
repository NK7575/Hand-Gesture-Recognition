#DETECT EXTENED FINGER

import cv2
from gesture_detector import GestureDetector


def main():
    detector = GestureDetector()
    cap = cv2.VideoCapture(0)
    
    while True:
        ignore, frame = cap.read()
        if not ignore:
            break
        results = detector.detect_hands(frame)
        #frame = detector.draw_landmarks(frame, results)
        landmarks = detector.get_landmarks(results)
        #print(landmarks)
        
        #print(gesture)
        
        #cv2.putText(frame, gesture, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

        if landmarks!=[]:
            tip = landmarks[0][4]
            pip = landmarks[0][3]
            dx = tip[0] - pip[0]
            dy = tip[1]-pip[1]
            dz = tip[2]-pip[2]
            if dx<0.05 and dx>-0.05 and dy<0.02 and dy>-0.1:
                print("Thumb extended")

        frame = cv2.flip(frame, 1)
        cv2.imshow('Detect extended Finger', frame)
        cv2.moveWindow('Detect extended Finger', 0, 0)
        
        
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()