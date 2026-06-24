from datetime import datetime


def log_grok_transaction(conversation_str, grok_decision):
    log_file = "grok_audit.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"========================================================================\n"
        f"⏱️ TIMESTAMP: {timestamp}\n"
        f"📋 30-SEC CONVERSATION SNAPSHOT:\n{conversation_str}\n"
        f"🧠 GROK DECISION RESPONSE: {grok_decision}\n"
        f"========================================================================\n\n"
    )
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️ Failed writing transaction logs to disk: {e}")