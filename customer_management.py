# Siddhartha Bank Ltd. - Customer & Nominee Management System
import random
import datetime

# কাস্টমার ডাটাবেজ মক (ইন-মেমোরি স্টোরেজ)
CUSTOMER_DATABASE = {}

def generate_account_number():
    """সিলদার্থ ব্যাংক লিমিটেডের জন্য একটি ইউনিক ১১ ডিজিটের অ্যাকাউন্ট নাম্বার তৈরি করা"""
    return "SBL" + "".join([str(random.randint(0, 9)) for _ in range(8)])

def register_customer(banker_role, customer_info, nominee_info):
    """নতুন কাস্টমার এবং নমিনি রেজিস্টার করার মেইন ফাংশন"""
    
    # সিকিউরিটি চেক: শুধু ব্যাংকাররাই কাস্টমার অ্যাড করতে পারবেন
    if not banker_role:
        print("[ERROR] Unauthorized Access! Only logged-in bankers can add customers.")
        return None

    # ১. আপনার শর্ত: ডুয়াল কারেন্সি এনাবল থাকলে পাসপোর্ট নম্বর বাধ্যতামূলক
    if customer_info.get("dual_currency") == "Enabled" or customer_info.get("dual_currency") == "Yes":
        if not customer_info.get("passport_number"):
            print("\n[REGISTRATION FAILED] Error: Passport Number is MANDATORY to enable Dual Currency part!")
            return None
        customer_info["dual_currency_status"] = "Enabled"
    else:
        customer_info["dual_currency_status"] = "Disabled"

    # ২. অ্যাকাউন্ট নম্বর এবং ওপেনিং ডেট জেনারেট করা
    account_number = generate_account_number()
    customer_info["account_number"] = account_number
    customer_info["account_balance"] = 0.00
    customer_info["account_status"] = "Active"
    customer_info["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d")
    customer_info["last_transaction_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # ৩. নমিনি ডাটা কাস্টমার প্রোফাইলের সাথে যুক্ত করা
    customer_info["nominee_details"] = nominee_info

    # ৪. ডাটাবেজে সেভ করা (অ্যাকাউন্ট নাম্বারকে কি (Key) হিসেবে ব্যবহার করে)
    CUSTOMER_DATABASE[account_number] = customer_info
    
    print(f"\n[SUCCESS] Customer Account Created Successfully in Siddhartha Bank Ltd.!")
    print(f"Generated Account Number: {account_number}")
    return account_number

# টেস্ট রান করার জন্য ডেমো ডাটা ইনপুট
if __name__ == "__main__":
    print("--- Siddhartha Bank Ltd. - New Account Opening Form ---")
    
    # কাস্টমারের তথ্যের নমুনা
    new_customer = {
        "full_name": "Rahat Alom",
        "father_name": "Abul Alom",
        "mother_name": "Rahima Begum",
        "phone_number": "01712345678", # এই নাম্বার দিয়ে পরে সার্চ করা যাবে
        "nid_number": "1995123456789",
        "passport_number": "",        # পাসপোর্ট খালি রাখা হলো টেস্ট করার জন্য
        "nationality": "Bangladeshi",
        "religion": "Islam",
        "present_address": "Dhaka, Bangladesh",
        "permanent_address": "Khulna, Bangladesh",
        "date_of_birth": "1995-05-12",
        "account_type": "Savings",
        "profession": "Software Engineer",
        "source_of_income": "Salary",
        "tin_number": "1234567890",
        "gmail_address": "rahat@gmail.com",
        "dual_currency": "Yes"       # ডুয়াল কারেন্সি অন করা হলো কিন্তু পাসপোর্ট দেওয়া হয়নি
    }
    
    # নমিনির তথ্যের নমুনা
    nominee = {
        "nominee_name": "Sultana Begum",
        "nominee_nid": "1998987654321",
        "relationship": "Wife",
        "share_percentage": 100
    }
    
    # টেস্ট ১: পাসপোর্ট ছাড়া ডুয়াল কারেন্সি অন করার চেষ্টা (এটি ফেইল হবে)
    print("\nAttempting to register with Dual Currency 'Yes' but NO Passport:")
    register_customer(banker_role="Teller", customer_info=new_customer, nominee_info=nominee)
    
    # টেস্ট ২: পাসপোর্ট নম্বর দিয়ে পুনরায় চেষ্টা (এটি সাকসেস হবে)
    print("\nAdding Passport Number and re-trying:")
    new_customer["passport_number"] = "BY0123456"
    account_no = register_customer(banker_role="Teller", customer_info=new_customer, nominee_info=nominee)
