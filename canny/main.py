import numpy as np
from skimage import io
from skimage import feature
from skimage import color

image = io.imread('pikachu.png')
edges = feature.canny(color.rgb2gray(image))
io.imsave('r.png', edges * 255)
io.imsave('g.png', color.rgb2gray(image))