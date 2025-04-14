from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/check', methods=['POST'])
def check_eligibility():
    credit_score = int(request.form['credit_score'])
    monthly_income = float(request.form['monthly_income'])
    debt_payments = float(request.form['debt_payments'])
    loan_amount = float(request.form['loan_amount'])
    loan_term = int(request.form['loan_term'])
    employment_status = request.form['employment_status']
    loan_type = request.form['loan_type']
    down_payment = float(request.form.get('down_payment', 0))
    state = request.form['state']
    collateral = request.form['collateral']

    dti = (debt_payments / monthly_income) * 100

    eligibility = "Eligible"
    reasons = []

    if loan_type == "Personal Loan":
        if credit_score < 600:
            eligibility = "Not Eligible"
            reasons.append("Credit score is too low for a personal loan.")
        if dti > 45:
            eligibility = "Not Eligible"
            reasons.append("DTI ratio is too high for a personal loan.")
    
    elif loan_type == "Mortgage Loan":
        if credit_score < 500:
            eligibility = "Not Eligible"
            reasons.append("Credit score is too low for an FHA mortgage.")
        elif credit_score < 620:
            eligibility = "Conditional"
            reasons.append("Eligible for FHA but not conventional mortgage.")
        if dti > 43:
            eligibility = "Not Eligible"
            reasons.append("DTI ratio exceeds mortgage requirements.")
        if down_payment <= 0:
            eligibility = "Not Eligible"
            reasons.append("Down payment required for a mortgage.")

    elif loan_type == "Auto Loan":
        if credit_score < 660:
            eligibility = "Not Eligible"
            reasons.append("Credit score is too low for an auto loan.")
        if dti > 50:
            eligibility = "Not Eligible"
            reasons.append("DTI ratio is too high for an auto loan.")
        if collateral != "Yes":
            eligibility = "Not Eligible"
            reasons.append("Collateral (vehicle) required for an auto loan.")

    elif loan_type == "Business Loan":
        if credit_score < 680:
            eligibility = "Not Eligible"
            reasons.append("Credit score is too low for a business loan.")

    elif loan_type == "Credit Card":
        if credit_score < 600:
            eligibility = "Not Eligible"
            reasons.append("Credit score is too low for a credit card.")
        if dti > 40:
            eligibility = "Not Eligible"
            reasons.append("DTI ratio is too high for a credit card.")

    return render_template('result.html', eligibility=eligibility, reasons=reasons, loan_type=loan_type, loan_amount=loan_amount)

if __name__ == "__main__":
    app.run(debug=True)
