import os

import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
from pytube import YouTube

from downloader import download_sets
from landmark_analysis import get_specific_landmark, save_landmark_video, plot_distance_over_time

plt.style.use('seaborn-v0_8')


def main():
    # for vid in os.listdir('./Videos'):
    #     get_specific_landmark(vid.split('.')[0], 'mp4', 20)

    plot_distance_over_time()


if __name__ == '__main__':
    main()
