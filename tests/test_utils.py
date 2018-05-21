from app.utils import shorten_url


def test_shorten_url():
    assert "ff90821f" == shorten_url("http://www.google.com/")
