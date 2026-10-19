from speech.transcriber import clean_text


def test_clean_text_removes_extra_spaces():
    assert clean_text("  привет   мир ") == "привет мир"
