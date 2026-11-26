
def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def check_eligibility(student, schemes):

    output = []

    marks = _number(student.get("marks"))
    income = _number(student.get("income"))

    education = student.get("education", "").strip().lower()
    state = student.get("state", "").strip().lower()
    category = student.get("category", "").strip().lower()
    gender = student.get("gender", "").strip().lower()
    disability = student.get("disability", "").strip().lower()
    religion = student.get("religion", "").strip().lower()

    labour_worker = student.get("labour_worker", "").strip().lower()
    ex_serviceman = student.get("ex_serviceman", "").strip().lower()
    swanath = student.get("swanath", "").strip().lower()

    for scheme in schemes:

        reasons = []
        rules = scheme.get("rules", {})

        allowed_education = [
            x.lower() for x in rules.get("education", [])
        ]

        if allowed_education and education not in allowed_education:
            reasons.append(
                "This scholarship is intended for: "
                + ", ".join(rules["education"])
                + ". Your selected education level does not match."
            )

        if rules.get("state") == "Karnataka" and state != "karnataka":
            reasons.append(
                "This scholarship is restricted to Karnataka students."
            )

        min_marks = rules.get("min_marks")

        if min_marks is not None:
            if marks is None:
                reasons.append("Enter your marks to verify the minimum requirement.")
            elif marks < min_marks:
                reasons.append(
                    f"Your marks ({marks:g}%) are below the required {min_marks}%."
                )

        max_income = rules.get("max_income")

        if max_income is not None:
            if income is None:
                reasons.append("Enter family income to verify the income limit.")
            elif income > max_income:
                reasons.append(
                    f"Your family income exceeds the limit of ₹{max_income:,.0f}."
                )

        allowed_categories = [
            x.lower() for x in rules.get("categories", [])
        ]

        if allowed_categories and category not in allowed_categories:
            reasons.append(
                "This scholarship is limited to: "
                + ", ".join(rules["categories"])
                + "."
            )

        required_gender = rules.get("gender", "").lower()

        if required_gender and gender != required_gender:
            reasons.append(
                "This scholarship requires the applicant to be "
                + required_gender + "."
            )

        if rules.get("disability") == "Yes" and disability != "yes":
            reasons.append(
                "This scholarship requires eligible disability status."
            )

        if rules.get("minority") == "Yes" and religion not in [
            "muslim", "christian", "sikh",
            "buddhist", "jain", "parsi"
        ]:
            reasons.append(
                "This scholarship requires membership in an eligible minority community."
            )

        if rules.get("labour_worker") == "Yes" and labour_worker != "yes":
            reasons.append(
                "This scholarship requires a parent to be a registered eligible labour worker."
            )

        if rules.get("ex_serviceman") == "Yes" and ex_serviceman != "yes":
            reasons.append(
                "This scholarship is intended for eligible children of ex-servicemen."
            )

        if rules.get("swanath") == "Yes" and swanath != "yes":
            reasons.append(
                "You have not confirmed the special-category conditions required for Swanath."
            )

        output.append({
            "scheme": scheme,
            "eligible": len(reasons) == 0,
            "reasons": reasons if reasons else [
                "Your details match the basic recorded conditions. Final eligibility must be confirmed using the official notification."
            ]
        })

    output.sort(
        key=lambda x: (
            not x["eligible"],
            x["scheme"]["name"]
        )
    )

    return output