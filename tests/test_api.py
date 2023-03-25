import requests as r

TIME_REQUEST = {
    "meta": {
        "locale": "ru-RU",
        "timezone": "Europe/Moscow",
        "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
        "interfaces": {"screen": {}, "account_linking": {}, "audio_player": {}},
    },
    "request": {
        "command": "Во сколько мне надо лечь, чтобы встать в 7:00",
        "type": "SimpleUtterance",
        "nlu": {
            "intents": {
                "sleep_calc": {
                    "slots": {
                        "time": {
                            "type": "YANDEX.DATETIME",
                            "value": {"hour": 7, "minute": 0},
                        }
                    }
                }
            }
        },
    },
    "session": {
        "message_id": 0,
        "session_id": "2eac4854-fce721f3-b845abba-20d60",
        "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
        "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
        "user": {
            "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
            "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT",
        },
        "application": {
            "application_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"
        },
        "new": True,
    },
    "state": {
        "session": {"value": 10},
        "user": {"value": 42},
        "application": {"value": 37},
    },
    "version": "1.0",
}


def makeRequest(command: str) -> dict:
    return {
        "meta": {
            "locale": "ru-RU",
            "timezone": "Europe/Moscow",
            "client_id": "ru.yandex.searchplugin/5.80 (Samsung Galaxy; Android 4.4)",
            "interfaces": {"screen": {}, "account_linking": {}},
        },
        "request": {
            "command": command,
            "original_utterance": command,
            "type": "SimpleUtterance",
            "markup": {"dangerous_context": True},
            "payload": {},
        },
        "session": {
            "message_id": 0,
            "session_id": "2eac4854-fce721f3-b845abba-20d60",
            "skill_id": "3ad36498-f5rd-4079-a14b-788652932056",
            "user_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8",
            "user": {
                "user_id": "6C91DA5198D1758C6A9F63A7C5CDDF09359F683B13A18A151FBF4C8B092BB0C2",
                "access_token": "AgAAAAAB4vpbAAApoR1oaCd5yR6eiXSHqOGT8dT",
            },
            "application": {
                "application_id": "47C73714B580ED2469056E71081159529FFC676A4E5B059D629A819E857DC2F8"
            },
            "new": True,
        },
        "version": "1.0",
    }


def sendRequest(req: dict) -> str:
    resp = r.post("http://localhost:5555/", json=req)
    return resp.json()["response"]["text"]


def test_start():
    req = makeRequest("Привет")
    print(sendRequest(req))


def test_time():
    print(sendRequest(TIME_REQUEST))


def test_mode():
    req = makeRequest("Длинный")
    print(sendRequest(req))


def test_sleep():
    req = makeRequest("Я хочу спать")
    print(sendRequest(req))
