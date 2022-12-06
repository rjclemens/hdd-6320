from PIL import Image
import numpy as np

ROWS = 12
COLS = 15

bits_per_ring = np.array([8, 14, 20, 26, 32, 38, 44])
starting_pos = np.array([0, 8, 22, 42, 68, 100, 138])
soft_mag = np.array([0, 11, 28, 42, 70, 101, 139])
diff = soft_mag - starting_pos
print(diff)


def rotate(arr, n):  # n=2: [1, 2, 3, 4, 5] -> [3, 4, 5, 1, 2]
    return arr[n:] + arr[:n]


def split_to_rings(bits):
    arr = []
    bit_num = 0
    for num in bits_per_ring:
        ring = []
        for _ in range(num):
            ring.append(bits[bit_num])
            bit_num += 1
        arr.append(ring)

    return arr


def argmax(arr):
    return arr.index(max(arr))


def argmin(arr):
    print(min(arr))
    return arr.index(min(arr))


def rotate_to_start(bit_list, volt_list):
    for i, volts in enumerate(volt_list):
        ind_min_volts = argmin(volts)  # find min index

        # find index of starting ring element
        st_index = ind_min_volts - diff[i]
        st_index = st_index % bits_per_ring[i]  # make index positive

        # rotate st_index to beginning
        bit_list[i] = rotate(bit_list[i], st_index)
        volts = rotate(volts, st_index)

    return bit_list


def collapse(bit_list):
    bits = []
    for b_list in bit_list:
        for b in b_list:
            bits.append(b)

    return bits


with open('out.txt', 'r') as f:
    bits = list(map(int, f.read().split()))

with open('volt.txt', 'r') as f:
    volts = list(map(float, f.read().split()))
    avg_voltage = sum(volts)/182

bit_list = split_to_rings(bits)
volt_list = split_to_rings(volts)

print("Avg Voltage: ", avg_voltage)

bit_list = rotate_to_start(bit_list, volt_list)
bits_st = collapse(bit_list)

print(bits)
print(bits_st)

white_row = np.zeros(ROWS)  # white pixel count per row

pxl_list = list(map(lambda x: [0, 0, 0] if x ==
                0 else [255, 255, 255], bits_st))

pxls = np.zeros((ROWS, COLS, 3), dtype=np.uint8)

for r in range(ROWS):
    for c in range(COLS):
        pix_num = r*15 + c
        if(pxl_list[pix_num] == [255, 255, 255]):
            white_row[r] += 1
        pxls[r][c] = pxl_list[pix_num]

print(white_row)
new_image = Image.fromarray(pxls)
new_image.save('ard_output/ard_out23.png')
