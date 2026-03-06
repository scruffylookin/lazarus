# Lazarus Watchdog

A network self-healing watchdog script for Raspberry Pi. Monitors WAN connectivity and automatically power-cycles networking equipment via a Shelly smart plug when outages are detected.

## How It Works

1. Pings `8.8.8.8` and `1.1.1.1` every 60 seconds to check internet connectivity
2. After 3 consecutive failures, runs diagnostics to identify the failure point:
   - ASUS Router (`192.168.50.1`)
   - AT&T Gateway (`192.168.1.254`)
   - ISP/WAN outage
3. Sends HTTP commands to a Shelly smart plug to power-cycle the equipment (off 10s, then on)
4. Queues Discord webhook notifications while offline, flushes them once connectivity is restored

## Safety Features

- **Rate limiting:** Max 3 reboots per 30-minute window
- **Cooldown:** 5-minute wait after each reboot cycle
- **Standdown:** 10-minute pause when rate limit is reached

## Requirements

- Python 3
- `requests` library (`pip install requests`)
- Shelly smart plug on the local network
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

3. Edit `lazarus_watchdog.py` and set your `DISCORD_WEBHOOK_URL`

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
