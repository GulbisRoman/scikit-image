import numpy as np
from skimage import io
import warnings

warnings.filterwarnings("ignore")

base = np.random.randint(0, 2, size=(100, 100))
io.imsave('images/base.png', base * 255)