'''
=====================================
Copyright © Masataka Okubo. All rights reserved.

All copyrights of this program belong to the creator, "Masataka Okubo."
Please be sure to obtain permission from the author when using, modifying, sharing, or publishing these programs.
Performing these actions without express permission from the author is copyright infringement and subject to legal penalties.
=====================================
'''


import socket
import ssl

import urllib.parse

import threading


import os

import sys

import datetime


#Cookie処理用関数
def get_cookie(data):
    start_pos = data.find('Cookie: ') + 8
    if '\r' in data[start_pos:]:
        end_pos = data.find('\r\n', start_pos)
    else:
        end_pos = data.find('\n', start_pos)
    data = data[start_pos:end_pos]
    print('COOKIE_DATA:',data)
    data = data.split('; ')
    new_data = {}
    for i in data:
        if i != '':
            e = i.split('=',1)
            new_data[e[0]] = e[1]
    print(new_data)
    return new_data

#Cookieデータ作成用関数
def make_cookie_data(data):
    new_data = 'Set-Cookie: '
    for i in list(data.keys()):
        new_data += str(i)+'='+str(data[i])+'; '
    if '; ' in new_data:
        new_data = new_data[:-2]
    return new_data


#ソケットが閉じているかどうかの判定
def is_socket_closed(sock):
    try:
        # send がエラーを起こさない場合はソケットはまだオープン
        sock.send(b'')
        return False
    except:# (BrokenPipeError, ConnectionResetError):
        # エラーが発生した場合はソケットが閉じられている
        return True


