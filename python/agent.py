import json

# -----------------------------
# Intake Agent
# -----------------------------
def intake_agent(applicant):
    required = ["annual_income", "credit_score", "loan_amount_requested", "loan_purpose"]
    for field in required:
        if field not in applicant:
            return False, f"Missing {field}"
    return True, "Validated"


# -----------------------------
# Risk Scoring Agent
# -----------------------------
def risk_scoring_agent(applicant):
    score = 0
    score += 2 if applicant["credit_score"] >= 700 else 1
    score += 2 if applicant["annual_income"] >= 60000 else 1
    return score


# -----------------------------
# Loan Term Suggestion Agent
# -----------------------------
def loan_term_suggestion_agent(applicant, risk_score):
    if risk_score >= 3:
        return {"term_years": 5, "interest_rate": 7.5}
    else:
        return {"term_years": 3, "interest_rate": 9.5}


# -----------------------------
# Offer Generation Agent
# -----------------------------
def offer_generation_agent(applicant, terms):
    return (
        f"Loan Offer for {applicant['name']}: "
        f"${applicant['loan_amount_requested']} at {terms['interest_rate']}% "
        f"for {terms['term_years']} years."
    )


# -----------------------------
# Post-Loan Monitoring Agent
# -----------------------------
def monitoring_agent(applicant, decision):
    flag = (
        "Watchlist"
        if applicant["credit_score"] < 650
        else "Standard monitoring"
    )
    return flag


# -----------------------------
# Orchestrator
# -----------------------------
def run_lending_workflow(applicant):
    valid, msg = intake_agent(applicant)
    if not valid:
        return {"id": applicant["id"], "status": "Rejected", "reason": msg}

    risk = risk_scoring_agent(applicant)
    terms = loan_term_suggestion_agent(applicant, risk)
    offer_text = offer_generation_agent(applicant, terms)
    monitor_flag = monitoring_agent(applicant, offer_text)

    return {
        "id": applicant["id"],
        "offer": offer_text,
        "monitoring": monitor_flag
    }


# -----------------------------
# Execution
# -----------------------------
if __name__ == "__main__":
    with open("sample_applicants.json") as f:
        applicants = json.load(f)

    for app in applicants:
        outcome = run_lending_workflow(app)
        print(outcome)
