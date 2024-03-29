
def success(data=None):
    ret = {
        "code": "0",
        "msg": "success",
        "data": data
    }
    return ret


def error(msg, code=None, data=None):
    ret = {
        "code": code,
        "msg": msg,
        "data": data
    }
    return ret


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print("############START###########")
