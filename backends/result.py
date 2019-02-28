
def general_message(code, msg, msg_show, bean={}, list=[], *args, **kwargs):
    result = {}
    data = dict()
    result["code"] = code
    result["msg"] = msg
    result["msg_show"] = msg_show
    data["bean"] = bean
    data["list"] = list
    data.update(kwargs)
    result["data"] = data
    return result


def error_message(en_msg=None):
    if not en_msg:
        return general_message(500, "system error", "系统异常")
    else:
        return general_message(500, en_msg, "系统异常")