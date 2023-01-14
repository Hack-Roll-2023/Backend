import cv2
import mediapipe as mp
import time

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    one_instance = None

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

            # if time.time() - start_time >= 3 and one_instance == None:
            #     one_instance = results
            #
            #     # access
            #     landmarks = results.pose_landmarks.landmark
            #
            #
            #     print(landmarks[0])
            #     print()
            #     print(help(one_instance.pose_landmarks))
            #     print()
            #     print(type(one_instance.pose_landmarks))
            #     print(type(one_instance.pose_landmarks[0]), len(one_instance.pose_landmarks))
            #
            #
            #     print(one_instance)


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

            if time.time() - start_time >= 45:
                break

    cap.release()

if __name__ == "__main__":
    main()
