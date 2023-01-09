import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt

from landmark_analysis import get_specific_landmark


def main():
    landmark_type = mp.solutions.pose.PoseLandmark.NOSE
    specific_landmark = get_specific_landmark('WvyvwlowHWM', 'mp4', landmark_type)

    # time_per_frame = 20 / 30

    x_width = 0.878 + 2 * 0.329
    y_width = x_width * 480 / 840

    distance_per_segment = specific_landmark[:-1] - specific_landmark[1:]
    distance_xy = np.sqrt((x_width * distance_per_segment[:, 0]) ** 2 + (y_width * distance_per_segment[:, 1]) ** 2)

    print(f'Total Distance: {sum(distance_xy) / 1000:.3f} km')

    # plt.xlim([0, 1])
    # plt.ylim([0, 1])
    # plt.plot(specific_landmark[:, 0], specific_landmark[:, 1])

    plt.plot(np.cumsum(distance_xy), label='WvyvwlowHWM')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
