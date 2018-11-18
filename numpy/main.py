import numpy as np
from skimage import io
from skimage import color

image = io.imread('pikachu.png')


print('type:', type(image))
print('shape:', image.shape)
print('min:', image.min())
print('mean:', image.mean())
print('max:', image.max())

print(image[100, 100])


#image[345:370, 375:395] = [10, 10, 10, 255]
#io.imsave('h.png', image)


#mask = np.logical_and(image[:, :, 0] > 100, image[:, :, 1] > 100)
#image[mask] = [128, 166, 255, 255]
#io.imsave('g.png', image)