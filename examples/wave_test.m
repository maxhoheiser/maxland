W = BpodWavePlayer('COM6');

W.SamplingRate = 1000; % Set the sampling rate to 1kHz
MyWave = ones(1,100000)*5; % Vector to play back, with 5V at every sample for 100s total play-time at 1kHz
W.loadWaveform(1, MyWave); % Load the waveform to the device as waveform 1

while i <= 1000
    W.play([1,2,3,4], 1);
    i = i+1;

clear W