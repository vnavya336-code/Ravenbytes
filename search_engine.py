from ddgs import DDGS

OFFICIAL_DOMAINS = [
    "ssp.karnataka.gov.in",
    "ssp.postmatric.karnataka.gov.in",
    "scholarships.gov.in",
    "aicte-india.org",
    "karnataka.gov.in"
]


def discover_scholarships(level):

    queries = {
        "10th": "Karnataka scholarships after 10th",
        "12th": "Karnataka scholarships after 12th",
        "Engineering": "Karnataka engineering undergraduate scholarships"
    }

    query = queries.get(level)

    if not query:
        return []

    results = []

    try:
        with DDGS() as search:

            search_results = search.text(
                query,
                max_results=15
            )

            for item in search_results:

                url = item.get("href", "")

                if any(domain in url.lower()
                       for domain in OFFICIAL_DOMAINS):

                    results.append({
                        "name": item.get("title", "Scholarship"),
                        "description": item.get("body", ""),
                        "website": url,
                        "verified": False
                    })

    except Exception as error:
        print("Search error:", error)

    return results