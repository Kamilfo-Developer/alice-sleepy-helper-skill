import requests as r

from skill.states import States

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


def make_request(command: str) -> dict:
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


def make_test(req: dict | str, target_state: str):
    if type(req) == str:
        req = make_request(req)
    resp = r.post("http://localhost:5555/", json=req)
    resp = resp.json()
    print(resp)
    assert resp["application_state"] == target_state.lower()


def test_handler_main_func_short():
    make_test("Привет", str(States.MAIN_MENU))

    make_test(TIME_REQUEST, str(States.IN_CALCULATOR))

    make_test("Долгий", str(States.CALCULATED))

    make_test("Да", str(States.MAIN_MENU))

    # make_test("Ночной сон", str(States.MAIN_MENU))


def test_handler_main_func_long():

    make_test("Я хочу спать", str(States.TIME_PROPOSED))

    make_test("Да", str(States.IN_CALCULATOR))

    make_test("Короткий", str(States.CALCULATED))

    make_test("Меню", str(States.MAIN_MENU))


def test_handler_ask_tip():

    make_test("Посоветуй", str(States.ASKING_FOR_TIP))

    make_test("Ночной сон", str(States.MAIN_MENU))


def test_handler_info():
    make_test("Расскажи о навыке", str(States.MAIN_MENU))
