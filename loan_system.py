# Siddhartha Bank Ltd. - Loan Management & Statement System
import datetime
from customer_management import CUSTOMER_DATABASE

# লোনের প্রকারভেদ এবং বার্ষিক সুদের হার (Siddhartha Bank Ltd. Policy)
LOAN_TYPES = {
    "1": {"name": "Home Loan", "interest_rate": 8.5},     # 8.5% Interest
    "2": {"name": "Car Loan", "interest_rate": 9.0},      # 9.0% Interest
    "3": {"name": "Personal Loan", "interest_rate": 11.5} # 11.5% Interest
}

LOAN_DATABASE = {}

def apply_for_loan(account_number, loan_choice, principal_amount, duration_months):
    """কাস্টমারের জন্য লোন সিলেক্ট এবং অ্যাপ্লাই করার ফাংশন"""
    
    # ১. অ্যাকাউন্ট ভ্যালিডেশন
    if account_number not in CUSTOMER_DATABASE:
        print(f"[ERROR] Loan Application Failed: Account {account_number} not found.")
        return False
        
    if loan_choice not in LOAN_TYPES:
        print("[ERROR] Invalid Loan Type Selection.")
        return False

    loan_details = LOAN_TYPES[loan_choice]
    rate = loan_details["interest_rate"]
    
    # ২. মোট সুদের হিসেব ও EMI ক্যালকুলেশন (সরল সুদ এবং মাসিক কিস্তি ফর্মুলা)
    # Total Interest = (P * R * T) / 100
    years = duration_months / 12
    total_interest = (principal_amount * rate * years) / 100
    total_payable = principal_amount + total_interest
    monthly_emi = total_payable / duration_months

    # ৩. লোন রেকর্ড তৈরি
    loan_id = "LNK" + str(datetime.datetime.now().strftime("%M%S"))
    loan_entry = {
        "loan_id": loan_id,
        "loan_type": loan_details["name"],
        "principal_amount": principal_amount,
        "interest_rate": f"{rate}%",
        "total_payable": total_payable,
        "current_outstanding": total_payable,
        "monthly_emi": round(monthly_emi, 2),
        "duration_months": duration_months,
        "applied_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "payments_history": [] # লোনের মাসিক স্টেটমেন্টের জন্য
    }

    # ৪. ডাটাবেজে লোন সেভ করা এবং কাস্টমারের মেইন অ্যাকাউন্টে লোনের টাকা ট্রান্সফার করা
    if account_number not in LOAN_DATABASE:
        LOAN_DATABASE[account_number] = []
        
    LOAN_DATABASE[account_number].append(loan_entry)
    
    # লোনের টাকা সরাসরি কাস্টমারের মূল ব্যালেন্সে যোগ হবে
    CUSTOMER_DATABASE[account_number]["account_balance"] += principal_amount
    
    print(f"\n[LOAN APPROVED] {loan_details['name']} approved for A/C: {account_number}")
    print(f"Loan ID: {loan_id} | Principal: BDT {principal_amount:,}")
    print(f"Monthly EMI: BDT {round(monthly_emi, 2):,} for {duration_months} Months.")
    print(f"BDT {principal_amount:,} has been credited to the customer's main account balance.")
    return True

def pay_loan_emi(account_number, loan_id, payment_amount):
    """কাস্টমার কর্তৃক লোনের মাসিক কিস্তি পরিশোধ এবং হিসেব রাখা"""
    if account_number not in LOAN_DATABASE:
        print("[ERROR] No active loan found for this account.")
        return False

    for loan in LOAN_DATABASE[account_number]:
        if loan["loan_id"] == loan_id:
            if loan["current_outstanding"] <= 0:
                print("[INFO] This loan is already fully paid!")
                return True
                
            # কিস্তি মাইনাস করা
            loan["current_outstanding"] -= payment_amount
            payment_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # লোন স্টেটমেন্টে হিসেব যোগ করা
            loan["payments_history"].append({
                "payment_date": payment_date,
                "amount_paid": payment_amount,
                "remaining_outstanding": loan["current_outstanding"]
            })
            print(f"\n[EMI PAID] BDT {payment_amount:,} received for Loan ID: {loan_id}. Outstanding: BDT {loan['current_outstanding']:,}")
            return True
            
    print("[ERROR] Loan ID not found.")
    return False

def generate_loan_statement(account_number, month_year):
    """নির্দিষ্ট মাসের লোন স্টেটমেন্ট দেখার ফাংশন (Format: YYYY-MM)"""
    if account_number not in LOAN_DATABASE or not LOAN_DATABASE[account_number]:
        print("\n[STATEMENT] No loan history found for this account.")
        return
        
    print(f"\n==================================================")
    print(f"   SIDDHARTHA BANK LTD. - MONTHLY LOAN STATEMENT   ")
    print(f"   Target Month: {month_year} | A/C: {account_number}   ")
    print(f"==================================================")
    
    for loan in LOAN_DATABASE[account_number]:
        print(f"Loan Type: {loan['loan_type']} | Loan ID: {loan['loan_id']}")
        print(f"Approved Amount: BDT {loan['principal_amount']:,} ({loan['interest_rate']})")
        print(f"Current Outstanding: BDT {loan['current_outstanding']:,}")
        print(f"Monthly EMI: BDT {loan['monthly_emi']:,}")
        print(f"--------------------------------------------------")
        print(f"{'Payment Date/Time':<25} | {'Amount Paid':<12}")
        print(f"--------------------------------------------------")
        
        has_records = False
        for payment in loan["payments_history"]:
            if payment["payment_date"].startswith(month_year):
                print(f"{payment['payment_date']:<25} | BDT {payment['amount_paid']:,}")
                has_records = True
                
        if not has_records:
            print("No EMI payments found for this specific month.")
            
    print(f"==================================================\n")

# টেস্ট রান করার জন্য ডেমো লোন প্রসেস টেস্টিং
if __name__ == "__main__":
    # টেস্টের জন্য কাস্টমার ডাটাবেজে একটি একাউন্ট তৈরি করে রাখা হলো
    CUSTOMER_DATABASE["SBL99998888"] = {
        "full_name": "Siddhartha Roy",
        "account_balance": 50000.00,
        "account_status": "Active"
    }
    
    print("--- Siddhartha Bank Ltd. - Loan Portal ---")
    print("Available Loans: 1. Home Loan (8.5%) | 2. Car Loan (9.0%) | 3. Personal Loan (11.5%)")
    
    # টেস্ট ১: ৫ লক্ষ টাকা হোম লোন ৩ বছরের (৩৬ মাস) জন্য অ্যাপ্লাই
    apply_for_loan(account_number="SBL99998888", loan_choice="1", principal_amount=500000, duration_months=36)
    
    # টেস্ট এর সুবিধার্থে লোন আইডিটি খুঁজে বের করে কিস্তি দেওয়া
    target_loan_id = LOAN_DATABASE["SBL99998888"][0]["loan_id"]
    
    # টেস্ট ২: একটি ইএমআই (EMI) জমা দেওয়া
    pay_loan_emi(account_number="SBL99998888", loan_id=target_loan_id, payment_amount=15486.11)
    
    # টেস্ট ৩: বর্তমান মাসের (২০২৬ সালের জুন মাস) লোন স্টেটমেন্ট দেখা
    current_month = "2026-06"
    generate_loan_statement("SBL99998888", current_month)
