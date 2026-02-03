import os
import google.generativeai as genai
from typing import Dict
from dotenv import load_dotenv

load_dotenv()   

class ResumeRewriter:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        self.role_descriptions = {
            "Builders": "Focus on innovation, vision, and strategic growth. Highlight architectural decisions and pioneering new solutions.",
            "Enablers": "Focus on execution, bridging gaps, and cross-functional collaboration. Highlight stakeholder management and operational excellence.",
            "Thrivers": "Focus on adaptability, speed, and performing under pressure. Highlight resilience in dynamic environments and rapid problem-solving.",
            "Supportees": "Focus on reliability, consistency, and stability. Highlight maintenance, quality assurance, and robust infrastructure management."
        }

    """
    Generates a rewritten resume summary aligned to the dominant RoleColor.
    Includes fallback logic if the LLM call fails.
    """
    def rewrite_summary(self, original_text: str, dominant_role: str, scores: Dict[str, float]) -> str:
        
        prompt = f"""
        You are a Senior AI Career Coach. Rewrite the following resume summary to align with the '{dominant_role}' team role.
        
        Role Context: {self.role_descriptions[dominant_role]}
        
        Original Resume Text:
        {original_text[:2000]}  # Truncate to avoid token limits
        
        Requirements:
        - Length: 4-6 lines.
        - Tone: Professional, impactful, and senior-level.
        - Focus: Emphasize traits of a {dominant_role} while staying true to the candidate's experience.
        - Output: Only the rewritten summary, no conversational filler.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return self._generate_fallback_summary(dominant_role, scores)

    """Template-based fallback if LLM is unavailable."""
    def _generate_fallback_summary(self, role: str, scores: Dict[str, float]) -> str:
        templates = {
            "Builders": "Visionary leader with a proven track record of driving innovation and strategic growth. Expert at architecting scalable solutions and pioneering new product directions to transform business landscapes.",
            "Enablers": "Collaborative professional focused on bridging gaps between strategy and execution. Skilled at coordinating cross-functional teams and streamlining workflows to ensure consistent delivery.",
            "Thrivers": "Dynamic problem-solver who excels in high-pressure, fast-paced environments. Highly adaptable and resilient, with a focus on rapid iteration and turning challenges into growth opportunities.",
            "Supportees": "Reliable infrastructure specialist dedicated to ensuring system stability and operational excellence. Committed to high-quality standards, meticulous documentation, and robust maintenance."
        }
        return f"[FALLBACK SUMMARY] {templates[role]}"

if __name__ == "__main__":
    try:
        rewriter = ResumeRewriter()
        
        sample_text = """
        Experienced Project Manager with 10+ years of leading cross-functional teams. 
        Proven track record in delivering complex software projects on time and within budget.
        Skilled in Agile methodologies, stakeholder management, and risk mitigation.
        """
        
        dominant_role = "Builders"
        scores = {"Builders": 0.4, "Enablers": 0.3, "Thrivers": 0.2, "Supportees": 0.1}
        
        print(f"Original Text:\n{sample_text}")
        print("-" * 50)
        print(f"Rewriting for Dominant Role: {dominant_role}")
        
        new_summary = rewriter.rewrite_summary(sample_text, dominant_role, scores)
        
        print("-" * 50)
        print("Rewritten Summary:")
        print(new_summary)
        
    except Exception as e:
        print(f"Driver Error: {e}")
