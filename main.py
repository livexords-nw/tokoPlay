from datetime import datetime
import json
import time
from colorama import Fore
import requests
import random

class tokoplay:
    BASE_URL = "https://minigame.tokocrypto.com/api/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8", 
        "referer": "https://minigame.tokocrypto.com/",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.user_id = None
        self.token = None

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Tokoplay Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔒 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        req_url = f"{self.BASE_URL}user/getToken?initDataRaw={token}&platform=TOKO"
        
        self.log(f"📋 Using token: {token[:10]}... (truncated for security)", Fore.CYAN)

        headers = self.HEADERS

        try:
            self.log("📡 Sending request to fetch token...", Fore.CYAN)
            response = requests.get(req_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Memeriksa apakah status OK dan data tersedia
            if data.get("status") == "OK" and "data" in data:
                token_value = data["data"].get("token")
                if token_value:
                    self.token = token_value
                    self.log("🔑 Authorization token successfully retrieved.", Fore.GREEN)
                    
                    # Mengambil informasi tambahan jika tersedia
                    username = data["data"].get("username", "Unknown")
                    user_ids = data["data"].get("userId", "Unknown")
                    platform = data["data"].get("platform", "Unknown")
                    
                    self.user_id = user_ids

                    self.log("✅ Login successful!", Fore.GREEN)
                    self.log(f"👤 Username: {username}", Fore.LIGHTGREEN_EX)
                    self.log(f"🆔 User ID: {user_ids}", Fore.CYAN)
                    self.log(f"💻 Platform: {platform}", Fore.LIGHTBLUE_EX)
                else:
                    self.log("⚠️ Token not found in response data.", Fore.YELLOW)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
            else:
                self.log("⚠️ Unexpected response structure or status not OK.", Fore.YELLOW)
                self.log(f"📄 Response content: {response.text}", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (possible JSON issue): {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            self.log(f"📄 Response content: {response.text}", Fore.RED)
            
    def task(self) -> None:
        """Menjalankan mekanik task per kategori: fetch tasks, inisiasi task, dan klaim reward.
        
        Catatan: Jika currentProgressValue bernilai 1, maka task dianggap sudah selesai dan tidak akan diproses.
        """
        # Daftar kategori yang akan diproses
        categories = ["Tokocrypto", "Socials", "Frens", "Matches"]
        headers = {**self.HEADERS, "authorization": self.token}

        for category in categories:
            self.log(f"📡 Fetching user tasks for category: {category}...", Fore.CYAN)
            req_url_tasks = f"{self.BASE_URL}task/getUserTasksInfo?userId={self.user_id}&platform=TOKO&categories={category}"
            try:
                response = requests.get(req_url_tasks, headers=headers)
                response.raise_for_status()
                tasks_data = response.json()

                if tasks_data.get("status") != "OK" or "data" not in tasks_data:
                    raise ValueError("Unexpected response structure or status not OK.")

                tasks_list = tasks_data["data"]
                self.log(f"✅ Tasks fetched successfully for {category}: {len(tasks_list)} tasks found.", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to fetch tasks for {category}: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                continue
            except ValueError as e:
                self.log(f"❌ Data error for {category}: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                continue
            except Exception as e:
                self.log(f"❌ Unexpected error for {category}: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                continue

            # Proses setiap task di kategori tersebut
            for task in tasks_list:
                task_id = task.get("taskId")
                task_title = task.get("title", "Unknown")
                if not task_id:
                    self.log("⚠️ Task missing taskId, skipping...", Fore.YELLOW)
                    continue

                # Cek apakah task sudah selesai (currentProgressValue == 1)
                current_progress = task.get("currentProgressValue", 0)
                if current_progress == 1:
                    self.log(f"✅ Task '{task_title}' (ID: {task_id}) already completed, skipping...", Fore.LIGHTGREEN_EX)
                    continue

                self.log(f"🔄 Processing task: {task_title} (ID: {task_id}) in category: {category}", Fore.CYAN)

                # Inisiasi task (doTaskGetReward)
                req_url_do = f"{self.BASE_URL}task/doTaskGetReward"
                payload = {
                    "userId": self.user_id,
                    "platform": "TOKO",
                    "taskId": task_id
                }
                try:
                    self.log("📡 Initiating task...", Fore.CYAN)
                    response = requests.post(req_url_do, headers=headers, json=payload)
                    response.raise_for_status()
                    result = response.json()

                    if result.get("status") == "OK" and result.get("data") is True:
                        self.log("✅ Task initiated successfully.", Fore.GREEN)
                    else:
                        self.log("⚠️ Task initiation failed or unexpected response.", Fore.YELLOW)
                        continue  # Lewati klaim jika task gagal diinisiasi
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to initiate task: {e}", Fore.RED)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    continue
                except Exception as e:
                    self.log(f"❌ Unexpected error during task initiation: {e}", Fore.RED)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    continue

                # Klaim reward task (claimReward)
                req_url_claim = f"{self.BASE_URL}task/claimReward"
                try:
                    self.log("📡 Claiming reward for task...", Fore.CYAN)
                    response = requests.post(req_url_claim, headers=headers, json=payload)
                    response.raise_for_status()
                    result = response.json()

                    if result.get("status") == "OK" and "data" in result:
                        reward = int(result["data"])
                        self.log(f"✅ Reward claimed successfully: {reward}", Fore.GREEN)
                    else:
                        self.log("⚠️ Reward claim failed or unexpected response.", Fore.YELLOW)
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to claim reward: {e}", Fore.RED)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    continue
                except Exception as e:
                    self.log(f"❌ Unexpected error during reward claim: {e}", Fore.RED)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
                    continue

    def game(self) -> None:
        """Menjalankan mekanik game: fetch user game info, detail game info, dan bermain game dengan reward.
        Fungsi ini akan terus bermain game selama energi pengguna > 0. Sebelum eksekusi API game/playGameGetReward, fungsi akan menunggu selama jeda acak antara 80-120 detik."""
        headers = {**self.HEADERS, "authorization": self.token}

        while True:
            # Step 1: Ambil informasi game pengguna
            req_url_game_info = f"{self.BASE_URL}game/getUserGameInfo?userId={self.user_id}&gameId=1&platform=TOKO"
            try:
                self.log("📡 Fetching user game info...", Fore.CYAN)
                response = requests.get(req_url_game_info, headers=headers)
                response.raise_for_status()
                game_info = response.json()
                if game_info.get("status") != "OK" or "data" not in game_info:
                    raise ValueError("Unexpected response structure or status not OK for user game info.")
                
                user_energy = game_info["data"].get("userCurrentEnergy", 0)
                self.log(f"✅ User game info fetched. Current energy: {user_energy}", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to fetch user game info: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return
            except ValueError as e:
                self.log(f"❌ Data error in game info: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return
            except Exception as e:
                self.log(f"❌ Unexpected error while fetching game info: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return

            # Jika energi habis, keluar dari loop
            if user_energy <= 0:
                self.log("⚠️ No energy left to play the game.", Fore.YELLOW)
                break

            # Step 2: Ambil detail game
            req_url_game_detail = f"{self.BASE_URL}game/getGamesInfoById?gameId=1&userId={self.user_id}"
            try:
                self.log("📡 Fetching detailed game info...", Fore.CYAN)
                response = requests.get(req_url_game_detail, headers=headers)
                response.raise_for_status()
                game_detail = response.json()
                if game_detail.get("status") != "OK" or "data" not in game_detail:
                    raise ValueError("Unexpected response structure or status not OK for game details.")
                
                game_name = game_detail["data"].get("name", "Unknown")
                self.log(f"✅ Detailed game info fetched. Game name: {game_name}", Fore.GREEN)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to fetch detailed game info: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return
            except ValueError as e:
                self.log(f"❌ Data error in game details: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return
            except Exception as e:
                self.log(f"❌ Unexpected error while fetching game details: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
                return

            # Step 3: Tunggu jeda acak antara 80-120 detik sebelum bermain game
            sleep_time = random.randint(80, 120)
            self.log(f"⏳ Waiting {sleep_time} seconds before playing the game...", Fore.YELLOW)
            time.sleep(sleep_time)

            # Step 4: Generate skor acak dan mainkan game
            random_score = random.randint(290, 340)
            self.log(f"🎲 Random score generated: {random_score}", Fore.CYAN)
            
            req_url_play_game = f"{self.BASE_URL}game/playGameGetReward"
            payload = {
                "categories": "Matches",
                "userId": self.user_id,
                "platform": "TOKO",
                "gameId": 1,
                "score": random_score,
                "multiplier": 1
            }
            try:
                self.log("📡 Playing game and claiming reward...", Fore.CYAN)
                response = requests.post(req_url_play_game, headers=headers, json=payload)
                response.raise_for_status()
                play_result = response.json()
                
                if play_result.get("status") == "OK":
                    self.log(f"✅ Game played successfully. Score: {random_score}", Fore.GREEN)
                else:
                    self.log("⚠️ Game play failed or unexpected response.", Fore.YELLOW)
                    self.log(f"📄 Response content: {response.text}", Fore.RED)
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to play game: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)
            except Exception as e:
                self.log(f"❌ Unexpected error during game play: {e}", Fore.RED)
                self.log(f"📄 Response content: {response.text}", Fore.RED)

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]

if __name__ == "__main__":
    toko = tokoplay()
    index = 0
    max_index = len(toko.query_list)
    config = toko.load_config()
    if config.get("proxy", False):
        proxies = toko.load_proxies()
        
    toko.log(
        "🎉 [LIVEXORDS] === Welcome to Tokoplay Automation === [LIVEXORDS]", Fore.YELLOW
    )
    toko.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = toko.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        toko.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )


        if config.get("proxy", False):
            toko.override_requests()
        else:
            toko.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)
        toko.login(index)

        toko.log("🛠️ Starting task execution...")
        tasks = {
            "task": "Task Auto Solve 🤖",
            "game": "Auto Playing Game 🎮"     
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            toko.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                toko.log(f"🔄 Executing {task_name}...")
                getattr(toko, task_key)()

        if index == max_index - 1:
            toko.log("🔁 All accounts processed. Restarting loop.")
            toko.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            toko.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
