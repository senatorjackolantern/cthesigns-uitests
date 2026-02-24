import requests

def test_assess_pt101_returns_assessment(http, api_base_url):
    url = f"{api_base_url}/assess/PT-101"

    # Your captured request had Content-Length: 0 (no body)
    r = http.post(url, timeout=30)

    assert r.status_code == 200, f"Expected 200, got {r.status_code}. Body: {r.text[:500]}"
    assert "application/json" in (r.headers.get("Content-Type") or ""), r.headers.get("Content-Type")

    data = r.json()

    # Patient
    assert "patient" in data and isinstance(data["patient"], dict)
    assert data["patient"].get("patient_id") == "PT-101"
    assert isinstance(data["patient"].get("symptoms"), list)

    # Assessment
    assert "assessment" in data and isinstance(data["assessment"], dict)
    assessment = data["assessment"]
    assert isinstance(assessment.get("risk_level"), str) and assessment["risk_level"].strip()
    assert isinstance(assessment.get("cancer_type"), str) and assessment["cancer_type"].strip()
    assert isinstance(assessment.get("recommended_action"), str) and assessment["recommended_action"].strip()
    assert isinstance(assessment.get("matched_recommendations"), list)

    # Citations
    assert "citations" in data and isinstance(data["citations"], list)
    # If citations should always exist for assessments, assert non-empty:
    assert len(data["citations"]) > 0

    first_cite = data["citations"][0]
    assert isinstance(first_cite, dict)
    assert "source" in first_cite
    assert "page" in first_cite


def test_assess_unknown_patient_is_not_500(http, api_base_url):
    url = f"{api_base_url}/assess/DOES-NOT-EXIST"
    r = http.post(url, timeout=30)

    assert r.status_code in (400, 404), f"Expected 400/404, got {r.status_code}. Body: {r.text[:500]}"