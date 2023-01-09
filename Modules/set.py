class HORSet:
    def __init__(self, link):
        self.link = link
        self.key = link.split('=')[-1]
