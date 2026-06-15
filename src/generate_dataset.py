import pandas as pd
import numpy as np
import random
from faker import Faker
import json
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

# ── Job roles and departments ──────────────────────────────────────────────────
ROLES = {
    "Software Engineer": "Engineering",
    "Data Analyst": "Analytics",
    "Marketing Manager": "Marketing",
    "HR Business Partner": "Human Resources",
    "Financial Analyst": "Finance",
    "Product Manager": "Product",
    "Sales Executive": "Sales",
    "Operations Manager": "Operations",
    "UI/UX Designer": "Design",
    "DevOps Engineer": "Engineering",
}

# ── Good vs bad writing templates ─────────────────────────────────────────────
# High-performing JDs: clear, welcoming, benefit-focused
GOOD_INTROS = [
    "We are looking for a passionate {role} to join our growing team. You will have the opportunity to work on exciting projects that make a real difference.",
    "Join our collaborative team as a {role}. We value innovation, inclusion, and continuous learning.",
    "We're hiring a talented {role} who is eager to grow with us. You'll work alongside brilliant minds in a supportive environment.",
    "Are you a driven {role} ready to make an impact? We offer competitive pay, flexible hours, and meaningful work.",
]

# Low-performing JDs: demanding, jargon-heavy, unclear
BAD_INTROS = [
    "We require an experienced {role} to fulfill mandatory duties. Candidates must meet all stated requirements without exception.",
    "Seeking a results-driven {role} rockstar who can hit the ground running. Must be a self-starter with ninja-level skills.",
    "Immediate opening for {role}. Responsibilities include but are not limited to the execution of assigned tasks.",
    "We need an exceptional {role} who exceeds expectations. This is a high-pressure role requiring extreme dedication.",
]

GOOD_RESPONSIBILITIES = [
    "Collaborate with cross-functional teams to deliver high-quality solutions.",
    "Contribute to strategic planning and help shape the direction of our products.",
    "Mentor junior team members and share your knowledge openly.",
    "Analyze data to generate actionable insights and drive decision-making.",
    "Build and maintain strong relationships with stakeholders across the organization.",
    "Lead projects from conception to delivery, ensuring timelines are met.",
    "Participate in regular team meetings and contribute your ideas.",
    "Create and present clear reports to management and stakeholders.",
]

BAD_RESPONSIBILITIES = [
    "Must execute all assigned duties in a timely and efficient manner.",
    "Required to perform miscellaneous tasks as directed by management.",
    "Responsible for end-to-end ownership of all deliverables without exception.",
    "Must demonstrate proficiency across all required competencies.",
    "Execute strategies in accordance with organizational directives.",
    "Perform analysis, reporting, and other duties as assigned.",
    "Interface with stakeholders to ensure requirements are communicated effectively.",
    "Must be available for ad-hoc tasks at all times during business hours.",
]

GOOD_REQUIREMENTS = [
    "3+ years of relevant experience (we value quality over quantity).",
    "Strong communication skills and a collaborative mindset.",
    "Degree in a relevant field or equivalent practical experience.",
    "Familiarity with modern tools in your domain — we'll help you grow.",
    "Passion for the work and a willingness to learn new things.",
    "Problem-solving ability and attention to detail.",
]

BAD_REQUIREMENTS = [
    "Must have 7+ years of experience in an identical role.",
    "Required: proficiency in every tool listed above without exception.",
    "Candidates must possess superior analytical capabilities.",
    "Must be available 24/7 including weekends when needed.",
    "Demonstrated excellence in all core competencies is mandatory.",
    "Must be a perfectionist with an obsessive attention to detail.",
    "Only candidates with Ivy League degrees will be considered.",
]

GOOD_BENEFITS = [
    "Competitive salary and annual performance bonus.",
    "Flexible working hours and remote-friendly culture.",
    "Comprehensive health, dental, and vision insurance.",
    "25 days paid leave plus public holidays.",
    "Annual learning and development budget.",
    "Monthly team events and a friendly, inclusive culture.",
]

