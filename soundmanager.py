import librosa
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time

# Label: [1,4] ; 4: fast ; 1: slow

# 3
def calculateRms(audioPath):
  start = time.time()
  y, sr = librosa.load(audioPath, sr=22050)
  rms = librosa.feature.rms(y=y)[0]
  print("Time taken for sound", round(time.time()-start,2))
  return float(np.mean(rms)), float(np.std(rms))

# 1
def calculateFundamentalFrequency(audioPath):
  start = time.time()
  y, sr = librosa.load(audioPath, sr=22050)
  f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
  f0Filtered = f0[~np.isnan(f0)]
  print("Time taken for sound", round(time.time()-start,2))
  return float(np.mean(f0Filtered)), float(np.std(f0Filtered))

# 2
def calculatePitchModulation(audioPath):
  start = time.time()
  y, sr = librosa.load(audioPath, sr=22050)
  f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
  f0Filtered = f0[~np.isnan(f0)]
  pitchModulation = np.diff(f0Filtered)
  print("Time taken for sound", round(time.time()-start,2))
  return float(np.mean(pitchModulation)), float(np.std(pitchModulation))

# 4
def calculateActiveSegmentDurations(audioPath):
  start = time.time()
  y, sr = librosa.load(audioPath, sr=22050)
  rms = librosa.feature.rms(y=y)[0]
  threshold = 0.02
  activity = rms > threshold
  activeSegments = np.diff(np.flatnonzero(np.concatenate(([activity[0]], activity[:-1] != activity[1:], [True]))))[::2]
  activeSegments = activeSegments * (len(y) / sr) / len(rms)
  print("Time taken for sound", round(time.time()-start,2))
  return [float(n) for n in list(activeSegments)]

def processAudioFiles(audioPaths):
  """
  with ProcessPoolExecutor() as executor:
    rmsResults = list(executor.map(calculateRms, audioPaths))[0]
    f0Results = list(executor.map(calculateFundamentalFrequency, audioPaths))[0]
    f0Results = list(map(lambda x: x*0.4641498494259757, f0Results))
    pitchResults = list(executor.map(calculatePitchModulation, audioPaths))[0]
    pitchResults = list(map(lambda x: x*0.1406827751568227, pitchResults))
    activeDurations = list(executor.map(calculateActiveSegmentDurations, audioPaths))[0]
    activeDurations = list(map(lambda x: x*0.8004364429896344, activeDurations))
  return rmsResults, f0Results, pitchResults, activeDurations
  """
  rmsResults = calculateRms(audioPaths[0])
  f0Results = calculateFundamentalFrequency(audioPaths[0])
  f0Results = list(map(lambda x: x*0.4641498494259757, f0Results))
  pitchResults = calculatePitchModulation(audioPaths[0])
  pitchResults = list(map(lambda x: x*0.1406827751568227, pitchResults))
  activeDurations = calculateActiveSegmentDurations(audioPaths[0])
  activeDurations = list(map(lambda x: x*0.8004364429896344, activeDurations))
  return rmsResults, f0Results, pitchResults, activeDurations


def isCrying(rms, f0, pitch, activeDurations):
  rmsMean, _ = rms
  f0Mean, _ = f0
  _, pitchStd = pitch
  
  rmsThreshold = 0.03 # Original 0.03 / 0.05
  f0ThresholdRange = (100, 500)
  pitchStdThreshold = 10 # Original: 10
  activeDurationThreshold = 0.5
  
  isRmsHigh = rmsMean > rmsThreshold
  isF0InRange = f0ThresholdRange[0] < f0Mean < f0ThresholdRange[1]
  isPitchModulationHigh = pitchStd > pitchStdThreshold
  totalActiveDuration = sum(activeDurations)
  isActiveDurationLong = totalActiveDuration > activeDurationThreshold
  falseCounter = 0
  trueCounter = 0
  
  for i in [isRmsHigh, isF0InRange, isPitchModulationHigh, isActiveDurationLong]:
    if i:
      trueCounter += 1
    else:
      falseCounter += 1
      
  return trueCounter > falseCounter
