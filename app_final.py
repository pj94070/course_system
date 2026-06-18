import os
import json
import urllib.request
import urllib.parse
import base64
from flask import Flask, request

app = Flask(__name__)

# 📊 依據官方 PDF 訓練簡章完整配置的網頁模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        
        .header-banner { background: linear-gradient(135deg, var(--dark-color), var(--primary-color)); color: white; text-align: center; padding: 50px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header-banner h1 { margin: 0; font-size: 34px; letter-spacing: 2px; }
        .header-banner p { margin: 12px 0 0 0; opacity: 0.9; font-size: 16px; }
        
        .main-container { max-width: 800px; margin: 30px auto; padding: 0 20px; display: flex; flex-direction: column; gap: 30px; }
        .section-card { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .form-section { border-top: 6px solid var(--secondary-color); }
        
        h2 { color: var(--primary-color); border-bottom: 2px solid #edf2f7; padding-bottom: 10px; margin-top: 0; font-size: 24px; display: flex; align-items: center; gap: 10px; }
        h3 { color: var(--dark-color); margin-top: 25px; font-size: 19px; border-left: 4px solid var(--secondary-color); padding-left: 8px; }
        
        .course-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 16px; text-align: left; }
        .course-table th, .course-table td { padding: 12px 15px; border: 1px solid #dee2e6; }
        .course-table th { background-color: #f1f7fe; color: var(--primary-color); font-weight: bold; }
        .course-table tr:nth-of-type(even) { background-color: #f8f9fa; }
        .value-add-row { background-color: #fff9db !important; font-weight: bold; color: #d9480f; }
        
        .advantage-grid { margin: 20px 0; }
        .advantage-item { background: var(--light-bg); padding: 15px 20px; margin-bottom: 12px; border-radius: 8px; border-left: 4px solid #28a745; }
        .advantage-title { font-weight: bold; color: var(--dark-color); font-size: 16px; }
        
        .course-card { background: #f1f7fe; border: 1px solid #cedfeffa; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        .course-title { font-weight: bold; color: var(--primary-color); font-size: 18px; margin-bottom: 8px; }
        
        .teacher-box { display: flex; gap: 20px; align-items: center; background: #fdfaf2; padding: 25px; border-radius: 8px; border: 1px dashed var(--accent-color); margin-top: 20px; }
        .teacher-avatar-img { width: 90px; height: 90px; border-radius: 50%; object-fit: cover; border: 3px solid var(--accent-color); flex-shrink: 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        
        .form-group { margin-bottom: 22px; }
        label { display: block; font-weight: bold; margin-bottom: 9px; color: #444; font-size: 16px; }
        input[type="text"], input[type="tel"], input[type="email"], select { width: 100%; padding: 13px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; font-size: 16px; background-color: #fafafa; }
        .radio-group { display: flex; gap: 25px; margin-top: 5px; }
        .radio-group label { font-weight: normal; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 16px; }
        
        button { width: 100%; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border: none; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,123,255,0.3); transition: all 0.3s; margin-top: 10px; }
        button:hover { background: linear-gradient(135deg, #0056b3, #004085); transform: translateY(-1px); }
        
        .footer { text-align: center; padding: 40px 20px; color: #6c757d; font-size: 14px; background: white; border-top: 1px solid #dee2e6; margin-top: 5px; }
        .footer a { color: var(--secondary-color); text-decoration: none; font-weight: bold; }
        .company-meta { margin-top: 15px; font-size: 13px; color: #868e96; line-height: 1.8; }
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
            <p style="font-weight: bold; color: #555;">課程代碼：WX-3D115001</p>
            <p>您想像過將腦中的藍圖，在 24 小時內轉化為手中真實的觸感幕？在唯修科技，我們將帶領您突破傳統製造的侷限，掌握未來工業的核心競爭力。</p>
            
            <h3>💡 為什麼選擇唯修科技？</h3>
            <div class="advantage-grid">
                <div class="advantage-item"><span class="advantage-title">● 實戰導向：</span>課程將介紹 3D 列印原理及相關介紹，讓你親手操作。</div>
                <div class="advantage-item"><span class="advantage-title">● 技術核心：</span>採小班制授課，藉由討論解決結構與材料難題的祕訣。</div>
                <div class="advantage-item"><span class="advantage-title">● 從零到一：</span>提供系統化的教學模組，涵蓋建模邏輯、切層軟體應用到後處理工藝。</div>
                <div class="advantage-item"><span class="advantage-title">● 跨界交流：</span>與不同領域的學員激盪火花，發掘 3D 列印在各行各業的無限可能。</div>
            </div>

            <h3>📅 課程內容與加值時數安排表</h3>
            <table class="course-table">
                <thead>
                    <tr>
                        <th>課程時數 (依授課情況而定)</th>
                        <th>課程內容安排</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>約 2 小時</td><td>基礎知識及介紹</td></tr>
                    <tr><td>約 1 小時</td><td>建模介紹及建立</td></tr>
                    <tr><td>約 1 小時</td><td>切片軟體之操作</td></tr>
                    <tr><td>約 1 小時</td><td>機器操作與維護</td></tr>
                    <tr><td>約 14 小時</td><td>建模基礎形狀之操作</td></tr>
                    <tr><td>約 2 小時</td><td>設計思維及創作</td></tr>
                    <tr><td>約 4 小時</td><td>3D 列印之實作及準備</td></tr>
                    <tr class="value-add-row"><td>⭐ 額外加值課程 (約 10 小時)</td><td>SOLIDWORKS 軟體認證輔導考證</td></tr>
                </tbody>
            </table>

            <h3>💰 費用、時數與授課說明</h3>
            <ul>
                <li><strong>課程時數：</strong>訓練課程約 30 小時（含繪圖指導及輔導考證）。</li>
                <li><strong>授課方式：</strong>採小班制授課，所有上課時間彈性調整，由學員以小組為單位與本公司訓練部門協調。未到課學員有 3 次補課機會。</li>
                <li><strong>課程費用：</strong>每人新台幣 18,000 元（本訓練含考照費用）。</li>
                <li><strong>優惠方案：</strong>三人同行，優惠合計新台幣 50,000 元。</li>
                <li><strong>電子發票：</strong>本公司將於課程結束後一週內以 Email 寄送電子發票。</li>
            </ul>
        </div>

        <div class="section-card">
            <h2>📚 招生開班項目</h2>
            <div class="course-card">
                <div class="course-title">📌 項目 1：3D列印基礎認識實務課程【🔥確定開班】</div>
                <p style="margin: 0; font-size: 15px; color: #555;">適合零基礎者。教授 FDM 原理、切片軟體精準操作、機台校準維護與參數調校。</p>
            </div>
            <div class="course-card">
                <div class="course-title">📌 項目 2：3D列印後處理進階課程【⏱️預約待開班】</div>
                <p style="margin: 0; font-size: 15px; color: #555;">探討高級支撐材拆除技巧、表面化學拋光、翻模拓樣與精細上色塗裝工藝。</p>
            </div>
        </div>

        <div class="section-card">
            <h2>👨‍🏫 唯修頂尖講師陣容</h2>
            <div class="teacher-box">
                <div style="width: 90px; height: 90px; border-radius: 50%; background-color: #1a4985; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 24px; border: 3px solid var(--accent-color); box-shadow: 0 4px 8px rgba(0,0,0,0.1); flex-shrink: 0;">金</div>
                <div class="teacher-info">
                    <p style="font-weight: bold; color: #d9480f; font-size: 17px;">金 總工程師 / 課程總召集人</p>
                    <p style="margin-top: 6px;">• 唯修科技 3D 列印技術研發部負責人</p>
                    <p>• 超過 10 年工業級 3D 列印、逆向工程與快速原型打樣實戰經驗</p>
                    <p>• 專長：FDM/SLA 參數優化、產品結構修改與高精度打樣</p>
                </div>
            </div>
        </div>

        <div class="section-card form-section">
            <h2>✍️ 快速學員線上登記</h2>
            <form action="/submit_registration" method="POST">
                <div class="form-group">
                    <label for="name">學員姓名</label>
                    <input type="text" id="name" name="name" placeholder="請輸入您的真實姓名" required>
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
                    <input type="tel" id="phone" name="phone" placeholder="範例：0912345678" required>
                </div>
                <div class="form-group">
                    <label for="email">電子信箱</label>
                    <input type="email" id="email" name="email" placeholder="範例：yourname@example.com" required>
                </div>
                <div class="form-group">
                    <label for="course_id">欲報名的課程項目</label>
                    <select id="course_id" name="course_id" required>
                        <option value="1">3D列印基礎認識實務課程 (確定開班)</option>
                        <option value="2">3D列印後處理進階課程 (待開班)</option>
                    </select>
                </div>
                <button type="submit">確認送出報名資訊 ➔</button>
            </form>
        </div>

    </div>

    <div class="footer">
        <p>🌐 歡迎訪問我們的官方網站：<a href="https://www.weixiu.com.tw" target="_blank">唯修科技有限公司 官方網站</a></p>
        <div class="company-meta">
            <strong>唯修科技有限公司 WEIXIU MAINTAIN TECHNOLOGY CORPORATION</strong><br>
            📞 聯絡電話：03-531-6873 | 📨 官方客服信箱：service@weixiu.com.tw<br>
            📍 上課地點：300075 新竹市香山區中華路四段518號9樓<br>
            🚊 交通建議：建議搭乘火車至三姓橋站，步行約 10 分鐘即可抵達。<br>
            💡 課後福利：課後可加入專屬技術交流群組，提供為期六個月的線上技術顧問諮詢。
        </div>
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
    
    course_map = {"1": "3D列印基礎認識實務課程", "2": "3D列印後處理進階課程"}
    selected_course = course_map.get(course_id, "未知課程")
    
    print(f"【新報名】學員：{name} | 電話：{phone} | 信箱：{email} | 課程：{selected_course}")
    
    # 🚀 使用 100% Python 內建的 urllib 庫發送 HTTPS 請求，完美避開 Render 對 SMTP 連接埠的封鎖
    try:
        api_url = "https://api.mailgun.net/v3/sandboxde876d21396b4bf09c058778f3cc3b0c.mailgun.org/messages"
        api_key = "key-86db49de48123da6c87157834571ab3d"
        
        # 準備信件內文
        mail_text = f"""您好，唯修科技管理團隊：
        
官方網頁接收到一筆全新的線上報名表單，詳情如下：

====================================
學員姓名：{name}
學員性別：{gender}
聯絡電話：{phone}
電子信箱：{email}
報名項目：{selected_course}
====================================

請負責同仁儘速與學員取得聯繫，謝謝！"""

        # 整理 Mailgun API 需要的 Form 表單欄位
        payload = {
            "from": "唯修科技自動報名系統 <mailgun@sandboxde876d21396b4bf09c058778f3cc3b0c.mailgun.org>",
            "to": "service@weixiu.com.tw",
            "subject": f"🔔 官網新學員報名通知：{name} 同學已報名 {selected_course}",
            "text": mail_text
        }
        
        # 將 payload 編碼為 application/x-www-form-urlencoded
        data_encoded = urllib.parse.urlencode(payload).encode('utf-8')
        
        # 建立請求物件
        req = urllib.request.Request(api_url, data=data_encoded, method='POST')
        
        # 計算 HTTP Basic Authentication 的認證字串 (Mailgun API 的規定)
        auth_str = f"api:{api_key}"
        auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        req.add_header('Authorization', f'Basic {auth_b64}')
        
        # 正式送出網頁連線
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            if status_code == 200:
                print("==== 🎉 【發信成功】客服郵件已順利穿透雲端限制，成功送達！ ====")
            else:
                print(f"⚠️ API 回傳異常代碼: {status_code}")
                
    except Exception as e:
        print(f"❌ 傳輸失敗原因: {str(e)}")

    return f"""
    <script>
        alert('【唯修科技】您好 {name} 同學，您已成功提交報名資訊！恭喜您邁向不一樣的世界');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
