# 🔥 Insta-Follower Bot

A simple Python script using Selenium to automatically follow the followers of a specified Instagram account.

> ## ⚠️ **Disclaimer**
>
> This project is for **educational purposes only**. Automating interactions on Instagram is **against their Terms of Service** and can lead to your account being rate-limited, temporarily blocked, or permanently **banned**.
>
> **Use this at your own risk.** The developer assumes no liability for any consequences.

---

## ✨ Features

* Logs into your Instagram account securely using a `.env` file.
* Navigates to a target "similar" account's profile.
* Opens their followers list.
* Scrolls the followers modal to load a set number of users.
* Finds and clicks the "Follow" button for each user in the list.
* Includes basic error handling for when a click is intercepted (e.g., by a popup).

---

## 🛠️ Tech Stack

* [Python](https://www.python.org/)
* [Selenium](https://www.selenium.dev/)
* [webdriver-manager](https://pypi.org/project/webdriver-manager/) (to automatically manage `chromedriver`)
* [python-dotenv](https://pypi.org/project/python-dotenv/) (to securely manage credentials)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/insta-follower-bot.git](https://github.com/your-username/insta-follower-bot.git)
cd insta-follower-bot
```

### 2. Create a Virtual Environment (Recommended)
This keeps your project's dependencies separate from your system.

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env Configuration File
Create a file named .env in the same directory. This script will read your credentials and target account from here.
```code snippet
# .env file
SIMILAR_ACCOUNT="target_account_username"
USERNAME="your_instagram_username"
PASSWORD="your_instagram_password"
```
🏃 Running the Bot
Once you have installed the dependencies and configured your .env file, simply run the main Python script:

```Bash
python main.py
```
