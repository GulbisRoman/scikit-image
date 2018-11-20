import numpy as np
from skimage import io
import os
import warnings

warnings.filterwarnings("ignore")

def subscale(image, x, y, value, coff):
	for w in range(coff):
		for h in range(coff):
			image[x + w, y + h] = value

def scale(image, coff):
	shape = image.shape
	newimage = np.random.randint(0, 2, size=(image.shape[0] * coff, image.shape[1] * coff))

	for i in range(shape[0]):
		for j in range(shape[1]):
			subscale(newimage, i * coff, j * coff, image[i, j], coff)

	return newimage


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

def generateRandomStateOfLive(size, iterations):
	field = np.random.randint(0, 2, size=size)
	return generateStateOfLive(field, iterations)


# Играем в жизнь
states = generateRandomStateOfLive(size=(10, 10), iterations=10)
#field = np.zeros((10, 10))
#field[0, 1] = 1
#field[1, 2] = 1
#field[2, 0] = 1
#field[2, 1] = 1
#field[2, 2] = 1
#states = generateStateOfLive(field, iterations=10)

# Сохраняем
if not os.path.exists('images/kek'):
	os.makedirs('images/kek')

for i in range(len(states)):
	io.imsave('images/kek/{:04d}.png'.format(i + 1), scale(states[i] * 255, 50))