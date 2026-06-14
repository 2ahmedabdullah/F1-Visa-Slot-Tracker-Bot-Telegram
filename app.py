#app.py

import os
import re
import json
import asyncio
import pyautogui
from telethon import TelegramClient, events
import time
import asyncio
from models import check_grok_stage1_trigger, check_grok_stage2_validation
from telegram import send_personal_telegram_async
from laptop_alarm import trigger_laptop_alarm
from website import open_visa_portals_parallel
from dotenv import load_dotenv
import sys

# Load credentials from your local environment setup
load_dotenv()

# ==========================================
# 1. CREDENTIALS & GLOBAL CONFIGURATION
# ==========================================
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", 123456))        
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "your_api_hash_here")    
TARGET_CHATS = ['@F1_visa_slots_india', '@F1_Visa_Slots_Group', '@f1_alarm_bot'] 
pyautogui.FAILSAFE = True

# ⏱️ TIMING ENGINE & CONTEXT AMASS MATRIX
COOLDOWN_PERIOD = 1200  
LAST_TRIGGER_TIME = 0.0  

# 🔒 NO-REAUTHENTICATION TRACKING STATE
BROWSER_PIPELINE_RUNNING = False  

# 🌀 CHANNEL-ISOLATED AMASSING STORAGE (Maps channel name -> active state and buffer)
CHANNEL_MATRIX = {}

