---

<h1 align="center">Tokoplay Bot</h1>

<p align="center">Automate tasks and gameplay in Tokoplay to maximize your rewards effortlessly!</p>

---

## 🚀 **About the Bot**

Tokoplay Bot is designed to automate various tasks and game plays on **Tokoplay**—a platform powered by Tokocrypto. This bot takes care of:

- **Auto Task Completion:**  
  Fetches tasks across multiple categories (Tokocrypto, Socials, Frens, Matches) and completes them automatically.
- **Auto Game Play:**  
  Simulates gameplay by generating random scores and waiting random intervals to claim rewards.
- **Multi-Account Support:**  
  Seamlessly switch between multiple accounts.
- **Proxy Support (Optional):**  
  Use proxies to enhance connectivity and manage account-specific requests.

With Tokoplay Bot, you can save time, reduce manual effort, and maximize your in-game rewards.

---

## 🌟 Version v1.0.0

### Updates

- **Task Automation:**  
  Tasks are automatically fetched and processed; completed tasks are skipped.
- **Game Automation:**  
  Game plays are executed with random delays (between 80–120 seconds) and randomized scores (between 290–340) to mimic human behavior.
- **Proxy Integration:**  
  Optional proxy usage for improved request routing.

---

### **Features in This Version:**

- **Auto Task Execution:**  
  Automatically fetch, initiate, and claim rewards from tasks in categories like Tokocrypto, Socials, Frens, and Matches.
- **Auto Game Play:**  
  Automatically play the game and claim rewards as long as you have sufficient energy.
- **Configurable Delays:**  
  Set delays for account switching and looping through accounts.
- **Multi-Account Support:**  
  Easily manage multiple accounts using your query list.
- **Optional Proxy Support:**  
  Enable proxy usage for enhanced connectivity (configured via `config.json`).

---

## ⚙️ **Configuration in `config.json`**

| **Function**           | **Description**                               | **Default** |
| ---------------------- | --------------------------------------------- | ----------- |
| `task`                 | Automatically complete tasks                  | `true`      |
| `game`                 | Automatically play game and claim rewards     | `true`      |
| `proxy`                | Enable/Disable proxy usage                    | `false`     |
| `delay_account_switch` | Delay between account switches (in seconds)   | `10`        |
| `delay_loop`           | Delay before restarting the loop (in seconds) | `500`       |

---

## 📥 **How to Register**

To start using Tokoplay Bot, ensure you have valid query data from your Tokoplay account. This data is typically available from your Tokocrypto minigame dashboard.

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Clone the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/Tokoplay-Bot.git
   ```

2. **Navigate to the Project Folder**  
   Change directory to the project folder:

   ```bash
   cd Tokoplay-Bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your Tokoplay query data (one per line).

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the following format:

   ```
   http://username:password@ip:port
   ```

6. **Configure Settings**  
   Edit the `config.json` file as needed. For example:

   ```json
   {
     "task": true,
     "game": true,
     "proxy": false,
     "delay_account_switch": 10,
     "delay_loop": 500
   }
   ```

7. **Run the Bot**  
   Start the bot with the following command:

   ```bash
   python main.py
   ```

---

### 🔹 Want Free Proxies? You can obtain free proxies from [Webshare.io](https://www.webshare.io/).

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or want to contribute, feel free to reach out:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
