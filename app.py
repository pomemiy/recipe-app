# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Gemini APIの設定
GOOGLE_API_KEY = "AIzaSyAOQDf4TAN2gCpQYKW2A6qBs68Zupz92zc"
genai.configure(api_key=GOOGLE_API_KEY)

def initialize_model():
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except Exception as e:
        raise Exception(f"モデルの初期化に失敗しました: {str(e)}")

def suggest_recipe(ingredients):
    if not ingredients.strip():
        return "材料が入力されていません。"
    
    prompt = f"""材料: {ingredients}
以下の形式でレシピを提案してください：
1. 料理名
2. 必要な材料（分量）
3. 調理手順
4. 調理時間
5. コツやポイント

日本語で回答してください。"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# モデルの初期化
model = initialize_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    ingredients = data.get('ingredients', '')
    result = suggest_recipe(ingredients)
    return jsonify({'recipe': result})

if __name__ == '__main__':
    app.run(debug=True) 