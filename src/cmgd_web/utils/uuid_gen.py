#!/usr/bin/env python3
import uuid
from typing import List

BASE_UUID=uuid.UUID('00000000000000000000000000000000')

def uuid_from_string(string: str) -> uuid:
    res = uuid.uuid5(BASE_UUID,string)
    return res
