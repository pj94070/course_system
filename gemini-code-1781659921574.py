import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 修正核心：在字串引號前方加上 r (Raw String)，徹底消除 Python 對 JavaScript \s 的轉義警告
HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>唯修科技有限公司 - 課程報名系統</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>html { scroll-behavior: smooth; }</style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans">

    <nav class="bg-blue-950 text-white sticky top-0 z-50 shadow-md">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="https://www.weixiu.com.tw/" target="_blank" class="text-xl font-bold tracking-wider hover:text-blue-300 transition">
                唯修科技有限公司
            </a>
            <div class="space-x-6 text-sm font-medium">
                <a href="#brochure" class="hover:text-blue-300 transition">課程簡章</a>
                <a href="#teachers" class="hover:text-blue-300 transition">專業師資</a>
                <a href="#register" class="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg transition">立即報名</a>
            </div>
        </div>
    </nav>

    <header class="bg-gradient-to-r from-blue-950 via-blue-900 to-slate-900 text-white py-16 px-4 text-center">
        <div class="max-w-4xl mx-auto">
            <span class="text-blue-400 font-semibold tracking-widest block mb-2">WEIXIU MAINTAIN TECHNOLOGY CORPORATION</span>
            <h1 class="text-3xl md:text-5xl font-extrabold mb-4 tracking-tight">別讓創意只停留在2D！</h1>
            <p class="text-xl md:text-2xl text-blue-200 mb-6 font-medium">唯修科技帶你從「想」到「摸得到」</p>
            <a href="#brochure" class="bg-white text-blue-950 font-bold px-8 py-3 rounded-full shadow-lg hover:bg-blue-50 transition transform hover:-translate-y-0.5 inline-block">瀏覽詳細課程與師資</a>
        </div>
    </header>

    <section id="brochure" class="py-16 max-w-4xl mx-auto px-4">
        <div class="bg-white p-8 md:p-12 rounded-2xl shadow-md border border-slate-200">
            <div class="border-b-2 border-blue-900 pb-4 mb-6 text-center">
                <h2 class="text-2xl md:text-3xl font-bold text-blue-950">3D 列印基礎訓練課程介紹</h2>
                <p class="text-slate-500 text-sm mt-2">課程代碼：WX-3D115001</p>
            </div>

            <div class="mb-8">
                <h3 class="text-lg font-bold text-blue-900 mb-3">💡 為什麼選擇唯修科技？</h3>
                <ul class="space-y-2 text-slate-700 text-sm pl-4 list-disc">
                    <li><strong class="text-blue-950">實戰導向：</strong>拒絕空談理論！課程將介紹3D 列印原理及相關介紹,讓你親手操作。</li>
                    <li><strong class="text-blue-950">技術核心：</strong>採小班制授課,分享不僅是操作,藉由討論解決結構與材料難題的祕訣。</li>
                    <li><strong class="text-blue-950">從零到一：</strong>提供系統化的教學模組,涵蓋建模邏輯、切層軟體應用到後處理工藝。</li>
                    <li><strong class="text-blue-950">跨界交流：</strong>與不同領域的學員激盪火花,發掘 3D 列印在各行各業的無限可能。</li>
                </ul>
                <p class="mt-4 font-semibold text-blue-700 text-center text-base">"將想像力「印」出來,就在這一刻!"</p>
            </div>

            <div class="grid md:grid-cols-2 gap-6 mb-8 text-sm text-slate-700 leading-relaxed">
                <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                    <h4 class="font-bold text-blue-950 mb-2">一、創意構想：開啟您的「造物主」視角</h4>
                    <p>您想像過將腦中的藍圖,在24小時內轉化為手中真實的觸感嗎?這不僅是一場技術講座課程,更是一場關於「維度跳躍」的實驗。在唯修科技,我們將帶領您突破傳統製造的侷限,從精密零件到客製化藝術品,掌握未來工業的核心競爭力。</p>
                </div>
                <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
                    <h4 class="font-bold text-blue-950 mb-2">二、課程說明</h4>
                    <p>本課程專為對 3D列印技術有實務需求之專業人士及愛好者設計。有鑑於3D列印技術廣泛應用於醫療、航太、工業設計及個人創作,本公司結合多年設備開發與維修經驗,導入最新的切層邏輯與材料科學實例作為訓練教材。</p>
                    <p class="mt-2 text-blue-800 font-medium">※ 本公司為讓學員增加專業技能,將安排基礎繪圖課程,並指導獲取證書。</p>
                </div>
            </div>

            <div class="mb-8 bg-blue-900 text-white p-6 rounded-xl">
                <h3 class="text-lg font-bold mb-3 border-b border-blue-700 pb-1">🪙 三、費用與報名說明</h3>
                <ol class="list-decimal pl-5 space-y-2 text-sm text-blue-100">
                    <li><span class="font-bold text-white">課程費用：</span>每人新台幣 <span class="text-yellow-300 font-bold text-base">18,000元</span>。請於收到錄取通知後一周內完成繳費。</li>
                    <li><span class="font-bold text-white">優惠方案：</span>三人同行,優惠合計新台幣 <span class="text-yellow-300 font-bold text-base">50,000元</span>。</li>
                    <li><span class="font-bold text-white">電子發票：</span>本公司將於課程結束後一週內以 Email 寄送電子發票。</li>
                </ol>
            </div>

            <div class="mb-8">
                <h3 class="text-lg font-bold text-blue-900 mb-3">📅 四、課程時間、課程表及地點</h3>
                <p class="text-sm mb-2 text-slate-600">● <strong>課程時數：</strong>訓練課程約30小時(含繪圖指導及輔導考證)。</p>
                <p class="text-sm mb-3 text-slate-600">● <strong>課程地點：</strong>本公司多功能會議室及3D列印室。</p>
                <div class="overflow-x-auto rounded-xl border border-slate-200 shadow-sm">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead>
                            <tr class="bg-blue-900 text-white border-b border-slate-300">
                                <th class="p-3 font-bold">課程時數 (依授課情況而定)</th>
                                <th class="p-3 font-bold">課程內容安排</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-200 text-slate-700 bg-white">
                            <tr><td class="p-3 bg-slate-50/50">約 2hrs</td><td class="p-3">基礎知識及介紹</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 1hr</td><td class="p-3">建模介紹及建立</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 1hr</td><td class="p-3">切片軟體之操作</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 1hr</td><td class="p-3">機器操作與維護</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 14hrs</td><td class="p-3 font-medium text-slate-900">建模基礎形狀之操作</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 2hrs</td><td class="p-3">設計思維及創作</td></tr>
                            <tr><td class="p-3 bg-slate-50/50">約 4hrs</td><td class="p-3">3D 列印之實作及準備</td></tr>
                            <tr class="bg-blue-50/70 font-semibold text-blue-950">
                                <td class="p-3 text-blue-800">額外加值課程 (約 10hrs)</td>
                                <td class="p-3">SOLIDWORKS 軟體認證</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <section id="teachers" class="py-12 bg-slate-100 border-t border-b border-slate-200">
        <div class="max-w-4xl mx-auto px-4">
            <h2 class="text-2xl md:text-3xl font-bold text-center text-blue-950 mb-2">專業教育課程師資</h2>
            <div class="w-12 h-1 bg-blue-600 mx-auto mb-8"></div>

            <div class="grid md:grid-cols-1 gap-6 max-w-xl mx-auto">
                <div class="bg-white rounded-2xl shadow-md overflow-hidden border border-slate-200 p-6 flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6">
                    <div class="w-32 h-32 rounded-xl overflow-hidden shadow-inner bg-slate-100 flex-shrink-0 border-2 border-blue-900">
                        <img src="https://images.gemini.googleusercontent.com/embed/666faaa40e34b100234c9c7f" alt="Sebastain 講師照片" class="w-full h-full object-cover">
                    </div>
                    <div class="flex-grow text-center sm:text-left">
                        <div class="flex items-center justify-center sm:justify-start space-x-2 mb-1">
                            <h3 class="text-xl font-bold text-slate-900">Sebastain</h3>
                            <span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full font-medium">男</span>
                        </div>
                        <p class="text-sm text-blue-700 font-semibold mb-3">負責課程：3D列印基礎認識實務課程</p>
                        <div class="text-xs text-slate-600 space-y-1 bg-slate-50 p-3 rounded-lg border border-slate-200 inline-block text-left w-full">
                            <p><strong>📧 聯繫方式：</strong><a href="mailto:pj94070@gmail.com" class="text-blue-600 hover:underline">pj94070@gmail.com</a></p>
                            <p><strong>🛠️ 專長領域：</strong>具有豐富 3D 設備研發及實戰生產經驗,專精於切層邏輯,材料科學及快速原型開發。</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="register" class="py-12 bg-blue-50/50">
        <div class="max-w-xl mx-auto px-4">
            <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-200">
                <h2 class="text-2xl font-bold text-blue-950 mb-2 text-center">課程報名處</h2>
                <p class="text-slate-500 text-center text-sm mb-6">請選擇欲報名之項目並填妥基本資料</p>

                <form id="regForm" onsubmit="handleFormSubmit(event)" novalidate>
                    <div class="mb-4">
                        <label class="block text-sm font-semibold text-slate-700 mb-1">選擇課程項目 *</label>
                        <select id="course_id" name="course_id" required class="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="1">3D列印基礎認識實務課程（開班）</option>
                            <option value="2">3D列印後處理進階課程（待開班）</option>
                        </select>
                    </div>

                    <div class="grid grid-cols-3 gap-4 mb-4">
                        <div class="col-span-2">
                            <label class="block text-sm font-semibold text-slate-700 mb-1">學員姓名 *</label>
                            <input type="text" id="name" name="name" required placeholder="請輸入姓名" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-1">性別 *</label>
                            <select id="gender" name="gender" required class="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option value="">請選擇</option>
                                <option value="男">男</option>
                                <option value="女">女</option>
                                <option value="其他">其他</option>
                            </select>
                        </div>
                    </div>

                    <div class="mb-4">
                        <label class="block text-sm font-semibold text-slate-700 mb-1">聯絡電話 *</label>
                        <input type="tel" id="phone" name="phone" required placeholder="例如：0912345678" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <p id="phoneError" class="text-xs text-red-600 mt-1 hidden">⚠️ 請填寫正確的電話格式。</p>
                    </div>

                    <div class="mb-6">
                        <label class="block text-sm font-semibold text-slate-700 mb-1">電子郵件 *</label>
                        <input type="email" id="email" name="email" required placeholder="example@email.com" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <p id="emailError" class="text-xs text-red-600 mt-1 hidden">⚠️ 電子郵件格式有誤，必須包含 @ 符號。</p>
                    </div>

                    <button type="submit" class="w-full bg-blue-700 hover:bg-blue-800 text-white font-bold py-3 px-4 rounded-lg shadow-md transition text-center">
                        確認並送出表單
                    </button>
                </form>
            </div>
        </div>
    </section>

    <footer class="bg-blue-950 text-slate-400 py-10 text-sm text-center">
        <p class="mb-3 text-slate-200 font-medium">&copy; 2026 唯修科技有限公司 創客培訓中心.</p>
        <p class="text-xs">📞 服務專線：03-531-6873 | 📍 公司地址：新竹市香山區中華路四段518號9樓</p>
    </footer>

    <script>
        function handleFormSubmit(event) {
            event.preventDefault();
            const form = document.getElementById('regForm');
            const studentName = document.getElementById('name').value.trim();
            const phoneInput = document.getElementById('phone').value.trim();
            const emailInput = document.getElementById('email').value.trim();

            const phoneError = document.getElementById('phoneError');
            const emailError = document.getElementById('emailError');

            const phoneRegex = /^([0-9]{2,4}-?[0-9]{3,4}-?[0-9]{3,4}$)/; 
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;           

            let hasError = false;

            if (!phoneRegex.test(phoneInput)) {
                phoneError.classList.remove('hidden');
                hasError = true;
            } else { phoneError.classList.add('hidden'); }

            if (!emailRegex.test(emailInput)) {
                emailError.classList.remove('hidden');
                hasError = true;
            } else { emailError.classList.add('hidden'); }

            if (hasError) return;

            const formData = new FormData(form);
            fetch('/submit_registration', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(`${studentName}恭喜您以朝偉大航道前進，未來創意無限`);
                form.reset();
            })
            .catch(error => {
                alert("傳送失敗，請稍後再試");
            });
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return HTML_CONTENT


@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    name = request.form.get('name')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    email = request.form.get('email')
    course_id = request.form.get('course_id')

    course_map = {
        "1": "3D列印基礎認識實務課程（開班）",
        "2": "3D列印後處理進階課程（待開班）"
    }
    selected_course = course_map.get(course_id, "未知課程")

    print(f"【成功接收報名】學員：{name} ({gender}) | 電話：{phone} | 信箱：{email} | 項目：{selected_course}")
    return jsonify({"status": "success", "student_name": name})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    print(f"\n==================================================")
    print(f" 唯修科技有限公司 - 報名系統已啟動！")
    print(f" 請在瀏覽器輸入： http://127.0.0.1:{port}")
    print(f"==================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)