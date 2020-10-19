import json
import traceback
import urllib.request
import urllib.parse
import asyncio
import sys
import cProfile

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    raise Exception("Python 3.8 or higher required")


session_url = "http://mhwsync-development.herokuapp.com/session/testsession"


class Response:
    status: int
    value: str

    def __init__(self, status: int, value: str):
        self.status = status
        self.value = value

    def __str__(self) -> str:
        return "status: " + str(self.status) + "\nvalue: " + self.value


def get(url):
    r = urllib.request.urlopen(session_url + url).read()
    r_json = json.loads(r)
    response = Response(r_json["status"], r_json["value"])

    return response


def handle_error(optional=""):
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    filename, line, func, text = tb_info[-1]

    print('An error occurred on line {} in statement {}'.format(line, text))
    if optional != "":
        print(optional)
    exit(1)


async def main():
    result = get("/create")
    if result.status == 2:
        try:
            assert(get("/delete").status == 0)
            assert(get("/create").status == 0)
        except AssertionError:
            handle_error()
    else:
        try:
            assert(result.status == 0)
        except AssertionError:
            handle_error("result = " + str(result))

    part_times_broken = [[0], [0, 0, 0], [0, 0]]
    part_hp_start = [[3680], [9348, 5168, 504], [7123, 31074]]
    part_hp = [[3680], [9348, 5168, 504], [7123, 31074]]
    part_hp_modifier = [30, 70, 110]

    ailment_buildup_start = [[190, 692], [21], [61, 28, 0]]
    ailment_buildup = [[190, 692], [21], [61, 28, 0]]
    ailment_buildup_modifier = [10, 15, 5]

    counter = 0

    # initialize values
    for i in range(len(part_hp_start)):
        for j in range(len(part_hp_start[i])):
            assert(get("/monster/" + str(i) + "/part/" + str(j) + "/max_hp/" + str(part_hp_start[i][j])).status == 0)
            assert(get("/monster/" + str(i) + "/part/" + str(j) + "/times_broken/" + str(part_times_broken[i][j])).status == 0)

    for i in range(len(ailment_buildup_start)):
        for j in range(len(ailment_buildup_start[i])):
            assert(get("/monster/" + str(i) + "/ailment/" + str(j) + "/current_buildup/" + str(ailment_buildup_start[i][j])).status == 0)

    while True:
        print("changing values")

        for i in range(len(part_hp)):
            for j in range(len(part_hp[i])):
                if part_hp[i][j] <= part_hp_modifier[i]:
                    part_hp[i][j] = int(part_hp_start[i][j] * 1.2)
                    assert (get("/monster/" + str(i) + "/part/" + str(j) + "/max_hp/" + str(part_hp[i][j])).status == 0)
                    assert (get("/monster/" + str(i) + "/part/" + str(j) + "/broken_count/" + str(part_hp[i][j])).status == 0)
                part_hp[i][j] -= part_hp_modifier[i]
                assert(get("/monster/" + str(i) + "/part/" + str(j) + "/current_hp/" + str(part_hp[i][j])).status == 0)

        for i in range(len(ailment_buildup)):
            for j in range(len(ailment_buildup[i])):
                ailment_buildup[i][j] += ailment_buildup_modifier[i]
                assert(get("/monster/" + str(i) + "/ailment/" + str(j) + "/current_buildup/" + str(ailment_buildup[i][j])).status == 0)

        counter += 1
        await asyncio.sleep(1)

try:
    cProfile.run("asyncio.run(main())", "test-host-stats")
    
except KeyboardInterrupt as e:
    pass
