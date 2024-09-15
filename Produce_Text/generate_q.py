import google.generativeai as genai
 
# API-KEYの設定
GOOGLE_API_KEY='AIzaSyC_8AXqUmn8f7L3vwSq4GtOqLVe-oUcZhg'
genai.configure(api_key=GOOGLE_API_KEY)

gemini_pro = genai.GenerativeModel("gemini-pro")

prompt ="15文字以上で知識を問うクイズを一つだけ考えてください。単語で回答できるようにしてください。問題文をひらがなにして問題と答えのみを出力"


response = gemini_pro.generate_content(prompt)
# print(response.text)
q_and_a = response.text
question, ans = q_and_a.split()
print(question)
print(ans)
prompt = f'{question}の答えとして{ans}は妥当ですか。'
response = gemini_pro.generate_content(prompt)
print(response.text)
