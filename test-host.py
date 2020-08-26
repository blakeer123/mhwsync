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


result = get("/create").status
if result == 2:
    assert(get("/delete").status == 0)
    assert (get("/create").status == 0)
else:
    assert(result == 0)


async def main():
    part_hp = [[3680], [9348, 5168, 504], [7123, 31074]]
    part_hp_modifier = [30, 70, 110]
    ailment_buildup = [[190, 692], [21], [61, 28, 0]]
    ailment_buildup_modifier = [10, 15, 5]

    while True:
        print("changing values")

        for i in range(len(part_hp)):
            for j in range(len(part_hp[i])):
                if part_hp[i][j] <= part_hp_modifier[i]:
                    part_hp[i][j] = 9999
                part_hp[i][j] -= part_hp_modifier[i]
                assert(get("/monster/" + str(i) + "/part/" + str(j) + "/hp/" + str(part_hp[i][j])).status == 0)

        for i in range(len(ailment_buildup)):
            for j in range(len(ailment_buildup[i])):
                ailment_buildup[i][j] += ailment_buildup_modifier[i]
                assert(get("/monster/" + str(i) + "/ailment/" + str(j) + "/buildup/" + str(ailment_buildup[i][j])).status == 0)

        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
