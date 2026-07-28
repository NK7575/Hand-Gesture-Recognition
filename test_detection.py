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
        gesture = detector.classify_gesture(landmarks)
        print(gesture)
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, gesture, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        
        cv2.imshow('Hand Detection', frame)
        cv2.moveWindow('Hand Detection', 0, 0)

        
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()