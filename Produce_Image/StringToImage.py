import readline
import math
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
"""
issue
1.正方形にするためどうしても空白が多くなってしまう
→5行も検討(？)・文字の横幅を調整する
"""

# 複数行の文字を出すのに、行ごとリストに入れてforで回す
texts = []
quiz = []
with open(str(input()),"r") as f: #入力されたファイルを読み込む(デフォでNO1_58_...スタートになってる)
    for w in f.read():  #ファイルの文章を読み込む
        texts.append(w)

#それぞれの文字列を1つの文字列に変換する
print(texts)
ntexts = "".join(texts)
print(ntexts)
quiz.append(ntexts)
print(quiz)
# test = ["こ れ は、","文 字 列 か ら","作 ら れ た ","画 像 で す 。"]

#文字列を4分割して、それぞれのリストに入れる
quarter = math.ceil(len(texts)/4)
print(quarter)

nquiz = [
    ntexts[0:quarter],
    ntexts[quarter:quarter*2],
    ntexts[quarter*2:quarter*3],
    ntexts[quarter*3:]
]
print(nquiz)

# PCローカルのフォントへのパスと、フォントサイズを指定
font_path = "/Library/Fonts/BIZUDGothic-Bold.ttf"
font = ImageFont.truetype(font_path, 60)

# RGB, 画像サイズ, 背景色を設定
image = Image.new("RGB", (quarter*60 + 20, quarter*60 + 20), (255, 255, 255))

draw = ImageDraw.Draw(image)
# 文字描画の初期位置（画像左上からx, yだけ離れた位置）
x = 10
y = 10

# 文字の描画
for i in range(4):
    # 描画位置、描画する文字、文字色、フォントを指定
    draw.text((x, y), nquiz[i], fill=(0, 0, 0), font=font)
    y += (quarter*60 - 60) // 3

# ファイルに出力
image.save("Produce_Image/image.png")

#作成した画像を16分割する
def ImgSplit(im):
    height = (quarter*60 + 20) // 4
    width = (quarter*60 + 20) // 4

    buff = []
    #縦の分割
    for y1 in range(4):
        #横の分割
        for x1 in range(4):
            #画像の切り取り
            x2 = x1 * width
            y2 = y1 * height
            # print(x2,y2,width + x2,height + y2)
            c = im.crop((x2, y2, width + x2, height + y2))
            buff.append(c)
    return buff

#スクリプトが直接害された場合にのみ実行される←？？
if __name__ == "__main__":
    os.makedirs("Produce_Image/SplitImg", exist_ok=True)
    #ファイルを開く
    im = Image.open("Produce_Image/image.png")
    ims = ImgSplit(im)
    for i, img in enumerate(ims):
        img.save("Produce_Image/SplitImg/image_" + str(i) + ".png")


import readline
import math
import os
import matplotlib.pyplot as plt
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from matplotlib.transforms import Affine2D
"""
issue
1.正方形にするためどうしても空白が多くなってしまう
→5行も検討(？)・文字の横幅を調整する
"""

# 複数行の文字を出すのに、行ごとリストに入れてforで回す
texts = []
quiz = []
with open(str(input()),"r") as f: #入力されたファイルを読み込む(デフォでNO1_58_...スタートになってる)
    for w in f.read():  #ファイルの文章を読み込む
        texts.append(w)

#それぞれの文字列を1つの文字列に変換する
print("texts : ",texts) #[こ, れ,  , は, 、, 文,  , 字,  , 列,  , か,  , ら,  , 作,  , ら,  , れ,  , た,  ,  , 画,  , 像,  , で,  , す,  ,  , 。]
ntexts = "".join(texts) 
print("ntexts : ",ntexts) #これ は、文 字 列 か ら作 ら れ た  画 像 で す  。
quiz.append(ntexts)
print("quiz : ",quiz) #['これ は、文字列から作られた 画像です 。']
# test = ["こ れ は、","文 字 列 か ら","作 ら れ た ","画 像 で す 。"]

