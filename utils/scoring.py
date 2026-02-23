def schematic_sort(candidates, semantic_scores):
    """
    Logic: 
    - Toppers: High semantic match AND high quiz score.
    - Near Misses: Low semantic match BUT high quiz score.
    """
    toppers = []
    near_misses = []

    for cand, semantic_score in zip(candidates, semantic_scores):
        if semantic_score >= 0.8 and cand.quiz_score >= 0.8:
            toppers.append(cand)
        elif semantic_score < 0.8 and cand.quiz_score >= 0.9:
            # The 'Second Chance' logic: Proved they have the skill despite the resume
            near_misses.append(cand)
            
    return toppers, near_misses