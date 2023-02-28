import datetime as dt


def year(request: int) -> int:
    del request
    return {'year': dt.datetime.now().year}
