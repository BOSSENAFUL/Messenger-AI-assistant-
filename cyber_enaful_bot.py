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
    """বটের আইডি কনফিগারেশন ফাইল থেকে ৫টি আইডি লোড করার অ্যাডজাস্টেড ফাংশন"""
    if os.path.exists(ID_CONFIG_FILE):
        try:
            with open(ID_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 'bot_ids' কি (key) থেকে লিস্টটি নিবে
                ids = data.get("bot_ids", [])
                return ids if ids else [" "]
        except Exception as e:
            print(f"⚠️ আইডি লোড করতে সমস্যা: {e}")
            return [" "]
    return [" "]

def load_all_replies():
    """
    ১ থেকে ২০ পর্যন্ত এবং ফোল্ডারে থাকা সব messenger_bot_*.json ফাইল 
    অটোমেটিক কল করার সিস্টেম।
    """
    master_data = {}
    
    # আপনার স্ক্রিনশট অনুযায়ী ১ থেকে ২০ পর্যন্ত ফাইলগুলো সুনির্দিষ্টভাবে চেক করবে
    print(f"\n[!] ডাটাবেজ সিনক্রোনাইজ করা হচ্ছে (১-২০ জেসন ফাইল)...")
    
    for i in range(1, 21):
        file_name = f"messenger_bot_{i}.json"
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # ফাইলের ভেতরে যদি 'replies' কী থাকে
                    if isinstance(data, dict) and "replies" in data:
                        master_data.update(data["replies"])
                    else:
                        master_data.update(data)
                    print(f"✅ কানেক্টেড: {file_name}")
            except Exception as e:
                print(f"⚠️ {file_name} পড়তে সমস্যা: {e}")
        else:
            # যদি কোনো ফাইল মিসিং থাকে তবে সেটা স্কিপ করবে
            continue
            
    print(f"\n📊 মোট {len(master_data)} টি ট্রিগার অ্যাক্টিভেট করা হয়েছে।\n")
    return master_data

# গ্লোবাল ডাটা লোড (একবারই লোড হবে)
ALL_REPLIES = load_all_replies()
BOT_IDS = load_bot_ids()

class CyberEnafulBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # নিজের পাঠানো মেসেজ হলে ইগনোর করবে (আপনার ৫টি আইডির যেকোনো একটি হলেও ইগনোর করবে)
        if author_id in self.uid or author_id in BOT_IDS:
            return

        msg_text = message_object.text.lower() if message_object.text else ""
        
        # ১-২০ জেসন ফাইল থেকে আসা সব রিপ্লাই এখানে চেক হবে
        reply_to_send = None
        for key in ALL_REPLIES:
            if key.lower() in msg_text:
                reply_to_send = ALL_REPLIES[key]
                break

        if reply_to_send:
            try:
                time.sleep(1) # সেফটির জন্য ডিলে
                self.send(Message(text=reply_to_send), thread_id=thread_id, thread_type=thread_type)
                print(f"📩 ম্যাচ পাওয়া গেছে! রিপ্লাই পাঠানো হয়েছে।")
            except Exception as e:
                print(f"❌ রিপ্লাই দিতে সমস্যা: {e}")

def run_bot():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🔱 {TEAM_NAME} - AI USERBOT")
    print(f"👤 ADMIN: {ADMIN_NAME}")
    print(f"🆔 ACTIVE IDS: {', '.join(BOT_IDS[:5])}") # প্রথম ৫টি আইডি দেখাবে
    print("🚀 STATUS: ALL 1-20 JSON CONNECTED")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    session_cookies = load_cookies()
    if not session_cookies:
        print("[!] সেশন ফাইল ছাড়া বট রান করা সম্ভব নয়।")
        sys.exit()

    while True:
        try:
            # সেশন দিয়ে লগইন
            bot = CyberEnafulBot(' ', ' ', session_cookies=session_cookies)
            print("✅ ফেসবুক সার্ভারের সাথে কানেকশন সফল!")
            bot.listen()
        except Exception as e:
            print(f"⚠️ কানেকশন এরর: {e}")
            print("[!] ৫ সেকেন্ড পর পুনরায় চেষ্টা করা হচ্ছে...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
            print(f"⚠️ {file_name} লোড করতে সমস্যা: {e}")
    
    print(f"📊 মোট {len(files_found)} টি ফাইল থেকে {len(master_data)} টি ট্রিগার লোড হয়েছে।\n")
    return master_data

# গ্লোবাল রিপ্লাই লিস্ট
ALL_REPLIES = load_all_replies()

class CyberEnafulBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # নিজের মেসেজ হলে ইগনোর করবে
        if author_id == self.uid:
            return

        # ইনকামিং মেসেজ টেক্সট
        msg_text = message_object.text.lower() if message_object.text else ""
        
        # মাস্টার ডাটাবেজ থেকে ম্যাচিং খোঁজা
        reply_to_send = None
        for key in ALL_REPLIES:
            if key.lower() in msg_text:
                reply_to_send = ALL_REPLIES[key]
                break

        if reply_to_send:
            try:
                # মেসেজ পাঠানোর আগে একটি ছোট ডিলে (ব্যান এড়াতে)
                time.sleep(1) 
                self.send(Message(text=reply_to_send), thread_id=thread_id, thread_type=thread_type)
                print(f"✅ রিপ্লাই সফল: {msg_text[:20]}...")
            except Exception as e:
                print(f"❌ রিপ্লাই পাঠাতে সমস্যা: {e}")

def run_bot():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🔱 {TEAM_NAME} - 𝔄ℑ 𝔘𝔰𝔢𝔯𝔟𝔬𝔱")
    print(f"👤 𝔄𝔡𝔪𝔦𝔫: {ADMIN_NAME}")
    print("🚀 𝔖𝔱𝔞𝔱𝔲𝔰: 𝔖𝔶𝔰𝔱𝔢𝔪 𝔅𝔬𝔬𝔱𝔦𝔫𝔔...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    session_cookies = load_cookies()
    if not session_cookies:
        print("[!] সেশন ফাইল ছাড়া বট রান করা সম্ভব নয়।")
        sys.exit()

    while True: # অটো-রানেকশন লুপ
        try:
            bot = CyberEnafulBot(' ', ' ', session_cookies=session_cookies)
            print("✅ ফেসবুক কানেকশন সফল! বট এখন ইনবক্স পাহারা দিচ্ছে।")
            bot.listen()
        except Exception as e:
            print(f"⚠️ কানেকশন বিচ্ছিন্ন হয়েছে: {e}")
            print("[!] ৫ সেকেন্ড পর পুনরায় চেষ্টা করা হচ্ছে...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
