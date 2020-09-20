#!/usr/bin/env python3
from collections import namedtuple

Pagination = namedtuple("Page", ['page', 'pagesize'])

async def pagination(page: int = 1, pagesize: int = 100):
    return Pagination(page, pagesize)
