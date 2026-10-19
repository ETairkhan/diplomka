def build_prompt(question, reference, answer):
    # The prompt has no personal data, only the question and the answers.
    return (
        "Question: " + question + "\n"
        "Reference answer: " + reference + "\n"
        "Student answer: " + answer + "\n"
        "Give a score from 0 to 10 and short feedback."
    )
