import librosa
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pandas as pd

babysDataset = pd.read_csv("baby_crying_dataset.csv")
x = babysDataset.drop(columns=['Crying']).values
scaler = StandardScaler()
x = scaler.fit_transform(x)
y = babysDataset['Crying']
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, train_size=0.7, stratify=y)

model = LogisticRegression()
model.fit(x_train, y_train)

y_predict = model.predict(x_test)
accuracy = accuracy_score(y_test, y_predict)
print(f"Accuracy: {accuracy:.2f}")

def predict_baby(Rms, Frequency, Speech_Modular, Segment_Audio_Duration):
    data_array = np.array([[Rms, Frequency, Speech_Modular, Segment_Audio_Duration]])
    data_array = scaler.transform(data_array)
    result = model.predict(data_array)
    return "The baby is crying." if result[0] == 1 else "Baby is happy."

def calculateRms(audioPath):
    start = time.time()
    y, sr = librosa.load(audioPath, sr=22050)
    rms = librosa.feature.rms(y=y)[0]
    print("Time taken for sound", round(time.time() - start, 2))
    return float(np.mean(rms)), float(np.std(rms))

def calculateFundamentalFrequency(audioPath):
    start = time.time()
    y, sr = librosa.load(audioPath, sr=22050)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0Filtered = f0[~np.isnan(f0)]
    print("Time taken for sound", round(time.time() - start, 2))
    return float(np.mean(f0Filtered)), float(np.std(f0Filtered))

def calculatePitchModulation(audioPath):
    start = time.time()
    y, sr = librosa.load(audioPath, sr=22050)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0Filtered = f0[~np.isnan(f0)]
    pitchModulation = np.diff(f0Filtered)
    print("Time taken for sound", round(time.time() - start, 2))
    return float(np.mean(pitchModulation)), float(np.std(pitchModulation))

def calculateActiveSegmentDurations(audioPath):
    start = time.time()
    y, sr = librosa.load(audioPath, sr=22050)
    rms = librosa.feature.rms(y=y)[0]
    threshold = 0.02
    activity = rms > threshold
    activeSegments = np.diff(np.flatnonzero(np.concatenate(([activity[0]], activity[:-1] != activity[1:], [True]))))[::2]
    activeSegments = activeSegments * (len(y) / sr) / len(rms)
    print("Time taken for sound", round(time.time() - start, 2))
    return [float(n) for n in list(activeSegments)]

def processAudioFiles(audioPaths):
    rmsResults = calculateRms(audioPaths[0])
    f0Results = calculateFundamentalFrequency(audioPaths[0])
    f0Results = list(map(lambda x: x * 0.4641498494259757, f0Results))
    pitchResults = calculatePitchModulation(audioPaths[0])
    pitchResults = list(map(lambda x: x * 0.1406827751568227, pitchResults))
    activeDurations = calculateActiveSegmentDurations(audioPaths[0])
    activeDurations = list(map(lambda x: x * 0.8004364429896344, activeDurations))
    return rmsResults, f0Results, pitchResults, activeDurations

def isCrying(rms, f0, pitch, activeDurations):
    rmsMean, _ = rms
    f0Mean, _ = f0
    _, pitchStd = pitch
    
    rmsThreshold = 0.03
    f0ThresholdRange = (100, 500)
    pitchStdThreshold = 10
    activeDurationThreshold = 0.5
    
    isRmsHigh = rmsMean > rmsThreshold
    isF0InRange = f0ThresholdRange[0] < f0Mean < f0ThresholdRange[1]
    isPitchModulationHigh = pitchStd > pitchStdThreshold
    totalActiveDuration = sum(activeDurations)
    isActiveDurationLong = totalActiveDuration > activeDurationThreshold
    
    conditions = [isRmsHigh, isF0InRange, isPitchModulationHigh, isActiveDurationLong]
    return sum(conditions) > len(conditions) // 2