#文字列を正方形に合うよう平方にして、それぞれのリストに入れる
quarter = math.ceil(len(texts)**0.5)
print("quarter : ",quarter)

nquiz = []
for i in range(quarter):
    nquiz.append(ntexts[i*quarter:(i+1)*quarter])
print("nquiz : ",nquiz)

# PCローカルのフォントへのパスと、フォントサイズを指定
font_path = "/Library/Fonts/BIZUDGothic-Bold.ttf"
font = ImageFont.truetype(font_path, 60)

# RGB, 画像サイズ, 背景色を設定
# image = Image.new("RGB", (quarter*60 + 20, quarter*60 + 20), (255, 255, 255))

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
for h in range(4):
    for i in range(4):
        for j in range(4):
            #位置の記録
            # 正方形の中心位置を計算
            x_center = (j + 0.5) * square_size
            y_center = (i + 0.5) * square_size

            # print(x_center,y_center)

            # ランダムなオフセットを追加
            x_offset = random.uniform(-0.4 * square_size, 0.4 * square_size)
            y_offset = random.uniform(-0.4 * square_size, 0.4 * square_size)

            # print(x_offset,y_offset)

            x = x_center + x_offset
            y = y_center + y_offset

            # print(x,y)

            size = random.uniform(100, 3000)  # マーカーサイズ(面積)
            color = (random.random(), random.random(), random.random())  # ランダムな色
            marker = random.choice(shapes) 
            rotate = random.uniform(0, 180)  # マーカーの回転角度
            # t = Affine2D().rotate_deg(rotate) + ax.transData  # 回転行列
            # マーカーをプロット
            ax.scatter(x, y, s=size, c=[color], marker=marker, alpha=0.4, )

#図を正方形に
ax.set_aspect('equal')
# 軸を非表示に
plt.axis("off")


#画像を表示
# plt.show()
# 画像を保存
plt.savefig("Produce_Image/backgroundImgProto.jpg", bbox_inches="tight", pad_inches=0)

# 背景画像を読み込む
backgroundImage = Image.open("Produce_Image/backgroundImgProto.jpg")

#文字サイズに合わせて画像をトリミング
text_size = quarter*60 + 20
backgroundWidth , backgroundHeight = backgroundImage.size
left = (backgroundWidth - text_size) //2
top = (backgroundHeight - text_size) //2
right = left + text_size
bottom = top + text_size

cropper_bg = backgroundImage.crop((left,top,right,bottom))

draw = ImageDraw.Draw(cropper_bg)
# 文字描画の初期位置（画像左上からx, yだけ離れた位置）
x = 10
y = 10

if len(ntexts) <= (quarter**2)-quarter:
    y += 30

# 文字の描画
for i in range(quarter):
    # 描画位置、描画する文字、文字色、フォントを指定
    draw.text((x, y), nquiz[i], fill=(0, 0, 0), font=font, stroke_width=2, stroke_fill=(250,250,250))
    y += 60

# ファイルに出力
cropper_bg.save("Produce_Image/image.png")

#作成した画像を16分割する
def ImgSplit(im):
    height = (quarter*60 + 20) // 4
    width = (quarter*60 + 20) // 4

    buff = []
    #縦の分割
    for y1 in range(4):
        #横の分割
        for x1 in range(4):
            #画像の切り取り
            x2 = x1 * width
            y2 = y1 * height
            # print(x2,y2,width + x2,height + y2)
            c = im.crop((x2, y2, width + x2, height + y2))
            buff.append(c)
    return buff

#スクリプトが直接害された場合にのみ実行される←？？
if __name__ == "__main__":
    os.makedirs("Produce_Image/SplitImg", exist_ok=True)
    #ファイルを開く
    im = Image.open("Produce_Image/image.png")
    ims = ImgSplit(im)
    for i, img in enumerate(ims):
        img.save("Produce_Image/SplitImg/image_" + str(i) + ".png")


