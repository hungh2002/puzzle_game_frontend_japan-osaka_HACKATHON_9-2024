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

os.chdir('/'.join(__file__.split('/')[:-1]))

IP_addr = 'bomu.info'
port_num = 60000
post_dic = {}
get_dic = {}

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
    "ranking":'''+self.ranking+'''
}
'''





RD = Read_Data()

get_dic['/make_room'] = RD.get_make_room
get_dic['/img_list'] = RD.get_img_list

get_dic['/'] = RD.get_intro_project_data
get_dic['/maintenance'] = RD.get_maintenance_data
get_dic['/css'] = RD.get_css_data
get_dic['/js'] = RD.get_js_data


listen_num = 10

wss_server = WSS.TCPServer(post_dic, get_dic, IP_addr, port_num, listen_num)

server_list = [threading.Thread(target=wss_server.serve) for i in range(listen_num)]
for i in server_list:
    i.start()


