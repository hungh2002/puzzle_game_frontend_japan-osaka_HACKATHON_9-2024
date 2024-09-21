import matplotlib.pyplot as plt
import random
from matplotlib.transforms import Affine2D

#背景画像を生成
x = 0
y = 0
size = 0
fig,ax = plt.subplots(figsize=(4,4),dpi = 256)
#背景を白に設定
ax.set_facecolor("white")

shapes = ["o","v","s","8","p","*","h","D","X"]

for a in range(20):
    x, y = random.uniform(0, 1), random.uniform(0, 1)  # ランダムな位置
    size = random.uniform(10, 2000)  # マーカーサイズ
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
plt.show()