import os
import pickle
import time

import mediapipe as mp
import cv2


def get_landmarks(path, type, calculate_again=False, save_video=False):
    """
    Analyse videos landmarks.

    :param type:
    :param calculate_again:
    :param path: path to video
    :return:
    """

    print("Getting Landmarks")

    if os.path.exists(f'Results/{path}.pkl') and not calculate_again:
        f = open(f'Results/{path}.pkl', 'rb')
        ld = pickle.load(f)
        f.close()
        return ld

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(f'{path}.{type}')

    if save_video:
        result = cv2.VideoWriter('swing.avi',
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 10, (1080, 1920))

    landmarks = []
    frame = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    last_frame = time.perf_counter()

    while True:
        fps = 1 / (time.perf_counter() - last_frame)
        last_frame = time.perf_counter()

        frame += 1

        print(f'\r{frame / total_frames * 100:.2f} % fps: {fps:.2f}', end='')

        success, img = cap.read()

        if success:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmark = []
            for idx, lm in enumerate(results.pose_landmarks.landmark):
                landmark.append([lm.x, 1 - lm.y, lm.z, lm.visibility])
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            landmarks.append(landmark)

            # img = cv2.resize(img, (1080, 1920), cv2.INTER_AREA)
            if save_video:
                result.write(img)

            # cv2.imshow("Image", img)
            #
            # cv2.waitKey(1)
        else:
            break

    f = open(f'Results/{path}.pkl', 'wb')
    pickle.dump(landmarks, f, -1)
    f.close()

    if save_video:
        result.release()

    cap.release()
    cv2.destroyAllWindows()

    return landmarks
