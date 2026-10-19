from ml.llm.anonymize import anonymize


def test_names_are_removed():
    text = "Aliya, solve the equation. Okay, Aliya."
    result = anonymize(text, ["Aliya"])
    assert "Aliya" not in result
    assert "Person1" in result
