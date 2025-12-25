
import os
from flask import Flask
import threading
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# Use Render-assigned PORT, fallback to 10000
port = int(os.environ.get("PORT", 10000))

def run_server():
    app.run(host="0.0.0.0", port=port)

# Start the web server in a separate thread
threading.Thread(target=run_server).start()

# Run your existing bot script as a subprocess
subprocess.run(["python3", "sequence.py"])

