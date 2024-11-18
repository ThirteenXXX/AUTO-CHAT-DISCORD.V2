import requests
import time
import os
from colorama import Fore
import random
from datetime import datetime
import pytz
import hashlib

ascii_art = r'''
  ________    _      __                 _  __
 /_  __/ /_  (_)____/ /____  ___  ____ | |/ /
  / / / __ \/ / ___/ __/ _ \/ _ \/ __ \|   / 
 / / / / / / / /  / /_/  __/  __/ / / /   |  
/_/ /_/ /_/_/_/   \__/\___/\___/_/ /_/_/|_|  

            >>> ᴀᴜᴛᴏ ʀᴇᴘʟᴀʏ ᴄʜᴀᴛ ᴅᴄ ᴡɪᴛʜ ᴀɪ
___________________________________________
'''

def gradient_text(text, colors):
    colored_text = ""
    color_index = 0
    for char in text:
        if char == ' ':
            colored_text += " "
        else:
            colored_text += f"\033[{colors[color_index]}m{char}\033[0m"
        color_index = (color_index + 1) % len(colors)
    return colored_text

colors = ['32']
colored_ascii = gradient_text(ascii_art, colors)
print(colored_ascii)

def hash_token(token):
    """SHA256"""
    return hashlib.sha256(token.encode()).hexdigest()

def validate_token_locally(token):
    try:
        with open("ThirteenX.txt", "r") as file:
            valid_hashes = [line.strip() for line in file.readlines()]
        
        token_hash = hash_token(token)

        return token_hash in valid_hashes
    except FileNotFoundError:
        print(Fore.RED + "File tidak ditemukan. Pastikan file tersebut ada.")
        return False
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan saat membaca file key: {e}")
        return False

license_key = input("ᴍᴀꜱᴜᴋᴀɴ ᴋᴇʏ ᴀɴᴅᴀ: ").strip()

if validate_token_locally(license_key):
    print(Fore.GREEN + " >>>>>  ᴋᴇʏ ᴠᴀʟɪᴅ  <<<<<")
else:
    print(Fore.RED + "ᴋᴇʏ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ, ʜᴜʙᴜɴɢɪ ᴛʜɪʀᴛᴇᴇɴx2023@ɢᴍᴀɪʟ.ᴄᴏᴍ")
    exit()

channel_id = input("ᴍᴀꜱᴜᴋᴋᴀɴ ɪᴅ ᴄʜᴀɴɴᴇʟ: ").strip()

try:
    sleep_interval = float(input("ᴍᴀꜱᴜᴋᴋᴀɴ ᴡᴀᴋᴛᴜ ɪɴᴛᴇʀᴠᴀʟ ꜱʟᴇᴇᴘ: ").strip())
    if sleep_interval < 0:
        print(Fore.RED + "Waktu interval terlalu kecil. Menggunakan nilai default 1 detik.")
        sleep_interval = 1
except ValueError:
    print(Fore.RED + "Input tidak valid. Menggunakan nilai default 1 detik.")
    sleep_interval = 1

# Read Discord token from file
with open("token.txt", "r") as f:
    discord_token = f.readline().strip()

# Read multiple API keys from file
with open("cohere_api_keys.txt", "r") as f:
    cohere_api_keys = [line.strip() for line in f.readlines()]

# Initialize API key index
current_api_key_index = 0

def get_current_api_key():
    global current_api_key_index
    return cohere_api_keys[current_api_key_index]

def rotate_api_key():
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(cohere_api_keys)
    print(Fore.YELLOW + f"API key rotated. Using key index: {current_api_key_index}")

last_message_id = None

prompts = {
    "curious": "{user_message}\nRespond with a short answer no more than 50 letter like someone who doesn't know much and always asks questions:"
}

# Tambahkan kata kunci baru di bagian keywords
keywords = {
"curious": ["what", "how", "why","help"]
}

kata_kunci_tentang_bot = [
    "are you a bot", "are you bot", "is this a bot", "is this bot", "are you the bot",
    "chat bot", "chat-bot", "bot", "BOT", "Bot", "b0t", "B0T",
    "this is bot", "this is a bot", "is this chat bot", "this is chat bot", "bot or human",
    "are you chatbot", "chatbot", "CHATBOT", "Chatbot", "chat-bot", "chat bot",
    "automated",
    "openai", "OpenAI", "OPENAI", "is this openai", "is this from openai", "are you openai bot",
    "are you from openai", "is this powered by openai", "open ai", "open AI", "OPEN AI",
    "GPT", "gpt", "ChatGPT", "chatgpt", "CHATGPT", "Chat GPT", "chat GPT", "CHAT GPT",
    "is this gpt", "gpt bot", "are you gpt", "are you chatgpt", "is this chatgpt", "chat gpt",
    "are you powered by gpt", "is this a gpt bot", "gpt chat", "openai gpt", "chat-gpt",
    "robot", "Robot", "ROBOT", "roboto", "ROBOTO", "robotic", "ROBOTIC", "ai bot", "AI Bot", "AI BOT", "ai-bot"
    # More keywords omitted for brevity
]

