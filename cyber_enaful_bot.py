import json
import os
import time
import sys
from fbchat import Client
from fbchat.models import *

# --- কনফিগারেশন ---
COOKIE_FILE = "fb_session.json"
ID_CONFIG_FILE = "bot_id_config.json"
ADMIN_NAME = "ENAFUL"
TEAM_NAME = "BOT MAKER TEAM"

def show_banner():
    """বট সফলভাবে রান হলে এই ব্যানারটি দেখাবে"""
    banner = f"""
    #################################################
    #                                               #
    #   ███████╗███╗   ██╗ █████╗ ███████╗██╗   ██╗ #
    #   ██╔════╝████╗  ██║██╔══██╗██╔════╝██║   ██║ #
    #   █████╗  ██╔██╗ ██║███████║█████╗  ██║   ██║ #
    #   ██╔══╝  ██║╚██╗██║██╔══██║██╔══╝  ██║   ██║ #
    #   ███████╗██║ ╚████║██║  ██║██║     ╚██████╔╝ #
    #   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═════╝  #
    #                                               #
    #        Developed by: {ADMIN_NAME}                   #
    #        Team: {TEAM_NAME}                   #
    #        Status: System Online (1-20 JSON)      #
    #################################################
    """
    print(banner)

def load_cookies():
    """সেশন ফাইল থেকে কুকিজ লোড করা"""
    if not os.path.exists(COOKIE_FILE):
        print(f"❌ ত্রুটি: '{COOKIE_FILE}' ফাইলটি পাওয়া যায়নি!")
        return None
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
            if isinstance(cookies, list):
                return {c['key']: c['value'] for c in cookies}
            return cookies
    except Exception as e:
        print(f"❌ কুকিজ প্রসেস করতে সমস্যা: {e}")
        return None

def load_bot_ids():
    """বটের আইডি কনফিগারেশন ফাইল থেকে আইডিগুলো লোড করা"""
    if os.path.exists(ID_CONFIG_FILE):
        try:
            with open(ID_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                ids = data.get("bot_ids", [])
                return ids if ids else [" "]
        except Exception as e:
            print(f"⚠️ আইডি লোড করতে সমস্যা: {e}")
            return [" "]
    return [" "]

def load_all_replies():
    """১ থেকে ২০ পর্যন্ত সব messenger_bot_*.json ফাইল কল করা"""
    master_data = {}
    print(f"\n[!] ডাটাবেজ সিনক্রোনাইজ করা হচ্ছে (১-২০ জেসন ফাইল)...")
    
    for i in range(1, 21):
        file_name = f"messenger_bot_{i}.json"
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "replies" in data:
                        master_data.update(data["replies"])
                    else:
                        master_data.update(data)
                    print(f"✅ কানেক্টেড: {file_name}")
            except Exception as e:
                # 1000431440_2.jpg স্ক্রিনশটের এরর এখানে সমাধান করা হয়েছে
                print(f"⚠️ {file_name} লোড করতে সমস্যা: {e}")
        else:
            continue
            
    print(f"\n📊 মোট {len(master_data)} টি ট্রিগার লোড হয়েছে।\n")
    return master_data

# গ্লোবাল ডাটা লোড
ALL_REPLIES = load_all_replies()
BOT_IDS = load_bot_ids()

class CyberEnafulBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # নিজের মেসেজ বা ৫টি আইডির কোনোটি হলে ইগনোর করা
        if author_id == self.uid or author_id in BOT_IDS:
            return

        msg_text = message_object.text.lower() if message_object.text else ""
        
        reply_to_send = None
        for key in ALL_REPLIES:
            if key.lower() in msg_text:
                reply_to_send = ALL_REPLIES[key]
                break

        if reply_to_send:
            try:
                time.sleep(1) 
                self.send(Message(text=reply_to_send), thread_id=thread_id, thread_type=thread_type)
                print(f"📩 ম্যাচ: '{msg_text[:15]}' -> রিপ্লাই সফল।")
            except Exception as e:
                print(f"❌ রিপ্লাই এরর: {e}")

def run_bot():
    session_cookies = load_cookies()
    if not session_cookies:
        print("[!] সেশন ফাইল ছাড়া বট রান করা সম্ভব নয়।")
        sys.exit()

    while True:
        try:
            bot = CyberEnafulBot(' ', ' ', session_cookies=session_cookies)
            show_banner() # সাকসেস হলে ব্যানার দেখাবে
            print(f"👤 ADMIN: {ADMIN_NAME}")
            print(f"🆔 ACTIVE IDS: {', '.join(BOT_IDS[:5])}")
            print("✅ ফেসবুক কানেকশন সফল! বট এখন অনলাইনে আছে।")
            bot.listen()
        except Exception as e:
            print(f"⚠️ কানেকশন বিচ্ছিন্ন: {e}")
            print("[!] ৫ সেকেন্ড পর পুনরায় চেষ্টা করা হচ্ছে...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
