import os
import sys
import re
import binascii
import time
import json
import urllib.request
import urllib.error
import html
import subprocess
import datetime
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from utils import generate_srt

# Load environment variables manually to avoid python-dotenv dependency
def load_env():
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    os.environ[key.strip()] = value

load_env()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here') # Change this for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Get API Keys
api_key = os.getenv("DEEPSEEK_API_KEY")
minimax_api_key = os.getenv("MINIMAX_API_KEY")
minimax_group_id = os.getenv("MINIMAX_GROUP_ID")

if not api_key or api_key == "your_api_key_here":
    print("错误: 未找到有效的 DEEPSEEK_API_KEY。请在 .env 文件中设置您的 API 密钥。")

AUDIO_DIR = os.path.join("static", "audio")
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# --- Models ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    is_pro = db.Column(db.Boolean, default=False)
    pro_expiry = db.Column(db.DateTime, nullable=True) # None means forever if is_pro is True, or check logic

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.is_pro}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, paid
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

# --- Helper function to replace requests library ---
def make_request(url, method="GET", headers=None, json_data=None):
    if headers is None:
        headers = {}
    
    data = None
    if json_data is not None:
        data = json.dumps(json_data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        # User-Agent is sometimes required by APIs
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'Python-urllib/3.x'

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_headers = {k.lower(): v for k, v in response.info().items()}
            content = response.read()
            return {
                "status_code": status_code,
                "headers": response_headers,
                "content": content,
                "json": lambda: json.loads(content.decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        content = e.read()
        return {
            "status_code": e.code,
            "headers": {k.lower(): v for k, v in e.headers.items()},
            "content": content,
            "json": lambda: json.loads(content.decode('utf-8') if content else "{}")
        }
    except urllib.error.URLError as e:
        # Check for connection refused (WinError 10061)
        if isinstance(e.reason, ConnectionRefusedError) or (hasattr(e.reason, 'winerror') and e.reason.winerror == 10061):
            print(f"Connection refused with proxy. Retrying without proxy for {url}...")
            # Create a proxy-bypassing opener
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            try:
                with opener.open(req) as response:
                    status_code = response.getcode()
                    response_headers = {k.lower(): v for k, v in response.info().items()}
                    content = response.read()
                    return {
                        "status_code": status_code,
                        "headers": response_headers,
                        "content": content,
                        "json": lambda: json.loads(content.decode('utf-8'))
                    }
            except Exception as retry_e:
                print(f"Retry without proxy failed: {retry_e}")
                raise e # Raise original error if retry fails
        else:
            raise e
    except Exception as e:
        raise e

def text_to_speech_minimax(text, output_filename, voice_id="male-qn-qingse"):
    # ... (Same as before, abbreviated for brevity in update, but full content preserved)
    if not minimax_api_key or not minimax_group_id:
        return None, "未配置 Minimax API Key"

    output_path = os.path.join(AUDIO_DIR, output_filename)
    url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={minimax_group_id}"
    
    headers = {
        "Authorization": f"Bearer {minimax_api_key}",
        "Content-Type": "application/json"
    }
    
    final_text = text
    # (Preserve existing logic for pauses)
    if voice_id == "Deep_Voice_Man":
        final_text = final_text.replace(".", "... ").replace("!", "... ").replace("?", "... ")
        final_text = final_text.replace(",", ", ")
    elif voice_id == "English_ReservedYoungMan":
        pause_tag = " <#0.83#> "
        final_text = final_text.replace(".", "." + pause_tag).replace("!", "!" + pause_tag).replace("?", "?" + pause_tag)
        final_text = final_text.replace("\n", pause_tag)
    elif voice_id == "English_expressive_narrator":
        pause_tag = " <#0.85#> "
        final_text = final_text.replace(".", "." + pause_tag).replace("!", "!" + pause_tag).replace("?", "?" + pause_tag)
        final_text = final_text.replace("\n", pause_tag)

    payload = {
        "model": "speech-01-turbo",
        "text": final_text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id, 
            "speed": 1.15,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        }
    }

    try:
        response = make_request(url, method="POST", headers=headers, json_data=payload)
        
        if response["status_code"] == 200:
            content_type = response["headers"].get("content-type", "")
            if "audio" in content_type:
                 with open(output_path, "wb") as f:
                    f.write(response["content"])
                 return output_filename, None

            try:
                data = response["json"]()
            except Exception:
                return None, "无法解析 API 响应"

            if data.get("base_resp", {}).get("status_code") == 0:
                if "data" in data and isinstance(data["data"], dict) and "audio" in data["data"]:
                    hex_audio = data["data"]["audio"]
                    try:
                        audio_content = binascii.unhexlify(hex_audio)
                        with open(output_path, "wb") as f:
                            f.write(audio_content)
                        return output_filename, None
                    except Exception as e:
                        return None, f"解析音频 Hex 数据失败: {e}"
                elif "audio_file" in data:
                     audio_url = data["audio_file"]
                     audio_resp = make_request(audio_url)
                     with open(output_path, "wb") as f:
                         f.write(audio_resp["content"])
                     return output_filename, None
                elif "audio_links" in data: 
                     audio_url = data["audio_links"][0]
                     audio_resp = make_request(audio_url)
                     with open(output_path, "wb") as f:
                         f.write(audio_resp["content"])
                     return output_filename, None
                else:
                     return None, "API 调用成功但未找到音频数据"
            else:
                return None, f"API 错误: {data.get('base_resp', {}).get('status_msg')}"
        else:
            return None, f"HTTP 请求失败: {response['status_code']}"
    except Exception as e:
        return None, f"语音生成异常: {e}"

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "12"))

