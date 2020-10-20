import traceback
import sys
import requests


class Globals:
    server_url = "http://mhwsync-development.herokuapp.com"
    sessionid = ""
    buffer_size = 50

class Response:
    status: int
    value: str

    def __init__(self, status: int, value: str):
        self.status = status
        self.value = value

    def __str__(self) -> str:
        return "status: " + str(self.status) + "\nvalue: " + self.value
    

def get(url):
    r = requests.get(Globals.server_url + "/session/" + Globals.sessionid + url)
    r_json = r.json()
    response = Response(r_json["status"], r_json["value"])

    return response


def handle_error(optional=""):
    _, _, tb = sys.exc_info()
    traceback.print_tb(tb)
    tb_info = traceback.extract_tb(tb)
    _, line, _, text = tb_info[-1]

    print('An error occurred on line {} in statement {}'.format(line, text))
    if optional != "":
        print(optional)
    exit(1)

