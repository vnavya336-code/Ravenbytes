
import os
import requests

NSP_URL = "https://scholarships.gov.in/Students"
NSP_SCHEMES_URL = "https://scholarships.gov.in/All-Scholarships"
SSP_URL = "https://ssp.postmatric.karnataka.gov.in/"

SCHEMES = [

    {
        "name": "Karnataka SSP Scholarship Portal",
        "description": "Karnataka State Scholarship Portal for eligible students. Individual schemes have different eligibility conditions.",
        "education": "10th, 12th and UG",
        "deadline": None,
        "application_url": None,
        "info_url": SSP_URL,
        "url": SSP_URL,
        "source": "Karnataka State Scholarship Portal",
        "rules": {
            "state": "Karnataka",
            "education": [
                "10th passed",
                "12th passed",
                "Engineering UG"
            ]
        }
    },

    {
        "name": "National Scholarship Portal (NSP)",
        "description": "Government portal containing multiple central and state scholarship schemes.",
        "education": "10th, 12th and UG",
        "deadline": None,
        "application_url": NSP_URL,
        "info_url": NSP_SCHEMES_URL,
        "url": NSP_URL,
        "source": "Government of India - NSP",
        "rules": {
            "education": [
                "10th passed",
                "12th passed",
                "Engineering UG"
            ]
        }
    },

    {
        "name": "AICTE Pragati Scholarship",
        "description": "Scholarship for eligible girl students admitted to approved technical degree programmes.",
        "education": "Engineering UG",
        "deadline": "30-11-2026 (2026-27, verify current scheme notice)",
        "application_url": NSP_URL,
        "info_url": NSP_SCHEMES_URL,
        "url": NSP_URL,
        "source": "AICTE / National Scholarship Portal",
        "rules": {
            "education": ["Engineering UG"],
            "gender": "Female"
        }
    },

    {
        "name": "AICTE Saksham Scholarship",
        "description": "Scholarship for eligible specially-abled students pursuing approved technical degree programmes.",
        "education": "Engineering UG",
        "deadline": "30-11-2026 (2026-27, verify current scheme notice)",
        "application_url": NSP_URL,
        "info_url": NSP_SCHEMES_URL,
        "url": NSP_URL,
        "source": "AICTE / National Scholarship Portal",
        "rules": {
            "education": ["Engineering UG"],
            "disability": "Yes"
        }
    },

    {
        "name": "PM-USP Central Sector Scholarship",
        "description": "Merit-based central scholarship for eligible students who have completed Class 12 and meet the applicable conditions.",
        "education": "12th passed / UG",
        "deadline": None,
        "application_url": NSP_URL,
        "info_url": NSP_SCHEMES_URL,
        "url": NSP_URL,
        "source": "Government of India - NSP",
        "rules": {
            "education": [
                "12th passed",
                "Engineering UG"
            ],
            "min_marks": 80,
            "max_income": 450000
        }
    }

]


def get_all_schemes():
    return SCHEMES


def search_online(query):

    api_key = os.getenv("GOOGLE_CSE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")

    if not api_key or not cx:
        return [], "Google discovery is not configured. Showing the available starter catalogue."

    try:

        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": api_key,
                "cx": cx,
                "q": query + " official scholarship application deadline",
                "num": 8
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("items", []):

            link = item.get("link", "")

            results.append({
                "title": item.get("title", "Scholarship result"),
                "description": item.get("snippet", ""),
                "snippet": item.get("snippet", ""),
                "application_url": None,
                "info_url": link,
                "url": link,
                "source": item.get("displayLink", "Web result"),
                "deadline": None
            })

        return results, "Search results are discovery links. Application links and deadlines must be verified from official scheme notices."

    except requests.RequestException as error:

        print("Google search error:", error)

        return [], "Online search is temporarily unavailable."