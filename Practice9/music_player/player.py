import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = sorted(
            filename
            for filename in os.listdir(music_folder)
            if filename.lower().endswith((".wav", ".mp3"))
        )
        self.index = 0
        self.is_playing = False

    def play(self):
        if not self.playlist:
            return

        track_path = os.path.join(
            self.music_folder,
            self.playlist[self.index],
        )
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if not self.playlist:
            return

        self.index = (self.index + 1) % len(self.playlist)
        self.play()

    def previous(self):
        if not self.playlist:
            return

        self.index = (self.index - 1) % len(self.playlist)
        self.play()

    def get_current_track_name(self):
        if not self.playlist:
            return "No tracks"
        return self.playlist[self.index]

    def get_position_seconds(self):
        if not self.is_playing:
            return 0

        position_ms = pygame.mixer.music.get_pos()
        return max(0, position_ms // 1000)
