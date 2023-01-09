from pytube import YouTube


def download_set(name):
    yt = YouTube(name)
    ys = yt.streams.filter(only_audio=False, only_video=False, progressive=True).get_lowest_resolution()
    ys.download()


if __name__ == '__main__':
    download_set('https://www.youtube.com/watch?v=WvyvwlowHWM')
