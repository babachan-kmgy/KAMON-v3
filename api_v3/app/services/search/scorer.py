def score_exact_match(query: str, candidate: str):
    """
    完全一致スコア。完全一致なら高得点。
    """
    return 100 if query == candidate else 0

def score_prefix(query: str, candidate: str):
    """
    前方一致スコア。
    """
    return 50 if candidate.startswith(query) else 0

def score_length_penalty(query: str, candidate: str):
    """
    長さの差に応じたペナルティ。
    """
    return -abs(len(candidate) - len(query))

def total_score(query: str, candidate: str):
    """
    総合スコア。
    """
    return (
        score_exact_match(query, candidate)
        + score_prefix(query, candidate)
        + score_length_penalty(query, candidate)
    )
