#!/usr/bin/env python3
import re
"""
Log message obfuscated to protect personal data
"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    pattern = r'({})=[^{}]*'.format('|'.join(map(re.escape, fields)),
                                    re.escape(separator))
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
