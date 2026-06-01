# Siddhartha Bank Ltd. - Automatic Account Lifecycle Closer
import datetime
from customer_management import CUSTOMER_DATABASE

def check_and_close_inactive_accounts():
    """৩ বছর বা তার বেশি সময় ধরে ইনঅ্যাক্টিভ থাকা অ্যাকাউন্টগুলো অটোমেটিক ক্লোজ করার ফাংশন"""
    print(f"\n[CRON JOB RUNNING] Scanning for inactive accounts... Current Date: {datetime.date.today()}")
    print("=" * 65)
    
    current_date = datetime.date.today()
    closed_count = 0
    
    # ডাটাবেজের প্রতিটা কাস্টমারের লাস্ট ট্রানজেকশন ডেট চেক করা
    for account_no, details in CUSTOMER_DATABASE.items():
        # অ্যাকাউন্ট অলরেডি ক্লোজড থাকলে স্কিপ করবে
        if details["account_status"] == "Closed":
            continue
            
        # স্ট্রিং ডেটকে পাইথনের ডেট অবজেক্টে রূপান্তর
        last_txn_str = details.get("last_transaction_date")
        last_txn_date = datetime.datetime.strptime(last_txn_str, "%Y-%m-%d").date()
        
        # দিন হিসেব করা (৩ বছর = ৩ * ৩৬৫ দিন = ১০৯৫ দিন)
        days_inactive = (current_date - last_txn_date).days
        
        # ৩ বছরের লজিক ভেরিফিকেশন
        if days_inactive >= 1095:
            details["account_status"] = "Closed"
            closed_count += 1
            print(f"[AUTO-CLOSED] A/C: {account_number_mask(account_no)} | Owner: {details['full_name']}")
            print(f"              Reason: Inactive for {days_inactive} days (Last Txn: {last_txn_str})")
            print("-" * 65)
            
    if closed_count == 0:
        print("[INFO] Scan complete. No inactive accounts found for closure today.")
    else:
        print(f"[COMPLETED] Total {closed_count} account(s) automatically closed today.")
    print("=" * 65 + "\n")

def account_number_mask(account_no):
    """নিরাপত্তার স্বার্থে অ্যাকাউন্ট নাম্বারের মাঝখানের অংশ মাস্ক বা হাইড করার ফাংশন"""
    return account_no[:5] + "****" + account_no[-2:]

# টেস্ট রান করার জন্য কোড সিমুলেশন
if __name__ == "__main__":
    # টেস্টের জন্য ৩ জন কাস্টমারের ডাটা তৈরি (১ জন অ্যাক্টিভ, ১ জন ২ বছর ইনঅ্যাক্টিভ, ১ জন ৩ বছরের বেশি ইনঅ্যাক্টিভ)
    
    # কাস্টমার ১: সম্পূর্ণ অ্যাক্টিভ (আজকের ডেট অনুসারে লেনদেন)
    CUSTOMER_DATABASE["SBL10000001"] = {
        "full_name": "Siddhartha Roy",
        "account_status": "Active",
        "last_transaction_date": datetime.date.today().strftime("%Y-%m-%d")
    }
    
    # কাস্টমার ২: ইনঅ্যাক্টিভ কিন্তু ৩ বছর হয়নি (ধরা যাক ২ বছর বা ৭৩০ দিন আগের লেনদেন)
    two_years_ago = (datetime.date.today() - datetime.timedelta(days=730)).strftime("%Y-%m-%d")
    CUSTOMER_DATABASE["SBL10000002"] = {
        "full_name": "Rahat Alom",
        "account_status": "Active",
        "last_transaction_date": two_years_ago
    }
    
    # কাস্টমার ৩: দীর্ঘ ৩ বছরের বেশি ইনঅ্যাক্টিভ (ধরা যাক ৪ বছর বা ১৪৬০ দিন আগের লেনদেন)
    four_years_ago = (datetime.date.today() - datetime.timedelta(days=1460)).strftime("%Y-%m-%d")
    CUSTOMER_DATABASE["SBL10000003"] = {
        "full_name": "Asif Iqbal",
        "account_status": "Active",
        "last_transaction_date": four_years_ago
    }
    
    # অটো-ক্লোজ স্ক্রিপ্ট রান করা
    check_and_close_inactive_accounts()
