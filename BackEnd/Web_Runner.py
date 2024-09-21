'''
=====================================
Copyright © Masataka Okubo. All rights reserved.

All copyrights of this program belong to the creator, "Masataka Okubo."
Please be sure to obtain permission from the author when using, modifying, sharing, or publishing these programs.
Performing these actions without express permission from the author is copyright infringement and subject to legal penalties.
=====================================
'''

import web_server_sider_MODULE_ver000013 as WSS
import threading
import os
import hashlib
import time
import json
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math

#from ..Produce_Image import StringToImage as STI

os.chdir('/'.join(__file__.split('/')[:-1]))

IP_addr = 'bomu.info'
port_num = 3000
post_dic = {}
get_dic = {}


#作成した画像を16分割する
def ImgSplit(im,quarter):
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



class Image_Maker:
    def __init__(self):
        pass

    def produce_img(self):

        # 複数行の文字を出すのに、行ごとリストに入れてforで回す
        texts = []
        quiz = []
        with open("Quiz_Text.txt","r") as f: #入力されたファイルを読み込む(デフォでNO1_58_...スタートになってる)
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
        quarter = math.ceil(len(ntexts)/4)
        print(quarter)

        nquiz = [
            ntexts[0:quarter],
            ntexts[quarter:quarter*2],
            ntexts[quarter*2:quarter*3],
            ntexts[quarter*3:]
        ]
        print(nquiz)

        # PCローカルのフォントへのパスと、フォントサイズを指定
        #font_path = "/Library/Fonts/BIZUDGothic-Bold.ttf"
        #font = ImageFont.truetype(font_path, 60)
        font = ImageFont.truetype('Arial.ttf', 60)

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
        image.save("base_image.png")

        #os.makedirs("SplitImg", exist_ok=True)
        #ファイルを開く
        im = Image.open("base_image.png")
        ims = ImgSplit(im,quarter)
        for i, img in enumerate(ims):
            img.save("img_" + str(int(i%self.width)) + str(int(i/self.width)) + ".png")

IM = Image_Maker()

###############################################################

def exist_check(path):
    return os.path.isfile(path)

def add_file(path):
    with open(path, mode='x',encoding='utf-8') as f:
        f.write('')

def read_file(path):
    with open(path,encoding='utf-8') as f:
        dl = f.read()
    return dl

def edit_file(path, dl):
    with open(path, mode='w',encoding='utf-8') as f:
        f.write(dl)

###############################################################



import hashlib
import time

def make_hash(di):
    return hashlib.sha256(di.encode()).hexdigest()

class Random_Module:

    def __init__(self,seed):
        self.seed = seed

    def rnd(self,max):
        output = int(make_hash(self.seed)[:8], 16) % max
        self.seed = make_hash(self.seed + str(output) + str(time.time()))
        return output

RM = Random_Module('Seed_2525' + str(time.time()))



def shuffle_puzzle(w,h):
    board = [[[i,e] for e in range(h)] for i in range(w)]
    for i in range(100):
        x = RM.rnd(w)
        y = RM.rnd(h)
        
        mv_x =  1 - 1 * RM.rnd(2)
        mv_y =  1 - 1 * RM.rnd(2)

        if x + mv_x < 0 or x + mv_x >= w:
            mv_x = -mv_x
        if y + mv_y < 0 or y + mv_y >= h:
            mv_y = -mv_y
        
        status = board[x][y]
        board[x][y] = board[x + mv_x][y + mv_y]
        board[x + mv_x][y + mv_y] = status
    return board




###############################################################





class Read_Data:
    def __init__(self):
        self.data_dic = {}
        self.width = 4
        self.height = 4

        self.ranking = []

        self.question = ""
        self.choice = []
        self.answer = 0

        self.start_hour = 0
        self.start_minute = 0

        self.finish_hour = 0
        self.finish_minute = 0

    def get_aasddds(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/html'
        if len(path_split) == 2:
            now_path = 'news.html'
        else:
            now_path = 'news/'+str(path_split[2])+'.html'
        
        html_data = self.data_dic.get(now_path)
        if html_data == None:
            html_data = read_file(now_path)

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def get_css_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/css'

        html_data = self.data_dic.get('css/'+str(path_split[2])+'')
        if html_data == None:
            html_data = read_file('css/'+str(path_split[2])+'')

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def get_js_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/js'

        html_data = self.data_dic.get('js/'+str(path_split[2])+'')
        if html_data == None:
            html_data = read_file('js/'+str(path_split[2])+'')

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def get_make_room(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        self.ranking = []
        self.question = "りんごは何色ですか？"
        self.choice = ["赤","黄","青","緑"]
        self.answer = 0

        dt_now = datetime.datetime.now()

        dt_start = dt_now + datetime.timedelta(minutes = 1)

        self.start_hour = dt_start.hour
        self.start_minute = dt_start.minute

        dt_finish = dt_start + datetime.timedelta(minutes = 3)

        self.finish_hour = dt_finish.hour
        self.finish_minute = dt_finish.minute

        IM.produce_img()

        html_data = '''{
    "result":"success"
}'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode
    
    def get_img_list(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        board = shuffle_puzzle(self.width,self.height)

        '''img_list = []
        for i in range(4):
            for e in range(4):
                img_list.append("img_"+str(i)+str(e)+".png")
        img_list_str = json.dumps(img_list)'''

        pos_dic = {}
        for i in range(4):
            pos_dic[i] = {}
            for e in range(4):
                pos_dic[i][e] = "img_"+str(board[i][e][0])+str(board[i][e][1])+".png"
        pos_dic_str = json.dumps(pos_dic)


        html_data = '''{
    "pos":'''+pos_dic_str+'''
}
'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode
    
    def get_ranking(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        html_data = '''{
    "ranking":'''+json.dumps(self.ranking)+'''
}
'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def get_q_and_a(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        html_data = '''{
    "question":'''+self.question+''',
    "answer":'''+json.dumps(self.choice)+''',
    "start_time":{
        "hour":"'''+str(self.start_hour)+'''",
        "minute":"'''+str(self.start_minute)+'''"
    },
    "finish_time":{
        "hour":"'''+str(self.finish_hour)+'''",
        "minute":"'''+str(self.finish_minute)+'''"
    }
}
'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def post_send_answer(self, path_split, user_cookie, cookie_data, post_dic):
        content_type = 'application/json'

        html_data = '''{
    "result":"success"
}
'''
        if self.answer == int(post_dic['choice_answer']):
            self.ranking.append(post_dic['user_name'])
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode



RD = Read_Data()

get_dic['/make_room'] = RD.get_make_room
get_dic['/img_list'] = RD.get_img_list
get_dic['/q_and_a'] = RD.get_q_and_a
get_dic['/ranking'] = RD.get_ranking

post_dic['/send_answer'] = RD.post_send_answer

get_dic['/css'] = RD.get_css_data
get_dic['/js'] = RD.get_js_data


listen_num = 10

wss_server = WSS.TCPServer(post_dic, get_dic, IP_addr, port_num, listen_num)

server_list = [threading.Thread(target=wss_server.serve) for i in range(listen_num)]
for i in server_list:
    i.start()


