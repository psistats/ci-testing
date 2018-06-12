from citest.citest import adder

def test_ci():

    x = adder(1,2)
    assert x == 3


def test_ci_weird():
    x = addr(2,2)
    assert x == 4

