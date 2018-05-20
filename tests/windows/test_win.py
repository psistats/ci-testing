from citest.w32.service import CitestService

def test_counter():

    s = CitestService()
    assert s.counter == 0

    s.counter()
    assert s.counter == 1

