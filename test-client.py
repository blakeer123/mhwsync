import urllib.request
import asyncio
import re

def get(url):
    response = urllib.request.urlopen(serverip + urllib.parse.quote(url)).read()
    response = re.search("'.*'", str(response)).group()
    response = response.strip("\'[]{}")
    return str(response)

async def main():
    while True:
        for i in range(3):
            result = get("/session/" + session + "/monster/" + str(i) + "/parts")
            assert(result != "false")
            print("monster " + str(i) + " parts: " + result)
            result = get("/session/" + session + "/monster/" + str(i) + "/ailments")
            assert(result != "false")
            print("monster " + str(i) + " ailments: " + result)
        print("")
        await asyncio.sleep(1)

serverip = "http://127.0.0.1:5000/"
session = get("/sessions")
assert(session != "")
print("joined " + session + "\n")

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
