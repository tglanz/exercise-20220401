import example

def test_false():
    assert 1 != 1

def test_true():
    assert example.loopback(1) == 1