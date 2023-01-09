import os

import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
from pytube import YouTube

from Modules.downloader import download_sets
from Modules.landmark_analysis import get_specific_landmark, save_landmark_video, plot_cumsum

plt.style.use('seaborn-v0_8')


def main():
    plot_cumsum(mp.solutions.pose.PoseLandmark.NOSE)


if __name__ == '__main__':
    main()
