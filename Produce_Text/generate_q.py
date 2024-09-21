<<<<<<< HEAD
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json  # jsonモジュールをインポート
import random
import re

def make_quiz(level='一般人',category='None'):
    categories = ['一般常識', '化学', '日本史', '世界史', '数学', '物理学', '生物学', '天文学', '地理学', '経済学', '政治学', '哲学', '心理学', '社会学', '文学', '詩', '演劇', '映画', '音楽', '美術', '建築', '写真', 'デザイン', 'テレビ番組', 'コンピューターサイエンス', 'テクノロジー', '機械学習', 'データサイエンス', 'ゲームデザイン', 'スポーツ', 'サッカー', '野球', 'バスケットボール', 'テニス', 'オリンピック', 'ファッション', '料理', '飲み物', 'ワイン', 'チーズ', 'フルーツ', '野菜', '魚介類', '肉料理', 'デザート', 'お茶', 'コーヒー', 'パスタ', 'ピザ', 'パン', '和食', '中華料理', 'イタリア料理', 'フランス料理', 'インド料理', 'メキシコ料理', '韓国料理', '天気', '環境問題', 'エネルギー', '宇宙探査', 'ロボット工学', '人工知能', '遺伝学', '神経科学', '医学', '健康とフィットネス', '栄養学', '言語学', '翻訳', '文法', '語彙', '民俗学', '宗教', '神話', '伝説', '漫画', 'アニメ', '映画', 'テレビシリーズ', 'ファンタジー', 'サイエンスフィクション', '推理小説', '恋愛小説', 'ドラマ', 'コメディ', 'ホラー', 'スリラー', '戦争', '動物', '鳥類', '爬虫類', '昆虫', '恐竜', '海洋生物', '植物', '天気', '地震', '火山']
    if(category=='None'):
        category = random.choice(categories)
    while True:
        prompt = f"""
        4択問題を一つだけ考えてください。知識問題でジャンルは{category}、難易度は{level}が解くレベルです。過去に出した問題と似た問題は出してはいけない。コードを書いてはいけない。答えは一つになるように。
        以下の形式で答えてください:
        {{
            "question": "string",
            "choices": ["string1", "string2", "string3", "string4"],
            "answer": "string"
        }}
        """
        
        response = model.generate_content(prompt)

        #JSONとしてパースする
        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e.msg}")
            print(f"Error at line: {e.lineno}, column: {e.colno}, char: {e.pos}")
            print(f"Response Text:", repr(response.text))
            continue  # 再試行する
        
        question = response_data['question']
        answer = answer=response_data['answer']
        if (accuracy_check(question,answer)==True):
            break
        print('問題と答えの整合性が取れていない')
        print(question,answer)
    return response_data

def accuracy_check(question,answer):
    #妥当性の数値化
    prompt = f"""{question}の答えとして{answer}は妥当の妥当性を1から100の整数で評価して。100が最も妥当性が高いとする。クイズとして成り立っていない場合、問題に回答が含まれている場合、選択肢が重複する場合スコアは低くなる。答えは100以下の数字一つのみ。"""
    accuracy = model.generate_content(prompt)

    #textから数値だけ抜き出す
    check_num = extract_number_from_string(accuracy.text)

    if (check_num>=80):
        return True
    elif(check_num>=0 ):
        return False
    else:
        print('プロンプトエラー')
        return False
    
def extract_number_from_string(input_string):
    # 正規表現で数字のみを抽出
    numbers = re.findall(r'\d+', input_string)
    
    if numbers:
        # リスト内の数字を結合し、一つの整数に変換
        combined_number = int(''.join(numbers))
        return combined_number
    else:
        return None  # 数字が見つからなかった場合

class Q_and_A:
    def __init__(self, question, choices, answer,level='一般人'):
       
        # クラスのコンストラクタ
        # :param question: クイズの問題文 (str)
        # :param choices: 選択肢のリスト (list(str))
        # :param answer: 正しい選択肢 (str)
        # :param level:難易度
        
        self.question = question
        self.choices = choices
        self.answer = answer
        self.level = level
    
load_dotenv()
# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("Google APIキーが設定されていません。環境変数を確認してください。")

genai.configure(api_key=GOOGLE_API_KEY)
#モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash",generation_config={"response_mime_type": "application/json"})

response = make_quiz()


# Q_and_Aインスタンスの作成
q_and_a = Q_and_A(
    question=response['question'],
    choices=response['choices'],
    answer=response['answer']
)

# 結果の出力
print("Question:", q_and_a.question)
print("Choices:", q_and_a.choices)
print("Answer:", q_and_a.answer)
<<<<<<< HEAD
=======
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json  # jsonモジュールをインポート
import random
import re

