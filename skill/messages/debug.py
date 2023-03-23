import datetime


def messages_showcase(messages_class):
    msg = messages_class()

    class QuaziTip:
        text = "ложитесь спать в полдень, это помогает пищеварению"
        tts = "лажитесь спать в п+олдень - это помогает пищеварению"

    class QuaziAct:
        description = "выкинуть мусор"
        tts = "в+ыкинуть м+усор"

    def prtwtts(twtts):
        print(f"Text: {twtts.text}")
        print(f"TTS: {twtts.tts}")
        print()

    prtwtts(msg.get_start_message_intro(datetime.datetime.now()))
    prtwtts(msg.get_start_message_comeback(datetime.datetime.now(), 42, 26))
    prtwtts(msg.get_menu_welcome_message())
    prtwtts(msg.get_info_message())
    prtwtts(msg.get_ask_tip_topic_message())
    prtwtts(
        msg.get_propose_yesterday_wake_up_time_message(
            datetime.datetime.now().time()
            )
    )
    prtwtts(msg.get_ask_wake_up_time_message())
    prtwtts(msg.get_ask_sleep_mode_message())
    prtwtts(msg.get_tip_message(QuaziTip()))
    prtwtts(
        msg.get_sleep_calc_time_message(
            datetime.datetime.now().time(),
            [QuaziAct()] * 4
        )
    )
    prtwtts(msg.get_good_night_message())
