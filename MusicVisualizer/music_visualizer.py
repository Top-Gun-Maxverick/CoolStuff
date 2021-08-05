import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import TclError

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

fig,ax = plt.subplots(1, figsize=(15,7))

p = pyaudio.PyAudio()

stream = p.open(
	format = FORMAT,
	channels = CHANNELS,
	rate = RATE,
	input = True,
	output = True,
	frames_per_buffer = CHUNK
)

x = np.arange(0, 2*CHUNK, 2)

line, = ax.plot(x, np.random(CHUNK), '-', lw=2)
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0,255)
ax.set_xlim(0,2*CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2*CHUNK], yticks=[0,128,255])

plt.show(block=False)
print('stream started')

frame_count = 0
start_time = time.time()

while True:
	data = stream.read(CHUNK)
	data_int = struct.unpack(str(2*CHUNK) + 'B', data)
	data_np = np.array(data_int, dtype='b')[::2] + 128
	line.set_ydata(data_np)

	try:
		fig.canvas.draw()
		fig.canvas.flush_events()
		frame_count += 1
	except TclError:
		frame_rate = frame_count /(time.time()-start_time)
		print('stream stopped')
		print('average frame rate = {:.0f} FPS'.format(frame_rate))
		break
