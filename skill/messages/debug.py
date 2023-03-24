import datetime
from skill.utils import TextWithTTS


def messages_showcase(messages_class):
    msg = messages_class()

    class QuaziTip:
        tip_content = TextWithTTS(
            "ложитесь спать в полдень, это помогает пищеварению",
            "лажитесь спать в п+олдень - это помогает пищеварению",
        )

    class QuaziAct:
        description = TextWithTTS("выкинуть мусор", "в+ыкинуть м+усор")

    print(msg.get_start_message_intro(datetime.datetime.now()))
    print()
    print(msg.get_start_message_comeback(datetime.datetime.now(), 42, 26))
    print()
    print(msg.get_menu_welcome_message())
    print()
    print(msg.get_info_message())
    print()
    print(msg.get_ask_tip_topic_message())
    print()
    print(
        msg.get_propose_yesterday_wake_up_time_message(
            datetime.datetime.now().time()
        )
    )
    print()
    print(msg.get_ask_wake_up_time_message())
    print()
    print(msg.get_ask_sleep_mode_message())
    print()
    print(msg.get_tip_message(QuaziTip()))
    print()
    print(
        msg.get_sleep_calc_time_message(
            datetime.datetime.now().time(), [QuaziAct()] * 4
        )
    )
    print()
    print(msg.get_good_night_message())
