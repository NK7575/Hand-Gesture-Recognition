import mediapipe as mp
import cv2
import numpy as np
import math

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def detect_hands(self, frame):
        """Detect hands"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results
    
    def get_gesture(self, results):
        """Recognize gesture using improved landmark analysis"""
        if not results.multi_hand_landmarks:
            return "No Hand", 0.0
        
        landmarks = results.multi_hand_landmarks[0]
        hand_label = results.multi_handedness[0]
        handedness = hand_label.classification[0].label  # "Left" or "Right"
        
        # Convert landmarks to list
        lm = [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
        
        # Detect gestures
        gesture, confidence = self._recognize_gesture(lm, handedness)
        return gesture, confidence
    
    def _recognize_gesture(self, lm, handedness):
        """Improved gesture recognition logic"""
        
        # Helper functions
        def distance(p1, p2):
            return math.sqrt((lm[p1][0] - lm[p2][0])**2 + (lm[p1][1] - lm[p2][1])**2)
        
        def is_extended(tip, pip, dip):
            """Check if finger is extended"""
            return lm[tip][1] < lm[pip][1]
        
        def is_closed(tip, pip):
            """Check if finger is folded"""
            return lm[tip][1] > lm[pip][1]
        
        # Finger distances from wrist
        thumb_dist = distance(4, 0)
        index_dist = distance(8, 0)
        middle_dist = distance(12, 0)
        ring_dist = distance(16, 0)
        pinky_dist = distance(20, 0)
        
        # Finger states
        thumb_extended = is_extended(4, 3, 2)
        index_extended = is_extended(8, 6, 5)
        middle_extended = is_extended(12, 10, 9)
        ring_extended = is_extended(16, 14, 13)
        pinky_extended = is_extended(20, 18, 17)
        
        # 1. OPEN PALM
        if thumb_extended and index_extended and middle_extended and ring_extended and pinky_extended:
            return "Open_Palm", 0.95
        
        # 2. THUMBS UP
        if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            if lm[4][1] < lm[0][1]:  # thumb tip above wrist
                return "Thumbs_Up", 0.95
        
        # 3. THUMBS DOWN
        if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            if lm[4][1] > lm[0][1]:  # thumb tip below wrist
                return "Thumbs_Down", 0.95
        
        # 4. PEACE SIGN / VICTORY
        if not thumb_extended and index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "Victory", 0.95
        
        # 5. POINTING UP (index only extended, upward)
        if not thumb_extended and index_extended and not middle_extended and not ring_extended and not pinky_extended:
            if lm[8][1] < lm[6][1]:  # index tip above knuckle
                return "Pointing_Up", 0.90
        
        # 6. POINTING DOWN (index only extended, downward)
        if not thumb_extended and index_extended and not middle_extended and not ring_extended and not pinky_extended:
            if lm[8][1] > lm[6][1]:  # index tip below knuckle
                return "Pointing_Down", 0.90
        
        # 7. FIST (all fingers closed)
        if not thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "Closed_Fist", 0.90
        
        # 8. OK SIGN (thumb & index tips close, others extended)
        thumb_index_dist = distance(4, 8)
        if thumb_index_dist < 0.05 and middle_extended and ring_extended and pinky_extended:
            return "OK", 0.85
        
        # 9. LOVE YOU (pinky & thumb out, middle fingers in)
        if thumb_extended and not index_extended and not middle_extended and not ring_extended and pinky_extended:
            return "ILY", 0.85
        
        return "Unknown", 0.5
    
    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame
