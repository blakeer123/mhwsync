import urllib.request
import asyncio
import re

def get(url):
    response = urllib.request.urlopen(serverip + urllib.parse.quote(url)).read()
    response = re.search("'.*'", str(response)).group()
    response = response.strip("\'[]")
    return str(response)

serverip = "http://127.0.0.1:5000/"
session = "testsession::?%"
result = get("/session/" + session + "/create")

async def main():
    parthpvalues = [[3680], [9348, 5168, 504], [7123, 31074]]
    partvalues = [30, 70, 110]
    ailmenthpvalues = [[0, 0], [0], [0, 0, 0]]
    ailmentvalues = [10, 15, 5]

    for i in range(len(parthpvalues)):
        for j in range(len(parthpvalues[i])):
            assert(get("/session/" + session + "/monster/" + str(i) + "/part/" + str(j) + "/create") == "true")
            assert(get("/session/" + session + "/monster/" + str(i) + "/part/" + str(j) + "/hp/" + str(parthpvalues[i][j])) == "true")

    print("parts created")

    for i in range(len(ailmenthpvalues)):
        for j in range(len(ailmenthpvalues[i])):
            assert(get("/session/" + session + "/monster/" + str(i) + "/ailment/" + str(j) + "/create") == "true")

    print("ailments created")

    while True:
        print("changing values")
        
        for i in range(len(parthpvalues)):
            for j in range(len(parthpvalues[i])):
                if parthpvalues[i][j] <= partvalues[i]:
                    parthpvalues[i][j] = 9999
                parthpvalues[i][j] -= partvalues[i]
                assert(get("/session/" + session + "/monster/" + str(i) + "/part/" + str(j) + "/hp/" + str(parthpvalues[i][j])) == "true")

        for i in range(len(ailmenthpvalues)):
            for j in range(len(ailmenthpvalues[i])):
                ailmenthpvalues[i][j] += ailmentvalues[i]
                assert(get("/session/" + session + "/monster/" + str(i) + "/ailment/" + str(j) + "/hp/" + str(ailmenthpvalues[i][j])) == "true")



        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    pass
