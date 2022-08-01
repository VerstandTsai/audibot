import wave
import numpy as np

class Morse:
    def __init__(self, unittime, samplerate, frequency):
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
        channel = np.sin(2 * np.pi * int(not isrest) * self.frequency * t)
        note = np.array([channel]).T
        self.audio = np.append(self.audio, note)
        self.audio = self.audio.reshape(self.audio.shape[0], 1)

    def fromtext(self, text):
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

    def export(self, filename):
        soundbytes = (self.audio * (2 ** 15 - 1)).astype('<h').tobytes()
        with wave.open(filename, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.samplerate)
            f.writeframes(soundbytes)

if __name__ == '__main__':
    morse = Morse(0.05, 44100, 700)
    morse.fromtext("All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.")
    morse.export('morse.wav')

