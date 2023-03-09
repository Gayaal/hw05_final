import datetime as dt
from typing import Dict


def year(request: Dict[str, int]) -> Dict[str, int]:
    del request
    return {'year': dt.datetime.now().year}
