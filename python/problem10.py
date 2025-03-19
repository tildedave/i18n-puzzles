import unicodedata
from typing import List
import bcrypt
from multiprocessing.pool import ThreadPool
from threading import Lock
from functools import partial

def all_forms(pw: str):
    pw = unicodedata.normalize('NFC', pw)
    prefixes = [(0, '')]
    forms = []

    while prefixes:
        l, prefix = prefixes.pop()
        if l == len(pw):
            forms.append(prefix)
            continue

        # otherwise grab the next character
        next_char = pw[l]
        # then all possiblities for this character
        decomposed_char = unicodedata.normalize('NFD', next_char)
        prefixes.append((l + 1, prefix + next_char))
        if decomposed_char != next_char:
            prefixes.append((l + 1, prefix + decomposed_char))

    return forms


def pw_attempt_is_valid(pw: str, salt: str):
    salt_bytes = salt.encode()
    for form in all_forms(pw):
        if bcrypt.checkpw(form.encode(), salt_bytes):
            return True

    return False


def test_example_input():
    salts = {
        "etasche": "$2b$07$0EBrxS4iHy/aHAhqbX/ao.n7305WlMoEpHd42aGKsG21wlktUQtNu",
        "mpataki": "$2b$07$bVWtf3J7xLm5KfxMLOFLiu8Mq64jVhBfsAwPf8/xx4oc5aGBIIHxO",
        "ssatterfield": "$2b$07$MhVCvV3kZFr/Fbr/WCzuFOy./qPTyTVXrba/2XErj4EP3gdihyrum",
        "mvanvliet": "$2b$07$gf8oQwMqunzdg3aRhktAAeU721ZWgGJ9ZkQToeVw.GbUlJ4rWNBnS",
        "vbakos": "$2b$07$UYLaM1I0Hy/aHAhqbX/ao.c.VkkUaUYiKdBJW5PMuYyn5DJvn5C.W",
        "ltowne": "$2b$07$4F7o9sxNeaPe..........l1ZfgXdJdYtpfyyUYXN/HQA1lhpuldO",
    }
    assert pw_attempt_is_valid(".pM?XÑ0i7ÈÌ", salts['etasche'])
    assert not pw_attempt_is_valid("2ö$p3ÄÌgÁüy", salts['mpataki'])
    assert not pw_attempt_is_valid("3+sÍkÜLg._", salts['ltowne'])
    assert pw_attempt_is_valid("3+sÍkÜLg?_", salts['ltowne'])


def answer(lines: List[str]):
    hashes = {}
    splitter = -1

    for i, line in enumerate(lines):
        if line.strip() == '' and splitter == -1:
            splitter = i
            continue

    hash_strs = lines[0:splitter]
    hashes = dict([line.split(' ') for line in hash_strs])
    login_attempts = lines[splitter+1:-1]

    lock = Lock()
    class IntegerRef:
        def __init__(self):
            self.value = 0

        def incr(self):
            self.value += 1


    def check_pw(intref: IntegerRef, line):
        user, pw = line.split(' ')
        if pw_attempt_is_valid(pw, hashes[user]):
            with lock:
                intref.incr()

    ref = IntegerRef()
    with ThreadPool(32) as p:
        p.imap_unordered(partial(check_pw, ref), login_attempts)
        p.close()
        p.join()

    print(ref.value)
