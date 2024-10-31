from soundmanager import *

sounds = ["storage/sound.wav"]

rms, f0, pitch, activeDurations = processAudioFiles(sounds)
cry = isCrying(rms, f0, pitch, activeDurations)

print(cry)