def terkait_identitas_bot(pesan_pengguna):
    return any(kata in pesan_pengguna.lower() for kata in kata_kunci_tentang_bot)

def select_prompt_type(user_message):
    for prompt_type, keyword_list in keywords.items():
        if any(keyword in user_message.lower() for keyword in keyword_list):
            return prompts[prompt_type]
    return random.choice(list(prompts.values()))

def dapatkan_respons_cohere(pesan_pengguna):
    global current_api_key_index

    if terkait_identitas_bot(pesan_pengguna):
        bot_identity_responses = [
            "Let's keep grinding",
            "You're cool", "You're the best", "Let's go", "Keep supporting this project", "I'm with you", "How are you", "Do you play games?", "Do you trade?"
        ]
        respons = random.choice(bot_identity_responses)
    else:
        selected_prompt = select_prompt_type(pesan_pengguna)
        formatted_prompt = selected_prompt.format(user_message=pesan_pengguna)

        while True:
            headers = {
                "Authorization": f"Bearer {get_current_api_key()}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "command-r-plus-08-2024",
                "prompt": formatted_prompt,
                "max_tokens": 50,
                "temperature": 1,
                "stop_sequences": ["\n"]
            }
            
            try:
                response = requests.post("https://api.cohere.ai/v1/generate", headers=headers, json=data, timeout=10)
                
                if response.status_code == 200:
                    response_data = response.json()
                    respons = response_data['generations'][0]['text'].strip()
                    break  # Exit the loop as the API call succeeded
                elif response.status_code == 429:  # Rate limit error
                    print(Fore.RED + "API limit reached. Rotating API key...")
                    rotate_api_key()
                else:
                    print(Fore.RED + f"Gagal mendapatkan respons dari Cohere: {response.status_code}")
                    respons = "Nice bro"
                    break
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"Error saat koneksi ke API: {e}")
                respons = "Oops, ada kesalahan koneksi."
                break
    
    respons = respons.replace('ai assistant', 'best friend').replace('chat bot', 'ThirteenX').replace('chatbot', 'ThirteenX').replace('cohere', 'my senior').replace('coral', 'ThirteenX').replace('hey there,', '').replace('"', '').replace(':', '').replace('!', ',').replace('-', ' ').replace('.', '').lower()
    return respons 

def get_bot_id():
    retries = 3
    for i in range(retries):
        try:
            response = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': discord_token}, timeout=10)
            if response.status_code == 200:
                return response.json()['id']
            else:
                print(Fore.RED + f"Gagal mendapatkan bot ID, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error mendapatkan bot ID: {e}")
            if i < retries - 1:
                print(Fore.YELLOW + "Mencoba lagi...")
                time.sleep(2)
    return None

bot_id = get_bot_id()
if not bot_id:
    print(Fore.RED + "Tidak dapat mendapatkan bot ID. Periksa token atau koneksi Anda.")
    exit()

while True:
    try:
        response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                headers={'Authorization': discord_token}, timeout=10)

        if response.status_code == 200:
            messages = response.json()

            if messages:
                latest_message = messages[0]
                user_message = latest_message['content']
                user_id = latest_message['author']['id']
                username = latest_message['author']['username']
                message_id = latest_message['id']

                if user_id != bot_id and (last_message_id is None or message_id != last_message_id):
                    last_message_id = message_id
                    
                    response_message = dapatkan_respons_cohere(user_message)

                    payload = {
                        'content': response_message,
                        'message_reference': {
                            'message_id': message_id
                        }
                    }

                    headers = {
                        'Authorization': discord_token
                    }

                    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", 
                                      json=payload, 
                                      headers=headers, 
                                      timeout=10)

                    if r.status_code == 200:
                        print(Fore.WHITE + f"Sent message reply to username {username}: ")
                        print(Fore.YELLOW + payload['content'])
                    else:
                        print(Fore.RED + f"Gagal mengirim balasan: {r.status_code}")
                    
                    time.sleep(sleep_interval)
                else:
                    wib_timezone = pytz.timezone("Asia/Jakarta")
                    current_time_wib = datetime.now(wib_timezone)
                    print(Fore.CYAN + f"Thirteen𝕏 | Menunggu Pesan Baru | {current_time_wib.strftime('%H:%M:%S %d-%m-%Y')}")
            else:
                print("Channel kosong atau tidak ada pesan baru.")
        else:
            print(f'Gagal mendapatkan pesan di channel: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Kesalahan koneksi saat mendapatkan pesan: {e}")
    
    time.sleep(sleep_interval)
