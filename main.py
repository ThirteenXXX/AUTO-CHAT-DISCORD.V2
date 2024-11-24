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
    lines = text.split('\n')
    for line in lines:
        color = random.choice(colors)
        colored_text += f"\033[{color}m{line}\033[0m\n"
    return colored_text

def animate_text(text, colors, delay=0.1):
    os.system('cls' if os.name == 'nt' else 'clear')
    lines = text.split('\n')
    for line in lines:
        color = random.choice(colors)
        print(f"\033[{color}m{line}\033[0m")
        time.sleep(delay)  
colors = ['36','36','37','37']

animate_text(ascii_art, colors)


def hash_token(token):
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

def animate_text(text, color, delay=0.1):
    for char in text:
        print(f"{color}{char}", end='', flush=True)
        time.sleep(delay)
    print()

license_key = input("\n𝙼𝙰𝚂𝚄𝙺𝙰𝙽 𝙺𝙴𝚈: ").strip()

if validate_token_locally(license_key):
    animate_text(r'''
  _  _________   __         __     ___    _     ___ ____  
 | |/ / ____\ \ / /         \ \   / / \  | |   |_ _|  _ \ 
 | ' /|  _|  \ V /   _____   \ \ / / _ \ | |    | || | | |
 | . \| |___  | |   |_____|   \ V / ___ \| |___ | || |_| |
 |_|\_\_____| |_|              \_/_/   \_\_____|___|____/ 
                                                          
 ''', Fore.CYAN, delay=0.005)
else:
    print(Fore.RED + "\n𝙺𝙴𝚈 𝚃𝙸𝙳𝙰𝙺 𝚅𝙰𝙻𝙸𝙳, 𝙷𝚄𝙱𝚄𝙽𝙶𝙸 𝚃𝙷𝙸𝚁𝚃𝙴𝙴𝙽𝚇2023@𝙶𝙼𝙰𝙸𝙻.𝙲𝙾𝙼")
    exit()

channel_id = input("\n𝙼𝙰𝚄𝚂𝚄𝙺𝙰𝙽 𝙸𝙳 𝙲𝙷𝙰𝙽𝙽𝙴𝙻: ").strip()

try:
    sleep_interval = float(input("𝙼𝙰𝚂𝚄𝙺𝙰𝙽 𝚆𝙰𝙺𝚃𝚄 𝙸𝙽𝚃𝙴𝚁𝚅𝙰𝙻 𝚂𝙻𝙴𝙴𝙿: ").strip())
    if sleep_interval < 0:
        print(Fore.RED + "Waktu interval terlalu kecil. Menggunakan nilai default 5 detik.")
        sleep_interval = 5
except ValueError:
    print(Fore.RED + "Input tidak valid. Menggunakan nilai default 5 detik.")
    sleep_interval = 5

with open("token.txt", "r") as f:
    discord_token = f.readline().strip()

with open("cohere_api_keys.txt", "r") as f:
    cohere_api_keys = [line.strip() for line in f.readlines()]

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
    "robot", "Robot", "ROBOT", "roboto", "ROBOTO", "robotic", "ROBOTIC", "ai bot", "AI Bot", "AI BOT", "ai-bot", "How are you?"
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
                    break
                elif response.status_code == 429:
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
    
    respons = respons.replace('ai assistant', 'best friend').replace('chat bot', 'homeless').replace('chatbot', 'homeless').replace('cohere', 'my senior').replace('coral', 'homeless').replace('hey there,', '').replace('bot,', 'homeless').replace('"', '').replace(':', '').replace('!', ',').replace('-', ' ').replace('.', '').lower()
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
    
# Tambahkan opsi replay
replay_mode = input("𝙿𝙸𝙻𝙸𝙷 𝙼𝙴𝚃𝙷𝙾𝙳𝙴 𝚁𝙴𝙿𝙻𝙰𝚈:\n1. 𝚁𝙴𝙿𝙻𝙰𝚈 𝙿𝙴𝚂𝙰𝙽 𝚃𝙴𝚁𝙱𝙰𝚁𝚄\n2. 𝚁𝙴𝙿𝙻𝙰𝚈 𝙿𝙴𝚂𝙰𝙽 𝚃𝙰𝚁𝙶𝙴𝚃 𝚄𝚂𝙴𝚁𝙽𝙰𝙼𝙴\n𝙿𝙸𝙻𝙸𝙷 𝙼𝙴𝚃𝙷𝙾𝙳𝙴 (1/2): ").strip()

if replay_mode == "2":
    target_username = input("𝙼𝙰𝚂𝚄𝙺𝙰𝙽 𝚄𝚂𝙴𝚁𝙽𝙰𝙼𝙴 𝚃𝙰𝚁𝙶𝙴𝚃: ").strip()
else:
    target_username = None

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
                referenced_message = latest_message.get("referenced_message")

                # Replay mode logic
                if replay_mode == "1":  # Membalas pesan terbaru
                    should_reply = user_id != bot_id and (last_message_id is None or message_id != last_message_id)
                elif replay_mode == "2":  # Membalas pesan jika username target membalas pesan bot
                    should_reply = (user_id != bot_id 
                                    and username == target_username
                                    and referenced_message is not None
                                    and referenced_message['author']['id'] == bot_id)
                else:
                    should_reply = False

                if should_reply:
                    last_message_id = message_id
                    
                    response_message = dapatkan_respons_cohere(user_message)

                    # Humanizer tambahan
                    humanizer_variants = [
                        f"{response_message} hehe",
                        f"{response_message} haha",
                        f"{response_message} bro", 
                        f"{response_message} buddy",
                        f"{response_message} my friend", 
                        f"{response_message} mate",
                        f"{response_message} brother",
                        f"{response_message} bruh", 
                        response_message
                    ]
                    response_message = random.choice(humanizer_variants)

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
                    print(Fore.CYAN + f"Thirteen𝕏 | Menunggu Pesan Baru... [{current_time_wib.strftime('%Y-%m-%d %H:%M:%S')}]")
            else:
                print("Channel kosong atau tidak ada pesan baru.")
        else:
            print(f'Gagal mendapatkan pesan di channel: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Kesalahan koneksi saat mendapatkan pesan: {e}")
    
    time.sleep(sleep_interval)
