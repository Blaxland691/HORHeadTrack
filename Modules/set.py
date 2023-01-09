from pytube import YouTube

from Modules.landmark_analysis import get_landmarks


class HORSet:
    def __init__(self, link):
        self.link = link
        self.key = link.split('=')[-1]

        # YouTube elements
        self.yt = YouTube(link)
        self.title = self.yt.title

        self.landmarks = get_landmarks(self.key, 'mp4', frame_iter=20)
