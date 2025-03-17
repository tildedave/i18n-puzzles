if __name__ == "__main__":
    f = open("input3.txt", 'r')
    lines = f.read().split('\n')
    num = 0
    for line in lines[0:-1]:
        if len(line) < 4:
            print(f'{line} error.InvalidLength')
            continue
        if len(line) > 12:
            print(f'{line} error.InvalidLength')
            continue

        has_digit = False
        has_non_ascii = False
        has_lower = False
        has_upper = False
        for ch in line:
            str_ch = str(ch)
            if str_ch.isupper():
                has_upper = True
            if str_ch.islower():
                has_lower = True
            if not str_ch.isascii():
                has_non_ascii = True
            if str_ch.isdigit():
                has_digit = True

        if not has_digit:
            print(f'{line} error.NoDigit')
            continue

        if not has_non_ascii:
            print(f'{line} error.NoNonAscii')
            continue

        if not has_upper:
            print(f'{line} error.NoUpper')
            continue

        if not has_lower:
            print(f'{line} error.NoLower')
            continue

        if has_digit and has_non_ascii and has_lower and has_upper:
            print(f'{line} true')
            num += 1
    print(num)