BAD_BENEFITS = [
    "Salary commensurate with experience.",
    "Standard benefits package.",
    "Compensation will be discussed during the interview process.",
]


def build_jd(role, quality="high"):
    """
    Build a job description string.
    quality = 'high' uses good templates, 'low' uses bad templates.
    Mixed uses a combination.
    """
    intro_pool    = GOOD_INTROS         if quality == "high" else BAD_INTROS
    resp_pool     = GOOD_RESPONSIBILITIES if quality == "high" else BAD_RESPONSIBILITIES
    req_pool      = GOOD_REQUIREMENTS   if quality == "high" else BAD_REQUIREMENTS
    benefit_pool  = GOOD_BENEFITS       if quality == "high" else BAD_BENEFITS

    intro = random.choice(intro_pool).format(role=role)

    n_resp = random.randint(4, 6)
    responsibilities = random.sample(resp_pool, min(n_resp, len(resp_pool)))

    n_req = random.randint(3, 5)
    requirements = random.sample(req_pool, min(n_req, len(req_pool)))

    n_ben = random.randint(3, 5)
    benefits = random.sample(benefit_pool, min(n_ben, len(benefit_pool)))

    resp_text = "\n".join(f"- {r}" for r in responsibilities)
    req_text  = "\n".join(f"- {r}" for r in requirements)
    ben_text  = "\n".join(f"- {b}" for b in benefits)

    jd = f"""{intro}

Responsibilities:
{resp_text}

Requirements:
{req_text}

What We Offer:
{ben_text}"""

    return jd.strip()


def simulate_applications(quality, jd_text):
    """
    Simulate application count based on quality.
    High quality JDs get more applications, with some noise.
    """
    base = {"high": 120, "medium": 65, "low": 25}[quality]
    
    # Bonus for mentioning benefits
    benefit_bonus = 15 if "offer" in jd_text.lower() else 0
    
    # Bonus for clear, inclusive language
    inclusive_bonus = 10 if any(w in jd_text.lower() for w in ["inclusive", "collaborative", "support", "grow", "flexible"]) else 0
    
    # Penalty for demanding language
    demand_penalty = -15 if any(w in jd_text.lower() for w in ["rockstar", "ninja", "mandatory", "must", "required", "24/7"]) else 0
    
    noise = random.randint(-20, 20)
    
    apps = base + benefit_bonus + inclusive_bonus + demand_penalty + noise
    return max(5, apps)  # at least 5 applications


def generate_dataset(n=200):
    records = []
    role_list = list(ROLES.keys())
    qualities = ["high", "high", "medium", "medium", "low"]  # more high than low

    for i in range(n):
        role = random.choice(role_list)
        dept = ROLES[role]
        quality = random.choice(qualities)

        # Mixed quality: take intro from one, rest from another
        if quality == "medium":
            jd = build_jd(role, quality="high") if random.random() > 0.5 else build_jd(role, quality="low")
        else:
            jd = build_jd(role, quality=quality)

        apps = simulate_applications(quality, jd)
        word_count = len(jd.split())

        records.append({
            "jd_id":            f"JD_{i+1:03d}",
            "job_title":        role,
            "department":       dept,
            "quality_label":    quality,       # ground truth for validation
            "job_description":  jd,
            "word_count":       word_count,
            "applications":     apps,
        })

    df = pd.DataFrame(records)
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/job_descriptions.csv", index=False)
    print(f"✅ Dataset generated: {len(df)} job descriptions saved to data/job_descriptions.csv")
    print(f"\nQuality distribution:\n{df['quality_label'].value_counts()}")
    print(f"\nApplication stats:\n{df['applications'].describe().round(1)}")
    return df


if __name__ == "__main__":
    df = generate_dataset(200)
    print("\nSample JD (first row):")
    print("-" * 60)
    print(df.iloc[0]['job_description'])