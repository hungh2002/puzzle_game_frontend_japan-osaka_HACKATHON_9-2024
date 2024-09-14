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

os.chdir('/'.join(__file__.split('/')[:-1]))

IP_addr = 'IP_addr'
port_num = 443
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



class Read_Data:
    def __init__(self):
        self.data_dic = {}
    def get_intro_project_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/html'
        if len(path_split) == 2:
            now_path = 'intro_project.html'
        else:
            now_path = 'intro_project/'+str(path_split[2])+'.html'
        
        html_data = self.data_dic.get(now_path)
        if html_data == None:
            html_data = read_file(now_path)

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode

    def get_news_data(self, path_split, user_cookie, bf_cookie_data):
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

    def get_maintenance_data(self, path_split, user_cookie, bf_cookie_data):
        content_type = 'text/html'

        html_data = self.data_dic.get('maintenance.html')
        if html_data == None:
            html_data = read_file('maintenance.html')

        add_cookie = False
        cookie_data = {}
        DL_mode = False
        return html_data, content_type, add_cookie, cookie_data, DL_mode
    
RD = Read_Data()

get_dic['/home.html'] = RD.get_home_data
get_dic['/'] = RD.get_home_data
get_dic['/maintenance'] = RD.get_maintenance_data
get_dic['/css'] = RD.get_css_data
get_dic['/js'] = RD.get_js_data

listen_num = 10

wss_server = WSS.TCPServer(post_dic, get_dic, IP_addr, port_num, listen_num)

server_list = [threading.Thread(target=wss_server.serve) for i in range(listen_num)]
for i in server_list:
    i.start()


