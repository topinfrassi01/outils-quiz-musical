import sys
from pathlib import Path
from pydub import AudioSegment
from natsort import natsorted
import csv

def convert_timeformat_to_ms(time_formatted):
    min_sec = time_formatted.split(':')

    return (int(min_sec[0])*60 + int(min_sec[1])) * 1000

if __name__ == '__main__':
    folder = Path(sys.argv[1])

    guesses = AudioSegment.silent(duration=2000)
    reveals = AudioSegment.silent(duration=2000)
    with open(folder / 'cuts.csv', 'r') as fs:
        csv_reader = csv.reader(fs)
        
        songs = [str(x) for x in list(folder.glob('*.mp3'))]
        songs = natsorted(songs)

        for mp3, cuts in zip(songs, csv_reader):
            ms_cuts = [convert_timeformat_to_ms(x) for x in cuts]
            
            sound = AudioSegment.from_mp3(str(mp3))

            guess = sound[ms_cuts[0]:ms_cuts[1]]
            reveal = sound[ms_cuts[2]:ms_cuts[3]]

            guesses += (guess + AudioSegment.silent(duration=2000))
            reveals += (reveal + AudioSegment.silent(duration=2000))

    guesses_fn = str(folder / 'quiz.mp3')
    reveals_fn = str(folder / 'reponses.mp3')

    guesses.export(guesses_fn, format="mp3")
    reveals.export(reveals_fn, format="mp3")