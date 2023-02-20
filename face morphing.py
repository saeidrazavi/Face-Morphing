import cv2
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import sys
import moviepy.video.io.ImageSequenceClip
import os


def wrap(trans: np.ndarray, trans2, image: np.ndarray, image1: np.ndarray, image_des: np.ndarray, x, y, len, a):

    [cols, rows] = image.shape[:2]

    inverse_trans1 = trans  # inverse of tranformation matrix
    inverse_trans2 = trans2  # inverse of tranformation matrix

    dst1 = cv2.warpAffine(source1, inverse_trans1, (2*cols, 2*rows))

    dst2 = cv2.warpAffine(source2, inverse_trans2, (2*cols, 2*rows))

    image_des[x, y, :] = (
        1-a/45)*dst1[x, y, :]+a/45*dst2[x, y, :]

    image_des = cv2.cvtColor(image_des, cv2.COLOR_BGR2RGB)

    return image_des


# ------------------------------
# ----------------------

def read_cor(name_of_file: str):

    txt = open(name_of_file, 'r')
    line = txt.readline()
    number_of_data = int(line)

    x_cor = []
    y_cor = []

    points = []

    for x in range(0, number_of_data):
        line = txt.readline()
        temp = line.split()

        x_cor.append(np.float32(temp[0]))

        y_cor.append(np.float32(temp[1]))

        points.append([np.float32(temp[1]), np.float32(temp[0])])

    return np.array(x_cor), np.array(y_cor), np.array(points)

# --------------------------------


source1 = cv2.imread('res01.jpg')
source1 = np.array(cv2.cvtColor(source1, cv2.COLOR_BGR2RGB))
[c1, c2] = source1.shape[:2]


source2 = cv2.imread('res02.jpg')
source2 = np.array(cv2.cvtColor(source2, cv2.COLOR_BGR2RGB))


des = np.zeros_like(source2)

x_cor1, y_cor1, points1 = read_cor('cor1.txt')

x_cor2, y_cor2, points2 = read_cor('cor2.txt')


tri1 = Delaunay(points1)


dirName = './pic'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory ", dirName,  " Created ")
except FileExistsError:
    print("Directory ", dirName,  " already exists")


file = sys.argv[0]
dirname = os.path.dirname(file)
dirname = dirname + './' + 'pic'
path = dirname

for alpha in range(0, 46, 1):

    x_middle = ((1-alpha/45)*x_cor1+alpha/45*x_cor2)

    y_middle = ((1-alpha/45)*y_cor1+alpha/45*y_cor2)

    for j in range(0, len(tri1.simplices)):

        h1, h2, h3 = tri1.simplices[j]

        x1, x2, x3 = x_cor1[h1], x_cor1[h2], x_cor1[h3]
        y1, y2, y3 = y_cor1[h1], y_cor1[h2], y_cor1[h3]

        xx1, xx2, xx3 = x_cor2[h1], x_cor2[h2], x_cor2[h3]
        yy1, yy2, yy3 = y_cor2[h1], y_cor2[h2], y_cor2[h3]

        a1, a2 = [y1, x1], [yy1, xx1]
        b1, b2 = [y2, x2], [yy2, xx2]
        c1, c2 = [y3, x3], [yy3, xx3]

# -----------------------------------new cordinates position
        x1_new, x2_new, x3_new = x_middle[h1], x_middle[h2], x_middle[h3]
        y1_new, y2_new, y3_new = y_middle[h1], y_middle[h2], y_middle[h3]

        new_a = [y1_new, x1_new]
        new_b = [y2_new, x2_new]
        new_c = [y3_new, x3_new]
# ----------------------------------
# making dataset for input and output cordinates
        input_cors = np.array([a1, b1, c1], dtype=np.int32)
        output_cors = np.array([new_a, new_b, new_c], dtype=np.int32)

        m1 = cv2.getAffineTransform(
            np.array([a1, b1, c1]), np.array([new_a, new_b, new_c]))

        m2 = cv2.getAffineTransform(
            np.array([a2, b2, c2]), np.array([new_a, new_b, new_c]))

# inverse_trans = np.linalg.inv(m)  # inverse of tranformation matrix

        cv2.fillConvexPoly(des, output_cors, (0, 0, 255))

        x_t, y_t = np.where((des == [0, 0, 255]).all(axis=2))

        lenght = len(x_t)

        frame = wrap(m1, m2, source1, source2, des, x_t, y_t, lenght, alpha)

    cv2.imwrite(os.path.join(path, f'{alpha}.png'), frame)

    if(alpha == 15 or alpha == 30):

        temp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imsave(f"res0{alpha//15+2}.jpg", temp)


image_folder = dirname
fps = 30
image_files = []

# make gif
for i in range(1, 46, 1):
    image_files.append(image_folder + '/' + str(i) + ".png")

for i in range(45, 0, -1):
    image_files.append(image_folder + '/' + str(i) + ".png")

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
    image_files, fps=fps)
clip.write_videofile('q1.mp4')
