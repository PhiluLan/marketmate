import pytest
from unittest.mock import patch, MagicMock
from keywords.services.google_ads_service import fetch_keyword_ideas

@patch("keywords.services.google_ads_service._load_client")
def test_fetch_keyword_ideas(mock_load):
    # Fake Response-Objekt
    fake_metric = MagicMock(avg_monthly_searches=500,
                            competition=MagicMock(name="MEDIUM"),
                            low_top_of_page_bid_micros=2000000,
                            high_top_of_page_bid_micros=5000000)
    fake_idea = MagicMock(text="testkw",
                          keyword_idea_metrics=fake_metric)
    svc = MagicMock(generate_keyword_ideas=[fake_idea])
    client = MagicMock(get_service=MagicMock(return_value=svc))
    client.get_service.return_value.generate_keyword_ideas = lambda request: [fake_idea]
    mock_load.return_value = client

    results = fetch_keyword_ideas(["testkw"], "8157050680")
    assert results == [{
        "keyword": "testkw",
        "monthly_searches": 500,
        "competition": "MEDIUM",
        "low_cpc": 2.0,
        "high_cpc": 5.0
    }]
