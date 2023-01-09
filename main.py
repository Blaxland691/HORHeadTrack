from downloader import download_set
from landmark_analysis import get_landmarks

if __name__ == '__main__':
    download_set('https://www.youtube.com/watch?v=VxV9ODD6IBs')
    download_set('https://www.youtube.com/watch?v=qbcBZS6sMxc')
    download_set('https://www.youtube.com/watch?v=WvyvwlowHWM')

    get_landmarks('Videos/WvyvwlowHWM', 'mp4')