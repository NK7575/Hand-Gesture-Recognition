import cv2
from emoji_mapper import map_gesture
from gesture_detector import GestureDetector

def main():
    detector = GestureDetector()
    cap = cv2.VideoCapture(0)
    count = 0
    gestures_list = []


    cv2.namedWindow("Gesture Recognition", cv2.WINDOW_FREERATIO)
    while True:
        ignore, frame = cap.read()
        height, width, _ = frame.shape
        if not ignore:
            break

        results = detector.detect_hands(frame)
        #frame = detector.draw_landmarks(frame, results)
        landmarks = detector.get_landmarks(results)
        #print(landmarks)
        extended_fingers = str(detector.return_extended_tuple(landmarks, frame, height, width))
        gesture = map_gesture(extended_fingers)
        if gesture:
            #print(gesture)
            if count<=10:
                count+=1
                gestures_list.append(gesture)
            else:
                count=0
                most_repeated = max(gestures_list, key=gestures_list.count)
                print(most_repeated)
                gestures_list.clear()
                
        
        #cv2.putText(frame, gesture, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),1 )
        

        cv2.imshow('Gesture Recognition', frame)
        cv2.moveWindow('Gesture Recognition', 200,200)
        

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
