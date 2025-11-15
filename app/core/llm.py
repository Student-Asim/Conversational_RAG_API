from transformers import pipeline

# Load text generation pipeline
generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

def call_llm(messages, max_tokens: int = 200, temperature: float = 0.7) -> str:
    """
    Generate text safely even for long prompts.
    messages: list of dicts with 'role' and 'content'.
    """
    # Combine messages into a single prompt
    prompt = "\n".join([m["content"] for m in messages])

    # Get model max length
    max_model_len = generator.model.config.n_positions  # tiny-gpt2: 128

    # Tokenize prompt to check length
    tokens = generator.tokenizer.encode(prompt, add_special_tokens=False)

    # Truncate if too long
    if len(tokens) > max_model_len:
        tokens = tokens[-max_model_len:]  # keep last tokens only
        prompt = generator.tokenizer.decode(tokens)

    # Generate text
    result = generator(
        prompt,
        max_new_tokens=max_tokens,
        temperature=temperature,
        do_sample=True,
        pad_token_id=generator.tokenizer.eos_token_id
    )

    return result[0]["generated_text"].strip()
