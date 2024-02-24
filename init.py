"""
Runs during docker build in order to pre-download additional
data files to ensure they are available at runtime.
"""
from load_models import load_ram_plus, load_ram, load_tag2text

IMAGE_SIZE = 384

load_ram_plus(IMAGE_SIZE)
load_ram(IMAGE_SIZE)
load_tag2text(IMAGE_SIZE)

print("Initialization complete")
