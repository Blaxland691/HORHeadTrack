import os

from pytube import YouTube


def download_sets(path):
    with open(path, 'r') as f:
        lines = [line.removesuffix('\n') for line in f.readlines()]

    for line in lines:
        download_set(line)


def download_set(name):
    yt = YouTube(name)

    # Check if path already exists
    for path in os.listdir('./Videos'):
        if name.split(sep='=')[-1] in path:
            return

    ys = yt.streams.filter(only_audio=False, only_video=False, progressive=True).get_lowest_resolution()

    print(f"Downloading: {yt.title}")

    ys.download(output_path='./Videos', filename=f'{name.split(sep="=")[-1]}.mp4')
