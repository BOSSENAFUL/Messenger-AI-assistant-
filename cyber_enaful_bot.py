import json
import os
import time
import sys
from fbchat import Client
from fbchat.models import *

# --- কনফিগারেশন ---
COOKIE_FILE = "fb_session.json"
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
            return {c['key']: c['value'] for c in cookies}
    except Exception as e:
        print(f"❌ কুকিজ প্রসেস করতে সমস্যা: {e}")
        return None

def load_all_replies():
    """ফোল্ডারে থাকা সব messenger_bot_*.json ফাইল অটোমেটিক খুঁজে লোড করা"""
    master_data = {}
    files_found = [f for f in os.listdir('.') if f.startswith("messenger_bot_") and f.endswith(".json")]
    
    print(f"\n[!] ডাটাবেজ সিনক্রোনাইজ করা হচ্ছে...")
    for file_name in sorted(files_found):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                replies = data.get("replies", {})
                master_data.update(replies)
        except Exception as e:
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
