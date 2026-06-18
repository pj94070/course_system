import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 📊 唯修科技 - 完整網頁 HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>唯修科技 - 3D列印專業訓練課程報名</title>
    <style>
        :root { --primary-color: #1a4985; --secondary-color: #007bff; --accent-color: #f59f00; --dark-color: #2b3a4a; }
        body { font-family: 'Helvetica Neue', sans-serif; background-color: #eef2f5; color: #333; margin: 0; padding: 0; line-height: 1.6; }
        .header { background: linear-gradient(135deg, var(--dark-color), var(--primary-color)); color: white; text-align: center; padding: 40px 20px; }
        .main-container { max-width: 700px; margin: -30px auto 30px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: var(--primary-color); border-bottom: 2px solid #edf2f7; padding-bottom: 10px; margin-top: 0; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 8px; color: #444; }
        input, select { width: 100%; padding: 12px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; font-size: 16px; background: #fafafa; }
        button { width: 100%; background: var(--secondary-color); color: white; border: none; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0056b3; }
        .footer { text-align: center; color: #6c757d; font-size: 13px; padding-bottom: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>唯修科技 WEIXIU TECHNOLOGY</h1>
        <p>3D列印專業訓練課程線上登記</p>
    </div>
    <div class="main-container">
        <h2>✍️ 學員線上登記</h2>
        <form action="/submit_registration" method="POST">
            <div class="form-group">
                <label>學員姓名</label>
                <input type="text" name="name" required>
            </div>
            <div class="form-group">
                <label>報名人數</label>
                <select name="people_count">
                    <option value="1人報名">1人報名</option>
                    <option value="2人報名">2人報名</option>
                    <option value="優惠小組報名（3人）">優惠小組報名（3人）</option>
                </select>
            </div>
            <div class="form-group">
                <label>課程項目</label>
                <select name="course_id">
                    <option value="1">3D列印基礎認識實務課程</option>
                    <option value="2">3D列印後處理進階課程</option>
                </select>
            </div>
            <div class="form-group">
                <label>聯絡電話</label>
                <input type="tel" name="phone" required>
            </div>
            <div class="form-group">
                <label>電子信箱</label>
                <input type="email" name="email" required>
            </div>
            <button type="submit">確認送出報名資訊 ➔</button>
        </form>
    </div>
    <div class="footer">© 2026 唯修科技有限公司 All Rights Reserved.</div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    # 獲取表單資料
    name = request.form.get('name')
    people = request.form.get('people_count')
    course_id = request.form.get('course_id')
    phone = request.form.get('phone')
    email = request.form.get('email')
    
    course_map = {"1": "3D列印基礎認識實務課程", "2": "3D列印後處理進階課程"}
    selected_course = course_map.get(course_id, "未知課程")
    
    # Discord Webhook 網址
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1517080613822398625/uKiiRNp_3knea-qs92sxGQmCHVLrQI_UdZrlLbmWqBmJ5atzFQYl7DcasQxV5G3xfVo1"
    
    # 建立 Discord Embed 通知內容
    payload = {
        "embeds": [{
            "title": "🔔 唯修科技 - 新學員報名通知",
            "color": 1104926,
            "fields": [
                {"name": "👤 學員姓名", "value": name, "inline": True},
                {"name": "👥 報名人數", "value": people, "inline": True},
                {"name": "📚 課程項目", "value": selected_course, "inline": False},
                {"name": "📞 聯絡電話", "value": phone, "inline": True},
                {"name": "✉️ 電子信箱", "value": email, "inline": False}
            ],
            "footer": {"text": "系統即時轉寄"}
        }]
    }
    
    # 執行轉送
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

    return f"""
    <script>
        alert('【唯修科技】感謝您的報名！資訊已轉發至伺服器。');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
