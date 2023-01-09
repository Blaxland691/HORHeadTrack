import os
import pickle
import time

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pytube import YouTube

landmark_legend = ['x', 'y', 'z', 'visibility']
yt_link_str = 'https://www.youtube.com/watch?v='


def plot_distance_over_time():
    for res in os.listdir('./Results'):
        name = 'https://www.youtube.com/watch?v=' + res.removesuffix('.pkl')
        result_hash = name.split('=')[-1]

        yt = YouTube(name)

        landmark_type = mp.solutions.pose.PoseLandmark.NOSE
        specific_landmark = get_specific_landmark(result_hash, 'mp4', landmark_type)

        x_width = 0.878 + 2 * 0.329
        y_width = x_width * 480 / 840

        distance_per_segment = specific_landmark[:-1] - specific_landmark[1:]
        distance_xy = np.sqrt((x_width * distance_per_segment[:, 0]) ** 2 + (y_width * distance_per_segment[:, 1]) ** 2)

        print(f'Total Distance: {sum(distance_xy):.3f} m')
        time_list = np.linspace(0, yt.length, len(distance_xy))
        plt.plot(time_list, np.cumsum(distance_xy), label=yt.title)

    plt.xlabel('Time (s)')
    plt.ylabel('Cumulative Distance (m)')
    plt.title('HOR Berlin Sets ( Oct 22 - )')
    plt.show()


def get_specific_landmark(path, path_suffix, pose_landmark: mp.solutions.pose.PoseLandmark):
    ld = get_landmarks(path, path_suffix, frame_iter=20)
    specific_landmark = np.array([landmark[pose_landmark] for landmark in ld])

    return specific_landmark


def save_landmark_video(path, path_suffix, frames):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(f'Videos/{path}.{path_suffix}')

    result = cv2.VideoWriter('swing.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             10, (1080, 1920))

    frame = 0

    while frames > frame:
        success, img = cap.read()

        y, x, z = img.shape
        x_cut = y * 9 / 16
        x2, x1 = (x - x_cut) / 2 + x_cut, (x - x_cut) / 2

        if success:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)

            if results.pose_landmarks:
                mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                continue

            for idx, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

            cropped = img[0:y, int(x1):int(x2)]

            img = cv2.resize(cropped, (1080, 1920), cv2.INTER_AREA)

            result.write(img)

            frame += 1
            # cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

            cv2.imshow("Image", img)

            cv2.waitKey(1)
        else:
            break

    result.release()
    cap.release()
    cv2.destroyAllWindows()


def get_landmarks(path, path_suffix, calculate_again=False, save_video=False, frame_iter=1):
    """
    Analyse videos landmarks.
    
    :param frame_iter:
    :param save_video:
    :param path_suffix:
    :param calculate_again:
    :param path: path to video
    :return:
    """

    print(f"Getting Landmarks for: {path}")

    if os.path.exists(f'Results/{path}.pkl') and not calculate_again:
        f = open(f'Results/{path}.pkl', 'rb')
        ld = pickle.load(f)
        f.close()
        return ld

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(f'Videos/{path}.{path_suffix}')

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

            frame += frame_iter
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)

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
