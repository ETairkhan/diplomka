def ffmpeg_command(src, dst):
    # Extract audio, convert to mono 16 kHz and normalize loudness (FR-5).
    return [
        "ffmpeg", "-y", "-i", src,
        "-vn", "-ac", "1", "-ar", "16000",
        "-af", "loudnorm",
        dst,
    ]
