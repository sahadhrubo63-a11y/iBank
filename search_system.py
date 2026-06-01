# Siddhartha Bank Ltd. - Customer Search & Dashboard System
from customer_management import CUSTOMER_DATABASE, register_customer

def search_customer(search_query):
    """অ্যাকাউন্ট নাম্বার অথবা ফোন নাম্বার দিয়ে কাস্টমার সার্চ করার ফাংশন"""
    print(f"\n[SEARCHING] Searching for: '{search_query}' in Siddhartha Bank Ltd. database...")
    
    # ডাটাবেজের সব কাস্টমার চেক করা
    for account_no, details in CUSTOMER_DATABASE.items():
        # শর্ত: অ্যাকাউন্ট নাম্বার অথবা ফোন নাম্বার মিললে প্রোফাইল দেখাবে
        if account_no == search_query or details.get("phone_number") == search_query:
            print("\n" + "="*50)
            print(f"       SIDDHARTHA BANK LTD. - CUSTOMER PROFILE       ")
            print("="*50)
            print(f"Account Number   : {account_no}")
            print(f"Account Status   : {details['account_status']} (Last Txn: {details['last_transaction_date']})")
            print(f"Current Balance  : BDT {details['account_balance']:,}")
            print(f"Account Type     : {details['account_type']}")
            print(f"Dual Currency    : {details['dual_currency_status']}")
            print("-"*50)
            print(f"Customer Name    : {details['full_name']}")
            print(f"Father's Name    : {details['father_name']}")
            print(f"Mother's Name    : {details['mother_name']}")
            print(f"Phone Number     : {details['phone_number']}")
            print(f"Gmail Address    : {details['gmail_address']}")
            print(f"NID Number       : {details['nid_number']}")
            print(f"Passport Number  : {details.get('passport_number', 'N/A')}")
            print(f"Date of Birth    : {details['date_of_birth']}")
            print(f"Nationality      : {details['nationality']} | Religion: {details['religion']}")
            print(f"Profession       : {details['profession']} | Source of Income: {details['source_of_income']}")
            print(f"TIN Number       : {details.get('tin_number', 'N/A')}")
            print(f"Present Address  : {details['present_address']}")
            print(f"Permanent Address: {details['permanent_address']}")
            print(f"Images Status    : [Photo: Saved] [Signature: Saved]")
            print("-"*50)
            
            # নমিনি ডিটেইলস প্রদর্শন
            nominee = details.get("nominee_details", {})
            print(f"Nominee Name     : {nominee.get('nominee_name')}")
            print(f"Nominee NID      : {nominee.get('nominee_nid')}")
            print(f"Relationship     : {nominee.get('relationship')}")
            print(f"Account Share    : {nominee.get('share_percentage')}%")
            print("="*50 + "\n")
            return details
            
    print("[NOT FOUND] No customer found with this Account Number or Phone Number.")
    return None

# টেস্ট রান করার জন্য ডেমো ডাটা তৈরি ও সার্চ টেস্টিং
if __name__ == "__main__":
    # টেস্টের সুবিধার্থে একটি কাস্টমার অ্যাকাউন্ট আগে তৈরি করে নিচ্ছি
    sample_customer = {
        "full_name": "Siddhartha Roy",
        "father_name": "Late B. Roy",
        "mother_name": "K. Roy",
        "phone_number": "01999888777",
        "nid_number": "5554443332211",
        "passport_number": "BA0987654",
        "nationality": "Bangladeshi",
        "religion": "Hinduism",
        "present_address": "Khulna, Bangladesh",
        "permanent_address": "Khulna, Bangladesh",
        "date_of_birth": "1990-01-01",
        "account_type": "Current",
        "profession": "Business",
        "source_of_income": "Trade",
        "gmail_address": "siddhartha@gmail.com",
        "dual_currency": "Yes"
    }
    sample_nominee = {
        "nominee_name": "Amit Roy",
        "nominee_nid": "111222333444",
        "relationship": "Brother",
        "share_percentage": 100
    }
    
    # অ্যাকাউন্টটি ডাটাবেজে সেভ হলো এবং নাম্বার জেনারেট হলো
    generated_acc = register_customer("Manager", sample_customer, sample_nominee)
    
    # টেস্ট ১: অ্যাকাউন্ট নাম্বার দিয়ে সার্চ (কাজ করবে)
    search_customer(generated_acc)
    
    # টেস্ট ২: ফোন নাম্বার দিয়ে সার্চ (কাজ করবে)
    search_customer("01999888777")
    
    # টেস্ট ৩: ভুল নাম্বার দিয়ে সার্চ (এরর দেখাবে)
    search_customer("01700000000")
