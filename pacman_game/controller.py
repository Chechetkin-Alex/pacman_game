from sounds_collection import SoundsCollection
import pygame


class Controller:
    end_time = {key: 0 for key in SoundsCollection.sounds.keys()}

    def set_sound(self, sound, wait=False, stop=False):
        if stop:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.pause()

        self.stop_sound(sound)
        if sound in ("victory", "restart"):
            for old_sound in SoundsCollection.sounds.keys():
                self.stop_sound(old_sound)

        SoundsCollection.sounds[sound].play()
        self.end_time[sound] = SoundsCollection.len_sounds[sound] + pygame.time.get_ticks()

        if wait:
            pygame.time.wait(SoundsCollection.len_sounds[sound])

    def stop_sound(self, sound):
        SoundsCollection.sounds[sound].stop()
        self.end_time[sound] = 0

    def set_sound_volumes(self, volume):
        for sound in SoundsCollection.sounds.values():
            pygame.mixer.Sound.set_volume(sound, volume)

    def play_music_if_no_sound(self):
        time = pygame.time.get_ticks()
        for sound in self.end_time:
            if self.end_time[sound] > time:
                return
        pygame.mixer.music.unpause()
