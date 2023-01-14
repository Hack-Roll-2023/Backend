import cv2
import mediapipe as mp
import time
#
# from ../tracker import *
# from ../movement import *
#
#
# def main():
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles
#     mp_pose = mp.solutions.pose
#
#     # For webcam input:
#     cap = cv2.VideoCapture(0)
#
#     start_time = time.time()
#     tracker = MoveTracker()
#
#     with mp_pose.Pose(
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             success, image = cap.read()
#             if not success:
#                 print("[Error] Ignoring empty camera frame.")
#                 # If loading a video, use 'break' instead of 'continue'.
#                 continue
#
#             # To improve performance, optionally mark the image as not writeable to
#             # pass by reference.
#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             results = pose.process(image)
#
#             # Draw the pose annotation on the image.
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             mp_drawing.draw_landmarks(
#                 image,
#                 results.pose_landmarks,
#                 mp_pose.POSE_CONNECTIONS,
#                 landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#
#             # Flip the image horizontally for a selfie-view display.
#             cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#             if cv2.waitKey(5) & 0xFF == 27:
#                 break
#
#             # Check movement
#             move_data = get_hand_movement_from_raw(results)
#             resp = tracker.update_movement(move_data)
#
#             if resp[0]:
#                 print(f"Booh, at time {time.time()-start_time:3.3f}\t from {resp[1]}")
#
#     cap.release()
#
#
# if __name__ == "__main__":
#     main()
