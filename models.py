#models.py

from datetime import datetime
import os
from groq import AsyncGroq  
import sys
from audit import log_grok_transaction
import asyncio
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
if not GROK_API_KEY:
    print("❌ Critical Error: Missing GROK_API_KEY in environment variables.")
    sys.exit()

llm_client = AsyncGroq(api_key=GROK_API_KEY)

async def check_grok_stage1_trigger(initial_message: str) -> bool:
    current_real_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    prompt = f"""You are a high-speed triage engine classifying live messages from a US Visa slot tracking group.
Current Time: {current_real_time}

Analyze this single message: "{initial_message}"

Is this message a report, alert, or announcement that slots are open, active, or currently being booked?
- Output YES if it reports a booking or drop occurrence (e.g., "slots open", "mumbai slots opened guys", "got my slots booked", "just booked june/july/aug/sept/oct"). Treat recent bookings as active alerts.
- Output NO only if it is a pure question asking for information ("when will slots open?", "any updates?"), general chatter, or explicitly references distant past days ("slots were open last week").

Format strictly as exactly one line:
STATUS: [YES or NO]"""

    try:
        response = await llm_client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}],
            temperature=0, max_tokens=15
        )
        res = response.choices[0].message.content.strip()
        print(f"⚡ [Grok Stage 1 Triage Triage]: {res}")
        return "YES" in res.upper()
    except Exception as e:
        print(f"⚠️ Grok Stage 1 Connection Issue: {e}")
        return True

async def check_grok_stage2_validation(initial_message: str, conversation_snapshot: str) -> bool:
    current_real_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    prompt = f"""You are an automated risk-evaluation engine tracking US F1 Visa slot availability.

Initial message: "{initial_message}"

Current Real System Time: {current_real_time}

Review the 30-second live group chat transcript below to confirm if slots are open right now, or if this is a false alarm.

=== LIVE 30-SECOND CHAT TRANSCRIPT ===
{conversation_snapshot}
======================================

ANTI-NITPICKING MANDATE: 
The text snippets listed in parentheses below are pure illustrative examples of conversational intent. If exact matches are there its okay. 
But Do NOT look for only exact word matches. Instead, evaluate the overall semantic meaning, human behavior, and consensus of the group chat.

CRITICAL EVALUATION PROTOCOLS:
1. OVERRIDE TO YES (REAL ALERT): If multiple users are excited, confirming bookings, 
   or if there is sudden high-velocity chaos/panic 
   (e.g., "site crashed", "error limit", "waiting?","submit button not working", "Booked", "many slots", "rate limited", "which date", "congratulations", "Mumbai still open"), 
   treat this as highly authentic. 
   - Multiple city names mentioned ("Chen Kol Mum") or "Hyd Kol" -> Output STATUS: YES.

2. ALLOW MODERATE DOUBT: Do not say NO just because people are asking questions (e.g., "now?", "stuck", "trying", "still available", "yep", "is it available?", "4 slots", "when?", "which location?", "which city?"). 
   Questions are a natural human reaction to a real drop. Output STATUS: YES.

3. STRICT REJECTION (FALSE ALARM): Output STATUS: NO if and only if the follow-up chat explicitly debunks the alert with absolute certainty. 
Look for concrete multiple (majority) counter-evidences not just 1 :
   - old timeframe (e.g., "I meant Tuesday", "happened yesterday", "morning", "yesterday night").
   - false alarm (e.g., "false alarm", "nothing there").
   - No Slots at ALL Location -> e.g., "All gone" or "gone" or "No Slots Available all locations" or "No slots all vac"
   - No Slots at ALL Location -> "No slots @ 5:45" or "None available" or "No VAC anywhere" or "Ghost Slot"
   - promotional 3rd Party -> "Agent did", "my friend helped", "they helped"
   - Output STATUS: NO.

4. HANDLING DEAD SILENCE (CRITICAL): If the transcript contains ONLY the "ORIGINAL ALERT TRIGGER" and absolutely no one else has chatted in 30 seconds.
   Do NOT reject due to silence. Output STATUS: YES.

Format the response strictly as exactly one line:
STATUS: [YES or NO]"""

    try:
        response = await llm_client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}],
            temperature=0, max_tokens=15
        )
        res = response.choices[0].message.content.strip()
        print(f"🤖 [Grok Stage 2 Context Verification]: {res}")
        log_grok_transaction(conversation_snapshot, res)
        return "YES" in res.upper()
    except Exception as e:
        print(f"⚠️ Grok Stage 2 Error: {e}")
        return False


async def manual_test_worker1():
    print("\n🔬 [TEST MODE 1] Simulating false alarm scenario in 6 seconds...")
    await asyncio.sleep(6.0)
    asyncio.create_task(
        process_message_pipeline(
            "Guys i got my slots booked along with 2 other friends for june and july start", 
            source="⚠️ TEST CHAT: F1_visa_slots_india"
        )
    )
    await asyncio.sleep(1.5)
    print("🔬 [TEST MODE 1] Dropping group feedback into the active amassing window...")
    await process_message_pipeline("When did you book?", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(2.0)
    await process_message_pipeline("No dude i booked it literally Tuesday morning", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("Rn no slots", source="⚠️ TEST CHAT: F1_visa_slots_india")
    print("🔬 [TEST MODE 1] All mock follow-up messages sent. Awaiting Stage 2 decision matrix...")




async def manual_test_worker2():
    print("\n🔬 [TEST MODE 2] Simulating chaos / active drop scenario in 6 seconds...")
    await asyncio.sleep(6.0)
    asyncio.create_task(
        process_message_pipeline("Guys i got my slots booked", source="⚠️ TEST CHAT: F1_visa_slots_india")
    )
    await asyncio.sleep(1.5)
    print("🔬 [TEST MODE 2] Dropping panic traffic into the amassing window...")
    await process_message_pipeline("When", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("rate limited", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("stuck waiting", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("same", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("available", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("hyd", source="⚠️ TEST CHAT: F1_visa_slots_india")
    print("🔬 [TEST MODE 2] All mock follow-ups sent. Expecting: STATUS: YES (Real Drop)")


async def manual_test_worker3():
    print("\n🔬 [TEST MODE 2] Simulating chaos / active drop scenario in 6 seconds...")
    await asyncio.sleep(6.0)
    asyncio.create_task(
        process_message_pipeline("Hey guys 12 slots available", source="⚠️ TEST CHAT: F1_visa_slots_india")
    )
    await asyncio.sleep(1.5)
    print("🔬 [TEST MODE 2] Dropping panic traffic into the amassing window...")
    await process_message_pipeline("OFC?", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("No vac", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("Dates ?", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("No ofc", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("Chill", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("No F1 slots   at 3.35", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("Absolute Ragebait", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("No slot available", source="⚠️ TEST CHAT: F1_visa_slots_india")
    await asyncio.sleep(1.0)
    await process_message_pipeline("Maybe it is for rescheduling folks", source="⚠️ TEST CHAT: F1_visa_slots_india")
    print("🔬 [TEST MODE 2] All mock follow-ups sent. Expecting: STATUS: YES (Real Drop)")