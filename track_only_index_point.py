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

        index_point = detector.get_index_point(results)
        print(index_point)
        if index_point!= None:
            h, w, _ = frame.shape
            cx = int(index_point.x * w)
            cy = int(index_point.y * h)

            cv2.circle(frame, (cx,cy), 15,(0,255,0), -1)#bgr format

        cv2.imshow('Find my Index tip', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()