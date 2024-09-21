import google.generativeai as genai
from dotenv import load_dotenv
import os
import json  # jsonモジュールをインポート


def make_quiz(level='一般人'):
    while True:
        prompt = f"""
        4択問題を一つだけ考えてください。難易度は{level}が解くレベルです。答えは一つになるように。
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

# prompt = f'{question}の答えとして{ans}は妥当ですか。'
# response = gemini_pro.generate_content(prompt)
#print(response.text)



