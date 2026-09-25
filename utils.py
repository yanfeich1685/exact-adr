def rho_decimal(m, k):
    if k <= m / 2:
        return k * (m - 1) / (k * k - 2 * k + m)
    else:
        return m * (m - 1) / (k * m - 2 * k + m)


def rho_frac(m, k):
    if k <= m / 2:
        return k * (m - 1), k * k - 2 * k + m
    else:
        return m * (m - 1), k * m - 2 * k + m


def bb_decimal(m, k):
    return (k + m) / (k + m / k)


def tws_decimal(m, k):
    return k * (m - 1) / (k * k - 2 * k + m)


def beg_decimal(m, k):
    return 2 * min(k, m / k)
