#!/usr/bin/env python3.7

import random
import time
import sys
import os
import io


def busywork(timeout=1):
    sys.stdout = io.TextIOWrapper(
        open(sys.stdout.fileno(), 'wb', 0), write_through=True)
    tot = 0
    count = 0
    while tot < 2000:
        num = random.randrange(89) + 10
        tot += num
        count += 1
        print(f"num {num:02d} sum={tot:<8d} avg={tot / count:8.2f}")
        time.sleep(timeout)


if __name__ == "__main__":
    busywork()
