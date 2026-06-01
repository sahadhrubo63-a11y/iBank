# Siddhartha Bank Ltd. - Banker Authentication System
import hashlib
import datetime

# ডেমো ডাটাবেজ (বাস্তবে এটি আমাদের তৈরি করা SQL ডাটাবেজের সাথে কানেক্টেড থাকবে)
# সিকিউরিটির জন্য পাসওয়ার্ড 'admin123' কে SHA-256 দিয়ে হ্যাশ করে রাখা হয়েছে
BANKER_DATABASE = {
    "banker001": {
        "name": "Siddhartha Roy",
        "password_hash": "240aa351b22cd89ed9e0e09275d2ae21f6b301dbe85d20fb9d8678b825a33fc1", # hash of 'admin123'
        "role": "Manager"
    },
    "banker002": {
        "name": "Anik Rahman",
        "password_hash": "8d969eee76ec8a32d27e621301bed39ebbb6434816a230661ffe519369c1660d", # hash of 'password567'
        "role": "Teller"
    }
}

def hash_password(password):
    """পাসওয়ার্ড সুরক্ষিত করার জন্য হ্যাশ ফাংশন"""
    return hashlib.sha256(password.encode()).hexdigest()

def banker_login(banker_id, password):
    """ব্যাংকার আইডি এবং পাসওয়ার্ড ভেরিফিকেশন ফাংশন"""
    # ১. আইডি চেক করা
    if banker_id in BANKER_DATABASE:
        input_password_hash = hash_password(password)
        stored_hash = BANKER_DATABASE[banker_id]["password_hash"]
        
        # ২. পাসওয়ার্ড মেলানো
        if input_password_hash == stored_hash:
            banker_name = BANKER_DATABASE[banker_id]["name"]
            banker_role = BANKER_DATABASE[banker_id]["role"]
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[SUCCESS] Login Successful!")
            print(f"Welcome back, {banker_name} ({banker_role})")
            print(f"Login Time: {current_time}")
            return True, banker_role
        else:
            print("\n[ERROR] Invalid Password! Access Denied.")
            return False, None
    else:
        print("\n[ERROR] Banker ID not found in Siddhartha Bank Ltd. records.")
        return False, None

# সিস্টেম টেস্ট রান করার জন্য কোড (সরাসরি রান করলে কাজ করবে)
if __name__ == "__main__":
    print("--- Siddhartha Bank Ltd. Login Portal ---")
    input_id = input("Enter Banker ID: ")
    input_pass = input("Enter Password: ")
    
    # লগইন প্রসেস শুরু
    is_logged_in, role = banker_login(input_id, input_pass)
