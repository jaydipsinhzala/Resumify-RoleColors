import sys
import json
from src.scorer import RoleColorScorer
from src.rewriter import ResumeRewriter

def run_pipeline(resume_text: str):
    if not resume_text.strip():
        print("Error: Empty resume text provided.")
        return

    # 1. Scoring
    scorer = RoleColorScorer()
    scores = scorer.score_resume(resume_text)
    dominant_role = scorer.get_dominant_role(scores)

    # 2. Rewriting
    rewriter = ResumeRewriter()
    summary = rewriter.rewrite_summary(resume_text, dominant_role, scores)

    # 3. Output
    result = {
        "role_scores": scores,
        "dominant_role": dominant_role,
        "rewritten_summary": summary
    }
    
    return result


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="RoleColor NLP Pipeline")
    parser.add_argument("--input_data", help="Path to resume file or raw text string", default=None)
    args = parser.parse_args()

    text = ""
    if args.input_data:
        # Check if it's a file
        if os.path.isfile(args.input_data):
            try:
                with open(args.input_data, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                sys.exit(1)
        else:
            print(f"Error: File not found at {args.input_data}")
            sys.exit(1)
    else:
        # Check if standard input is being piped
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
             # Default sample for quick run / testing
            text = "I am a software engineer who loves building new things, innovating on strategy, and architecting systems."

    if not text.strip():
        print("Error: No input text provided. Use --input_data or pipe text to stdin.")
        sys.exit(1)

    output = run_pipeline(text)
    print(json.dumps(output, indent=4))