# 🎯 FIX: Changed MemorySession() to a string identifier "f1_tracker_session".
tg_client = TelegramClient("f1_tracker_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)


# ==========================================
# 2. THE DYNAMIC FILTER PIPELINE (JSON LOADER)
# ==========================================
CONFIG_FILE = "config.json"
matrix_lock = asyncio.Lock()


async def process_message_pipeline(message_text, source="Unknown_Channel", is_forwarded=False):
    global LAST_TRIGGER_TIME, BROWSER_PIPELINE_RUNNING, CHANNEL_MATRIX
    lowered_text = message_text.lower()
    current_time_epoch = time.time()
    
    # Clean the channel key identifier name
    channel_key = str(source).replace("🟢 REAL TRAFFIC: ", "").replace("⚠️ TEST CHAT: ", "").strip()
    
    # CHANGE HERE: Move this lock to the top. If an amass window is open, 
    # save the message instantly and exit without running any filters.
    async with matrix_lock:
        if channel_key in CHANNEL_MATRIX and CHANNEL_MATRIX[channel_key]["active"]:
            print(f"📥 [ISOLATED BUFFERING - {channel_key}] -> {message_text}")
            CHANNEL_MATRIX[channel_key]["buffer"].append(f"- {message_text}")
            return

    print(f"\n📥 Incoming message [{source}]: \"{message_text}\"")

    # Regular filter checks apply ONLY to incoming base messages
    if SPAM_REGEX.search(lowered_text) or NEGATION_REGEX.search(lowered_text) or LOOSE_TALK_REGEX.search(lowered_text):
        print(f"🗑️ Dropped by core regex block filters.")
        return

    if is_forwarded or PAST_TIMELINE_RE.search(lowered_text):
        print(f"⏳ Identified as historical lookback talk or forward. Trigger killed.")
        return

    if TEST_TRIGGER_REGEX.search(lowered_text):
        # 🔒 NO-REAUTHENTICATION CONTROL
        if BROWSER_PIPELINE_RUNNING:
            print("🛡️ [NO-REAUTH SYSTEM ACTIVE]: Browser automated pipeline is already running. Request dropped securely.")
            return

        time_elapsed = current_time_epoch - LAST_TRIGGER_TIME
        if time_elapsed < COOLDOWN_PERIOD:
            print(f"🛡️ [SYSTEM LOCKOUT ACTIVE]: Skipping tracking loops.")
            return

        # 🧠 STAGE 1: Fast AI classification check
        print(f"⚡ Pattern matched! Executing Stage 1 Fast Filter Triage on channel [{channel_key}]...")
        stage1_passed = await check_grok_stage1_trigger(message_text)
        
        if not stage1_passed:
            print("❌ Stage 1 rejected: Text evaluated as generic historical discussion or query.")
            return

        # Double check re-auth lock before spinning resources
        if BROWSER_PIPELINE_RUNNING:
            print("🛡️ [NO-REAUTH LOCKOUT]: Parallel portal instance prevented.")
            return

        print(f"⏳ Stage 1 Passed! Opening 30-second context container strictly isolated for channel [{channel_key}]...")
        
        # Initialize an isolated buffer specific to this channel identifier
        async with matrix_lock:
            CHANNEL_MATRIX[channel_key] = {
                "active": True,
                "buffer": [f"ORIGINAL ALERT TRIGGER: {message_text}"]
            }

        # Hold execution loop for 30 seconds while incoming logs pool up on THIS channel only
        await asyncio.sleep(30.0)

        # Close tracking gate for this channel and extract context block
        async with matrix_lock:
            CHANNEL_MATRIX[channel_key]["active"] = False
            conversation_snapshot = "\n".join(CHANNEL_MATRIX[channel_key]["buffer"])
            del CHANNEL_MATRIX[channel_key] # Clean memory mapping container frame

        print(f"⚡ Amass window closed for channel [{channel_key}]. Forwarding isolated package to Groq Stage 2...")
        
        final_confirmation = await check_grok_stage2_validation(message_text, conversation_snapshot)
        
        if final_confirmation:
            # 🔒 ENGAGE NO-REAUTH
            BROWSER_PIPELINE_RUNNING = True
            print(f"🔥 SYSTEM DROPS CONFIRMED BY SEQUENTIAL PIPELINE CHAIN! LAUNCHING OPERATIONS...")
            LAST_TRIGGER_TIME = time.time()
            
            # 1. Dispatch the personal Telegram notification asynchronously
            asyncio.create_task(send_personal_telegram_async(message_text))
            
            # 2. Get the running loop to handle thread workers
            loop = asyncio.get_running_loop()
            
            # 3. Fire BOTH the blocking sound loop and the browser sequence simultaneously 
            print("🔊 Dispatching Audio Alarm Thread...")
            loop.run_in_executor(None, trigger_laptop_alarm)
            
            print("🌐 Dispatching Parallel Browser Portals Thread...")
            await loop.run_in_executor(None, open_visa_portals_parallel)
            return
        else:
            print(f"❌ Verification Failed: Stage 2 successfully filtered out false alarm chatter on channel [{channel_key}].")
            return
    
    print(f"💤 Message passed filters safely but did not contain target trigger keywords.")


async def main():
    print("💻 Desk-Mode Automated F1 Slot Tracker active.")
    
    # On first run, this line will explicitly prompt you to type your phone number
    # and confirmation code into the terminal. Once complete, it saves the session 
    # to your disk so it won't ask again next time.
    await tg_client.start()
    
    resolved_chats = []
    for chat in TARGET_CHATS:
        try:
            entity = await tg_client.get_entity(chat)
            resolved_chats.append(entity)
            print(f"   ✅ Linked to target: {chat} (ID: {entity.id})")
        except Exception as e:
            print(f"   ❌ Link Failure for {chat}: {e}")

    # 🔬 Active Test Simulation
    # asyncio.create_task(manual_test_worker2())

    @tg_client.on(events.NewMessage(chats=resolved_chats))
    async def slot_handler(event):
        if not event.text: return
        try:
            chat_entity = await event.get_chat()
            source_title = getattr(chat_entity, 'username', getattr(chat_entity, 'title', str(event.chat_id)))
        except: 
            source_title = str(event.chat_id)
            
        is_forwarded = event.message.fwd_from is not None 
        display_source = f"🟢 REAL TRAFFIC: {source_title}"
            
        await process_message_pipeline(event.text.strip(), source=display_source, is_forwarded=is_forwarded)

    print("\n🎧 Monitoring target text data feeds live...")
    await tg_client.run_until_disconnected()


try:
    if not os.path.exists(CONFIG_FILE):
        config_data = {
            "SPAM_AND_JARGON": ["scam", "payment", "agent", "dm me", "paid slot"],
            "NEGATIONS": ["no slots", "closed", "locked", "finished", "gone"],
            "LOOSE_TALK": ["any updates", "when will slots open", "is it open", "predict"],
            "TEST_TRIGGER_KEYWORDS": ["slots opened", "bulk drop", "active", "open now", "go go"]
        }
        print("⚠️ Warning: config.json missing. Using internal default arrays.")
    else:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        print("⚙️ Successfully loaded keyword configurations from JSON layout.")

    SPAM_REGEX = re.compile(r"|".join(config_data["SPAM_AND_JARGON"]), re.IGNORECASE)
    NEGATION_REGEX = re.compile(r"|".join(config_data["NEGATIONS"]), re.IGNORECASE)
    LOOSE_TALK_REGEX = re.compile(r"|".join(config_data["LOOSE_TALK"]), re.IGNORECASE)
    TEST_TRIGGER_REGEX = re.compile(r"|".join(config_data["TEST_TRIGGER_KEYWORDS"]), re.IGNORECASE)

except Exception as err:
    print(f"❌ Failed to parse or compile filters from config.json: {err}")
    sys.exit()

PAST_TIMELINE_RE = re.compile(
    r"\b(yesterday|last night|days ago|weeks ago|months ago|hours ago|back then|last week|last month)\b", 
    re.IGNORECASE
)


if __name__ == "__main__":
    if sys.platform != "win32":
        print("❌ Windows Required.")
        sys.exit()
        
    sys.stdout.reconfigure(line_buffering=True)
    
    try: 
        asyncio.run(main())
    except KeyboardInterrupt: 
        print("\n🛑 Tracker script shut down safely.")