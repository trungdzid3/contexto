from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- CẤU HÌNH ---
# Link API thật bạn vừa tìm được
TARGET_API_URL = "https://minhqnd.com/api/dictionary/contexto"

# ID của màn chơi. Bạn có thể đổi số này để chơi các màn khác nhau.
# Ví dụ: Hôm nay là màn 1, mai bạn thích đổi sang màn 2 thì sửa số này.
GAME_ID = 1 

# Headers giả lập trình duyệt (để không bị chặn)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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

        if not user_word:
            return jsonify({"error": "Chưa nhập từ nha!"}), 400

        # Tham số gửi đi (theo đúng link bạn tìm được: ?id=1&guess=...)
        params = {
            "id": GAME_ID,
            "guess": user_word
        }

        # Gửi GET request
        response = requests.get(TARGET_API_URL, params=params, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "error": "Lỗi kết nối server gốc",
                "detail": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dòng này để chạy dưới máy (Vercel sẽ tự bỏ qua)
if __name__ == '__main__':
    app.run(debug=True)