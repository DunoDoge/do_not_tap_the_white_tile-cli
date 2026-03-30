import random
import threading
import numpy as np

try:
    import pygame
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False


class SoundManager:
    SAMPLE_RATE = 44100
    NOTE_DURATION = 0.12
    
    NOTE_FREQUENCIES = {
        'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
        'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    }
    
    PIANO_NOTES = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 
                   'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5']
    ERROR_NOTE = 'C3'
    
    _sound_cache = {}
    
    def __init__(self):
        self.enabled = HAS_PYGAME
    
    def _generate_piano_sound(self, frequency, duration):
        cache_key = (frequency, duration)
        if cache_key in self._sound_cache:
            return self._sound_cache[cache_key]
        
        samples = int(self.SAMPLE_RATE * duration)
        t = np.linspace(0, duration, samples, False)
        
        wave = (
            np.sin(2 * np.pi * frequency * t) * 0.5 +
            np.sin(2 * np.pi * frequency * 2 * t) * 0.25 +
            np.sin(2 * np.pi * frequency * 3 * t) * 0.125 +
            np.sin(2 * np.pi * frequency * 4 * t) * 0.0625
        )
        
        envelope = np.exp(-t * 8)
        wave = wave * envelope
        
        wave = (wave * 32767 * 0.5).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        self._sound_cache[cache_key] = sound
        return sound
    
    def _play_note_async(self, note):
        if not self.enabled:
            return
        
        def _play_thread():
            try:
                freq = self.NOTE_FREQUENCIES.get(note)
                if freq:
                    sound = self._generate_piano_sound(freq, self.NOTE_DURATION)
                    sound.play()
            except Exception:
                pass
        
        thread = threading.Thread(target=_play_thread, daemon=True)
        thread.start()
    
    def play_piano_note(self):
        if not self.enabled:
            return
        
        note = random.choice(self.PIANO_NOTES)
        self._play_note_async(note)
    
    def play_error_sound(self):
        if not self.enabled:
            return
        
        self._play_note_async(self.ERROR_NOTE)
