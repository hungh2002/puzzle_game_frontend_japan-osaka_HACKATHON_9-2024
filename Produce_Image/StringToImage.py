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


