<h1 align="center"><b>
    ──「 SEQUENCE BOT 」──</b>
</h1>
<p align="center">
  <a href="https://www.python.org">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg" width ="250">
  </a>
</p>

## 🤖 About the Bot

The **Sequence Bot** is a specialized tool designed to organize and sequence media files (Movies, Series, Episodes) automatically. It parses filenames **OR captions** to detect Season, Episode, and Quality, ensuring that files are delivered to your users in the perfect order.

---

## ✨ KEY FEATURES

<details>
<summary><b>🔄 SMART FILE PARSING</b></summary>

- Automatically detects:
  - Season number
  - Episode number
  - Video quality (480p, 720p, 1080p, etc.)
- Works from **filenames** OR **file captions**
- **Dual Mode Support** (File mode / Caption mode)
- No manual renaming required

</details>

<details>
<summary><b>🎯 TWO SEQUENCING MODES</b></summary>

**MODE 1: EPISODE FLOW**
- Sorting Order:
  Season → Episode → Quality
- Best for:
  - Anime series
  - TV shows
  - Episodic content

**MODE 2: QUALITY FLOW**
- Sorting Order:
  Season → Quality → Episode
- Best for:
  - Quality-wise uploads
  - Batch posting

</details>

<details>
<summary><b>📄 DUAL SOURCE MODE (FILE / CAPTION)</b></summary>

**📁 FILE MODE**
- Uses **filename** for parsing metadata
- Default mode for most users
- Works with all file types

**📝 CAPTION MODE**
- Uses **file caption** for parsing metadata
- Perfect for files with detailed captions
- Skip files without captions automatically
- Switch anytime with `/sf` command

</details>

<details>
<summary><b>🔗 LS MODE (LINK SEQUENCE)</b></summary>

- Sequence files using Telegram message links
- Supports:
  - Public channels
  - Private channels
- Bot automatically:
  - Validates message links
  - Checks admin permissions
- Allows:
  - Message range selection (start link -> end link)

</details>

<details>
<summary><b>🔐 FORCE SUBSCRIBE SYSTEM</b></summary>

- Supports up to 3 channels
- Compatible with:
  - Public channels
  - Private channels
- Fully optional
- Can be disabled by setting channel ID to 0
  
</details>

<details>
<summary><b>📊 USER STATISTICS & LEADERBOARD</b></summary>

- MongoDB-based tracking
- Tracks:
  - Total users
  - Total files sequenced
  - Bot uptime
- Command support: `/leaderboard`
</details>

<details>
<summary><b>📢 ADMIN BROADCAST SYSTEM</b></summary>

- Owner-only access
- FloodWait-safe broadcasting
- Tracks:
  - Successful deliveries
  - Failed messages
  - Blocked users
- Broadcast stats saved in database
</details>

<details>
<summary><b>🌐 WEB SERVER INTEGRATION</b></summary>

- Built-in Flask web server
- Keeps bot alive on:
  - Render
  - Koyeb
  - Railway
- No external keep-alive service required

</details>

---

🧠 HOW THE BOT WORKS (OPERATIONAL FLOW)

<details>
<summary><b><u>NORMAL FILE SEQUENCING MODE</u></b></summary>

**STEP 1: START SEQUENCE**

1. User sends: `/sequence`
2. Bot Action: Activates a new sequence session, initializes temporary storage, and clears any old data.

**STEP 2: MODE SELECTION**

1. User chooses mode via `/sf`:
   - **File Mode**: Uses filename for parsing
   - **Caption Mode**: Uses file caption for parsing
2. Bot Action: Sets user preference in database

**STEP 3: FILE COLLECTION**

1. User sends multiple files (videos, documents, audio).
2. Bot Action: For each file:
   - **File Mode**: Reads filename and extracts metadata
   - **Caption Mode**: Reads caption and extracts metadata (skips files without captions)

**STEP 4: SEQUENCING PROFILE (ORDER LOGIC)**

