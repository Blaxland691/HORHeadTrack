import mediapipe as mp

from landmark_analysis import get_specific_landmark


def main():
    get_specific_landmark('qbcBZS6sMxc', 'mp4', mp.solutions.pose.PoseLandmark.NOSE)


if __name__ == '__main__':
    main()
