"""
RoleColor Keyword Framework
--> keyword mapping for the four team roles:
    - Builders: Innovation, vision, strategy
    - Enablers: Connection, execution, bridging gaps
    - Thrivers: Pressure, adaptation, speed
    - Supportees: Reliability, consistency, stability
"""

ROLE_KEYWORDS = {
    "Builders": [
        "innovation", "vision", "strategy", "architect", "design", "pioneer", 
        "conceptualize", "roadmap", "disrupt", "growth", "scaling", "founder",
        "product-led", "transform", "ideation", "strategic", "future-proof",
        "breakthrough", "invent", "optimize", "leverage", "paradigm"
    ],
    "Enablers": [
        "connect", "execute", "bridge", "collaborate", "facilitate", "coordinate",
        "stakeholder", "cross-functional", "alignment", "partnership", "workflow",
        "delivery", "operationalize", "synergy", "communication", "liaison",
        "integration", "streamline", "agile", "scrum", "project management"
    ],
    "Thrivers": [
        "pressure", "adapt", "fast-paced", "dynamic", "resilient", "agile",
        "pivot", "turnaround", "high-growth", "startup", "emergency", "deadline",
        "rapid", "iterative", "problem-solving", "grit", "tenacity", "flexible",
        "unstructured", "chaos", "scale-up", "high-stakes"
    ],
    "Supportees": [
        "reliability", "consistency", "stability", "maintenance", "quality assurance",
        "documentation", "standardization", "process", "compliance", "support",
        "infrastructure", "security", "governance", "accuracy", "detail-oriented",
        "best practices", "robust", "scalable", "monitoring", "operations"
    ]
}

def get_role_colors():
    return list(ROLE_KEYWORDS.keys())

if __name__ == "__main__":
    print("Testing RoleColor Framework...")
    roles = get_role_colors()
    print(f"Available Roles: {roles}")
    
    total_keywords = 0
    for role, keywords in ROLE_KEYWORDS.items():
        count = len(keywords)
        total_keywords += count
        print(f"\nRole: {role}")
        print(f"  Keyword Count: {count}")
        print(f"  Sample Keywords: {', '.join(keywords[:5])}...")
    
    print(f"\nTotal Keywords across all roles: {total_keywords}")
