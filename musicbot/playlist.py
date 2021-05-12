from collections import deque
import random



class Playlist:
    """Stores the youtube links of songs to be played and already played and offers basic operation on the queues"""

    def __init__(self):
        # Stores the links os the songs in queue and the ones already played
        self.playque = deque()
        self.playhistory = deque()

        # A seperate history that remembers the names of the tracks that were played
        self.trackname_history = deque()

        self.loop = False

    def __len__(self):
        return len(self.playque)

    def add_name(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > 15:
            self.trackname_history.popleft()

    def add(self, track):
        self.playque.append(track)

    def next(self):

        if len(self.playque) == 0:
            return None

        song_played = self.playque[0]

        if self.loop:
            if song_played != "Dummy":
                self.playque.clear()
                self.add(song_played)

        if len(self.playque) == 0:
            return None

        if song_played != "Dummy":
            self.playhistory.append(song_played)
            if len(self.playhistory) > 10:
                self.playhistory.popleft()

        return self.playque[0]

    def prev(self):
        if len(self.playhistory) == 0:
            dummy = "DummySong"
            self.playque.appendleft(dummy)
            return dummy
        self.playque.appendleft(self.playhistory.pop())
        return self.playque[0]

    def shuffle(self):
        random.shuffle(self.playque)

    def empty(self):
        self.playque.clear()
        self.playhistory.clear()
