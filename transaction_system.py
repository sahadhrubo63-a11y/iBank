# Siddhartha Bank Ltd. - Transaction & Notification System
import datetime
from customer_management import CUSTOMER_DATABASE

# প্রতিটি অ্যাকাউন্টের স্টেটমেন্ট হিস্ট্রি রাখার জন্য গ্লোবাল ডিকশনারি
TRANSACTION_STATEMENTS = {}

def send_instant_notification(account_number, gmail, phone, action_type, amount, current_balance):
    """কাস্টমারের ফোনে SMS এবং জিমেইলে ইনস্ট্যান্ট নোটিফিকেশন পাঠানোর মক ফাংশন"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # SMS নোটিফিকেশন মেসেজ
    sms_text = f"[SMS Alert] SBL A/C {account_number[-4:]} {action_type} BDT {amount:,} on {timestamp}. Balance: BDT {current_balance:,}."
    # Email নোটিফিকেশন মেসেজ
    email_text = (f"[Email Notification to {gmail}]\n"
                  f"Subject: Transaction Alert - Siddhartha Bank Ltd.\n"
                  f"Dear Customer, your account {account_number} has been {action_type} with BDT {amount:,}.\n"
                  f"Available Balance: BDT {current_balance:,}.\n"
                  f"Thank you for banking with Siddhartha Bank Ltd.")
    
    print("\n--- TRIGGERING INSTANT NOTIFICATIONS ---")
    print(sms_text)
    print(email_text)
    print("----------------------------------------")

def execute_transaction(account_number, transaction_type, amount, description):
    """টাকা জমা বা উত্তোলনের মেইন ফাংশন যা স্টেটমেন্ট আপডেট করবে এবং নোটিফিকেশন পাঠাবে"""
    
    # ১. অ্যাকাউন্ট চেক করা
    if account_number not in CUSTOMER_DATABASE:
        print(f"[ERROR] Transaction Failed: Account Number {account_number} not found.")
        return False

    customer = CUSTOMER_DATABASE[account_number]
    
    # অ্যাকাউন্ট ক্লোজ বা ইনঅ্যাক্টিভ থাকলে লেনদেন হবে না
    if customer["account_status"] != "Active":
        print(f"[ERROR] Transaction Failed: Account is currently {customer['account_status']}.")
        return False

    current_time = datetime.datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # ২. লেনদেনের ধরন অনুযায়ী ক্যালকুলেশন
    if transaction_type.lower() == "deposit":
        customer["account_balance"] += amount
        action_word = "Credited"
    elif transaction_type.lower() == "withdraw":
        if customer["account_balance"] < amount:
            print(f"[ERROR] Transaction Failed: Insufficient Balance! Available: BDT {customer['account_balance']:,}")
            return False
        customer["account_balance"] -= amount
        action_word = "Debited"
    else:
        print("[ERROR] Invalid Transaction Type. Choose 'deposit' or 'withdraw'.")
        return False

    # ৩. সর্বশেষ লেনদেনের তারিখ আপডেট (৩ বছর ইনঅ্যাক্টিভ অটো-ক্লোজ লজিকের জন্য)
    customer["last_transaction_date"] = date_str

    # ৪. স্টেটমেন্ট এডিশন (তারিখ ও টাইপ অনুসারে)
    txn_entry = {
        "date_time": timestamp_str,
        "type": transaction_type.upper(),
        "name_description": description,
        "amount": amount,
        "balance_after_txn": customer["account_balance"]
    }
    
    if account_number not in TRANSACTION_STATEMENTS:
        TRANSACTION_STATEMENTS[account_number] = []
    
    TRANSACTION_STATEMENTS[account_number].append(txn_entry)
    
    print(f"\n[SUCCESS] BDT {amount:,} {action_word} successfully.")

    # ৫. কাস্টমারকে তাৎক্ষণিক SMS & Email নোটিফিকেশন পাঠানো
    if customer.get("sms_notification_enabled", True):
        send_instant_notification(
            account_number, 
            customer["gmail_address"], 
            customer["phone_number"], 
            action_word, 
            amount, 
            customer["account_balance"]
        )
        
    return True

# টেস্ট রান করার জন্য ডেমো ট্রানজেকশন টেস্টিং
if __name__ == "__main__":
    # টেস্টের জন্য কাস্টমার ডাটাবেজে একটি ফেক অ্যাকাউন্ট সাময়িকভাবে পুশ করা হলো
    CUSTOMER_DATABASE["SBL12345678"] = {
        "full_name": "Rahat Alom",
        "phone_number": "01712345678",
        "gmail_address": "rahat@gmail.com",
        "account_balance": 10000.00, # প্রারম্ভিক ব্যালেন্স ১০,০০০
        "account_status": "Active",
        "sms_notification_enabled": True,
        "last_transaction_date": "2026-06-01"
    }
    
    print("--- Siddhartha Bank Ltd. - Transaction Simulation ---")
    
    # টেস্ট ১: টাকা জমা দেওয়া (Deposit)
    execute_transaction(
        account_number="SBL12345678", 
        transaction_type="deposit", 
        amount=5000, 
        description="Cash Deposit at Khulna Branch"
    )
    
    # 테스트 ২: কেনাকাটার জন্য টাকা কাটা (Withdraw)
    execute_transaction(
        account_number="SBL12345678", 
        transaction_type="withdraw", 
        amount=3000, 
        description="Merchant Pay: Aarong"
    )
