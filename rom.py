from PIL import Image
import numpy as np

ROWS = 12
COLS = 15

with open('out.txt', 'r') as f:
    bits = f.read().split()


pxl_list = list(map(lambda x: [0, 0, 0] if x ==
                '0' else [255, 255, 255], bits))

pxls = np.zeros((ROWS, COLS, 3), dtype=np.uint8)

for r in range(ROWS):
    for c in range(COLS):
        pix_num = r*15 + c
        pxls[r][c] = pxl_list[pix_num]


new_image = Image.fromarray(pxls)
new_image.save('ard_out11.png')
