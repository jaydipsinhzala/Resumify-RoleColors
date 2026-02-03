import re
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple
from .framework import ROLE_KEYWORDS

class RoleColorScorer:
    def __init__(self):
        self.framework = ROLE_KEYWORDS
        
    def preprocess_text(self, text: str) -> List[str]:
        """
        Clean and tokenize text. Handles edge cases like empty input, 
        special characters, and case sensitivity.
        """
        if not text or not isinstance(text, str):
            return []
        
        # Lowercase and remove non-alphanumeric characters except spaces
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', ' ', text)
        
        # Tokenize and remove empty strings
        tokens = [t.strip() for t in text.split() if t.strip()]
        return tokens

    def score_resume(self, text: str) -> Dict[str, float]:
        """
        Scores the resume across all four RoleColors using keyword presence.
        Uses a normalized frequency approach to handle varying resume lengths.
        Handles both single-word and multi-word keywords.
        """
        tokens = self.preprocess_text(text)
        if not tokens:
            return {role: 0.0 for role in self.framework.keys()}
        
        # Keep lowercased original text for multi-word keyword matching
        text_lower = text.lower() if text else ""
        counts = Counter(tokens)
        scores = {}
        
        for role, keywords in self.framework.items():
            # Calculate score based on keyword matches
            # We use a weighted approach: more unique keywords found is better than one keyword repeated
            role_score = 0
            for kw in keywords:
                if ' ' in kw:
                    # Multi-word keyword: search in original lowercased text
                    occurrences = text_lower.count(kw)
                    if occurrences > 0:
                        role_score += (1 + np.log1p(occurrences))
                elif kw in counts:
                    # Single-word keyword: use tokenized counts
                    # Logarithmic scaling to prevent a single keyword from dominating
                    role_score += (1 + np.log1p(counts[kw]))
            
            scores[role] = role_score

        # Normalize scores to sum to 1.0 (Probability distribution)
        total_score = sum(scores.values())
        if total_score == 0:
            # Uniform distribution if no keywords found
            return {role: 1.0/len(scores) for role in scores}
            
        normalized_scores = {role: round(score / total_score, 4) for role, score in scores.items()}
        return normalized_scores

    def get_dominant_role(self, scores: Dict[str, float]) -> str:
        """Returns the role with the highest score."""
        return max(scores, key=scores.get)

if __name__ == "__main__":
    print("Testing RoleColor Scorer...")
    scorer = RoleColorScorer()
    
    # Sample resume text with keywords from different roles
    sample_text = """
    Experienced Product Manager with a track record of innovation and strategic vision.
    Skilled in agile methodologies, cross-functional team leadership, and executing complex roadmaps.
    Thrives in fast-paced startup environments and adapts quickly to changing market conditions.
    Dedicated to process improvement, documentation, and ensuring reliability in all deliverables.
    """
    
    print(f"\nAnalyzing Sample Text:\n{sample_text.strip()}\n")
    
    scores = scorer.score_resume(sample_text)
    print("Scores:")
    for role, score in scores.items():
        print(f"  {role}: {score:.4f}")
        
    dominant_role = scorer.get_dominant_role(scores)
    print(f"\nDominant Role: {dominant_role}")

