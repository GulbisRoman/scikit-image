import numpy as np
from skimage import io
from skimage import feature
from skimage import color
from skimage.filters import sobel
import warnings

warnings.filterwarnings("ignore")

# Пикачу
image = io.imread('images/pikachu.png')
io.imsave('images/pikachu_gray.png', color.rgb2gray(image))

sobel_image = sobel(color.rgb2gray(image))
io.imsave('images/pikachu_sobel.png', sobel_image)

edges = feature.canny(color.rgb2gray(image)) # default sigma=1.0
io.imsave('images/pikachu_result.png', edges * 255)

# Самолет
image = io.imread('images/plane.png')
io.imsave('images/plane_gray.png', color.rgb2gray(image))

sobel_image = sobel(color.rgb2gray(image))
io.imsave('images/plane_sobel.png', sobel_image)

edges = feature.canny(color.rgb2gray(image), sigma=4.0)
io.imsave('images/plane_result.png', edges * 255)