import numpy as np
from skimage import io
import os

def next(x, y, shape):
	return x - shape[0] if(x >= shape[0]) else x, y - shape[1] if(y >= shape[1]) else y

def evolve(data):
	field = np.copy(data)
	shape = field.shape
	for i in range(shape[0]):
		for j in range(shape[1]):
			friendly_neighborhood = field[i - 1, j - 1] + field[i, j - 1] + field[next(i + 1, j - 1, shape)] + field[i - 1, j] + field[next(i + 1, j, shape)] + field[next(i - 1, j + 1, shape)] + field[next(i, j + 1, shape)] + field[next(i + 1, j + 1, shape)]
			o = field[i, j]
			if(field[i, j]):
				field[i, j] = int(friendly_neighborhood == 2 or friendly_neighborhood == 3)
			else:
				field[i, j] = int(friendly_neighborhood == 3)
	return field

def generateStateOfLive(**kwargs):
	field = np.random.randint(0, 2, size=kwargs['size'])

	states = [field]
	for i in range(kwargs['iterations']):
		states.append(evolve(states[-1]))

	return states

states = generateStateOfLive(size=(25, 25), iterations=10)

# Сохраняем

if not os.path.exists('kek'):
	os.makedirs('kek')

for i in range(len(states)):
	io.imsave('kek/{:04d}.png'.format(i + 1), states[i] * 255)