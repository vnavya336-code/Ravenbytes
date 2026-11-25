def check_eligibility(student, scheme):

    reasons = []

    if student["level"] not in scheme["level"]:
        reasons.append("Education level does not match")

    if student["income"] > scheme["income_limit"]:
        reasons.append("Income exceeds the scheme limit")

    if scheme["category"] != "All":

        if student["category"] not in scheme["category"]:
            reasons.append("Category does not match")

    if student["marks"] < scheme["min_marks"]:
        reasons.append("Minimum marks requirement not satisfied")

    if reasons:
        return {
            "status": "Not Eligible",
            "reasons": reasons
        }

    return {
        "status": "Eligible",
        "reasons": ["All listed conditions matched"]
    }