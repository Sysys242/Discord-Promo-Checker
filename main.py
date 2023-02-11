import httpx, itertools
from easyui import *

def printSuccess(text):
    Console.printSuccess(text, PrintType.CLEAN)

def printError(text):
    Console.printError(text, PrintType.CLEAN)

def printInfo(text):
    Console.printInfo(text, PrintType.CLEAN)

proxies = itertools.cycle(open("input/0 - proxies.txt", "r").read().splitlines())
links = open("input/0 - link.txt", "r").read().splitlines()
linksLen = len([ii for n,ii in enumerate(links) if ii not in links[:n]])
links = itertools.cycle([ii for n,ii in enumerate(links) if ii not in links[:n]])

checked = 0

def checkCode(code,proxy):
    res = httpx.get("https://discord.com/api/v9/entitlements/gift-codes/" + code +"?country_code=ES&with_application=false&with_subscription_plan=true", proxies="http://" + proxy)
    if res.status_code == 200:
        if res.json()['redeemed'] == False:
            if res.json()['max_uses'] != res.json()['uses']:
                expiration = str(res.json()['promotion']['inbound_header_text']).split('T')[0]
                return expiration
            else:
                return "redeemed"
    return "nope"


def checkLoop():
    global checked
    while True:
        try:
            if checked >= linksLen:
                break

            link = next(links)
            proxy = next(proxies)

            res = checkCode(link.split("https://promos.discord.gg/")[1], proxy)

            checked += 1
            if res == "redeemed":
                printError("Already Used [" + link.split("https://promos.discord.gg/")[1] + "]")
            elif res == "nope":
                printError("Invalid [" + link.split("https://promos.discord.gg/")[1] + "]")
            else:
                printSuccess("Valid [" + res + "] [" + link.split("https://promos.discord.gg/")[1] + "]")
                with open("output/valid.txt", "a") as f:
                    f.write(link + " | "  + res + "\n")
        except:
            printError("Got an error 💀")

if __name__ == "__main__":
    Console.clear()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_purple, Ascii.get("PromoChecker", AsciiType.BANNER))) + "\n" + Center.XCenter("By Not Sysy's#6700 - V0.0.1"))
    thread = int(input("Thread: "))
    for i in range(thread):
        threading.Thread(target=checkLoop).start()
