import sys
import json

import cv2
import mediapipe as mp
import time


# format mediapipe res to csv
def format_pose(processed):
    local_landmarks = processed.pose_landmarks.landmark
    global_landmarks = processed.pose_world_landmarks.landmark

    local_res = []
    for land_mark in local_landmarks:
        local_res.append({
            "x": land_mark.x,
            "y": land_mark.y,
            "z": land_mark.z,
            "vis": land_mark.visibility
        })

    global_res = []
    for land_mark in global_landmarks:
        global_res.append({
            "x": land_mark.x,
            "y": land_mark.y,
            "z": land_mark.z,
            "vis": land_mark.visibility
        })
    return local_res, global_res



def capture(delay_time, output_path):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    # For webcam input:
    cap = cv2.VideoCapture(0)

    start_time = time.time()

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if time.time() - start_time >= delay_time:
                local_lst, global_lst = format_pose(results)

                with open(f"{output_path}_local.json", "w") as outfile:
                    json.dump(local_lst, outfile)
                with open(f"{output_path}_global.json", "w") as outfile:
                    json.dump(global_lst, outfile)

                break

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()


# main
delay_time = eval(sys.argv[1])
output_path = sys.argv[2]
capture(delay_time, output_path)
