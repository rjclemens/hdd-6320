from PIL import Image
import numpy as np

pixels = [
    [(54, 54, 54), (232, 23, 93), (71, 71, 71), (168, 167, 167)],
    [(204, 82, 122), (54, 54, 54), (168, 167, 167), (232, 23, 93)],
    [(71, 71, 71), (168, 167, 167), (54, 54, 54), (204, 82, 122)],
    [(168, 167, 167), (204, 82, 122), (232, 23, 93), (54, 54, 54)]
]

# Convert the pixels into an array using numpy
array = np.array(pixels, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('new.png')


im = Image.open('cry.png')

h, w = im.size
block = (w*h)//182

px = im.load()

past = (0, 0, 0)
trans = (238, 238, 238)
white = (255, 255, 255)
pxls = np.zeros((11, 16, 3), dtype=np.uint8)
for r in range(h):
    for c in range(w):
        re, g, b, t = px[r, c]
        rgb = (re, g, b)
        pixel = r*w+c
        pixel_new = pixel//block
        if rgb == trans:
            rgb = white
        if not rgb == past:
            print("pixel {}: rgb {}".format(pixel_new, rgb))
        if(pixel_new < 176):
            pxls[pixel_new//16, pixel_new % 16] = rgb
        past = rgb

print(pxls)

# pxls = [
#     [(54, 54, 54, 255), (232, 23, 93, 255),
#      (71, 71, 71, 255), (168, 167, 167, 255)]
# ]
# print(array)
pxls = np.array(pxls, dtype=np.uint8)

new_image = Image.fromarray(pxls)
new_image.save('cry_cmpr.png')
