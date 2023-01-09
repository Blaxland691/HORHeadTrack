import os

from pytube import YouTube

from downloader import download_set

if __name__ == '__main__':
    download_set('https://www.youtube.com/watch?v=VxV9ODD6IBs')
    download_set('https://www.youtube.com/watch?v=qbcBZS6sMxc')
    download_set('https://www.youtube.com/watch?v=WvyvwlowHWM')