def extract_tiktok_subtitles(url):
    print(f"DEBUG: Extracting subtitles for {url}")
    
    # 1. Try yt-dlp first
    ytdlp_exe = os.path.join(os.getcwd(), "yt-dlp.exe")
    use_exe = os.path.exists(ytdlp_exe)
    cmd = []
    if use_exe:
        cmd = [ytdlp_exe]
    else:
        try:
            subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cmd = [sys.executable, "-m", "yt_dlp"]
        except:
            pass

    if cmd:
        try:
            full_cmd = cmd + ["--write-subs", "--sub-lang", "all", "--skip-download", "--print-json", "--no-warnings", "--output", "temp_%(id)s", url]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore', startupinfo=startupinfo)
            try:
                stdout, stderr = process.communicate(timeout=25)
            except subprocess.TimeoutExpired:
                try:
                    process.kill()
                except Exception:
                    pass
                stdout, stderr = "", "yt-dlp timeout"
            
            if process.returncode == 0 and stdout:
                try:
                    video_info = json.loads(stdout)
                    
                    # Cleanup temp files
                    video_id = video_info.get("id")
                    if video_id:
                        temp_pattern = f"temp_{video_id}"
                        for file in os.listdir(os.getcwd()):
                            if file.startswith(temp_pattern) or file.endswith(".vtt"):
                                try: os.remove(file)
                                except: pass

                    subtitles = video_info.get("subtitles", {})
                    results = []
                    for lang, subs in subtitles.items():
                        for sub in subs:
                            if sub.get("ext") in ["vtt", "srt", "ttml"]:
                                sub_url = sub.get("url")
                                try:
                                    req_sub = urllib.request.Request(sub_url, headers={"User-Agent": "Mozilla/5.0"})
                                    with urllib.request.urlopen(req_sub, timeout=REQUEST_TIMEOUT) as response:
                                        content = response.read().decode('utf-8')
                                        results.append((lang, content))
                                        break
                                except: continue
                    
                    metadata = {
                        "thumbnail": video_info.get("thumbnail"), 
                        "title": video_info.get("title") or "TikTok Video", 
                        "video_url": video_info.get("webpage_url") or url
                    }
                    
                    if results: 
                        return results, metadata, None
                except Exception as e: 
                    print(f"yt-dlp parsing error: {e}")
        except Exception as e: 
            print(f"yt-dlp execution error: {e}")

    # 2. Fallback: Manual Scraping
    print("DEBUG: Falling back to manual scraping")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.tiktok.com/"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            html_content = response.read().decode('utf-8')
        
        results = []
        metadata = {"thumbnail": "", "title": "TikTok Video", "video_url": url}
        
        # Try SIGI_STATE
        sigi_match = re.search(r'window\.SIGI_STATE\s*=\s*({.*?});', html_content)
        if sigi_match:
            try:
                sigi_data = json.loads(sigi_match.group(1))
                item_module = sigi_data.get("ItemModule", {})
                for video_id, video_data in item_module.items():
                    metadata["thumbnail"] = video_data.get("video", {}).get("cover", "")
                    metadata["title"] = video_data.get("desc", "TikTok Video")
                    
                    subs = video_data.get("video", {}).get("subtitleInfos", [])
                    for sub in subs:
                        lang = sub.get("LanguageCodeName", "unknown")
                        sub_url = sub.get("Url")
                        format_fmt = sub.get("Format")
                        if sub_url and format_fmt in ["vtt", "srt", "webvtt"]:
                             try:
                                req_sub = urllib.request.Request(sub_url, headers=headers)
                                with urllib.request.urlopen(req_sub, timeout=REQUEST_TIMEOUT) as response:
                                    content = response.read().decode('utf-8')
                                    results.append((lang, content))
                             except: pass
            except: pass

        if results:
             return results, metadata, None
             
    except Exception as e:
        print(f"Manual scraping error: {e}")
        return None, None, "服务器无法访问 TikTok（可能被网络拦截或超时），请稍后重试或更换网络环境。"

    return None, None, "无法提取字幕，请确认链接有效或该视频无字幕。"

def extract_text(full_text, language):
    pattern = rf"###\s*{language}.*?\n(.*?)(?=\n###|$)"
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    if match: return match.group(1).strip()
    return None

