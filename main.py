import os
import sys
import requests
import re
import binascii
import time
from dotenv import load_dotenv
from openai import OpenAI
from utils import generate_srt

# 加载环境变量
load_dotenv()

# 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")
minimax_api_key = os.getenv("MINIMAX_API_KEY")
minimax_group_id = os.getenv("MINIMAX_GROUP_ID")

if not api_key or api_key == "your_api_key_here":
    print("错误: 未找到有效的 DEEPSEEK_API_KEY。请在 .env 文件中设置您的 API 密钥。")
    print("你可以复制 .env.example 为 .env 并填入密钥。")
    sys.exit(1)

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def text_to_speech_minimax(text, output_file="output.mp3", voice_id="male-qn-qingse"):
    """
    使用 Minimax API 将文本转换为语音。
    """
    if not minimax_api_key or not minimax_group_id:
        print("跳过语音生成: 未在 .env 中找到 MINIMAX_API_KEY 或 MINIMAX_GROUP_ID。")
        return

    # Minimax API URL (使用 T2A V2 接口)
    # 国际版: https://api.minimax.io/v1/t2a_v2
    # 国内版: https://api.minimax.chat/v1/t2a_v2
    url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={minimax_group_id}"
    
    headers = {
        "Authorization": f"Bearer {minimax_api_key}",
        "Content-Type": "application/json"
    }
    
    # 使用 T2A V2 的 Payload 结构
    
    # 如果是葡萄牙语，我们通过替换标点符号来增加停顿
    # Minimax 有时支持 <#0.5#> 这样的 SSML 标签，但更通用的方式是利用标点
    # 这里我们尝试简单地将句号、逗号替换为带有更多停顿的标记（视模型支持情况而定）
    # 或者简单地通过在文本中插入换行符或省略号来暗示停顿
    
    final_text = text
    # 针对特定的音色或需求进行停顿处理
    if voice_id == "Deep_Voice_Man":
        # 将句号替换为 "..." 以增加句尾停顿感
        final_text = final_text.replace(".", "... ").replace("!", "... ").replace("?", "... ")
        # 也可以尝试在逗号后增加空格
        final_text = final_text.replace(",", ", ")
    
    elif voice_id == "English_ReservedYoungMan":
        # 用户要求每句间隔 0.83s
        # Minimax 支持 <#time#> 格式的静音标签
        pause_tag = " <#0.83#> "
        final_text = final_text.replace(".", "." + pause_tag).replace("!", "!" + pause_tag).replace("?", "?" + pause_tag)
        # 处理可能的新行作为句子分隔
        final_text = final_text.replace("\n", pause_tag)

    elif voice_id == "English_expressive_narrator":
        # 用户要求每句间隔 0.85s
        pause_tag = " <#0.85#> "
        final_text = final_text.replace(".", "." + pause_tag).replace("!", "!" + pause_tag).replace("?", "?" + pause_tag)
        final_text = final_text.replace("\n", pause_tag)

    payload = {
        "model": "speech-01-turbo", # 尝试使用 Turbo 模型
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
        print(f"正在请求 Minimax 生成语音 (Endpoint: t2a_v2, Model: {payload['model']})...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # 如果 Content-Type 是 audio/mpeg，说明直接返回了音频流
            if "audio" in response.headers.get("Content-Type", ""):
                 with open(output_file, "wb") as f:
                    f.write(response.content)
                 print(f"语音生成成功！已保存为: {output_file}")
                 return

            # 否则解析 JSON
            try:
                data = response.json()
            except Exception:
                print(f"无法解析 API 响应为 JSON。响应内容前200字符: {response.text[:200]}")
                return

            if data.get("base_resp", {}).get("status_code") == 0:
                # 1. 检查 T2A V2 接口的 hex audio (data.audio)
                if "data" in data and isinstance(data["data"], dict) and "audio" in data["data"]:
                    hex_audio = data["data"]["audio"]
                    try:
                        audio_content = binascii.unhexlify(hex_audio)
                        with open(output_file, "wb") as f:
                            f.write(audio_content)
                        print(f"语音生成成功！已保存为: {output_file}")
                        return
                    except Exception as e:
                        print(f"解析音频 Hex 数据失败: {e}")

                # 2. 检查 audio_file (URL)
                elif "audio_file" in data:
                     audio_url = data["audio_file"]
                     print("检测到音频 URL，正在下载...")
                     audio_resp = requests.get(audio_url)
                     with open(output_file, "wb") as f:
                         f.write(audio_resp.content)
                     print(f"语音生成成功！已保存为: {output_file}")
                
                # 3. 检查 audio_links (URL 列表)
                elif "audio_links" in data: 
                     audio_url = data["audio_links"][0]
                     print("检测到音频链接列表，正在下载第一个...")
                     audio_resp = requests.get(audio_url)
                     with open(output_file, "wb") as f:
                         f.write(audio_resp.content)
                     print(f"语音生成成功！已保存为: {output_file}")
                
                else:
                     # 截断输出，防止刷屏
                     print(f"API 调用成功但未找到音频数据。返回数据概览: {str(data)[:200]}...")
            else:
                print(f"API 返回错误状态码: {data.get('base_resp', {}).get('status_code')}")
                print(f"错误信息: {data.get('base_resp', {}).get('status_msg')}")
        else:
            print(f"HTTP 请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
    except Exception as e:
        print(f"语音生成过程中发生错误: {e}")

def extract_text(full_text, language):
    """
    通用文本提取函数。
    """
    # Try to match "### Language" followed by optional colon/space and newline
    pattern = rf"###\s*{language}.*?\n(.*?)(?=\n###|$)"
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    return None

def translate_text(text, second_language):
    """
    使用 DeepSeek 将英文文本翻译成中文和指定的第二语言（法语或葡萄牙语）。
    """
    system_prompt = "You are a professional translator. Your task is to translate English text into Chinese and a second specified language accurately and fluently."
    
    user_prompt = f"""
Please translate the following English text into Chinese and {second_language}.

For the Chinese translation, please strictly follow these rules:
1. Split the content into individual short sentences.
2. Output each sentence on a new separate line.
3. Remove all punctuation marks (replace them with spaces or just remove them).
4. Remove unnecessary adjectives to make the text concise.
5. Ensure the total length is strictly under 400 characters.

Output format:
### Chinese
[Chinese translation]

### {second_language}
[{second_language} translation]

Text to translate:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"翻译过程中发生错误: {e}"

def translate_cn_to_en(text):
    """
    使用 DeepSeek 将中文文本翻译成英文。
    """
    system_prompt = "You are a professional translator. Your task is to translate Chinese text into English accurately and fluently."
    
    user_prompt = f"""
Please translate the following Chinese text into English.

Rules:
1. Split the content into individual sentences.
2. Output each sentence on a new separate line.

Output format:
### English
[English translation]

Text to translate:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"翻译过程中发生错误: {e}"

def translate_cn_to_pt(text):
    """
    使用 DeepSeek 将中文文本翻译成葡萄牙语。
    """
    system_prompt = "You are a professional translator. Your task is to translate Chinese text into Portuguese accurately and fluently."
    
    user_prompt = f"""
Please translate the following Chinese text into Portuguese.

Output format:
### Portuguese
[Portuguese translation]

Text to translate:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"翻译过程中发生错误: {e}"

def extract_english_text(full_text):
    """
    Deprecated. Use extract_text(full_text, "English") instead.
    """
    return extract_text(full_text, "English")

def main():
    print("欢迎使用 DeepSeek 多语种翻译神器！")
    print("-----------------------------------")
    
    # 模式选择
    print("请选择模式:")
    print("1. 英文文案 -> 中文 + (法语/葡萄牙语/日语/德语)")
    print("2. 中文文案 -> 英文")
    print("3. 中文文案 -> 葡萄牙语")
    print("4. 纯翻译模式 (无配音)")
    
    enable_tts = True
    
    while True:
        mode = input("请输入模式编号 (1、2、3 或 4): ").strip()
        if mode in ["1", "2", "3", "4"]:
            break
        print("无效输入，请输入 1、2、3 或 4。")

    if mode == "4":
        enable_tts = False
        print("\n您选择了纯翻译模式。请选择具体的翻译类型:")
        print("1. 英文文案 -> 中文 + (法语/葡萄牙语/日语/德语)")
        print("2. 中文文案 -> 英文")
        print("3. 中文文案 -> 葡萄牙语")
        while True:
            sub_mode = input("请输入翻译类型编号 (1、2 或 3): ").strip()
            if sub_mode in ["1", "2", "3"]:
                mode = sub_mode
                break
            print("无效输入，请输入 1、2 或 3。")

    if mode == "1":
        # 获取用户输入
        print("请输入您要翻译的英文文案 (输入 'END' 并回车结束输入):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip().lower() == 'end':
                    break
                lines.append(line)
            except EOFError:
                break
        
        if not lines:
            print("未检测到输入内容。")
            return

        english_text = "\n".join(lines)
        
        while True:
            choice = input("\n请选择第二目标语言 (1: 法语, 2: 葡萄牙语, 3: 日语, 4: 德语): ").strip()
            if choice == "1":
                second_lang = "French"
                break
            elif choice == "2":
                second_lang = "Portuguese"
                break
            elif choice == "3":
                second_lang = "Japanese"
                break
            elif choice == "4":
                second_lang = "German"
                break
            else:
                print("无效输入，请输入 1、2、3 或 4。")

        print("\n正在请求 DeepSeek 进行翻译，请稍候...\n")
        
        result = translate_text(english_text, second_lang)
        
        print("================ 翻译结果 ================")
        print(result)
        print("==========================================")
        
        # 如果选择了法语或葡萄牙语，尝试生成语音
        if enable_tts:
            import time
            timestamp = int(time.time())

            if second_lang == "French":
                french_text = extract_text(result, "French")
                if french_text:
                    print("\n检测到法语内容，准备生成语音...")
                    output_filename = f"french_audio_{timestamp}.mp3"
                    # 使用 male-qn-qingse 作为法语配音 (通用音色)
                    text_to_speech_minimax(french_text, output_filename, voice_id="male-qn-qingse")
                    # 生成 SRT
                    srt_filename = f"french_audio_{timestamp}.srt"
                    with open(srt_filename, "w", encoding="utf-8") as f:
                        f.write(generate_srt(french_text))
                    print(f"SRT 字幕已保存为: {srt_filename}")
                else:
                    print("\n未检测到有效的法语翻译内容，跳过语音生成。")

            elif second_lang == "Portuguese":
                pt_text = extract_text(result, "Portuguese")
                if pt_text:
                    print("\n检测到葡萄牙语内容，准备生成语音...")
                    output_filename = f"portuguese_audio_{timestamp}.mp3"
                    # 使用 male-qn-qingse 作为葡萄牙语的配音
                    text_to_speech_minimax(pt_text, output_filename, voice_id="male-qn-qingse")
                    # 生成 SRT
                    srt_filename = f"portuguese_audio_{timestamp}.srt"
                    with open(srt_filename, "w", encoding="utf-8") as f:
                        f.write(generate_srt(pt_text))
                    print(f"SRT 字幕已保存为: {srt_filename}")
                else:
                    print("\n未检测到有效的葡萄牙语翻译内容，跳过语音生成。")
            
            elif second_lang == "Japanese":
                jp_text = extract_text(result, "Japanese")
                if jp_text:
                    print("\n检测到日语内容，准备生成语音...")
                    output_filename = f"japanese_audio_{timestamp}.mp3"
                    text_to_speech_minimax(jp_text, output_filename, voice_id="male-qn-qingse")
                    # 生成 SRT
                    srt_filename = f"japanese_audio_{timestamp}.srt"
                    with open(srt_filename, "w", encoding="utf-8") as f:
                        f.write(generate_srt(jp_text))
                    print(f"SRT 字幕已保存为: {srt_filename}")
                else:
                    print("\n未检测到有效的日语翻译内容，跳过语音生成。")

            elif second_lang == "German":
                de_text = extract_text(result, "German")
                if de_text:
                    print("\n检测到德语内容，准备生成语音...")
                    output_filename = f"german_audio_{timestamp}.mp3"
                    text_to_speech_minimax(de_text, output_filename, voice_id="male-qn-qingse")
                    # 生成 SRT
                    srt_filename = f"german_audio_{timestamp}.srt"
                    with open(srt_filename, "w", encoding="utf-8") as f:
                        f.write(generate_srt(de_text))
                    print(f"SRT 字幕已保存为: {srt_filename}")
                else:
                    print("\n未检测到有效的德语翻译内容，跳过语音生成。")

    elif mode == "2":
        # 中文转英文模式
        print("请输入您要翻译的中文文案 (输入 'END' 并回车结束输入):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip().lower() == 'end':
                    break
                lines.append(line)
            except EOFError:
                break
        
        if not lines:
            print("未检测到输入内容。")
            return

        chinese_text = "\n".join(lines)
        
        print("\n正在请求 DeepSeek 进行翻译，请稍候...\n")
        result = translate_cn_to_en(chinese_text)
        
        print("================ 翻译结果 ================")
        print(result)
        print("==========================================")
        
        # 生成英文配音
        if enable_tts:
            en_text = extract_text(result, "English")
            if en_text:
                print("\n检测到英文内容，准备生成语音...")
                import time
                timestamp = int(time.time())
                output_filename = f"english_audio_{timestamp}.mp3"
                # 使用 English_FriendlyPerson 作为英文配音 (更成熟自然的音色)
                text_to_speech_minimax(en_text, output_filename, voice_id="English_FriendlyPerson")
                # 生成 SRT
                srt_filename = f"english_audio_{timestamp}.srt"
                with open(srt_filename, "w", encoding="utf-8") as f:
                    f.write(generate_srt(en_text))
                print(f"SRT 字幕已保存为: {srt_filename}")
            else:
                print("\n未检测到有效的英文翻译内容，跳过语音生成。")

    elif mode == "3":
        # 中文转葡萄牙语模式
        print("请输入您要翻译的中文文案 (输入 'END' 并回车结束输入):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip().lower() == 'end':
                    break
                lines.append(line)
            except EOFError:
                break
        
        if not lines:
            print("未检测到输入内容。")
            return

        chinese_text = "\n".join(lines)
        
        print("\n正在请求 DeepSeek 进行翻译，请稍候...\n")
        result = translate_cn_to_pt(chinese_text)
        
        print("================ 翻译结果 ================")
        print(result)
        print("==========================================")
        
        # 生成葡萄牙语配音
        if enable_tts:
            pt_text = extract_text(result, "Portuguese")
            if pt_text:
                print("\n检测到葡萄牙语内容，准备生成语音...")
                import time
                timestamp = int(time.time())
                output_filename = f"portuguese_audio_{timestamp}.mp3"
                # 使用 English_ReservedYoungMan 作为葡萄牙语配音 (每句间隔 0.83s)
                text_to_speech_minimax(pt_text, output_filename, voice_id="English_ReservedYoungMan")
                # 生成 SRT
                srt_filename = f"portuguese_audio_{timestamp}.srt"
                with open(srt_filename, "w", encoding="utf-8") as f:
                    f.write(generate_srt(pt_text))
                print(f"SRT 字幕已保存为: {srt_filename}")
            else:
                print("\n未检测到有效的葡萄牙语翻译内容，跳过语音生成。")

    input("按回车键退出程序...")

if __name__ == "__main__":
    main()
