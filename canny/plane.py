import numpy as np
from skimage import io
from skimage import feature
from skimage import color

image = io.imread('plane.png')
edges = feature.canny(color.rgb2gray(image), sigma=4)
io.imsave('gray.png', color.rgb2gray(image))
io.imsave('result.png', edges * 255)