def make_quiz(level='一般人',category='None'):
    categories = ['一般常識', '化学', '日本史', '世界史', '数学', '物理学', '生物学', '天文学', '地理学', '経済学', '政治学', '哲学', '心理学', '社会学', '文学', '詩', '演劇', '映画', '音楽', '美術', '建築', '写真', 'デザイン', 'テレビ番組', 'コンピューターサイエンス', 'テクノロジー', '機械学習', 'データサイエンス', 'ゲームデザイン', 'eスポーツ', 'スポーツ', 'サッカー', '野球', 'バスケットボール', 'テニス', 'オリンピック', 'ファッション', '料理', '飲み物', 'ワイン', 'チーズ', 'フルーツ', '野菜', '魚介類', '肉料理', 'デザート', 'お茶', 'コーヒー', 'パスタ', 'ピザ', 'パン', '和食', '中華料理', 'イタリア料理', 'フランス料理', 'インド料理', 'メキシコ料理', '韓国料理', '天気', '環境問題', 'エネルギー', '宇宙探査', 'ロボット工学', '人工知能', '遺伝学', '神経科学', '医学', '健康とフィットネス', '栄養学', '言語学', '翻訳', '文法', '語彙', '民俗学', '宗教', '神話', '伝説', '漫画', 'アニメ', '映画', 'テレビシリーズ', 'ファンタジー', 'サイエンスフィクション', '推理小説', '恋愛小説', 'ドラマ', 'コメディ', 'ホラー', 'スリラー', '戦争', '動物', '鳥類', '爬虫類', '昆虫', '恐竜', '海洋生物', '植物', '天気', '地震', '火山']
    if(category=='None'):
        category = random.choice(categories)
        print(category)
    while True:
        prompt = f"""
        4択問題を一つだけ考えてください。知識問題でジャンルは{category}、難易度は{level}が解くレベルです。過去に出した問題と似た問題は出してはいけない。コードを書いてはいけない。答えは一つになるように。
        以下の形式で答えてください:
        {{
            "question": "string",
            "choices": ["string1", "string2", "string3", "string4"],
            "answer": "string"
        }}
        """
        
        response = model.generate_content(prompt)

        #JSONとしてパースする
        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e.msg}")
            print(f"Error at line: {e.lineno}, column: {e.colno}, char: {e.pos}")
            print(f"Response Text:", repr(response.text))
            continue  # 再試行する
        
        
        question = response_data['question']
        answer = answer=response_data['answer']
        if (accuracy_check(question,answer)==True):
            break
        print('問題と答えの整合性が取れていない')
        print(question,answer)
    return response_data

def accuracy_check(question,answer):
    #妥当性の数値化
    prompt = f"""{question}の答えとして{answer}は妥当の妥当性を1から100の整数で評価して。100が最も妥当性が高いとする.答えは数字のみ"""
    accuracy = model.generate_content(prompt)

    check_num = extract_number_from_string(accuracy.text)
    print(check_num)

    if (check_num>=80):
        return True
    elif(check_num>=0 ):
        return False
    else:
        print('プロンプトエラー')
        return False
def extract_number_from_string(input_string):
    # 正規表現で数字のみを抽出
    numbers = re.findall(r'\d+', input_string)
    
    if numbers:
        # リスト内の数字を結合し、一つの整数に変換
        combined_number = int(''.join(numbers))
        return combined_number
    else:
        return None  # 数字が見つからなかった場合

class Q_and_A:
    def __init__(self, question, choices, answer,level='一般人'):
       
        # クラスのコンストラクタ
        # :param question: クイズの問題文 (str)
        # :param choices: 選択肢のリスト (list(str))
        # :param answer: 正しい選択肢 (str)
        # :param level:難易度
        
        self.question = question
        self.choices = choices
        self.answer = answer
        self.level = level
    
load_dotenv()
# API-KEYの設定
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("Google APIキーが設定されていません。環境変数を確認してください。")

genai.configure(api_key=GOOGLE_API_KEY)
#モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash",generation_config={"response_mime_type": "application/json"})

response = make_quiz()


# Q_and_Aインスタンスの作成
q_and_a = Q_and_A(
    question=response['question'],
    choices=response['choices'],
    answer=response['answer']
)

# 結果の出力
print("Question:", q_and_a.question)
print("Choices:", q_and_a.choices)
print("Answer:", q_and_a.answer)
>>>>>>> 0ef789c5e9224a2418dc86e1aaac2d877d4c7c1c
=======
>>>>>>> bdccf45a98b8d25baee081a9290f8b0f3c6b7e82
