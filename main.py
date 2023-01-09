import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
from pytube import YouTube

from downloader import download_sets
from landmark_analysis import get_specific_landmark, save_landmark_video, plot_distance_over_time


def main():
    download_sets('last_6m')

    plot_distance_over_time()


if __name__ == '__main__':
    main()
