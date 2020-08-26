import json
import urllib.request
import urllib.parse
import asyncio
import re
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    raise Exception("Python 3.8 or higher required")


class Response:
    def __init__(self, status, value):
        self.status = status
        self.value = value


def get(url):
    r = urllib.request.urlopen("http://mhwsync.herokuapp.com/session/testsession" + url).read()
    r = re.search("'.*'", str(r)).group()
    r = r.strip("\'\\\nn")
    r_json = json.loads(r)
    response = Response(r_json["status"], r_json["value"])

    return response


async def main():
    while True:
        for i in range(3):
            print("monster " + str(i) + " parts: ")
            for j in range(5):
                result = get("/monster/" + str(i) + "/part/" + str(j) + "/hp")
                assert(result.status == 0)
                print(result.value + " ")
            print("\n")
            print("monster " + str(i) + " ailments: ")
            for j in range(5):
                result = get("/monster/" + str(i) + "/ailment/" + str(j) + "/buildup")
                assert (result.status == 0)
                print(result.value + " ")
            print("\n")
        print("")
        await asyncio.sleep(1)


assert(get("/exists").status == 0)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
