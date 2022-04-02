# Made by Recrucity

import requests
import colorama
import time
import random
import configparser
import atexit

print(colorama.Fore.LIGHTGREEN_EX + "WELCOME " + colorama.Fore.RESET + "Loading config...")

config = configparser.ConfigParser()
config.read_file(open(r"config.ini"))

itemToWatch = int(config.get("scanning", "itemToWatch"))
maxPrice = int(config.get("scanning", "maxPrice"))
checkDelay = int(config.get("scanning", "checkDelay"))

webhook = config.get("discord", "webhook")

cookie = config.get("auth", "cookie")

while True:
    # Set up session with random proxy from proxies.txt
    time.sleep(checkDelay)
    s = requests.session()
    s.cookies[".ROBLOSECURITY"] = cookie
    proxy = set()

    with open("proxies.txt", "r") as f:
        file_lines1 = f.readlines()
        for line1 in file_lines1:
            proxy.add(line1.strip())

    proxies = {
        "http": random.choice(list(proxy))
    }

    try:
        resellers = s.get("https://economy.roblox.com/v1/assets/ " + str(itemToWatch) + "/resellers", proxies=proxies).json()
        data = resellers["data"]
        bestPrice = data[0]["price"]

        if bestPrice <= maxPrice:
            print(colorama.Fore.LIGHTGREEN_EX + "FOUND " + colorama.Fore.RESET + "Item " + str(itemToWatch) + " selling for " + str(bestPrice) + " robux!")

            # Send discord webhook message
            data = {
                "content": "@everyone Item " + str(itemToWatch) + " is being sold for " + str(bestPrice) + " Robux!\n https://www.roblox.com/catalog/" + str(itemToWatch)
            }
            requests.post(webhook, data=data)

        else:
            print(colorama.Fore.LIGHTBLUE_EX + "INFO " + colorama.Fore.RESET + "Item " + str(
                itemToWatch) + " too expensive (Price: " + str(bestPrice) + ")")
    except:
        print(colorama.Fore.RED + "ERROR " + colorama.Fore.RESET + "Item doesn't exist or you've been rate limited or config issue!")

# Made by Recrucity
