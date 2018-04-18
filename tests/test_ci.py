from citest.citest import adder

def test_ci():

    x = adder(1,2)
    assert x == 3

