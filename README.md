# 🏦 Simple Bank System

A command-line banking application built with Python, demonstrating OOP principles, file persistence, and clean code practices.

---

## Features

- Create bank accounts
- Deposit & withdraw funds
- Transfer money between accounts
- Check account balance
- Data persisted to a local JSON file

---

## Project Structure

```
simple-bank/
├── main.py            # Core Bank and Account logic + CLI
├── test_bank.py       # Full pytest test suite
├── requirements.txt   # Dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/simple-bank.git
cd simple-bank
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python main.py
```

---

## Running Tests

```bash
pytest test_bank.py -v
```

Tests use temporary files via `pytest`'s `tmp_path` fixture — no leftover files, no test pollution.

---

## Example Usage

```
╔══════════════════════════════╗
║      Simple Bank System      ║
╠══════════════════════════════╣
║  1. Create Account           ║
║  2. Deposit                  ║
║  3. Withdraw                 ║
║  4. Transfer                 ║
║  5. Check Balance            ║
║  6. Exit                     ║
╚══════════════════════════════╝

Choose an option (1-6): 1
Enter account holder's name: Alice
Account created successfully. Account ID: 1001
```

---

## Tech Stack

- **Python 3.10+**
- **JSON** for lightweight persistence
- **pytest** for testing
- Type hints & docstrings throughout
