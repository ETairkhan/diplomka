from evaluator.prompts import build_prompt


def test_prompt_contains_all_parts():
    prompt = build_prompt("What is RAM?", "Memory", "It is memory")
    assert "What is RAM?" in prompt
    assert "Memory" in prompt
    assert "It is memory" in prompt
