import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, request, jsonify

app = Flask(__name__)

# 💡 終極解法：直接將網頁 HTML 內嵌在程式中，徹底解決 TemplateNotFound 找不到檔案的問題！
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>唯修科技 - 3D列印課程線上報名系統</title>
    <style>
        body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; background: #fff; margin: 30px auto; padding: 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); }
        h2 { color: #0056b3; text-align: center; margin-bottom: 10px; font-size: 28px; }
        .subtitle { text-align: center; color: #666; margin-bottom: 30px; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-weight: bold; margin-bottom: 8px; color: #444; }
        input[type="text"], input[type="tel"], input[type="email"], select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        .radio-group { display: flex; gap: 20px; margin-top: 5px; }
        .radio-group label { font-weight: normal; display: flex; align-items: center; gap: 5px; cursor: pointer; }
        button { width: 100%; background: #007bff; color: white; border: none; padding: 14px; font-size: 18px; font-weight: bold; border-radius: 6px; cursor: pointer; transition: background 0.3s; margin-top: 10px; }
        button:hover { background: #0056b3; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <h2>唯修科技 WEIXIU</h2>
        <div class="subtitle">🚀 3D列印專業課程 - 學員線上報名系統</div>
        
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
                <label for="course_id">欲報名的 3D列印課程項目</label>
                <select id="course_id" name="course_id" required>
                    <option value="1">3D列印基礎認識實務課程 (確定開班)</option>
                    <option value="2">3D列印後處理進階課程 (預約待開班)</option>
                </select>
            </div>
            
            <button type="submit">確認送出報名資訊 ➔</button>
        </form>
        
        <div class="footer">© 唯修科技 WEIXIU TECHNOLOGY. All Rights Reserved.</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # 💡 核心變更：不再透過外部讀取，直接吐出上面刻好的 HTML 報名畫面
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
        
        # ⚠️ 請記得在下方更換成您發信用的 Gmail 帳號與 16 位元應用程式密碼
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

    # 💡 報名成功後直接彈出提示視窗並導回路徑，體驗極佳
    return f"""
    <script>
        alert('【唯修科技】報名成功！感謝您的參與，我們將儘速與您聯絡。');
        window.location.href = '/';
    </script>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
