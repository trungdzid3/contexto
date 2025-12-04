from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API Gốc
TARGET_API_URL = "https://minhqnd.com/api/dictionary/contexto"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://minhqnd.com/",
    "Origin": "https://minhqnd.com"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/proxy_guess', methods=['POST'])
def proxy_guess():
    try:
        data = request.json
        user_word = data.get('word')
        # Nhận gameId từ Client gửi lên (để cả phòng chơi cùng 1 từ)
        # Nếu không có thì mặc định là 1
        game_id = data.get('gameId', 1) 

        if not user_word:
            return jsonify({"error": "Chưa nhập từ!"}), 400

        # Gửi sang server gốc với đúng ID màn chơi
        params = {
            "id": game_id,
            "guess": user_word
        }

        response = requests.get(TARGET_API_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Lỗi server gốc", "detail": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
