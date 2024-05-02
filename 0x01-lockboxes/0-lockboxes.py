#!/usr/bin/python3
""" Lockboxes contains methods that finds keys to open other lockboxes
"""


def canUnlockAll(boxes):
    unlocked = set()

    for obj, box in enumerate(boxes):
        if len(box) == 0 or obj == 0:
            unlocked.add(obj)
        for key in box:
            if key < len(boxes) and key != obj:
                unlocked.add(key)
        if len(unlocked) == len(boxes):
            return True
    return False
