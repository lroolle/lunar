from .const import LMD, S11


def get_bit_int(data, length, shift):
    return (data & (((1 << length) - 1) << shift)) >> shift


def solar_from_int(g):
    y = (10000 * g + 14780) // 3652425
    ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
    if ddd < 0:
        y -= 1
        ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
    mi = (100 * ddd + 52) // 3060
    mm = (mi + 2) % 12 + 1
    y += (mi + 2) // 12
    dd = ddd - (mi * 306 + 5) // 10 + 1
    return y, mm, dd


def solar_to_int(y, m, d):
    m = (m + 9) % 12
    y -= m // 10
    return 365 * y + y // 4 - y // 100 + y // 400 + (m * 306 + 5) // 10 + (d - 1)


def is_leap_month(days, m):
    leap = get_bit_int(days, 4, 13)
    return leap != 0 and m > leap and m == leap + 1


def lunar_to_solar(y, m, d, isleap=False):
    days = LMD[y - LMD[0]]
    leap = get_bit_int(days, 4, 13)
    offset = 0
    loopend = leap
    if not isleap:
        if m <= leap or leap == 0:
            loopend = m - 1
        else:
            loopend = m

    for i in range(0, loopend):
        offset += get_bit_int(days, 1, 12 - i) == 1 and 30 or 29

    offset += d
    solar11 = S11[y - S11[0]]

    _y = get_bit_int(solar11, 12, 9)
    _m = get_bit_int(solar11, 4, 5)
    _d = get_bit_int(solar11, 5, 0)
    return solar_from_int(solar_to_int(_y, _m, _d) + offset - 1)


def solar_to_lunar(y, m, d):
    _y, _m, _d, isleap = 0, 0, 0, False
    index = y - S11[0]
    data = (y << 9) | (m << 5) | d
    if S11[index] > data:
        index -= 1

    solar11 = S11[index]
    _y = get_bit_int(solar11, 12, 9)
    _m = get_bit_int(solar11, 4, 5)
    _d = get_bit_int(solar11, 5, 0)
    offset = solar_to_int(y, m, d) - solar_to_int(_y, _m, _d)

    days = LMD[index]
    _y, _m = index + S11[0], 1
    offset += 1

    for i in range(0, 13):
        dm = get_bit_int(days, 1, 12 - i) == 1 and 30 or 29
        if offset > dm:
            _m += 1
            offset -= dm
        else:
            break
    _d = int(offset)

    if is_leap_month(days, _m):
        _m -= 1
        isleap = True

    return _y, _m, _d, isleap
