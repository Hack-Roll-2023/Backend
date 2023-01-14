import cv2
import mediapipe as mp
import time

from tracker import *
from movement import *


class Detector:
    '''
    The detector function for tracking the hand movement.
    - Initialise one object when the service starts,
    - and call the process_static_img() function every time when the backend receives a new img
    '''
    def __init__(self):
        self.start_time = time.time()
        self.tracker = MoveTracker()

    def process_static_img(self, img) -> bool:
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # Check movement
            move_data = get_hand_movement_from_raw(results)
            resp = self.tracker.update_movement(move_data)

            if resp[0]:
                print(f"Booh, at time {time.time()-self.start_time:3.3f}\t from {resp[1]}")
            return resp[0]
