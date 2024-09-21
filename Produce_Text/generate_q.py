import google.generativeai as genai
from dotenv import load_dotenv
import os

def make_quiz(level='一般人'):
    prompt =f"4択問題を一つだけ考えてください。難易度は{level}が解くレベルです。答えは一つになるように。問題"
    response = gemini_pro.generate_content(prompt)
    return response

class Q_and_A:
    def __init__(self, question, choices, answer,level='一般人'):
       
        # クラスのコンストラクタ
        # :param question: クイズの問題文 (str)
        # :param choices: 選択肢のリスト (list)
        # :param answer: 正しい選択肢 (str)
        # :param level:難易度
        
        self.question = question
        self.choices = choices
        self.answer = answer
        self.level = level
load_dotenv()
# API-KEYの設定

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

gemini_pro = genai.GenerativeModel("gemini-pro")


response = make_quiz()
# # print(response.text)
# q_and_a = response.text
# question, ans = q_and_a.split()
# print(question)
# print(ans)
# prompt = f'{question}の答えとして{ans}は妥当ですか。'
# response = gemini_pro.generate_content(prompt)
print(response.text)

