import streamlit as st

st.set_page_config(page_title="Borrower Risk Estimator", page_icon="📉", layout="centered")

def calculate_borrower_risk(monthly_income, employment_status, years_employed,
                            loan_amount, interest_rate, loan_tenure_months,
                            existing_monthly_debt_payments, total_outstanding_debt,
                            prior_default_history, credit_score=None):

    score = 0
    loan_to_income_ratio = loan_amount / monthly_income if monthly_income > 0 else 10
    debt_payment_ratio = existing_monthly_debt_payments / monthly_income if monthly_income > 0 else 1

    if loan_to_income_ratio > 2:
        score += 25
    elif loan_to_income_ratio > 1:
        score += 15
    else:
        score += 5

    if debt_payment_ratio > 0.4:
        score += 20
    elif debt_payment_ratio > 0.2:
        score += 10
    else:
        score += 3

    emp = employment_status.lower()
    if emp in ["unemployed", "contract"]:
        score += 20
    elif emp == "self-employed":
        score += 12
    else:
        score += 5

    if years_employed < 1:
        score += 15
    elif years_employed < 3:
        score += 8
    else:
        score += 3

    if prior_default_history == "Yes":
        score += 20

    if credit_score is not None:
        if credit_score < 500:
            score += 20
        elif credit_score < 650:
            score += 10
        else:
            score += 2

    probability_of_default = min(max(score, 5), 95)

    if probability_of_default < 20:
        risk_category = "Low Risk"
        interpretation = "Borrower appears relatively lower risk based on current inputs."
    elif probability_of_default < 40:
        risk_category = "Moderate Risk"
        interpretation = "Borrower shows some elevated risk factors that may require closer review."
    elif probability_of_default < 65:
        risk_category = "Elevated Risk"
        interpretation = "Borrower profile suggests materially elevated risk."
    else:
        risk_category = "High Risk"
        interpretation = "Borrower appears high risk and may require stronger underwriting caution."

    return {
        "probability_of_default": round(probability_of_default, 2),
        "risk_category": risk_category,
        "loan_to_income_ratio": round(loan_to_income_ratio, 2),
        "debt_payment_ratio": round(debt_payment_ratio * 100, 2),
        "interpretation": interpretation
    }

st.title("Borrower Risk Estimator")
st.write("Get an indicative borrower risk estimate using income, debt burden, employment profile, and loan details.")

with st.form("borrower_risk_form"):
    monthly_income = st.number_input("Monthly Income", min_value=0.0, step=1000.0)
    employment_status = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Contract", "Unemployed"])
    years_employed = st.number_input("Years Employed", min_value=0.0, step=1.0)
    loan_amount = st.number_input("Loan Amount", min_value=0.0, step=1000.0)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.5)
    loan_tenure_months = st.number_input("Loan Tenure (Months)", min_value=1, step=1)
    existing_monthly_debt_payments = st.number_input("Existing Monthly Debt Payments", min_value=0.0, step=1000.0)
    total_outstanding_debt = st.number_input("Total Outstanding Debt", min_value=0.0, step=1000.0)
    prior_default_history = st.selectbox("Prior Default History", ["No", "Yes"])
    credit_score = st.number_input("Credit Score (Optional)", min_value=0, max_value=1000, step=1)
    submitted = st.form_submit_button("Estimate Risk")

if submitted:
    if monthly_income <= 0:
        st.error("Monthly income must be greater than zero.")
    else:
        credit_score_input = credit_score if credit_score > 0 else None

        result = calculate_borrower_risk(
            monthly_income, employment_status, years_employed,
            loan_amount, interest_rate, loan_tenure_months,
            existing_monthly_debt_payments, total_outstanding_debt,
            prior_default_history, credit_score_input
        )

        st.success("Assessment Complete")
        st.metric("Indicative Probability of Default", f"{result['probability_of_default']}%")
        st.metric("Risk Category", result['risk_category'])
        st.write(f"**Loan-to-Income Ratio:** {result['loan_to_income_ratio']}")
        st.write(f"**Debt Payment Ratio:** {result['debt_payment_ratio']}%")
        st.write(f"**Interpretation:** {result['interpretation']}")

        st.info("Indicative output only. For a deeper credit risk review, contact Quant Vision Labs.")
        st.markdown("[Request Consultation](https://yourwebsite.com/request-consultation)")
