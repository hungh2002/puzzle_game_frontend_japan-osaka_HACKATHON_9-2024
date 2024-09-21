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
import datetime
import math

import API_KEY

import discord
from discord import app_commands

import Token

TOKEN = Token.TOKEN

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


#カレントディレクトリをしっかりと指定
os.chdir('/'.join(__file__.split('/')[:-1]))

IP_addr = 'bomu.info'
port_num = 3000
post_dic = {}
get_dic = {}



##################################################################################################


import google.generativeai as genai


#Geminiを使用した問題文の生成

def make_quiz(level='一般人', genre = '地理'):
    while True:
        prompt = f"""
        4択問題を一つだけ考えてください。難易度は{level}が解くレベルです。また、問題のジャンルは「{genre}」でお願いします。答えは一つになるように。
        以下の形式で答えてください:
        {{
            "question": "string",
            "choices": ["string1", "string2", "string3", "string4"],
            "answer": "string"
        }}
        """
        response = model.generate_content(prompt)
        # JSONとしてパースする
        response_data = json.loads(response.text)
        question = response_data['question']
        answer = answer=response_data['answer']
        if (accuracy_check(question,answer)==True):
            break
        print('問題と答えの生合成が取れていない')
    return response_data

#回答の妥当性のチェック
def accuracy_check(question,answer):
    prompt = f"""{question}の答えとして{answer}は妥当の妥当性を1から100の整数で評価して。100が最も妥当性が高いとする.答えは数字のみ
    """
    accuracy = model.generate_content(prompt)
    print(accuracy.text)
    if(int(accuracy.text) > 80):
        return True
    elif(int(accuracy.text)>=0 ):
        return False
    else:
        print('プロンプトエラー')
        return False


# API-KEYの設定
GOOGLE_API_KEY=API_KEY.key
if not GOOGLE_API_KEY:
    raise EnvironmentError("Google APIキーが設定されていません。環境変数を確認してください。")

genai.configure(api_key=GOOGLE_API_KEY)
#モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash",generation_config={"response_mime_type": "application/json"})



##################################################################################################

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



#スライドパズル用素材画像生成クラス
class Image_Maker:
    def __init__(self):
        pass

    def produce_img(self, question_text, width):

        # 複数行の文字を出すのに、行ごとリストに入れてforで回す
        texts = []
        quiz = []

        ntexts = question_text

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
        print("D_Flags_00000")
        font = ImageFont.truetype('./Noto_Sans_JP/NotoSansJP-VariableFont_wght.ttf', 60)

        print("D_Flags_00001")
        # RGB, 画像サイズ, 背景色を設定
        image = Image.new("RGB", (quarter*60 + 20, quarter*60 + 20), (255, 255, 255))

        print("D_Flags_00002")
        draw = ImageDraw.Draw(image)
        print("D_Flags_00003")
        # 文字描画の初期位置（画像左上からx, yだけ離れた位置）
        x = 10
        y = 10

        # 文字の描画
        for i in range(4):
            # 描画位置、描画する文字、文字色、フォントを指定
            draw.text((x, y), nquiz[i], fill=(0, 0, 0), font=font)
            y += (quarter*60 - 60) // 3

        print("D_Flags_00004")
        # ファイルに出力
        image.save("base_image.png")

        print("D_Flags_00005")
        #os.makedirs("SplitImg", exist_ok=True)
        #ファイルを開く
        im = Image.open("base_image.png")
        print("D_Flags_00006")
        ims = ImgSplit(im,quarter)
        print("D_Flags_00007")
        for i, img in enumerate(ims):
            img.save("img_" + str(int(i%width)) + str(int(i/width)) + ".png")
        print("D_Flags_00008")

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

#hash関数生成関数
def make_hash(di):
    return hashlib.sha256(di.encode()).hexdigest()

#hash値による乱数生成クラス
class Random_Module:

    def __init__(self,seed):
        self.seed = seed

    def rnd(self,max):
        output = int(make_hash(self.seed)[:8], 16) % max
        self.seed = make_hash(self.seed + str(output) + str(time.time()))
        return output

RM = Random_Module('Seed_2525' + str(time.time()))


