import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 📊 唯修科技 - 網頁 HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>唯修科技 WEIXIU TECHNOLOGY - 3D列印專業訓練課程報名</title>
    <style>
        :root {
            --primary-color: #1a4985;
            --secondary-color: #007bff;
            --dark-color: #2b3a4a;
        }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #eef2f5; color: #333; margin: 0; padding: 20px; line-height: 1.6; }
        .main-container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 8px; }
        input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; background: #007bff; color: white; border: none; padding: 15px; font-size: 18px; border-radius: 6px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="main-container">
        <h2>✍️ 快速學員線上登記</h2>
        <form action="/submit_registration" method="POST">
            <div class="form-group">
                <label for="name">學員姓名</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label>性別</label>
                <div style="display:flex; gap:20px;">
                    <label><input type="radio" name="gender" value="男" checked> 男</label>
                    <label><input type="radio" name="gender" value="女"> 女</label>
                </div>
            </div>
            <div class="form-group">
                <label for="phone">聯絡電話</label>
                <input type="tel" id="phone" name="phone" required>
            </div>
            <div class="form-group">
                <label for="email">電子信箱</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="course_id">課程項目</label>
                <select id="course_id" name="course_id" required>
                    <option value="1">3D列印基礎認識實務課程</option>
                    <option value="2">3D列印後處理進階課程</option>
                </select>
            </div>
            <div class="form-group">
                <label for="people_count">報名人數</label>
                <select id="people_count" name="people_count" required>
                    <option value="1人報名">1人報名</option>
                    <option value="2人報名">2人報名</option>
                    <option value="優惠方案小組報名（3人）">優惠方案小組報名（3人）</option>
                </select>
            </div>
            <button type="submit">確認送出報名資訊 ➔</button>
        </form>
    </div>
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
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    course_id = request.form.get('course_id')
    people_count = request.form.get('people_count')
    
    course_map = {"1": "3D列印基礎認識實務課程", "2": "3D列印後處理進階課程"}
    selected_course = course_map.get(course_id, "未知課程")
    
    # Discord Webhook
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1517080613822398625/uKiiRNp_3knea-qs92sxGQmCHVLrQI_UdZrlLbmWqBmJ5atzFQYl7DcasQxV5G3xfVo1"
    
    payload = {
        "embeds": [{
            "title": "🔔 唯修科技 - 新學員線上登記通知",
            "color": 1104926,
            "fields": [
                {"name": "👤 學員姓名", "value": str(name), "inline": True},
                {"name": "🚻 性別", "value": str(gender), "inline": True},
                {"name": "👥 報名人數", "value": str(people_count), "inline": True},
                {"name": "📞 聯絡電話", "value": str(phone), "inline": False},
                {"name": "✉️ 電子信箱", "value": str(email), "inline": False},
                {"name": "📚 報名項目", "value": str(selected_course), "inline": False}
            ]
        }]
    }
    
    # 發送請求 (移除掉定義不全的 headers 變數)
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            print(f"✅ 成功傳送至 Discord: {name}")
        else:
            print(f"⚠️ Discord 回傳異常狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord 傳輸發生錯誤: {str(e)}")

    return f"""
    <script>
        alert('【唯修科技】報名已送出，我們將盡快與您聯繫！');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
