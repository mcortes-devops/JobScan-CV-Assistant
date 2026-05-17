from collections import Counter

from app.models import JobOffer
from app.services.skill_extractor import SkillMatches, extract_skills


def calculate_skill_statistics(offers: list[JobOffer]) -> SkillMatches:
    counters: dict[str, Counter[str]] = {}

    for offer in offers:
        matches = extract_skills(offer.raw_description)
        for category, skills in matches.items():
            counters.setdefault(category, Counter()).update(skills)

    return {
        category: dict(counter.most_common())
        for category, counter in sorted(counters.items())
    }
