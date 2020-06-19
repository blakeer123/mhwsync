import urllib.request
import asyncio
import re


def get(url):
    response = urllib.request.urlopen(
        serverip + urllib.parse.quote(url)).read()
    response = re.search("'.*'", str(response)).group()
    response = response.strip("\'[]")
    return str(response)


serverip = "http://127.0.0.1:5000/"
session = "testsession::?%"
result = get("/session/" + session + "/create")


async def main():
    hpvalues = [[3680], [9348, 5168, 504], [7123, 31074]]

    for i in range(1):
        assert(get("/session/" + session + "/monster/0/parts/add") == "true")
        assert(get("/session/" + session + "/monster/0/part/" +
                   str(i) + "/hp/" + str(hpvalues[0][i])) == "true")
    for i in range(3):
        assert(get("/session/" + session + "/monster/1/parts/add") == "true")
        assert(get("/session/" + session + "/monster/1/part/" +
                   str(i) + "/hp/" + str(hpvalues[1][i])) == "true")
    for i in range(2):
        assert(get("/session/" + session + "/monster/2/parts/add") == "true")
        assert(get("/session/" + session + "/monster/2/part/" +
                   str(i) + "/hp/" + str(hpvalues[2][i])) == "true")

    print("parts created")

    while True:
        print("changing part hp values")
        value = 10
        for i in range(1):
            hpvalues[0][i] -= value
            value += 3
            assert(get("/session/" + session + "/monster/0/part/" +
                       str(i) + "/hp/" + str(hpvalues[0][i])) == "true")

        for i in range(3):
            hpvalues[1][i] -= value
            value += 2
            assert(get("/session/" + session + "/monster/1/part/" +
                       str(i) + "/hp/" + str(hpvalues[1][i])) == "true")

        for i in range(2):
            hpvalues[2][i] -= value
            value += 1
            assert(get("/session/" + session + "/monster/2/part/" +
                       str(i) + "/hp/" + str(hpvalues[2][i])) == "true")

        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
