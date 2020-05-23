def function(x, eps):
    assert abs(x) < 1
    assert eps > 0

    a = 1
    s = a
    i = 1
    while abs(a) > eps:
        a *= - x
        s += a
        i += 1
    return s