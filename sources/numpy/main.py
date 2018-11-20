import numpy as np
from skimage import io
from skimage import color

image = io.imread('images/pikachu.png')


print('type:', type(image))
print('shape:', image.shape)
print('min:', image.min())
print('mean:', image.mean())
print('max:', image.max())

print(image[100, 100])


image[345:370, 375:395] = [10, 10, 10, 255]
io.imsave('images/h.png', image)

image = io.imread('images/pikachu.png')
mask = np.logical_and(np.logical_and(image[:, :, 0] > 150, image[:, :, 1] > 150), image[:, :, 2] < 150)
image[mask] = [128, 166, 255, 255]
io.imsave('images/g.png', image)