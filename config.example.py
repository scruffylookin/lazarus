# Copy this file to config.py and fill in your values
# config.py is gitignored and will not be committed

DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

SHELLY_IP = "192.168.x.x"
ASUS_GATEWAY = "192.168.x.x"
ATT_GATEWAY = "192.168.x.x"
WAN_TARGETS = ["8.8.8.8", "1.1.1.1"]

LOG_FILE = "/var/log/lazarus_watchdog.log"
QUEUE_FILE = "/home/pi/lazarus_queue.json"

REBOOT_LIMIT = 3
LIMIT_WINDOW = 1800  # 30 minutes
COOLDOWN = 300       # 5 minutes