- **PROFILE: EPISODE FLOW** (Season → Episode → Quality)
  - Example Order: S01E01 480p → S01E01 720p → S01E02 480p
  - Best for: Anime, TV series.
  
- **PROFILE: QUALITY FLOW** (Season → Quality → Episode)
  - Example Order: All Season 1 480p episodes → All Season 1 720p episodes.
  - Best for: Batch quality uploads.

**STEP 5: USER CONFIRMATION**

1. Bot displays inline buttons: Send | Cancel.
2. User Action: "Send" continues the process; "Cancel" clears the session.

**STEP 6: FILE DELIVERY**

1. Bot Action: Sorts files based on the selected profile and sends them one-by-one with safe delays.
2. Completion: Temporary data is cleared, and the session closes.

**STEP 7: DATABASE UPDATE**

1. Bot Action: Updates MongoDB with new stats (total files sequenced, user activity).
2. Data Usage: Powers the `/leaderboard` command and admin analytics.

</details>

<details>
<summary><b><u>CHANNEL / LINK SEQUENCING (LS MODE)</u></b></summary>

**STEP 1: START LS MODE**

1. User sends: `/ls`
2. Bot Action: Activates LS mode and prepares to accept message links.

**STEP 2: MODE CHECK**

1. Bot checks user's current mode (File/Caption) from database
2. Shows current mode in activation message

**STEP 3: MESSAGE RANGE INPUT**

1. User sends the first message link (start point).
2. Bot Action: Validates the link format and channel access.
3. User sends the second message link (end point).
4. Bot Action: Ensures both links are from the same channel.

**STEP 4: TARGET SELECTION**

