import urllib.request
import asyncio
import re
import argparse

def get(url):
    response = urllib.request.urlopen("http://" + args.url + urllib.parse.quote(url)).read()
    response = re.search("'.*'", str(response)).group()
    response = response.strip("\'[]{}")
    return str(response)

async def main():
    while True:
        for i in range(3):
            result = get("/session/" + args.session + "/monster/" + str(i) + "/parts")
            assert(result != "false")
            print("monster " + str(i) + " parts: " + result)
            result = get("/session/" + args.session + "/monster/" + str(i) + "/ailments")
            assert(result != "false")
            print("monster " + str(i) + " ailments: " + result)
        print("")
        await asyncio.sleep(1)

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("session")
args = parser.parse_args()
assert(get("/session/" + args.session + "/exists") != "false")

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
