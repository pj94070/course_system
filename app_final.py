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
    <title>唯修科技 WEIXIU TECHNOLOGY - 3D列印專業訓練課程報名</title>
    <style>
        :root {
            --primary-color: #1a4985;
            --secondary-color: #007bff;
            --accent-color: #f59f00;
            --dark-color: #2b3a4a;
            --light-bg: #f8f9fa;
        }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #eef2f5; color: #333; margin: 0; padding: 0; line-height: 1.7; }
        .header-banner { background: linear-gradient(135deg, var(--dark-color), var(--primary-color)); color: white; text-align: center; padding: 50px 20px; }
        .main-container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .section-card { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
        h2 { color: var(--primary-color); border-bottom: 2px solid #edf2f7; padding-bottom: 10px; }
        .form-group { margin-bottom: 22px; }
        label { display: block; font-weight: bold; margin-bottom: 9px; }
        input[type="text"], input[type="tel"], input[type="email"], select { width: 100%; padding: 13px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; }
        .radio-group { display: flex; gap: 25px; margin-top: 5px; }
        button { width: 100%; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border: none; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; }
        .footer { text-align: center; padding: 40px 20px; color: #6c757d; font-size: 14px; background: white; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>唯修科技 WEIXIU TECHNOLOGY</h1>
        <p>別讓創意只停留在 2D！帶你從「想」到「摸得到」🚀</p>
    </div>
    <div class="main-container">
        <div class="section-card">
            <h2>🎯 3D 列印基礎訓練課程介紹</h2>
            <p>唯修科技帶領您突破傳統製造侷限，掌握未來工業的核心競爭力。</p>
            <h3>💰 費用說明</h3>
            <ul>
                <li><strong>每人費用：</strong>新台幣 18,000 元</li>
                <li><strong>優惠方案：</strong>三人同行，優惠合計新台幣 50,000 元</li>
            </ul>
        </div>
        <div class="section-card">
            <h2>✍️ 快速學員線上登記</h2>
            <form action="/submit_registration" method="POST">
                <div class="form-group">
                    <label for="name">學員姓名</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label>性別</label>
                    <div class="radio-group">
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
    </div>
    <div class="footer">
        <p>唯修科技有限公司 | 新竹市香山區中華路四段518號9樓</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    name = request.form.get('name')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    course_id = request.form.get('course_id')
    people_count = request.form.get('people_count')
    
    course_map = {"1": "3D列印基礎認識實務課程", "2": "3D列印後處理進階課程"}
    selected_course = course_map.get(course_id, "未知課程")
    
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
    
    try:
        # 直接發送，不需要手動定義 headers
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code not in [200, 204]:
            print(f"⚠️ Discord 回傳異常狀態碼: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord 傳輸發生錯誤: {str(e)}")

    return f"""
    <script>
        alert('【唯修科技】您好 {name} 同學，您的報名資訊已成功提交！');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
