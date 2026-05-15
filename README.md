# FinTech Banking API

A simple banking backend project built using Python, Flask, MySQL, and raw SQL queries.

This project provides REST APIs for basic banking operations such as:

- Account Creation
- Deposit Money
- Withdraw Money
- Transfer Funds
- Check Balance

---

# Tech Stack

- Python
- Flask
- MySQL
- MySQL Connector
- REST API
- Raw SQL Queries

---

# Project Structure

```text
FinTech/
│
├── app.py
├── routes.py
├── bank.py
├── db.py
├── accounts.py
├── requirements.txt
├── README.md
└── test_bank.py
```

---

# Features

## Create Account
Creates a new bank account.

## Deposit
Deposits money into an account.

## Withdraw
Withdraws money from an account with balance validation.

## Transfer
Transfers money between two accounts.

## Check Balance
Returns account details and current balance.

---

# Database Schema

## Accounts Table

```sql
CREATE TABLE accounts(
    acc_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    balance FLOAT DEFAULT 0
);
```

## Transactions Table

```sql
CREATE TABLE transactions(
    trans_id INT PRIMARY KEY AUTO_INCREMENT,
    trans_acc_id INT,
    related_acc_id INT NULL,
    type VARCHAR(20),
    amount FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Fintech.git
```

## Navigate to Project

```bash
cd Fintech
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Database

Update `db.py` with your MySQL credentials.

```python
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='Fintech'
)
```

---

# Run the Application

```bash
python app.py
```

Server runs on:

```text
http://127.0.0.1:5000
```

---

# API Endpoints

## Create Account

```http
POST /account/create
```

### JSON Body

```json
{
    "name": "Srushti"
}
```

---

## Deposit

```http
POST /account/deposit
```

### JSON Body

```json
{
    "acc_id": 1,
    "amount": 5000
}
```

---

## Withdraw

```http
POST /account/withdraw
```

### JSON Body

```json
{
    "acc_id": 1,
    "amount": 1000
}
```

---

## Transfer

```http
POST /account/transfer
```

### JSON Body

```json
{
    "sender": 1,
    "reciever": 2,
    "amount": 500
}
```

---

## Check Balance

```http
GET /account/check_balance/1
```

---

# Future Improvements

- User Authentication
- Transaction History
- Unit Testing
- Docker Support
- SQLAlchemy Integration
- JWT Authentication
- Account Deletion
- Better Error Handling

---

# Author

Developed by Srushti
