import mediapipe as mp
import cv2
import numpy as np


class GestureDetector:
    def __init__(self):#the ai detector, built for every different GestureDetector object
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode = False, #we are looking at a video ryt....put "True" if you are using an image
            max_num_hands = 2,
            min_detection_confidence = 0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, frame):#finds hands in the video
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#opencv send bgr file, but mediapipe needs rgb file
        results = self.hands.process(rgb_frame)
        return results #returns results containing 21 landmarks 

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_index_point(self, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                return hand_landmarks.landmark[8]

    def get_landmarks(self, results):
        hand_data = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])  # x, y, z coordinates
                hand_data.append(landmarks)
        
        return hand_data
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def is_finger_extended(self, landmarks, finger_tip, finger_pip):
        tip = landmarks[0][finger_tip]
        pip = landmarks[0][finger_pip]
        return tip[1] < pip[1]

    def classify_gesture(self, landmarks):
        if not landmarks:
            return None

        # Landmark indices
        THUMB_TIP = 4
        THUMB_PIP = 3
        INDEX_TIP = 8
        INDEX_PIP = 6
        MIDDLE_TIP = 12
        MIDDLE_PIP = 10
        RING_TIP = 16
        RING_PIP = 14
        PINKY_TIP = 20
        PINKY_PIP = 18
        WRIST = 0

        thumb_extended = self.is_finger_extended(landmarks, THUMB_TIP, THUMB_PIP)
        index_extended = self.is_finger_extended(landmarks, INDEX_TIP, INDEX_PIP)
        middle_extended = self.is_finger_extended(landmarks, MIDDLE_TIP, MIDDLE_PIP)
        ring_extended = self.is_finger_extended(landmarks, RING_TIP, RING_PIP)
        pinky_extended = self.is_finger_extended(landmarks, PINKY_TIP, PINKY_PIP)

        if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return landmarks[0][THUMB_PIP]
        if not thumb_extended and index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return None
        if not thumb_extended and not index_extended and middle_extended and not ring_extended and not pinky_extended:
            return None
        if not thumb_extended and not index_extended and not middle_extended and ring_extended and not pinky_extended:
            return None
        if not thumb_extended and not index_extended and not middle_extended and not ring_extended and pinky_extended:
            return None
   
        return None



#test run
'''
gesture_detector = GestureDetector()

cam = cv2.VideoCapture(0)
while True:
    ignore, frame = cam.read()
    results = gesture_detector.detect_hands(frame)
    cv2.imshow('Hand Detector', frame)
    cv2.moveWindow('Hand Detector', 0,0)
    if cv2.waitKey(1) & 0xff == ord('x'):
        break
    
    print(results.multi_hand_landmarks)

cam.release()

'''