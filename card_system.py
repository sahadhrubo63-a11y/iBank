# Siddhartha Bank Ltd. - Card & Checkbook Management System
import random
import datetime
from customer_management import CUSTOMER_DATABASE

# কার্ড এবং চেকবুকের ডাটাবেজ মক (ইন-মেমোরি)
CARD_DATABASE = {}
CHECKBOOK_DATABASE = {}

def generate_card_number(card_type):
    """১৬ ডিজিটের ইউনিক কার্ড নাম্বার তৈরি করা (VISA/Mastercard Standard)"""
    prefix = "4152" if card_type.lower() == "debit" else "5221" # VISA or Mastercard Prefix
    remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(12)])
    return prefix + remaining_digits

def issue_new_card(account_number, card_type):
    """নতুন ডেবিট বা ক্রেডিট কার্ড ইস্যু করার ফাংশن"""
    
    # ১. অ্যাকাউন্ট ভ্যালিডেশন
    if account_number not in CUSTOMER_DATABASE:
        print(f"[ERROR] Card Issuance Failed: Account {account_number} not found.")
        return None
        
    customer = CUSTOMER_DATABASE[account_number]
    
    # ২. ডেট ক্যালকুলেশন (ইস্যু ডেট আজ, এক্সপায়ারি ডেট ঠিক ৫ বছর পর)
    issue_date = datetime.date.today()
    expiry_date = issue_date.replace(year=issue_date.year + 5)
    
    card_number = generate_card_number(card_type)
    
    card_entry = {
        "card_number": card_number,
        "card_type": card_type.upper(),
        "issue_date": issue_date.strftime("%Y-%m-%d"),
        "expiry_date": expiry_date.strftime("%Y-%m-%d"),
        # কাস্টমারের প্রোফাইলের ডুয়াল কারেন্সি স্ট্যাটাস সিঙ্ক করা
        "dual_currency": customer.get("dual_currency_status", "Disabled"),
        "card_status": "Active"
    }
    
    if account_number not in CARD_DATABASE:
        CARD_DATABASE[account_number] = []
        
    CARD_DATABASE[account_number].append(card_entry)
    
    print(f"\n[SUCCESS] New {card_type.upper()} Card Issued for A/C: {account_number}")
    print(f"Card No: {card_number[:4]}-{card_number[4:8]}-{card_number[8:12]}-{card_number[12:]}")
    print(f"Issue Date: {card_entry['issue_date']} | Expiry Date: {card_entry['expiry_date']}")
    print(f"Dual Currency Status: {card_entry['dual_currency']}")
    return card_number

def toggle_card_dual_currency(account_number, card_number, enable=True):
    """কার্ডের ডুয়াল কারেন্সি পার্ট এনাবল বা ডিসাবেল করার ফাংশন"""
    if account_number not in CARD_DATABASE:
        print("[ERROR] No cards found for this account.")
        return False
        
    customer = CUSTOMER_DATABASE.get(account_number, {})
    
    # সিকিউরিটি শর্ত: কাস্টমার প্রোফাইলে পাসপোর্ট না থাকলে কার্ডেও ডুয়াল কারেন্সি অন হবে না
    if enable and not customer.get("passport_number"):
        print(f"\n[ACTION DENIED] Cannot enable dual currency! Passport number is missing in Customer Profile.")
        return False

    for card in CARD_DATABASE[account_number]:
        if card["card_number"] == card_number:
            card["dual_currency"] = "Enabled" if enable else "Disabled"
            status_text = "ENABLED" if enable else "DISABLED"
            print(f"\n[STATUS UPDATED] Dual Currency has been {status_text} for Card: {card_number}")
            return True
            
    print("[ERROR] Card number not found.")
    return False

def issue_new_checkbook(account_number, leaves_count=20):
    """কাস্টমারকে নতুন চেকবুক ইস্যু করার অপশন"""
    if account_number not in CUSTOMER_DATABASE:
        print("[ERROR] Checkbook Issuance Failed.")
        return False
        
    checkbook_id = "CB-" + "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    checkbook_entry = {
        "checkbook_id": checkbook_id,
        "leaves": leaves_count,
        "status": "Active",
        "issued_date": datetime.date.today().strftime("%Y-%m-%d")
    }
    
    CHECKBOOK_DATABASE[account_number] = checkbook_entry
    print(f"\n[SUCCESS] New Cheque Book Issued. ID: {checkbook_id} ({leaves_count} Leaves) for A/C: {account_number}")
    return True

# টেস্ট রান করার জন্য কোড সিমুলেশন
if __name__ == "__main__":
    # টেস্টের জন্য ২টি আলাদা কাস্টমার অ্যাকাউন্ট সিমুলেট করা হলো (একটি পাসপোর্টসহ, একটি ছাড়া)
    CUSTOMER_DATABASE["SBL11112222"] = {
        "full_name": "Anik Rahman",
        "passport_number": "", # পাসপোর্ট নেই
        "dual_currency_status": "Disabled"
    }
    CUSTOMER_DATABASE["SBL33334444"] = {
        "full_name": "Siddhartha Roy",
        "passport_number": "BA0987654", # পাসপোর্ট আছে
        "dual_currency_status": "Enabled"
    }
    
    print("--- Siddhartha Bank Ltd. - Cards & Cheque Management ---")
    
    # টেস্ট ১: ডেবিট কার্ড ইস্যু
    card_no_1 = issue_new_card("SBL11112222", "Debit")
    
    # টেস্ট ২: পাসপোর্ট ছাড়া কাস্টমারের ডুয়াল কারেন্সি অন করার চেষ্টা (ফেইল হবে)
    toggle_card_dual_currency("SBL11112222", card_no_1, enable=True)
    
    print("\n------------------------------------------------")
    
    # টেস্ট ৩: পাসপোর্টধারী কাস্টমারের ক্রেডিট কার্ড ইস্যু এবং ডুয়াল কারেন্সি টেস্ট (সাকসেস হবে)
    card_no_2 = issue_new_card("SBL33334444", "Credit")
    
    # টেস্ট ৪: নতুন চেকবুক ইস্যু
    issue_new_checkbook("SBL33334444", leaves_count=50)
