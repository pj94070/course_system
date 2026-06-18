import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, request, jsonify

app = Flask(__name__)

# 💡 將原本不見的師資、課程詳情、品牌圖文資訊，全部以精美現代的 RWD 網頁樣式完美內嵌！
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>唯修科技 WEIXIU TECHNOLOGY - 3D列印專業課程報名</title>
    <style>
        :root {
            --primary-color: #0056b3;
            --secondary-color: #17a2b8;
            --dark-color: #2c3e50;
            --light-bg: #f8f9fa;
        }
        body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f1f3f5; color: #333; margin: 0; padding: 0; line-height: 1.6; }
        .header-banner { background: linear-gradient(135deg, var(--dark-color), var(--primary-color)); color: white; text-align: center; padding: 40px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header-banner h1 { margin: 0; font-size: 32px; letter-spacing: 2px; }
        .header-banner p { margin: 10px 0 0 0; opacity: 0.9; font-size: 16px; }
        
        .main-wrapper { max-width: 1000px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1.3fr 1fr; gap: 30px; }
        @media (max-width: 768px) { .main-wrapper { grid-template-columns: 1fr; } }
        
        .info-section { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .form-section { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 5px solid var(--primary-color); height: fit-content; }
        
        h2 { color: var(--primary-color); border-bottom: 2px solid #edf2f7; padding-bottom: 8px; margin-top: 0; font-size: 22px; display: flex; align-items: center; gap: 8px; }
        h3 { color: var(--dark-color); margin-top: 20px; font-size: 18px; }
        
        /* 課程與師資樣式 */
        .course-card { background: var(--light-bg); border-left: 4px solid var(--secondary-color); padding: 15px; margin-bottom: 15px; border-radius: 0 8px 8px 0; }
        .course-title { font-weight: bold; color: var(--dark-color); font-size: 16px; }
        .course-desc { font-size: 14px; color: #666; margin: 5px 0 0 0; }
        
        .teacher-box { display: flex; gap: 15px; align-items: center; background: #fff9db; padding: 15px; border-radius: 8px; border: 1px dashed #f59f00; margin-top: 15px; }
        .teacher-avatar { width: 60px; height: 60px; background: #e9ecef; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #495057; font-size: 20px; border: 2px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .teacher-info p { margin: 0; font-size: 14px; color: #495057; }
        
        /* 表單樣式 */
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 8px; color: #444; font-size: 15px; }
        input[type="text"], input[type="tel"], input[type="email"], select { width: 100%; padding: 12px; border: 1px solid #ced4da; border-radius: 6px; box-sizing: border-box; font-size: 15px; transition: border-color 0.2s; }
        input:focus, select:focus { border-color: var(--primary-color); outline: none; }
        .radio-group { display: flex; gap: 20px; margin-top: 5px; }
        .radio-group label { font-weight: normal; display: flex; align-items: center; gap: 5px; cursor: pointer; }
        
        button { width: 100%; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border: none; padding: 14px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,123,255,0.3); transition: all 0.3s; margin-top: 10px; }
        button:hover { background: linear-gradient(135deg, #0056b3, #004085); transform: translateY(-1px); box-shadow: 0 6px 14px rgba(0,123,255,0.4); }
        
        .footer { text-align: center; padding: 30px 20px; color: #868e96; font-size: 13px; background: #fff; margin-top: 5px; border-top: 1px solid #dee2e6; }
    </style>
</head>
<body>

    <div class="header-banner">
        <h1>唯修科技 WEIXIU TECHNOLOGY</h1>
        <p>💡 卓越品牌 ✕ 頂尖智慧 | 3D列印專業技術實務培訓班</p>
    </div>

    <div class="main-wrapper">
        <div class="info-section">
            <h2>🎯 課程簡介與核心亮點</h2>
            <p>唯修科技致力於推廣工業級與商用 3D 列印技術。本年度精心規劃兩大核心主題課程，從零基礎概念建立到高階工藝後處理加工，全面輔導學員掌握產業關鍵技術，縮短產品開發週期。</p>
            
            <h2>📚 開班課程資訊</h2>
            <div class="course-card">
                <div class="course-title">📌 課程 A：3D列印基礎認識實務課程【🔥確定開班】</div>
                <p class="course-desc">適合完全零基礎者。課程涵蓋 3D 列印原理剖析、主流切片軟體操作實務、機台校準校正維護，以及常用線材（PLA/PETG）特性與列印參數調校優化。</p>
            </div>
            
            <div class="course-card">
                <div class="course-title">📌 課程 B：3D列印後處理進階課程【⏱️預約待開班】</div>
                <p class="course-desc">專為追求極致成品外觀的學員設計。深入探討支撐材拆除技巧、表面化學拋光、噴砂處理、基礎翻模拓樣、多層次上色與精細塗裝工藝。</p>
            </div>

            <h2>👨‍🏫 唯修專業講師陣容</h2>
            <div class="teacher-box">
                <div class="teacher-avatar">金</div>
                <div class="teacher-info">
                    <p style="font-weight: bold; color: #d9480f; font-size: 16px;">金 總工程師 / 課程總召集人</p>
                    <p style="margin-top: 4px;">• 唯修科技 3D 列印技術研發部負責人</p>
                    <p>• 超過 10 年工業級 3D 列印、逆向工程與快速原型打樣實戰經驗</p>
                    <p>• 專長：FDM/SLA 參數優化、產品結構結構改良與高精度打樣</p>
                </div>
            </div>
        </div>

        <div class="form-section">
            <h2>✍️ 快速學員登記</h2>
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
        © 2026 唯修科技 WEIXIU TECHNOLOGY. All Rights Reserved. <br>
        技術支援：3D列印自動化課程招生管理系統
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
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # ⚠️ 請在此處更換成您發信用的 Gmail 帳號與 16 位元應用程式密碼
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
        
        print("【系統通知】正在透過 587 連線至郵件伺服器...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()  
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
