Guide: Setting up a Self-Healing WiFi Power Cycle
Device: Shelly Plug US Gen4

Goal: Configure the Shelly to automatically restore power to a WiFi router after a manual "Off" command, ensuring the reboot completes even if the network is down.

Step 1: Access the Shelly Local Interface
Connect to your local network and navigate to the Shelly's IP address in a web browser.

URL: http://192.168.50.110

[INSERT SCREENSHOT: Shelly Home Dashboard]

Step 2: Navigate to the Switch Component
On the main dashboard, you need to access the specific settings for the power output.

Click on Home in the left sidebar.

Click on the Output (0) or Switch:0 card.

[INSERT SCREENSHOT: Components or Home screen showing the Switch card]

Step 3: Open the Timer Settings
Once inside the Switch settings, scroll down to the Automations section at the bottom of the page.

Locate the horizontal menu containing "Actions", "Schedules", and "Timers".

Click on Timers.

[INSERT SCREENSHOT: Automations section with Timers tab selected]

Step 4: Configure Auto ON
This is the "Self-Healing" mechanism. It tells the Shelly to flip the relay back to 'On' automatically after it has been turned 'Off'.

Find the field labeled Auto ON (in seconds).

Enter 20 (this gives your router 20 seconds of "power off" time to clear its capacitors).

Ensure Auto OFF is set to 0 (disabled).

Click the blue Save button.

[INSERT SCREENSHOT: Timer settings with 20 seconds entered and Save button visible]

How to use this for a Router Reboot
Now that this is configured, you can trigger a reboot even when the internet is failing:

Trigger: Send an OFF command to the Shelly (via the Web UI, a local Home Automation ping, or the HTTP API).

The "Cut": The Shelly cuts power to the router. Your WiFi and Internet will go offline immediately.

The Countdown: Because the instruction is stored locally on the Shelly, it doesn't need WiFi to finish the job. It will count down 20 seconds internally.

The Recovery: After 20 seconds, the Shelly flips itself back to ON. Your router powers up and restores your internet connection.
