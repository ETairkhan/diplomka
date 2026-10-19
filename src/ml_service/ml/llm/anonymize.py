def anonymize(text, names):
    # Replace real names with neutral labels before the text goes to an external LLM.
    for i, name in enumerate(names):
        text = text.replace(name, "Person" + str(i + 1))
    return text