- Bot shows destination options: Chat (user's DM) or Channel (repost).

**STEP 5: PERMISSION CHECK**

- If the target is a Channel, the bot verifies it has admin posting rights. If not, the process stops.

**STEP 6: FILE EXTRACTION & SORTING**

1. Bot Action: Fetches all messages between the start and end message IDs.
2. Filtering: Identifies videos, documents, and audio files.
3. Sequencing: Applies the chosen Episode Flow or Quality Flow logic.
4. **Mode-Specific Processing**:
   - **File Mode**: Uses filename for metadata
   - **Caption Mode**: Uses file caption for metadata (skips files without captions)

**STEP 7: FILE REPOSTING**

1. Bot Action: Reposts the files in the correct sequence with flood control.
2. Completion: Updates user statistics and clears the LS session.

</details>

<details>
<summary><b><u>MODE SWITCHING (/sf COMMAND)</u></b></summary>

**WHEN TO USE FILE MODE:**
- Files have descriptive filenames
- No captions available
- Default mode for general use

**WHEN TO USE CAPTION MODE:**
- Files have detailed captions
- Filenames are generic or numbered
- Want to skip files without metadata

**HOW TO SWITCH:**
1. Send `/sf` command
2. Interactive buttons appear
3. Select desired mode
4. Mode is saved for future sessions

</details>

---



## ⚙️ CONFIGURATION (config.py)

| Variable | Description |
| :--- | :--- |
| API_ID | Telegram API ID (from my.telegram.org) |
| API_HASH | Telegram API Hash (from my.telegram.org) |
| BOT_TOKEN | Bot token from @BotFather |
| MONGO_URI | MongoDB connection URI |
| OWNER_ID | Telegram user ID of the bot owner |
| FSUB_CHANNEL | Force subscribe channel ID (0 to disa## 🧾 COMMANDS LIST

👤 User Commands:
```
/start - Start the bot
/sequence - Start file sequencing
/fileseq - Choose sequencing mode
/ls - Sequence files from channel links
/leaderboard - View top users
/sf - Switch between File mode and Caption mode
```
👑 Admin Commands (OWNER only):
```
/status - Bot uptime, ping, users
/broadcast - Send message to all users
```
<details>
<summary><b>View Configuration Template</b></summary>

```python
# config.py

# Get these from https://my.telegram.org
API_ID = 123456
API_HASH = "your_api_hash_here"

# Get this from @BotFather on Telegram
BOT_TOKEN = "your_bot_token_here"

# MongoDB database connection string
MONGO_URI = "your_mongodb_uri_here"

# Your Telegram User ID (Get from @userinfobot)
OWNER_ID = 123456789

# Force Subscribe Channel IDs (Set to 0 to disable)
FSUB_CHANNEL = -1001234567890
FSUB_CHANNEL_2 = 0  # Set to 0 if not used
FSUB_CHANNEL_3 = 0  # Set to 0 if not used
```

</details>

NOTE: To completely disable the Force Subscribe system, set all FSUB_CHANNEL values to 0.

---

🚀 DEPLOYMENT METHODS

<h3 align="center">
    <b><u>──「 ᴅᴇᴩʟᴏʏ ᴏɴ ᴠᴘs / ʟᴏᴄᴀʟ ᴍᴀᴄʜɪɴᴇ 」──</u></b>
</h3>

1. Clone the Repository

```bash
git clone https://github.com/N4-Bots/SEQUENCE-BOT.git SequenceBot
cd SequenceBot
```

1. Install Requirements

```bash
pip3 install -r requirements.txt
```

1. Configure the Bot
   Edit theconfig.py file with your credentials as shown above.
2. Run the Bot
   You need to runtwo commands in separate terminal sessions:

· Command 1: Start the Web Server

```bash
python3 webserver.py
```

· Command 2: Start the Main Bot Engine

```bash
python3 sequence.py
```

<h3 align="center">
    <u>──「 ᴅᴇᴩʟᴏʏ ᴏɴ ʀᴇɴᴅᴇʀ / ᴋᴏʏᴇʙ / ʜᴇʀᴏᴋᴜ 」──</u>
</h3>

<p>These platforms are excellent for free-tier hosting. The built-in Flask web server (webserver.py) is specifically designed to keep the bot alive on these services.</p>

<ol>
  <li>Fork this repository to your GitHub account.</li>
  <li>Create a new project/app on your chosen platform (Render, Koyeb, Railway).</li>
  <li>Connect your GitHub repository.</li>
  <li>Set the required environment variables (API_ID, API_HASH, BOT_TOKEN, MONGO_URI, etc.).</li>
  <li>Set the start command to: <code>python3 sequence.py</code> (the platform will handle the web server).</li>
  <li>Deploy!</li>
</ol>

<p><strong>For the fastest deployment, click the button below for your preferred platform:</strong></p>

<h3>Deploy on Heroku</h3>
<a href="https://heroku.com/deploy?template=https://github.com/N4-Bots/SEQUENCE-BOT">
<img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy on Heroku">
</a>


<h3>Deploy on Railway</h3>
<a href="https://railway.app/new/template?template=https://github.com/N4-Bots/SEQUENCE-BOT">
<img src="https://railway.app/button.svg" alt="Deploy on Railway" width="147">
</a>


<h3>Deploy on Koyeb</h3>
<a href="https://app.koyeb.com/deploy?type=git&repository=https://github.com/N4-Bots/SEQUENCE-BOT&branch=main&name=sequence-bot">
<img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy on Koyeb">
</a>

---

## 🤝 SUPPORT

<p align="center">
<a href="https://t.me/N4_Bots">
    <img src="https://img.shields.io/badge/Support%20Group-blue?style=for-the-badge&logo=telegram" alt="Support Group">
</a>
<a href="https://t.me/N4_Bots">
    <img src="https://img.shields.io/badge/Support%20Channel-blue?style=for-the-badge&logo=telegram" alt="Support Channel">
</a>
</p>

---

## LICENSE & CREDITS

· 📝 License: This project is licensed under the MIT License.<br>
· 🤝 Contributing: Contributions are welcome! Feel free to open pull requests to improve this project.<br>
· 🙏 Credits:<br>
             · Made by: [N4 BOTS (TG)](https://t.me/N4_Bots)<br>
             · Powered by: [N4_Bots (TG)](https://t.me/N4_Bots)
##

   **Star this Repo if you Liked it ⭐⭐⭐**

