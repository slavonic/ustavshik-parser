from ustav import tidyup

def test():
    html = tidyup('<body> Hello<span> red </span>!')

    assert html == '<body> Hello <span>red</span> !'


def test_class():
    html = tidyup('<body> Hello<span class="u"> red </span>!')

    assert html == '<body> Hello <span class="u">red</span> !'