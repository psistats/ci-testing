from citest.business import Business

def test_simple_counter():
    b = Business()

    assert b.counter == 0

    b.run()

    assert b.counter == 1
