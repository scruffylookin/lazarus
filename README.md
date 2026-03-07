<div align="center">

<img src="lazarus.png" alt="Lazarus — a neon green phoenix made of ethernet cables and Wi-Fi signals, rising from a graveyard of dead routers" width="400">

# Lazarus Watchdog

**Your network dies. Lazarus brings it back.**

A self-healing watchdog for Raspberry Pi that monitors your internet connection and automatically power-cycles networking equipment via a Shelly smart plug when outages are detected.

---

</div>

## How It Works

1. Pings `8.8.8.8` and `1.1.1.1` every 60 seconds to check internet connectivity
2. After 3 consecutive failures, runs diagnostics to identify the failure point:
   - ASUS Router (`192.168.50.1`)
   - AT&T Gateway (`192.168.1.254`)
   - ISP/WAN outage
3. Sends an **OFF** command to the Shelly smart plug — cutting power to the router and sawing off the branch it's sitting on. The Shelly's **Auto ON timer** (configured to 20s) handles restoration entirely on its own, no network needed.
4. Queues Discord webhook notifications while offline, flushes them once connectivity is restored

> **Why only OFF?** Once the Pi kills the router, the local network goes down with it. There's no way to send a follow-up "on" command. The Shelly's Auto ON timer runs on the plug's local firmware, so it will always restore power — even with zero network connectivity. See [Shelly Configuration](shelly_config.md) for setup details.

## Safety Features

- **Rate limiting:** Max 3 reboots per 30-minute window
- **Cooldown:** 5-minute wait after each reboot cycle
- **Standdown:** 10-minute pause when rate limit is reached

## Requirements

- Python 3
- `requests` library (`pip install requests`)
- Shelly smart plug on the local network (with Auto ON timer configured — see [Shelly Configuration](shelly_config.md))
- Discord webhook URL (for notifications)

## Setup

1. Clone the repo to your Raspberry Pi:
   ```bash
   git clone https://github.com/scruffylookin/lazarus.git /home/pi/lazarus
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. [Create a Discord webhook](#discord-webhook-setup) and paste the URL into `lazarus_watchdog.py` as the `DISCORD_WEBHOOK_URL` value

4. Create the log file:
   ```bash
   sudo touch /var/log/lazarus_watchdog.log && sudo chmod 666 /var/log/lazarus_watchdog.log
   ```

5. Create the systemd service:
   ```bash
   sudo nano /etc/systemd/system/lazarus.service
   ```

   Paste the following:
   ```ini
   [Unit]
   Description=Lazarus Network Watchdog
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /home/pi/lazarus_watchdog.py
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   ```

6. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable lazarus.service
   sudo systemctl start lazarus.service
   ```

## Discord Webhook Setup

1. Open Discord and go to the channel where you want Lazarus alerts
2. Click the gear icon to open **Channel Settings**
3. Go to **Integrations** > **Webhooks**
4. Click **New Webhook**
5. Give it a name (e.g. "Lazarus") and click **Copy Webhook URL**
6. Paste the URL into `lazarus_watchdog.py`:
   ```python
   DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url-here"
   ```

### Bonus: Give Lazarus a Personality

Why settle for a boring bot name when your watchdog rises from the dead to resurrect your network? Lean into the theme.

**Custom name and avatar in Discord:**

In the webhook settings (step 4 above), you can set a custom name and upload an avatar image. Some ideas:

- **Name:** `LAZARUS` / `The Resurrector` / `Network Necromancer`
- **Avatar:** A phoenix, a skull with glowing Wi-Fi eyes, or a zombie hand gripping an ethernet cable

**Custom name and avatar per message (overrides webhook defaults):**

You can also set the name and avatar dynamically from the script itself. In `lazarus_watchdog.py`, modify the `flush_discord_queue` payload:

```python
payload = {
    "username": "LAZARUS",
    "avatar_url": "https://i.imgur.com/YOUR_IMAGE.png",
    "content": "⚡ **Lazarus Status Update:**\n" + "\n".join(queue)
}
```

This overrides the webhook's default name and avatar on a per-message basis, so you can even get creative with different avatars for different states:

```python
# Calm — everything is fine
avatar = "https://i.imgur.com/sleeping-phoenix.png"

# Reboot triggered — the resurrection
avatar = "https://i.imgur.com/phoenix-rising.png"

# Rate limit hit — standing down
avatar = "https://i.imgur.com/exhausted-phoenix.png"
```

**Pro tip:** Use an AI image generator to create a custom Lazarus mascot. Prompt idea: *"A pixel-art phoenix made of ethernet cables and Wi-Fi signals rising from a pile of dead routers, dark background, glowing neon green"* — upload that as your webhook avatar and your Discord alerts will go from functional to legendary.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_WEBHOOK_URL` | — | Your Discord webhook URL |
| `SHELLY_IP` | `192.168.50.110` | Shelly smart plug IP |
| `ASUS_GATEWAY` | `192.168.50.1` | ASUS router IP |
| `ATT_GATEWAY` | `192.168.1.254` | AT&T gateway IP |
| `REBOOT_LIMIT` | `3` | Max reboots per window |
| `LIMIT_WINDOW` | `1800` | Rate limit window (seconds) |
| `COOLDOWN` | `300` | Post-reboot cooldown (seconds) |

## Logs

- Local log: `/var/log/lazarus_watchdog.log`
- Discord: Queued notifications sent when connectivity is restored
