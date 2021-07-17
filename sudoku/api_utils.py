import json

import requests


def patch_request(path, data: dict = None, headers: dict = None) -> requests.Response:
    if headers is None:
        headers = {
            "content-type": "application/json"
        }

    if data is None:
        data = {}

    return requests.patch(path, data=json.dumps(data), headers=headers)


def error_chk(res: dict) -> bool:
    if "status" not in res.keys():
        return True

    if res["status"] != "ok":
        return True

    return False
