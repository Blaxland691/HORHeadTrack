import os

from pytube import YouTube


def download_sets(path):
    pass


def download_set(name):
    yt = YouTube(name)

    # Check if path already exists
    for path in os.listdir('./Videos'):
        if name.split(sep='=')[-1] in path:
            return

    ys = yt.streams.filter(only_audio=False, only_video=False, progressive=True).get_lowest_resolution()

    print("Downloading...")

    ys.download(output_path='./Videos', filename=f'{name.split(sep="=")[-1]}.mp4')