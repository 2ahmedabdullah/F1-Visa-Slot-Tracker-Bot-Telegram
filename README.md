# Realtime US Visa F1 Slot Tracker - Telegram (Latency under 60 seconds)

Asynchronous Python-based monitoring tool that listens to Telegram groups for messages related to US F1 visa slot availability.
It uses rule-based filtering and an optional LLM-based classification step (via Groq-hosted models) to help reduce irrelevant alerts. When a potential match is detected, the system sends notifications through a Telegram bot and can optionally trigger a local audio alert.

## 📱 Personalised Alert to Telegram Chat (Mobile Screenshots)

Below are mobile screenshots demonstrating the pipeline in action. When a high-priority consensus is verified by the Stage 2 model, the system immediately pushes alerts directly to the personal Telegram Bot.

![Alarm](img5.png)


## 📸 Live Tracking (Laptop Terminal Screenshots)

Below are the terminal logs showing real-time console telemetry as the pipeline ingests, triages, buffers, and triggers alerts on incoming telegram data packets.

![Live Tracking](terminal0.png)

![Live Tracking](terminal1.png)

## 🛡️ The Claim
⚡Latency: The entire pipeline executes in under 60 seconds; when a slot alert occurs, it undergoes a rapid 2-step verification process to eliminate false alarms before triggering.

💰 Low Fee: Leverages an ultra-low-cost infrastructure utilizing Groq's high-speed API endpoints to process thousands of community interactions daily without premium SaaS subscription fees.

🕞 24x7: Engineered specifically to tackle sudden, high-stakes bulk drops that notoriously occur in the dead of night (2 AM, 3 AM, or later), this system acts as your tireless digital sentinel. 

🌐 Cross Channel: Architected with a modular ingestion layer. The Telethon backend can be scaled instantly to monitor 5+ localized immigration channels, discord servers, or community feeds concurrently without degrading triage performance.


## 🚀 Key Features
Listens to multiple Telegram groups using Telethon and processes incoming messages asynchronously.

**Real-time Telegram Monitoring**  
Listens to multiple Telegram groups using Telethon and processes incoming messages asynchronously.

**Two-stage filtering pipeline**

- **Regex: Rule-based filtering (regex + keywords)**  
  Incoming messages are first evaluated using predefined regex and keyword rules.  
  This stage removes a large portion of irrelevant or noisy messages (e.g., spam, generic chat, non-visa discussions).

- **Stage 1: LLM-based contextual evaluation (Groq API)**  
  Messages that match Rule based triggers are forwarded to an LLM for classification.  
  The model evaluates whether the message likely indicates a real visa slot-related event.

- **Stage 2: Context buffering window (30 seconds)**  
   When Stage 1 is triggered, the system collects additional messages from the same chat over a short time window (e.g., ~30 seconds). This context is included in the LLM prompt to improve classification accuracy.

**Noise reduction design**  
The combination of rule-based filtering and LLM evaluation is designed to reduce false positives while keeping detection latency low.


## 🚨 Dual-Channel Alert Output

Once a targeted event is officially confirmed by Stage 2, the system executes two parallel alert vectors:

📢 Local Hardware Sound Horn Alert: Triggers a persistent, high-frequency Windows audio beep loop (winsound) directly on the host laptop hardware unit to ensure immediate physical awareness.

🔊 Remote Notification Bot: Dispatches an instant alert through a personalized Telegram Bot, delivering a direct identity-link to the target conversation.


## 🛠️ Project Structure & Prerequisites
This application is built exclusively for Windows due to its deep integration with winsound and native desktop process triggers (chrome.exe, msedge.exe).

Installation
Clone or download this project directory to your local Windows machine.

Install all required upstream dependencies using the project's requirements file:

Bash
```
pip install -r requirements.txt
```

Keyword Configuration File (config.json)
Create a config.json file in your root folder to store regular expression filters. If this file is missing, internal defaults will be used:

JSON
```
{
  "SPAM_AND_JARGON": ["scam", "payment", "agent", "dm me", "paid slot"],
  "NEGATIONS": ["no slots", "closed", "locked", "finished", "gone"],
  "LOOSE_TALK": ["any updates", "when will slots open", "is it open", "predict"],
  "TEST_TRIGGER_KEYWORDS": ["slots opened", "bulk drop", "active", "open now", "go go"]
}
```

## ⚙️ Environment Variables Setup (.env)
Create a .env file in the root of your directory to manage credentials and configurations securely.

💡 System Concept: The specific Telegram client account configured here acts as your physical "listener node." When a drop is verified, you will immediately receive a notification via your personal bot showing you exactly which account/host machine has triggered the local automation and laptop audio sequence.

Code snippet
```
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
ALERT_BOT_TOKEN=
MY_PERSONAL_CHAT_ID=
GROK_API_KEY=
```

## 🕹️ Workflow Architecture
Listen: The tracker hooks into targeted Telegram chats via app.py.

Regex Filter: Incoming traffic is stripped of obvious spam, negation statements, or looking-back text using strict regex evaluation blocks.

Stage 1 (Triage): If trigger words are found, the message is dispatched to llama-3.3-70b-versatile to parse semantic intent.

Stage 2 (Amass Window): If Stage 1 yields a YES, a strict isolated 30-second context window starts collecting group responses to evaluate collective group consensus.

Action Suite: If verified as authentic, the program activates an asynchronous sequence:

Dispatches a dedicated Telegram notification alert down to your personal chat interface, calling out the active connected listener account.

Plays a loud, distinct looping beep alarm directly on your computer speakers.



## System Architecture

```text
┌──────────────────────────────┐
│     Target Telegram Feeds    │
│  (Group Chat A /Group Chat B)│
└──────────────┬───────────────┘
      [New Message Inflow]
               ▼
┌──────────────────────────────┐
│     Regex Filtering Pass     │
│(Drops Spam & Historical Talk)│
└──────────────┬───────────────┘
        [Pattern Match]
               ▼
┌──────────────────────────────┐
│      Grok LLM: Stage 1       │
│        (Fast Triage)         │
└──────────────┬───────────────┘
          [Result: YES]
               ▼
┌──────────────────────────────┐
│    30-Second Context Window  │
│  (Amasses Live Group Chat)   │
└──────────────┬───────────────┘
       [Window Concludes]
               ▼
┌──────────────────────────────┐
│      Grok LLM: Stage 2       │
│    (Consensus Evaluation)    │
└──────────────┬───────────────┘
        [Drop Confirmed]
     ┌─────────┴─────────┐
     ▼                   ▼
┌───────────────────┐┌───────────────────┐
│  Laptop Hardware  ││   User Personal   │
│       Unit        ││      TG Bot       │
│(Windows Beep loop)││(Pushes Ident-Link)│
└───────────────────┘└───────────────────┘
```

## 🏎️ Running the Script

Execute the system by running the primary application script:

Bash
```
python app.py
```

## 🧪 Testing Environment
The framework includes simulated testing workers (manual_test_worker1, manual_test_worker2, etc.) mimicking authentic community interactions (e.g., false alarms, genuine chaos, or group panic). To safely stress-test your system pipelines without relying on active telegram drops, uncomment your target worker function inside the main() block initialization process.