def translate_logic(text, mode, second_lang=None):
    # ... (Preserve translate_logic)
    if mode == "3": return text
    if mode == "1":
        system_prompt = "You are a professional translator. Output separate blocks."
        user_prompt = f"Translate to Chinese and {second_lang}.\n\nOutput format:\n### Chinese\n...\n\n### {second_lang}\n...\n\nText:\n{text}"
    elif mode == "2":
        system_prompt = f"Translate Chinese to {second_lang}."
        user_prompt = f"Translate to {second_lang}.\n\nOutput format:\n### {second_lang}\n...\n\nText:\n{text}"
    else: return None

    try:
        url = "https://api.deepseek.com/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "deepseek-chat", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "stream": False}
        response = make_request(url, method="POST", headers=headers, json_data=payload)
        if response["status_code"] == 200: return response["json"]()["choices"][0]["message"]["content"]
        else: return f"Error: {response['status_code']}"
    except Exception as e: return f"Error: {e}"

# --- Routes ---

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # Admin Bypass Logic
            if username == 'admin': 
                user.is_pro = True
                db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pricing')
@login_required
def pricing():
    return render_template('pricing.html')

@app.route('/tiktok')
@login_required
def tiktok():
    return render_template('tiktok.html')

@app.route('/api/create_order', methods=['POST'])
@login_required
def create_order():
    data = request.json
    method = data.get('method') # wechat / alipay
    amount = data.get('amount')
    
    # Generate unique order ID
    order_id = str(uuid.uuid4())
    order = Order(order_id=order_id, user_id=current_user.id, amount=amount)
    db.session.add(order)
    db.session.commit()
    
    # --- MOCK PAYMENT LOGIC ---
    # In a real scenario, you would call WeChat/Alipay API here to get the QR code URL
    # Since we don't have keys, we return a dummy QR code
    
    # Placeholder QR Code (Google Charts API for demo)
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=MOCK_PAYMENT_FOR_{order_id}"
    
    return jsonify({
        "order_id": order_id,
        "qr_code_url": qr_code_url
    })

@app.route('/api/check_order/<order_id>')
def check_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({"status": "not_found"}), 404
        
    # --- MOCK STATUS CHECK ---
    # For testing, we verify it automatically after 5 seconds (simulated)
    # In real life, this would check DB status updated by Payment Callback
    
    # Auto-approve for demo purposes immediately
    if order.status != 'paid':
        order.status = 'paid'
        user = User.query.get(order.user_id)
        user.is_pro = True
        db.session.commit()
        
    return jsonify({"status": order.status})

@app.route('/api/process', methods=['POST'])
@login_required
def process():
    if not current_user.is_pro:
        return jsonify({"error": "Pro membership required for this feature."}), 403
    data = request.json or {}
    mode = str(data.get('mode', '')).strip()
    text = (data.get('text') or '').strip()
    second_lang = data.get('second_lang')
    enable_tts = bool(data.get('enable_tts', True))
    voice_id = data.get('voice_id', 'male-qn-qingse')

    if mode == "4":
        results, metadata, error = extract_tiktok_subtitles(text)
        if error:
            return jsonify({"error": error}), 500
        if not results:
            return jsonify({"error": "No subtitles found or failed to extract."}), 404
        return jsonify({"subtitles": results, "metadata": metadata})

    if not text:
        return jsonify({"error": "请输入文本"}), 400

    try:
        translation = translate_logic(text, mode, second_lang)
        if isinstance(translation, str) and translation.startswith("Error:"):
            return jsonify({"error": translation}), 500
        resp = {"translation": None}
        if mode == "1":
            zh = extract_text(translation, "Chinese") or ""
            sl = extract_text(translation, second_lang or "") or ""
            combined = f"【中文】\n{zh}\n\n【{second_lang}】\n{sl}".strip()
            resp["translation"] = combined
            tts_source = sl or zh
        elif mode == "2":
            sl = extract_text(translation, second_lang or "") or ""
            combined = f"【{second_lang}】\n{sl}".strip()
            resp["translation"] = combined
            tts_source = sl
        elif mode == "3":
            resp["translation"] = text
            tts_source = text
        else:
            return jsonify({"error": "无效模式"}), 400

        resp["audio_url"] = None
        if enable_tts and tts_source:
            filename = f"{uuid.uuid4()}.mp3"
            audio_file, err = text_to_speech_minimax(tts_source, filename, voice_id)
            if audio_file and not err:
                resp["audio_url"] = url_for('static', filename=f'audio/{audio_file}', _external=False)
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

@app.route('/api/synthesize', methods=['POST'])
@login_required
def synthesize():
    if not current_user.is_pro:
        return jsonify({"error": "Pro membership required for this feature."}), 403
        
    data = request.json
    text = data.get('text')
    voice_id = data.get('voice_id', 'male-qn-qingse')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    
    output_filename, error = text_to_speech_minimax(text, filename, voice_id)
    
    if error:
        return jsonify({"error": f"Speech synthesis failed: {error}"}), 500
        
    audio_url = url_for('static', filename=f'audio/{output_filename}', _external=True)
    
    return jsonify({"audio_url": audio_url})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5005))
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=port)
    except ImportError:
        app.run(debug=False, host="0.0.0.0", port=port)
