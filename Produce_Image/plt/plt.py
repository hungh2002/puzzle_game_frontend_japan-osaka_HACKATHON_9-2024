import matplotlib.pyplot as plt
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from matplotlib.transforms import Affine2D


#背景画像を生成
x = 0
y = 0
size = 0
imgsize = 2048
fig,ax = plt.subplots(figsize=(20.48,20.48))
#背景を白に設定
ax.set_facecolor("white")

square_size = imgsize // 4

shapes = ["o","v","s","8","p","*","h","D","X"]
for h in range(2):
    for i in range(4):
        for j in range(4):
            #位置の記録
            # 正方形の中心位置を計算
            x_center = (j + 0.5) * square_size
            y_center = (i + 0.5) * square_size

            # print(x_center,y_center)

            # ランダムなオフセットを追加
            x_offset = random.uniform(-0.1 * square_size, 0.1 * square_size)
            y_offset = random.uniform(-0.1 * square_size, 0.1 * square_size)

            # print(x_offset,y_offset)

            x = x_center + x_offset
            y = y_center + y_offset

            # print(x,y)

            size = random.uniform(100, 5000)  # マーカーサイズ(面積)
            color = (random.random(), random.random(), random.random())  # ランダムな色
            marker = random.choice(shapes) 
            rotate = random.uniform(0, 180)  # マーカーの回転角度
            t = Affine2D().rotate_deg(rotate) + ax.transData  # 回転行列
            # マーカーをプロット
            ax.scatter(x, y, s=size, c=[color], marker=marker, alpha=0.4, transform=t)

#図を正方形に
ax.set_aspect('equal')
# 軸を非表示に
plt.axis("off")


#画像を表示
# plt.show()
