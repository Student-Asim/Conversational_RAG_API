from typing import List
from core.utils import generate_embeddings
from core.vector_db import query_vectors
from core.llm import call_llm


def build_context_from_matches(matches: List[dict], max_chars_per_match: int = 400) -> str:
    parts = []
    for m in matches:
        meta = m.get("metadata", {})
        text = meta.get("text") or meta.get("snippet") or ""
        parts.append(text[:max_chars_per_match])
    return "\n\n---\n\n".join(parts)


def tensor_to_list(x):
    """
    Recursively converts PyTorch/TensorFlow tensors or nested lists into flat Python lists.
    """
    if hasattr(x, "detach"):       # PyTorch tensor
        return x.detach().cpu().tolist()
    elif hasattr(x, "numpy"):      # TensorFlow tensor
        return x.numpy().tolist()
    elif isinstance(x, list):
        return [tensor_to_list(e) for e in x]
    else:
        return float(x)            # scalar fallback


def rag_answer(query: str, memory_text: str = "", top_k: int = 5) -> str:
    # 1) embed query
    emb = generate_embeddings([query])[0]

    # 2) convert to safe list
    emb = tensor_to_list(emb)

    # 3) query vector DB
    matches = query_vectors(emb, top_k=top_k)

    # 4) assemble context
    context = build_context_from_matches(matches)

    # 5) craft prompt as messages (chat format)
    system_prompt = (
        "You are an assistant that answers user questions using the provided context. "
        "If the context doesn't contain the answer, say you don't know."
    )
    messages = [{"role": "system", "content": system_prompt}]
    if memory_text:
        messages.append({"role": "system", "content": f"Conversation memory:\n{memory_text}"})
    if context:
        messages.append({"role": "system", "content": f"Context:\n{context}"})
    messages.append({"role": "user", "content": query})

    # 6) call LLM
    reply = call_llm(messages)
    return reply
