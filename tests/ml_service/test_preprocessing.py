from ml.preprocessing import ffmpeg_command


def test_ffmpeg_makes_mono_16khz():
    cmd = ffmpeg_command("lesson.mp4", "lesson.wav")
    assert "-ac" in cmd and cmd[cmd.index("-ac") + 1] == "1"
    assert "-ar" in cmd and cmd[cmd.index("-ar") + 1] == "16000"
    assert "-vn" in cmd
