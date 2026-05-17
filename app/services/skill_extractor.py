import json
import re
from pathlib import Path

SkillDictionary = dict[str, list[str]]
SkillMatches = dict[str, dict[str, int]]

DEFAULT_DICTIONARY_PATH = Path(__file__).with_name("skill_dictionary.json")


def load_skill_dictionary(path: Path = DEFAULT_DICTIONARY_PATH) -> SkillDictionary:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _count_skill(text: str, skill: str) -> int:
    pattern = re.compile(rf"(?<!\w){re.escape(skill.lower())}(?!\w)")
    return len(pattern.findall(text))


def extract_skills(
    text: str,
    skill_dictionary: SkillDictionary | None = None,
) -> SkillMatches:
    normalized_text = text.lower()
    dictionary = skill_dictionary or load_skill_dictionary()
    matches: SkillMatches = {}

    for category, skills in dictionary.items():
        category_matches: dict[str, int] = {}
        for skill in skills:
            frequency = _count_skill(normalized_text, skill)
            if frequency > 0:
                category_matches[skill] = frequency
        if category_matches:
            matches[category] = category_matches

    return matches
