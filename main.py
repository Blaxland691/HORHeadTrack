import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
from pytube import YouTube
from landmark_analysis import get_specific_landmark


def main():
    yt_link_str = 'https://www.youtube.com/watch?v='
    name = 'https://www.youtube.com/watch?v=WvyvwlowHWM'
    result_hash = name.split('=')[-1]
    yt = YouTube(name)

    landmark_type = mp.solutions.pose.PoseLandmark.NOSE
    specific_landmark = get_specific_landmark(result_hash, 'mp4', landmark_type)

    x_width = 0.878 + 2 * 0.329
    y_width = x_width * 480 / 840

    distance_per_segment = specific_landmark[:-1] - specific_landmark[1:]
    distance_xy = np.sqrt((x_width * distance_per_segment[:, 0]) ** 2 + (y_width * distance_per_segment[:, 1]) ** 2)

    print(f'Total Distance: {sum(distance_xy) / 1000:.3f} km')

    plt.plot(specific_landmark[:, 0], specific_landmark[:, 1])

    time = np.linspace(0, yt.length, len(distance_xy))

    plt.plot(time, np.cumsum(distance_xy), label=result_hash)
    plt.xlabel('Time (s)')
    plt.ylabel('Cumulative Distance (m)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
