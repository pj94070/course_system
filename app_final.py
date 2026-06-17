import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 如果您有其他路由（例如首頁 /），請保留在您的檔案上方
```python
   @app.route('/')
   def index():
       return render_template('index.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    name = request.form.get('name')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    course_id = request.form.get('course_id')
    
    course_map = {"1": "3D列印基礎認識實務課程 (開班)", "2": "3D列印後處理進階課程 (待開班)"}
    selected_course = course_map.get(course_id, "未知課程")
    
    # 本地 Log 紀錄
    print(f"【成功接收報名】學員：{name} ({gender}) | 電話：{phone} | 信箱：{email} | 項目：{selected_course}")
    
    # ======= 🚀 核心：自動寄送 Email 給唯修科技客服（587 加強版） =======
    try:
        # 1. 將伺服器埠口改為 587
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        sender_email = "填入您發信用的Gmail@gmail.com"        
        sender_password = "填入16位元應用程式密碼"  # 格式如: abcd efgh ijkl mnop
        
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
        
        # 2. 改用標準 SMTP 並加上 timeout=10 避免網頁死當，隨後啟動 TLS 安全加密
        print("【系統通知】正在連線至郵件伺服器...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            server.starttls()  # 關鍵：啟動 TLS 加密通道
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print("【系統通知】公司客服郵件通知已成功寄出！")
        
    except Exception as e:
        # 如果真的又失敗，會印出具體錯誤，但絕對不會再讓網頁 Timeout 崩潰
        print(f"❌ 【系統錯誤】郵件寄送失敗，錯誤原因: {str(e)}")
    # ====================================================
    # ====================================================

    return jsonify({"status": "success", "student_name": name})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
