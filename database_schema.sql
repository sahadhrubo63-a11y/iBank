-- Siddhartha Bank Ltd. - Database Schema Specification

-- ১. ব্যাংকার টেবিল (লগইন এবং অ্যাক্সেস কন্ট্রোল)
CREATE TABLE Bankers (
    banker_id VARCHAR(20) PRIMARY KEY,
    banker_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- সিকিউরিটির জন্য হ্যাশ পাসওয়ার্ড
    role VARCHAR(30) DEFAULT 'Teller',   -- Manager, Admin, Teller
    last_login TIMESTAMP
);

-- ২. কাস্টমার মূল প্রোফাইল টেবিল
CREATE TABLE Customers (
    customer_id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL, -- এই নাম্বার দিয়ে ব্যাংকার সার্চ করবেন
    phone_number VARCHAR(15) UNIQUE NOT NULL,   -- এই নাম্বার দিয়েও সার্চ করা যাবে
    full_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100) NOT NULL,
    mother_name VARCHAR(100) NOT NULL,
    nid_number VARCHAR(20) UNIQUE NOT NULL,
    passport_number VARCHAR(20) UNIQUE,        -- ডুয়াল কারেন্সির জন্য জরুরি
    nationality VARCHAR(50) DEFAULT 'Bangladeshi',
    religion VARCHAR(30),
    present_address TEXT NOT NULL,
    permanent_address TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    account_type VARCHAR(20) NOT NULL,          -- Savings, Current, Fixed
    profession VARCHAR(50) NOT NULL,
    source_of_income VARCHAR(100) NOT NULL,
    tin_number VARCHAR(20),                     -- অপশনাল
    customer_picture_url TEXT,                  -- ছবির লিংক
    customer_signature_url TEXT,                -- সিগনেচারের লিংক
    gmail_address VARCHAR(100) UNIQUE,
    account_status VARCHAR(20) DEFAULT 'Active', -- Active, Dormant, Closed
    account_balance DECIMAL(15, 2) DEFAULT 0.00,
    dual_currency_status VARCHAR(10) DEFAULT 'Disabled', -- Enabled / Disabled
    sms_notification_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- ৩ বছর ইনঅ্যাক্টিভ চেক করার জন্য
);

-- ৩. নমিনি টেবিল
CREATE TABLE Nominees (
    nominee_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id) ON DELETE CASCADE,
    nominee_name VARCHAR(100) NOT NULL,
    nid_card_number VARCHAR(20) NOT NULL,
    picture_url TEXT,
    account_share_percentage INT NOT NULL -- কত পার্সেন্ট শেয়ার পাবে
);

-- ৪. কার্ড টেবিল (Debit/Credit)
CREATE TABLE Cards (
    card_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id),
    card_type VARCHAR(20) NOT NULL,             -- Debit / Credit
    card_number VARCHAR(19) UNIQUE NOT NULL,    -- এনক্রিপ্টেড ফরম্যাট বা মাস্কড নাম্বার
    issuing_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    card_status VARCHAR(20) DEFAULT 'Active'    -- Active, Blocked
);

-- দ্রুত সার্চ করার জন্য ইনডেক্সিং (Banker Search Optimization)
CREATE INDEX idx_customer_account ON Customers(account_number);
CREATE INDEX idx_customer_phone ON Customers(phone_number);
