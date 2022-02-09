def topic(name):
    if not name or len(name) < 3 or len(name) > 100:
        return False
    return True

def chain(name):
    if not name or len(name) < 3 or len(name) > 100:
        return False
    return True

def msg(content):
    if not content or len(content) < 3 or len(content) > 5000:
        return False
    return True