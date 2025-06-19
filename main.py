# -*- coding: utf-8 -*-
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Gemini APIの設定
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

load_dotenv()

def initialize_model():
    try:
        # 利用可能なモデルを確認
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
                # print(f"利用可能なモデル: {m.name}")
        
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

if __name__ == "__main__":
    try:
        model = initialize_model()
        while True:
            user_input = input("\n使いたい材料をカンマ区切りで入力してください（終了するには 'q' を入力）: ")
            if user_input.lower() == 'q':
                print("プログラムを終了します。")
                break
                
            result = suggest_recipe(user_input)
            print("\n=== レシピの提案 ===\n")
            print(result.strip())
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
