# RoleColor Resume Rewriter

This project is a lightweight NLP prototype built for an AI Engineer take-home assignment. The goal is to analyze a resume's text, identify the dominant "RoleColor" (a team-role framework), and rewrite the resume summary to reflect the candidate's core strengths within that role.

## The RoleColor Framework

Recruiters often struggle to understand how a candidate fits into a team beyond their technical skills. The RoleColor framework addresses this by categorizing professional strengths into four distinct team roles:

- **Builders:** Drive innovation, vision, and long-term strategy. They are the architects and pioneers.
- **Enablers:** Connect people, execute plans, and bridge gaps. They are the collaborators and facilitators.
- **Thrivers:** Perform under pressure and adapt quickly to changing environments. They are resilient and agile problem-solvers.
- **Supportees:** Ensure reliability, consistency, and stability. They are the guardians of quality and process.

This prototype helps align a candidate's resume with these roles, making it easier for recruiters to see their potential team contribution.

## Approach and Implementation

my approach prioritizes clarity, robustness, and practical usefulness. The system is designed to handle real-world resume text and provide meaningful, actionable output.

### 1. RoleColor Keyword Framework

The foundation of the scoring system is a manually curated keyword framework. Based on industry knowledge and leadership principles, I developed a list of keywords and phrases that strongly correlate with each RoleColor. This mapping is designed to be extensible and is located in `src/framework.py`.

**Assumptions:**
- The keywords are representative of the language used in professional resumes.
- The presence of these keywords is a strong indicator of a candidate's alignment with a role.

### 2. Resume RoleColor Scoring

The scoring engine (`src/scorer.py`) processes the raw resume text and calculates a score for each RoleColor. The process is as follows:

1.  **Preprocessing:** The input text is cleaned by converting it to lowercase, removing special characters, and tokenizing it. This ensures that the scoring is not affected by formatting inconsistencies.
2.  **Scoring:** The engine counts the occurrences of each keyword from the framework. To prevent a single, frequently mentioned keyword from dominating the score, a logarithmic scaling `(1 + log1p(count))` is applied. This rewards resumes that demonstrate a breadth of skills within a role.
3.  **Normalization:** The raw scores are normalized into a probability distribution (summing to 1.0). This makes the output easy to interpret and compare.

**Edge Case Handling:**
- **Empty/Invalid Input:** The system gracefully handles empty strings or `None` inputs, returning a zero score for all roles.
- **No Keywords Found:** If no keywords are matched, the scorer returns a uniform distribution (0.25 for each role), indicating no clear alignment.

### 3. Resume Summary Rewrite

Once the dominant RoleColor is identified, the `ResumeRewriter` (`src/rewriter.py`) generates a new, 4-6 line summary. This leverages the Google Gemini API (`gemini-2.0-flash`) to produce a professional, impactful summary that aligns with the dominant role.

**Fallback Mechanism:** In the event of an API failure, a template-based fallback summary is generated. This ensures the system remains robust and always provides a useful result.

## How to Run

### Prerequisites
- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`.
- A Gemini API key set as an environment variable (`GEMINI_API_KEY`).

### Instructions

1.  Clone the repository.
2.  Place your resume text in a plain text file (e.g., `my_resume.txt`).
3.  Run the main script from the project's root directory:

```bash
cd Resumify-RoleColors
python main.py --input_data rolecolor_nlp/data/sample_resume.txt
```

The output will be a JSON object containing the score distribution and the rewritten summary, printed to the console.

## Sample Input & Output

### Input (`data/sample_resume.txt`)

```
John Doe
Senior Software Engineer

Experience:
- Led the architectural design of a new cloud-native platform, driving innovation across the engineering department.
- Developed a long-term technical roadmap and strategy for scaling our infrastructure by 10x.
- Pioneered the use of generative AI to automate internal workflows, resulting in a 30% increase in productivity.
- Acted as a technical founder for an internal incubator project, conceptualizing and launching 3 new products.

Skills:
System Architecture, Strategic Planning, Product Innovation, Cloud Computing, Python, Go, AWS.
```

### Output (`outputs/sample_output.json`)

```json
{
    "role_scores": {
        "Builders": 0.8786,
        "Enablers": 0.0,
        "Thrivers": 0.0,
        "Supportees": 0.1214
    },
    "dominant_role": "Builders",
    "rewritten_summary": "Visionary Senior Software Engineer with a proven track record of architecting scalable, cloud-native platforms that drive strategic growth. Expert in pioneering cutting-edge solutions, including generative AI automation, to transform workflows and accelerate productivity. Skilled at defining long-term technical roadmaps and launching innovative products as a technical founder within incubator environments. Adept at leading cross-functional teams to realize groundbreaking technology visions."
}
```
