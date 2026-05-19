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


def test_extract_skills_detects_expected_mvp_keywords():
    text = "Python SQL Git Linux Docker APIs REST PostgreSQL"

    result = extract_skills(text)

    assert result["languages"]["python"] == 1
    assert result["languages"]["sql"] == 1
    assert result["devops"]["git"] == 1
    assert result["devops"]["linux"] == 1
    assert result["devops"]["docker"] == 1
    assert result["backend"]["apis rest"] == 1
    assert result["databases"]["postgresql"] == 1
