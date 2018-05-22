from citest.win_business import WinBusiness

def test_counter():

    b = WinBusiness()
    
    assert b.counter == 0

    b.run()
    assert b.counter == 2

