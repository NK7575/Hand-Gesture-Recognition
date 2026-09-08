import emoji


GESTURES = {
    # ☝️ Index pointing up
    "(False, True, False, False, False, 1)": emoji.emojize(":index_pointing_up:"),

    # 👇 Index pointing down
    "(False, True, False, False, False, 0)": emoji.emojize(":backhand_index_pointing_down:"),

    # ✌️ Peace sign
    "(False, True, True, False, False, 1)": emoji.emojize(":victory_hand:"),

    # 🖕 Middle finger
    "(False, False, True, False, False, 1)": emoji.emojize(":middle_finger:"),

    # 🤘 Rock and roll
    "(False, True, False, False, True, 1)": emoji.emojize(":sign_of_the_horns:"),

    # 🖐️ Open hand
    "(True, True, True, True, True, 1)": emoji.emojize(":raised_hand:"),

    # 👌 OK sign
    "(False, False, True, True, True, 1)": emoji.emojize(":OK_hand:"),

    # 👍 Thumbs up
    "(True, False, False, False, False, 1)": emoji.emojize(":thumbs_up:"),

    # 👎 Thumbs down
    "(True, False, False, False, False, 0)": emoji.emojize(":thumbs_down:"),

    # ✊ Fist
    "(False, False, False, False, False, 1)": emoji.emojize(":raised_fist:"),

    # 🤟 I love you
    "(True, True, False, False, True, 1)": emoji.emojize(":love-you_gesture:"),

    # 🤙 Call me
    "(True, False, False, False, True, 1)": emoji.emojize(":call_me_hand:"),
}



def map_gesture(gesture):
    return GESTURES.get(gesture)