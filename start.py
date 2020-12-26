import subprocess
from flask import Flask
from os import environ


BOT_START_FILE = 'run_bot.py'
PYTHON_PROCESS = 'python3'

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Bot is On"


print(f"Running {BOT_START_FILE}")
bot_process = subprocess.Popen([PYTHON_PROCESS, BOT_START_FILE])
app.run()