class TCPServer:
    """
    TCP通信を行うサーバーを表すクラス
    """
    def __init__(self, post_dic, get_dic, IP_addr, port_num, listen_num):
        
        self.post_dic = post_dic
        self.get_dic = get_dic

        print("=== サーバーを起動します ===")

        try:
            # socketを生成
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.IP_addr = IP_addr
            self.port_num = port_num

            # socketをlocalhostのポート8080番に割り当てる
            self.server_socket.bind((self.IP_addr, self.port_num))
            self.server_socket.listen(listen_num)
            self.listen_num = listen_num
            
            self.URL_data = 'https://' + self.IP_addr + ':' + str(self.port_num)
        except Exception as e:
            print('!--CAUTION--!___ERROR___!--CAUTION--!')
            try:
                print('Type:'+str(type(e)))
            except:
                pass
            try:
                print('Args:'+str(e.args))
            except:
                pass
            try:
                print('Message:'+str(e.message))
            except:
                pass
            try:
                print('Error_Object:'+str(e))
            except:
                pass
            print('======================================')
    
    def serve(self):
        """
        サーバーを起動する
        """
        
        
        #http通信をSSL化してhttps通信にする
        for i in range(self.listen_num):
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="letsencrypt_SSL_BOMU.crt", keyfile="./letsencrypt_BOMU.key")
            context.load_verify_locations(cafile='letsencrypt_Middle_BOMU.crt')
            try:
                ssoc = context.wrap_socket(self.server_socket, server_side=True)#←Bad file descriptorの原因の箇所
                threading.Thread(target=self.handle_client, args=(ssoc,)).start()
            except:
                pass
    
    #メインの通信用関数
    def handle_client(self,ssoc):
        while True:
            html_data = ''
            try:
                #通信のタイムアウト時間を設定する
                socket.setdefaulttimeout(5.0)
                
                # 外部からの接続を待ち、接続があったらコネクションを確立する
                print("=== クライアントからの接続を待ちます ===")
                (client_socket, address) = ssoc.accept()
                print(f"=== クライアントとの接続が完了しました remote_address: {address} ===")
                try:
                    while True:
                        
                        # クライアントから送られてきたデータを取得する
                        request = client_socket.recv(10000000)
                        
                        recv_data = request.decode('Shift_JIS')
                        html_data = ''
                        
                        print('=========================RECV_DATA=========================')
                        print(recv_data)
                        print('===========================================================')
                        
                        recv_split = recv_data.split('\n')
                        
                        user_cookie = False
                        
                        cookie_data = []
                
                        print('CK_FLAG:0010')
                        if 'Cookie: ' in recv_data:
                            print('CK_FLAG:0011')
                            cookie_data = get_cookie(recv_data)
                            print('CK_FLAG:0012')
                            
                            user_cookie = True
                        print('CK_FLAG:0013')
                        
                        
                        content_type = 'text/html'
                        
                        #ファイルダウンロードモードをOFFにする
                        DL_mode = False
                        DL_data = b''

                        add_cookie = False
                        
                        get_mode = False
                        post_mode = False
                        post_data = []
                        print('_FLAG_:A000000')

                        if recv_split[0][0:7] == 'OPTIONS':
                            content_type = 'Authorization'
                            html_data = ''
                            path = recv_split[0][8:-10]
                        
                        #GETメソッドの場合はGet_ModeをONにする
                        if recv_split[0][0:3] == 'GET':
                            get_mode = True
                            print('Path:',recv_split[0][4:-10])
                            
                            path = recv_split[0][4:-10]
                        print('_FLAG_:A000001')

                        #GETメソッドの場合はPost_ModeをONにする
                        if recv_split[0][0:4] == 'POST':
                            post_mode = True
                            print('Path:',recv_split[0][5:-10])
                            
                            path = recv_split[0][5:-10]
                            
                            post_data = recv_split[-1].split('&')
                            post_dic = {}
                            print('_FLAG_:A000002')
                            for i in post_data:
                                if '=' in i:
                                    e = i.split('=',1)
                                    post_dic[urllib.parse.unquote(e[0])] = urllib.parse.unquote(e[1])
                        print('_FLAG_:A000003')

                        #画像送信に関する処理の部分
                        pic_send_mode = False
                        if '.png' in path:
                            pic_file_path = '.'+path
                            print(pic_file_path)
                            pic_send_mode = True
                            pic_type = 'png'
                        elif '.jpeg' in path or '.jpg' in path:
                            pic_file_path = '.'+path
                            print(pic_file_path)
                            pic_send_mode = True
                            pic_type = 'jpeg'
                            
                        if path != '/favicon.ico':
                            html_data = '<html><body><h1>No Support</h1></body></html>'
                        print('_FLAG_:A000004')
                        
                        path_split = path.split('/')
                        
                        #Post_Modeの時の処理内容
                        if post_mode:
                            print('pOsT_FlAg')
                            if '/'+path_split[1] in list(self.post_dic.keys()):
                                
                                print(path_split)
                                print(self.post_dic)
                                
                                #Postメソッド対応用の関数として登録されている関数を検索して処理させる
                                html_data, content_type, add_cookie, cookie_data, DL_mode = self.post_dic['/'+path_split[1]](path_split, user_cookie, cookie_data, post_dic)
                            else:
                                html_data = "<script>location = 'https://bomu.info/home.html';</script>"
                                content_type = 'text/html'
                                add_cookie = user_cookie
                                DL_mode = False

                        print('_FLAG_:A000005')

                        #Get_Modeの時の処理内容
                        if get_mode:
                            print('gEt_FlAg')
                            if '/'+path_split[1] in list(self.get_dic.keys()):
                                
                                print(path_split)

                                #GETメソッド対応用の関数として登録されている関数を検索して処理させる
                                html_data, content_type, add_cookie, cookie_data, DL_mode = self.get_dic['/'+path_split[1]](path_split, user_cookie, cookie_data)
                            else:
                                html_data = "<script>location = 'https://bomu.info/home.html';</script>"
                                content_type = 'text/html'
                                add_cookie = user_cookie
                                DL_mode = False
                            
                        print(path)
                        print('_FLAG_:A000006')
                        print(type(html_data))

                        #htmlに記載するURLを動的に変更できるようにするためのスペシャルタグ処理
                        html_data = html_data.replace('<>ThisIsURL<>',self.URL_data)
                        print('_FLAG_:A000007')
                        print(path,html_data)
                        
                        #ダウンロードモードがONの時にはダウンロード処置をさせる
                        if DL_mode:
                            content_type = 'application/force-download'
                            html_data = DL_data
                            data_length = len(html_data)
                        else:
                            data_length = len(html_data.encode('UTF-8'))
                        print('_FLAG_:A000008')
                        if pic_send_mode:
                            content_type = 'image/'+pic_type
                            with open(pic_file_path,'rb') as f:
                                html_data = f.read()
                            #DL_mode = True
                            data_length = len(html_data)
                        print('_FLAG_:A000009')

                        # 現在のGMT時間を取得
                        gmt_time = datetime.datetime.utcnow()

                        # GMT形式で文字列に変換
                        gmt_time_str = gmt_time.strftime('%a, %d %b %Y %H:%M:%S GMT')

                        print('CK_FLAG:0000')
                        cookie_data_str = ''
                        if add_cookie:
                            cookie_keys = list(cookie_data.keys())
                            for i in range(len(cookie_keys)-1):
                                cookie_data_str = '\n' + make_cookie_data({cookie_keys[i]:cookie_data[cookie_keys[i]]})
                                resP = '''HTTP/1.1 200 OK
Date: '''+gmt_time_str+'''
Server: Apache/2.4.41 (Unix)
Content-Location: index.html.ja
Vary: negotiate'''+cookie_data_str+'''
TCN: choice
Last-Modified: Thu, 29 Aug 2019 05:05:59 GMT
ETag: "2d-5913a76187bc0"
Accept-Ranges: bytes
Content-Length: ''' + str(data_length) + '''
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: ''' + str(content_type) + '''; charset=UTF-8
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: *
Access-Control-Allow-http: *
Access-Control-Allow-Mathod: *
Access-Control-Allow-Credentials: true
'''
                                cookie_data_str = ''
                                response = resP.encode('utf_8')
                                client_socket.send(response)
                            print('CK_FLAG:0001')
                            
                            cookie_data_str = '\n' + make_cookie_data({cookie_keys[-1]:cookie_data[cookie_keys[-1]]})
                            print('CK_FLAG:0002')
                        print('CK_FLAG:0003')
                        resP = '''HTTP/1.1 200 OK
Date: '''+gmt_time_str+'''
Server: Apache/2.4.41 (Unix)
Content-Location: index.html.ja
Vary: negotiate'''+cookie_data_str+'''
TCN: choice
Last-Modified: Thu, 29 Aug 2019 05:05:59 GMT
ETag: "2d-5913a76187bc0"
Accept-Ranges: bytes
Content-Length: ''' + str(data_length) + '''
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: ''' + str(content_type) + '''; charset=UTF-8
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: *
Access-Control-Allow-http: *
Access-Control-Allow-Mathod: *
Access-Control-Allow-Credentials: true
'''
                        
                        
                        if DL_mode or pic_send_mode:
                            response = resP.encode("utf-8") + '\n'.encode("utf-8") + html_data
                        else:
                            resP = resP + '\n' + html_data
                            response = resP.encode('utf_8')
                        
                        
                        # クライアントへレスポンスを送信する
                        client_socket.sendall(response)
                        print('～～～送信完了～～～')

                        # 通信を終了させる
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                except Exception as e:

                    print('!--CAUTION_L2--!___ERROR___!--CAUTION--!')
                    
                    try:
                        print('Type:'+str(type(e)))
                    except:
                        pass
                    try:
                        print('Args:'+str(e.args))
                    except:
                        pass
                    try:
                        print('Message:'+str(e.message))
                    except:
                        pass
                    try:
                        print('Error_Object:'+str(e))
                    except:
                        pass
                    print('======================================')
                finally:
                    pass
                    try:
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                    except:
                        pass
                    #print("=== サーバーを停止します。 ===")'''
            except Exception as e:
                print('!--CAUTION_L1--!___ERROR___!--CAUTION--!')

                try:
                    print('Type:'+str(type(e)))
                except:
                    pass
                try:
                    print('Args:'+str(e.args))
                except:
                    pass
                try:
                    print('Message:'+str(e.message))
                except:
                    pass
                try:
                    print('Error_Object:'+str(e))
                except:
                    pass
                
                try:
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                except:
                    pass
