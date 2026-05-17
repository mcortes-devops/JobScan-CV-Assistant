from app.services.skill_extractor import extract_skills


def test_extract_skills_returns_categories_and_frequency():
    dictionary = {
        "languages": ["python", "javascript"],
        "backend": ["fastapi"],
        "soft_skills": ["communication"],
    }
    text = "Python developer with FastAPI. Python and communication required."

    result = extract_skills(text, dictionary)

    assert result == {
        "languages": {"python": 2},
        "backend": {"fastapi": 1},
        "soft_skills": {"communication": 1},
    }


def test_extract_skills_ignores_missing_skills():
    result = extract_skills("No relevant keywords here.", {"languages": ["python"]})

    assert result == {}
