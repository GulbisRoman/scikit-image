import numpy as np
from skimage import io
import os
import sys
import warnings

warnings.filterwarnings("ignore")

import ctypes
import ctypes.wintypes
import time

def get_size(obj, seen=None):
	# From https://goshippo.com/blog/measure-real-size-any-python-object/
	# Recursively finds size of objects
	size = sys.getsizeof(obj)
	if seen is None:
		seen = set()
	obj_id = id(obj)
	if obj_id in seen:
		return 0

	# Important mark as seen *before* entering recursion to gracefully handle
	# self-referential objects
	seen.add(obj_id)
	if isinstance(obj, dict):
		size += sum([get_size(v, seen) for v in obj.values()])
		size += sum([get_size(k, seen) for k in obj.keys()])
	elif hasattr(obj, '__dict__'):
		size += get_size(obj.__dict__, seen)
	elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
		size += sum([get_size(i, seen) for i in obj])
	return size

def next(x, y, shape):
	return x - shape[0] if(x >= shape[0]) else x, y - shape[1] if(y >= shape[1]) else y

def evolve(data):
	base = np.copy(data)
	field = np.copy(data)
	shape = field.shape
	for i in range(shape[0]):
		for j in range(shape[1]):
			friendly_neighborhood = base[i - 1, j - 1] + base[i, j - 1] + base[next(i + 1, j - 1, shape)] + base[i - 1, j] + base[next(i + 1, j, shape)] + base[next(i - 1, j + 1, shape)] + base[next(i, j + 1, shape)] + base[next(i + 1, j + 1, shape)]
			if(base[i, j]):
				field[i, j] = int(friendly_neighborhood == 2 or friendly_neighborhood == 3)
			else:
				field[i, j] = int(friendly_neighborhood == 3)
	return field

def generateStateOfLive(base, iterations):
	states = [base]
	for i in range(iterations):
		states.append(evolve(states[-1]))

	return states

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
starting_time = ctypes.wintypes.LARGE_INTEGER()
ending_time = ctypes.wintypes.LARGE_INTEGER()
elapsed_microseconds = ctypes.wintypes.LARGE_INTEGER()
frequency = ctypes.wintypes.LARGE_INTEGER()

kernel32.QueryPerformanceFrequency(ctypes.byref(frequency)) 
kernel32.QueryPerformanceCounter(ctypes.byref(starting_time))
	
base = io.imread('images/base.png') // 255
states = generateStateOfLive(base, 100)

#print(get_size(states))

# Сохраняем
if not os.path.exists('images/e'):
	os.makedirs('images/e')

for i in range(len(states)):
	io.imsave('images/e/{:04d}.png'.format(i + 1), states[i] * 255)
	
kernel32.QueryPerformanceCounter(ctypes.byref(ending_time))
elapsed_microseconds = ending_time.value - starting_time.value
elapsed_microseconds *= 1000
elapsed_microseconds /= frequency.value

print(elapsed_microseconds)
