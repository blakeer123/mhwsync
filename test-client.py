import asyncio
import sys
import cProfile
import json
from prettytable import PrettyTable
from definitions import get, Globals, handle_error


if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    raise Exception("Python 3.8 or higher required")


async def fetch(url: str) -> int:
    return int(get(url).value)


async def main():
    print("initializing...")
    result = None
    current_hp = list()
    max_hp = list()
    times_broken = list()
    current_buildup = list()
    max_buildup = list()
    for i in range(3):
        current_hp.append(list())
        max_hp.append(list())
        times_broken.append(list())
        current_buildup.append(list())
        max_buildup.append(list())
        for _ in range (Globals.buffer_size):
            current_hp[i].append(0)
            max_hp[i].append(0)
            times_broken[i].append(0)
            current_buildup[i].append(0)
            max_buildup[i].append(0)


    # count_parts = 0
    # count_ailments = 0
    try:
        while True:
            # retrieve values
            print("retrieving values...")

            for i in range(3):
                for j in range(Globals.buffer_size):
                    result = get("/monster/" + str(i) + "/part/" + str(j) + "/")
                    assert(result.status == 0)
                    r = json.loads(result.value)
                    current_hp[i][j] = r["current_hp"]
                    max_hp[i][j] = r["max_hp"]
                    times_broken[i][j] = r["times_broken"]

                    result = get("/monster/" + str(i) + "/ailment/" + str(j) + "/")
                    assert(result.status == 0)
                    r = json.loads(result.value)
                    current_buildup[i][j] = r["current_buildup"]
                    max_buildup[i][j] = r["max_buildup"]

            # print values
            print("creating table...")
            x = PrettyTable()
            x.field_names = ["Monster", "current_hp 0", "max_hp 0", "broken 0", "current_hp 1", "max_hp 1", "broken 1", "current_hp 2", "max_hp 2", "broken 2", "buildup 0", "buildup_max 0", "buildup 1", "buildup_max 1", "buildup 2", "buildup_max 2"]
            for i in range(3):
                x.add_row([i, current_hp[i][0], max_hp[i][0], times_broken[i][0], current_hp[i][1], max_hp[i][1], times_broken[i][1], current_hp[i][2], max_hp[i][2], times_broken[i][2], current_buildup[i][0], max_buildup[i][0], current_buildup[i][1], max_buildup[i][1], current_buildup[i][2], max_buildup[i][2]])
            print(x)

            await asyncio.sleep(1)
            exit(0)
    except AssertionError:
        handle_error("result = " + str(result))


if __name__ == "__main__":  
    if len(sys.argv) == 2:
        Globals.sessionid = sys.argv[1]

    if len(sys.argv) == 3:
        Globals.server_url = sys.argv[1]
        Globals.sessionid = sys.argv[2]
        
    else:
        print("usage: test-client.py <optional: server> sessionid")
        exit(1)

    try:
        assert(get("/exists").status == 0)
        cProfile.run("asyncio.run(main())", "stats/test-client-stats")
    except KeyboardInterrupt:
        exit(0)
    except AssertionError:
        handle_error()
