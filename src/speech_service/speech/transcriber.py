def clean_text(text):
    # Remove extra spaces from the recognized text.
    return " ".join(text.split())


def transcribe(audio_path, language="ru"):
    # TODO: connect the speech-to-text engine (see docs/comparisons).
    raise NotImplementedError("Speech-to-text engine is not connected yet")
