import os
import time
import requests
import json
from datetime import datetime
from config import (
    DISCORD_WEBHOOK_URL, SHELLY_IP, ASUS_GATEWAY, ATT_GATEWAY,
    WAN_TARGETS, LOG_FILE, QUEUE_FILE, REBOOT_LIMIT, LIMIT_WINDOW, COOLDOWN
)

def log_and_queue(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    
    # Write to local text log
    with open(LOG_FILE, "a") as f:
        f.write(formatted_msg + "\n")
    print(formatted_msg)

    # Add to Discord queue
    try:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "r") as f:
                queue = json.load(f)
        else:
            queue = []
        queue.append(formatted_msg)
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f)
    except Exception as e:
        print(f"Error queuing: {e}")

def flush_discord_queue():
    if not os.path.exists(QUEUE_FILE):
        return
    
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
        
        if not queue:
            return

        # Combine messages and send
        payload = {"content": "⚡ **Lazarus Status Update:**\n" + "\n".join(queue)}
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        
        if res.status_code < 300:
            os.remove(QUEUE_FILE) # Clear queue on success
    except:
        pass # Internet might still be flaky

def ping(host):
    return os.system(f"ping -c 1 -W 2 {host} > /dev/null 2>&1") == 0

def trigger_lazarus(reason):
    log_and_queue(f"🚨 **REBOOT TRIGGERED**\nReason: `{reason}`")
    try:
        # Send OFF only — the Shelly's Auto ON timer (20s) handles restoration.
        # Once power is cut, the network goes down and we can't send a follow-up command.
        requests.post(f"http://{SHELLY_IP}/rpc/Switch.Set?id=0&on=false", timeout=5)
        return True
    except:
        log_and_queue("⚠️ Failed to reach Shelly Plug locally.")
        return False

def main():
    consecutive_failures = 0
    reboot_history = []

    log_and_queue("🚀 Lazarus Watchdog Service Started.")

    while True:
        # Check WAN
        wan_up = any(ping(t) for t in WAN_TARGETS)
        
        if wan_up:
            if consecutive_failures >= 3:
                log_and_queue("✅ **Internet Restored.**")
            consecutive_failures = 0
            flush_discord_queue() # Send any pending alerts
        else:
            consecutive_failures += 1
            
            if consecutive_failures == 3:
                # Diagnostics
                if not ping(ASUS_GATEWAY):
                    reason = f"ASUS Router ({ASUS_GATEWAY}) Unreachable"
                elif not ping(ATT_GATEWAY):
                    reason = f"AT&T Gateway ({ATT_GATEWAY}) Unreachable"
                else:
                    reason = "ISP/WAN Outage"
                
                # Check Rate Limit
                now = time.time()
                reboot_history = [t for t in reboot_history if now - t < LIMIT_WINDOW]
                
                if len(reboot_history) < REBOOT_LIMIT:
                    if trigger_lazarus(reason):
                        reboot_history.append(now)
                        time.sleep(COOLDOWN)
                else:
                    log_and_queue("🛑 **Rate Limit Reached.** Standing down for 10 mins.")
                    time.sleep(600)

        time.sleep(60)

if __name__ == "__main__":
    main()
