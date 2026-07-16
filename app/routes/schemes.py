from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_schemes() -> Any:
    return [
        {
            "id": "scheme_1",
            "name": "PM-KISAN",
            "category": "Subsidy",
            "eligibility": "Small and marginal farmers",
            "description": "Income support for agricultural households",
            "benefits": ["Direct cash transfer"],
            "link": "https://pmkisan.gov.in",
            "crops": ["Wheat", "Rice"],
        },
        {
            "id": "scheme_2",
            "name": "Fasal Bima Yojana",
            "category": "Insurance",
            "eligibility": "Registered farmers",
            "description": "Crop insurance against yield loss",
            "benefits": ["Premium subsidy", "Compensation"],
            "link": "https://pmfby.gov.in",
            "crops": ["Tomato", "Potato", "Onion"],
        },
    ]