#スライドパズルのシャッフル関数
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

        #スライドパズルの横方向の個数と縦方向の個数
        self.width = 4
        self.height = 4

        #ランキングリスト
        self.ranking = []

        #問題文と選択肢と正解
        self.question = ""
        self.choice = []
        self.answer = ""

        #開始時刻
        self.start_hour = 0
        self.start_minute = 0

        #終了時刻
        self.finish_hour = 0
        self.finish_minute = 0

    #CSSファイルリクエストへの対応関数
    def get_css_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/css'

        html_data = self.data_dic.get('css/'+str(path_split[2])+'')
        if html_data == None:
            html_data = read_file('css/'+str(path_split[2])+'')

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    #JavaScriptファイルへの対応関数
    def get_js_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/js'

        html_data = self.data_dic.get('js/'+str(path_split[2])+'')
        if html_data == None:
            html_data = read_file('js/'+str(path_split[2])+'')

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    #部屋の作成リクエストへの対応関数
    def get_make_room(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        #ランキングを初期化
        self.ranking = []

        #問題文と選択肢と回答を生成する
        response = make_quiz()

        self.question = response['question']
        self.choice = response['choices']
        self.answer = response['answer']

        print('Debug_Flag_0000')
        dt_now = datetime.datetime.now()

        print('Debug_Flag_0001')

        #開始時刻は1分後に設定
        dt_start = dt_now + datetime.timedelta(minutes = 1)

        print('Debug_Flag_0002')
        self.start_hour = dt_start.hour
        self.start_minute = dt_start.minute
        print('Debug_Flag_0003')

        #終了時刻は開始時刻の3分後に設定
        dt_finish = dt_start + datetime.timedelta(minutes = 3)

        self.finish_hour = dt_finish.hour
        self.finish_minute = dt_finish.minute

        #スライドパズルの素材画像生成
        IM.produce_img(self.question, self.width)

        html_data = '''{
    "result":"success"
}'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode
    
    #スライドパズルの初期状態における配置と画像一覧のリクエストへの対応関数
    def get_img_list(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        #画像の並べ方を決定
        board = shuffle_puzzle(self.width,self.height)

        pos_dic = {}
        for i in range(4):
            pos_dic[i] = {}
        for i in range(4):
            for e in range(4):
                pos_dic[e][i] = "img_"+str(board[i][e][0])+str(board[i][e][1])+".png"
        pos_dic_str = json.dumps(pos_dic)


        html_data = '''{
    "pos":'''+pos_dic_str+'''
}
'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode
    
    #ランキングリクエストへの対応関数
    def get_ranking(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        html_data = '''{
    "ranking":'''+json.dumps(self.ranking, ensure_ascii=False)+'''
}
'''
        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    #問題文と選択肢と開始時刻・終了時刻リクエストへの対応関数
    def get_q_and_a(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'application/json'

        html_data = '''{
    "question":"'''+self.question+'''",
    "answer":'''+json.dumps(self.choice, ensure_ascii=False)+''',
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

    #フロントエンドからのユーザーごとの回答送信への対応関数(POSTメソッド)
    def post_send_answer(self, path_split, user_cookie, cookie_data, post_dic):
        content_type = 'application/json'

        html_data = '''{
    "result":"success"
}
'''

        print('#########____RECV____##########')
        print(post_dic)
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

############################################################################################################


@tree.command(name="ゲーム開始設定",description="スライドパズルゲームの開始時刻と終了時刻を設定します")
@app_commands.choices(genre=[
    discord.app_commands.Choice(name="地理", value="地理"),
    discord.app_commands.Choice(name="スポーツ", value="スポーツ"),
    discord.app_commands.Choice(name="理科", value="理科"),
    discord.app_commands.Choice(name="数学", value="数学"),
    discord.app_commands.Choice(name="化学", value="化学"),
    discord.app_commands.Choice(name="物理", value="物理"),
    discord.app_commands.Choice(name="生物学", value="生物学"),
    discord.app_commands.Choice(name="天文学", value="天文学"),
    discord.app_commands.Choice(name="コンピューターサイエンス", value="コンピューターサイエンス"),
    discord.app_commands.Choice(name="テクノロジー", value="テクノロジー"),
    discord.app_commands.Choice(name="ゲーム", value="ゲーム"),
    discord.app_commands.Choice(name="料理", value="料理"),
    discord.app_commands.Choice(name="英語", value="英語"),
    discord.app_commands.Choice(name="健康", value="健康とフィットネス"),
    discord.app_commands.Choice(name="漫画", value="漫画"),
    discord.app_commands.Choice(name="アニメ", value="アニメ")
    ])
@app_commands.choices(difficulty=[
    discord.app_commands.Choice(name="めちゃむずレベル", value="専門家"),
    discord.app_commands.Choice(name="高校生レベル", value="高校生"),
    discord.app_commands.Choice(name="小学生レベル", value="小学生")
    ])
async def test_command(interaction: discord.Interaction,
                        start_min: int,
                        term_min: int,
                        genre: str,
                        difficulty: str):#デフォルト値を指定
    
    await interaction.response.send_message('ルーム作成を開始します',ephemeral=True)

    response = make_quiz(level = difficulty, genre = genre)

    RD.ranking = []
    RD.question = response['question']
    RD.choice = response['choices']
    RD.answer = response['answer']

    dt_now = datetime.datetime.now()
    dt_start = dt_now + datetime.timedelta(minutes = start_min)

    RD.start_hour = dt_start.hour
    RD.start_minute = dt_start.minute

    dt_finish = dt_start + datetime.timedelta(minutes = term_min)

    RD.finish_hour = dt_finish.hour
    RD.finish_minute = dt_finish.minute

    IM.produce_img(RD.question, RD.width)    

    mes = '''まもなくゲームが開始されます。\n参加をご希望される皆さんはお急ぎください。'''
    embed = discord.Embed(title = '=== ゲーム開始 ' + str(start_min) + ' 分前 ===', color = 0x00ff00, description = mes)
    
    mes = str(dt_start.hour) + '時' + str(dt_start.minute)+'分'
    embed.add_field(name = 'ゲーム開始時刻',value = mes,inline=False)

    mes = str(dt_finish.hour) + '時' + str(dt_finish.minute)+'分'
    embed.add_field(name = '終了時刻',value = mes,inline=False)

    mes = str(genre)
    embed.add_field(name = 'ジャンル',value = mes,inline=False)

    mes = str(difficulty)
    embed.add_field(name = '難易度',value = mes,inline=False)

    
    embed.set_footer(text="ゲーム開始予告")
    
    await interaction.channel.send(embed = embed)



@tree.command(name="稼働終了",description="Botを停止させる。管理者権限必須")
@app_commands.default_permissions(administrator=True)
async def test_command(interaction:discord.Interaction):
    await interaction.response.send_message("Botを停止します。",ephemeral=True)
    await client.close()




@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    await tree.sync()

    print('起動')

    
    


client.run(TOKEN)
