import wave
import numpy as np

class Morse:
    def __init__(self, unittime=0.05, samplerate=44100, frequency=700):
        self.audio = np.array([])
        self.unittime = unittime
        self.samplerate = samplerate
        self.frequency = frequency
        self.morse_table = {
            'A': '.-',   'B': '-...', 'C': '-.-.',
            'D': '-..',  'E': '.',    'F': '..-.',
            'G': '--.',  'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-',  'L': '.-..',
            'M': '--',   'N': '-.',   'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...',
            'T': '-',    'U': '..-',  'V': '...-',
            'W': '.--',  'X': '-..-', 'Y': '-.--', 'Z': '--..',

            '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.', '0': '-----',

            ',': '--..--', '.': '.-.-.-',
            ':': '---...', ';': '-.-.-.',
            "'": '.----.', '"': '.-..-.',
            '!': '-.-.--', '?': '..--..',
            '/': '-..-.',  '$': '...-..-', '&': '.-...', '@': '.--.-.',
            '+': '.-.-.',  '-': '-....-',  '_': '..--.-',
            '(': '-.--.',  ')': '-.--.-'
        }

    def add_note(self, length, isrest):
        t = np.linspace(0, length, int(self.samplerate * length))
        channel = 0.5 * np.sin(2 * np.pi * int(not isrest) * self.frequency * t)
        note = np.array([channel]).T
        self.audio = np.append(self.audio, note)

    def fromtext(self, text):
        self.audio = np.array([])
        text = text.upper()
        for c in text:
            if c == ' ':
                self.add_note(self.unittime * 4, True)
                continue
            if not c in self.morse_table:
                continue
            for d in self.morse_table[c]:
                if d == '.':
                    self.add_note(self.unittime, False)
                else:
                    self.add_note(self.unittime * 3, False)
                self.add_note(self.unittime, True)
            self.add_note(self.unittime * 2, True)

    def export(self, filename, noise=0):
        self.audio += noise * (np.random.rand(self.audio.size) - 0.5)
        soundbytes = (self.audio * (2 ** 15 - 1)).astype('<h').tobytes()
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.samplerate)
            f.writeframes(soundbytes)

if __name__ == '__main__':
    morse = Morse()
    morse.fromtext("The quick brown fox jumps over the lazy dog.")
    morse.export('morse.wav', noise=0.1)

