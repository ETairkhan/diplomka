from ml.diarization import merge_speakers


def test_words_get_speaker_labels():
    words = [{"text": "hello", "start": 0.5}, {"text": "hi", "start": 3.0}]
    segments = [
        {"speaker": "teacher", "start": 0.0, "end": 2.0},
        {"speaker": "student", "start": 2.0, "end": 5.0},
    ]
    result = merge_speakers(words, segments)
    assert result[0]["speaker"] == "teacher"
    assert result[1]["speaker"] == "student"
