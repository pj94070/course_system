import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, request, jsonify

app = Flask(__name__)

# 💡 官方簡章終極版：465 連接埠防禦、單欄純垂直排版、圖片路徑修正、師資與電話正名
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
        
        /* 頂部 Banner */
        .header-banner { background: linear-gradient(135deg, var(--dark-color), var(--primary-color)); color: white; text-align: center; padding: 50px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header-banner h1 { margin: 0; font-size: 34px; letter-spacing: 2px; }
        .header-banner p { margin: 12px 0 0 0; opacity: 0.9; font-size: 16px; }
        
        /* 核心包覆區：嚴格全單欄往下排列 */
        .main-container { max-width: 800px; margin: 30px auto; padding: 0 20px; display: flex; flex-direction: column; gap: 30px; }
        
        /* 區塊通用樣式 */
        .section-card { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .form-section { border-top: 6px solid var(--secondary-color); }
        
        h2 { color: var(--primary-color); border-bottom: 2px solid #edf2f7; padding-bottom: 10px; margin-top: 0; font-size: 24px; display: flex; align-items: center; gap: 10px; }
        h3 { color: var(--dark-color); margin-top: 25px; font-size: 19px; border-left: 4px solid var(--secondary-color); padding-left: 8px; }
        
        /* 課表圖片區塊 */
        .course-image-container { text-align: center; margin: 20px 0; background: var(--light-bg); padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }
        .course-image-container img { max-width: 100%; height: auto; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        
        /* 優勢條列 */
        .advantage-grid { margin: 20px 0; }
        .advantage-item { background: var(--light-bg); padding: 15px 20px; margin-bottom: 12px; border-radius: 8px; border-left: 4px solid #28a745; }
        .advantage-title { font-weight: bold; color: var(--dark-color); font-size: 16px; }
        
        /* 課程卡片 */
        .course-card { background: #f1f7fe; border: 1px solid #cedfeffa; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
        .course-title { font-weight: bold; color: var(--primary-color); font-size: 18px; margin-bottom: 8px; }
        
        /* 師資卡片 (正名為工程師) */
        .teacher-box { display: flex; gap: 20px; align-items: center; background: #fff9db; padding: 20px; border-radius: 8px; border: 1px dashed var(--accent-color); margin-top: 20px; }
        .teacher-avatar { width: 70px; height: 70px; background: var(--primary-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 24px; flex-shrink: 0; }
        .teacher-info p { margin: 3px 0; font-size: 15px; color: #495057; }
        
        /* 表單元素 */
        .form-group { margin-bottom: 22px; }
        label { display: block; font-weight: bold; margin-bottom: 9px; color: #444; font-size: 16px; }
        input[type="text"], input[type="tel"], input[type="email"], select { width: 100%; padding: 13px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; font-size: 16px; transition: border-color 0.2s; background-color: #fafafa; }
        input:focus, select:focus { border-color: var(--secondary-color); background-color: #fff; outline: none; }
        .radio-group { display: flex; gap: 25px; margin-top: 5px; }
        .radio-group label { font-weight: normal; display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 16px; }
        
        button { width: 100%; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border: none; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,123,255,0.3); transition: all 0.3s; margin-top: 10px; }
        button:hover { background: linear-gradient(135deg, #0056b3, #004085); transform: translateY(-1px); box-shadow: 0 6px 16px rgba(0,123,255,0.4); }
        
        /* 頁尾聯絡與官網連結 */
        .footer { text-align: center; padding: 40px 20px; color: #6c757d; font-size: 14px; background: white; border-top: 1px solid #dee2e6; margin-top: 5px; }
        .footer a { color: var(--secondary-color); text-decoration: none; font-weight: bold; }
        .footer a:hover { text-decoration: underline; }
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
            <p>您想像過將腦中的藍圖，在 24 小時內轉化為手中真實的觸感嗎？本課程專為對 3D 列印技術有實務需求之專業人士及愛好者設計。結合唯修科技多年的設備開發與維修經驗，導入最新的切層邏輯與材料科學實例作為訓練教材，全面協助學員排除常見列印失敗痛點，推動快速原型開發能力！</p>
            
            <h3>💡 為什麼選擇唯修科技？</h3>
            <div class="advantage-grid">
                <div class="advantage-item">
                    <span class="advantage-title">● 實戰導向：</span>拒絕空談理論！課程將介紹 3D 列印原理及相關介紹，讓你親手操作。
                </div>
                <div class="advantage-item">
                    <span class="advantage-title">● 技術核心：</span>採小班制授課，分享不僅是操作，藉由討論解決結構與材料難題的祕訣。
                </div>
                <div class="advantage-item">
                    <span class="advantage-title">● 從零到一：</span>提供系統化的教學模組，涵蓋建模邏輯、切層軟體應用到後處理工藝。
                </div>
                <div class="advantage-item">
                    <span class="advantage-title">● 跨界交流：</span>這裡不僅是教室，更是創新社群。與不同領域的學員激盪火花，發掘 3D 列印在各行各業的無限可能。
                </div>
            </div>

            <h3>📊 課程時間、時數與地點</h3>
            <ul>
                <li><strong>課程時數：</strong>訓練課程約 30 小時（含繪圖指導及輔導考證）。</li>
                <li><strong>授課方式：</strong>本公司為求教學品質及學員需求，故採小班制實施授課教學，所有上課時間彈性調整，由學員以小組為單位，與本公司訓練部門協調授課時間，未到課學員則有三次補課機會。</li>
                <li><strong>課程地點：</strong>本公司多功能會議室及 3D 列印室。</li>
            </ul>

            <h3>📅 課程內容安排表</h3>
            <div class="course-image-container">
                <img src="/static/IMG_8743.JPG" alt="唯修科技3D列印課程大綱排班表">
                <p style="font-size: 12px; color: #868e96; margin-top: 8px;">（上圖為 3D 列印與 SOLIDWORKS 認證加值課表進度安排）</p>
            </div>

            <h3>💰 費用與報名說明</h3>
            <ul>
                <li><strong>課程費用：</strong>每人新台幣 18,000 元（本訓練含考照費用）。請於收到錄取通知後一週內完成繳費並回傳證明。</li>
                <li><strong>🔥 優惠方案：</strong>三人同行，優惠合計新台幣 50,000 元。</li>
                <li><strong>電子發票：</strong>為落實環境保護，本公司將於課程結束後一週內以 Email 寄送電子發票。</li>
            </ul>
        </div>

        <div class="section-card">
            <h2>📚 招生開班項目</h2>
            <div class="course-card">
                <div class="course-title">📌 項目 1：3D列印基礎認識實務課程【🔥確定開班】</div>
                <p style="margin: 0; font-size: 15px; color: #555;">適合零基礎者。教授 FDM 原理、切片軟體精準操作、機台校準校正維護，以及常用線材（PLA/PETG）參數調校優化。</p>
            </div>
            <div class="course-card">
                <div class="course-title">📌 項目 2：3D列印後處理進階課程【⏱️預約待開班】</div>
                <p style="margin: 0; font-size: 15px; color: #555;">探討高級支撐材拆除技巧、表面化學拋光、噴砂處理、基礎翻模拓樣、多層次上色與精細塗裝工藝。</p>
            </div>
        </div>

        <div class="section-card">
            <h2>👨‍🏫 唯修頂尖講師陣容</h2>
            <div class="teacher-box">
                <div class="teacher-avatar">S</div>
                <div class="teacher-info">
                    <p style="font-weight: bold; color: #d9480f; font-size: 17px;">Sebastian 工程師 / 課程總召集人</p>
                    <p style="margin-top: 6px;">• 唯修科技 3D 列印技術研發部負責人</p>
                    <p>• 超過 10 年工業級 3D 列印、逆向工程與快速原型打樣實戰生產經驗</p>
                    <p>• 專長：FDM/SLA 參數優化、產品結構結構改良與高精度打樣</p>
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
            📞 聯絡電話：0976-575-583（歡迎來電洽詢課程部門） | 📨 官方客服信箱：<a href="mailto:service@weixiu.com.tw">service@weixiu.com.tw</a><br>
            📍 公司地址：300075 新竹市香山區中華路四段518號9樓<br>
            🚊 交通建議：建議搭乘火車至三姓橋站，步行約 10 分鐘即可抵達本公司多功能會議室及 3D 列印室。<br>
            🅿️ 停車需求：本公司設有機車停車格，若有汽車車位需求，須聯繫本公司再行回覆。<br>
            🌱 環保叮嚀：現場提供飲水設備，請學員自備環保杯，讓我們為地球盡一份心力。
        </div>
        <p style="margin-top: 20px; font-size: 12px; color: #adb5bd;">© 2026 唯修科技. All Rights Reserved. 3D自動化招生管理系統平台</p>
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
    
    course_map = {"1": "3D列印基礎認識實務課程 (開班)", "2": "3D列印後處理進階課程 (待開班)"}
    selected_course = course_map.get(course_id, "未知課程")
    
    print(f"【成功接收報名】學員：{name} ({gender}) | 電話：{phone} | 信箱：{email} | 項目：{selected_course}")
    
    try:
        # 💡 安全性核心變更：由 587 連接埠改為更穩定的 SSL 465 加密連接埠，穿透 Render 免費版的防火牆限制！
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        
        # ⚠️ 請記得在這裡更換成您發信用的 Gmail 帳號與 16 位元應用程式密碼
        sender_email = "填入您發信用的Gmail@gmail.com"        
        sender_password = "填入16位元應用程式密碼"  
        
        receiver_email = "service@weixiu.com.tw" 
        
        mail_content = f"""
        您好，唯修科技管理員：
        
        網站收到了一筆新的學員課程報名資訊！
        
        【報名詳情】
        ====================================
        學員姓名：{name}
        性別：{gender}
        聯絡電話：{phone}
        電子信箱：{email}
        報名課程：{selected_course}
        ====================================
        
        請儘速與學員取得聯繫。
        本信件由 3D列印課程報名系統 自動發出。
        """
        
        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['From'] = Header(f"唯修科技報名系統 <{sender_email}>", 'utf-8')
        message['To'] = Header("唯修科技客服 <service@weixiu.com.tw>", 'utf-8')
        message['Subject'] = Header(f"🔔 新增報名通知：{name} 同學已報名 {selected_course}", 'utf-8')
        
        print("【系統通知】正在透過 465 加密連接埠連線至郵件伺服器...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print("【系統通知】公司客服郵件通知已成功寄出！")
        
    except Exception as e:
        print(f"❌ 【系統錯誤】郵件寄送失敗，錯誤原因: {str(e)}")

    return f"""
    <script>
        alert('【唯修科技】報名成功！感謝您的參與，我們將儘速與您聯絡。');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
