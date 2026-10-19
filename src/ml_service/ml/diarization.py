def merge_speakers(words, segments):
    # Give every recognized word the speaker of the segment where the word starts.
    result = []
    for word in words:
        speaker = "unknown"
        for seg in segments:
            if seg["start"] <= word["start"] < seg["end"]:
                speaker = seg["speaker"]
                break
        result.append({"text": word["text"], "start": word["start"], "speaker": speaker})
    return result
