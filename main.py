import json
from typing import Dict, Optional, Tuple


class Account:
    """Represents a bank account with basic operations like deposit and withdraw."""

    def __init__(self, acc_id: str, name: str, balance: float = 0) -> None:
        """
        Initialize an account.

        :param acc_id: Unique account ID
        :param name: Account holder's name
        :param balance: Initial balance (default 0)
        """
        self.acc_id = acc_id
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> Tuple[bool, str]:
        """
        Deposit money into the account.

        :param amount: Amount to deposit (must be > 0)
        :return: Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Deposit amount must be greater than 0."
        self.balance += amount
        return True, f"Deposited ₹{amount:.2f} successfully. Current balance: ₹{self.balance:.2f}"

    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """
        Withdraw money from the account.

        :param amount: Amount to withdraw (must be > 0 and <= balance)
        :return: Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0."
        if amount > self.balance:
            return False, "Insufficient balance."
        self.balance -= amount
        return True, f"Withdrew ₹{amount:.2f} successfully. Current balance: ₹{self.balance:.2f}"

    def __repr__(self) -> str:
        return f"Account(id={self.acc_id}, name={self.name}, balance={self.balance:.2f})"


class Bank:
    """Manages multiple bank accounts and persists data to a JSON file."""

    def __init__(self, file_name: str = "accounts.json") -> None:
        """
        Initialize the bank and load existing accounts from a JSON file.

        :param file_name: Path to the JSON file for storing account data
        """
        self.file_name = file_name
        self.accounts: Dict[str, Account] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Load account data from the JSON file. Silently starts fresh if not found."""
        self.accounts = {}
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
                for acc_id, acc_data in data.items():
                    self.accounts[acc_id] = Account(
                        acc_id, acc_data["name"], acc_data["balance"]
                    )
        except FileNotFoundError:
            self.accounts = {}

    def save_data(self) -> None:
        """Persist all account data to the JSON file."""
        data: Dict[str, dict] = {
            acc_id: {"name": account.name, "balance": account.balance}
            for acc_id, account in self.accounts.items()
        }
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

    def _generate_account_id(self) -> str:
        """Generate the next sequential account ID starting from 1001."""
        if not self.accounts:
            return "1001"
        return str(max(int(i) for i in self.accounts) + 1)

    def create_account(self, name: str) -> Tuple[bool, str]:
        """
        Create a new bank account.

        :param name: Full name of the account holder
        :return: Tuple of (success, message with account ID)
        """
        name = name.strip()
        if not name:
            return False, "Account holder name cannot be empty."
        acc_id = self._generate_account_id()
        self.accounts[acc_id] = Account(acc_id, name)
        self.save_data()
        return True, f"Account created successfully. Account ID: {acc_id}"

    def find_account(self, acc_id: str) -> Optional[Account]:
        """
        Look up an account by ID.

        :param acc_id: The account ID to search for
        :return: Account object if found, else None
        """
        return self.accounts.get(acc_id)

    def deposit(self, acc_id: str, amount: float) -> Tuple[bool, str]:
        """
        Deposit money into a specific account.

        :param acc_id: Target account ID
        :param amount: Amount to deposit
        :return: Tuple of (success, message)
        """
        account = self.find_account(acc_id)
        if account is None:
            return False, f"Account {acc_id} not found."
        success, message = account.deposit(amount)
        if success:
            self.save_data()
        return success, message

    def withdraw(self, acc_id: str, amount: float) -> Tuple[bool, str]:
        """
        Withdraw money from a specific account.

        :param acc_id: Target account ID
        :param amount: Amount to withdraw
        :return: Tuple of (success, message)
        """
        account = self.find_account(acc_id)
        if account is None:
            return False, f"Account {acc_id} not found."
        success, message = account.withdraw(amount)
        if success:
            self.save_data()
        return success, message

    def transfer(self, send_id: str, rec_id: str, amount: float) -> Tuple[bool, str]:
        """
        Transfer money from one account to another.

        :param send_id: Sender's account ID
        :param rec_id: Receiver's account ID
        :param amount: Amount to transfer
        :return: Tuple of (success, message)
        """
        if amount <= 0:
            return False, "Transfer amount must be greater than 0."
        if send_id == rec_id:
            return False, "Cannot transfer to the same account."

        sender = self.find_account(send_id)
        receiver = self.find_account(rec_id)

        if sender is None:
            return False, f"Sender account {send_id} not found."
        if receiver is None:
            return False, f"Receiver account {rec_id} not found."

        success, message = sender.withdraw(amount)
        if not success:
            return False, f"Transfer failed: {message}"

        receiver.deposit(amount)
        self.save_data()
        return True, f"Transferred ₹{amount:.2f} from {send_id} to {rec_id} successfully."

    def check_balance(self, acc_id: str) -> Tuple[bool, str]:
        """
        Check the balance of an account.

        :param acc_id: Account ID to check
        :return: Tuple of (success, balance message)
        """
        account = self.find_account(acc_id)
        if account is None:
            return False, f"Account {acc_id} not found."
        return True, f"Account [{acc_id}] | Name: {account.name} | Balance: ₹{account.balance:.2f}"


def print_menu() -> None:
    print("""
╔══════════════════════════════╗
║      Simple Bank System      ║
╠══════════════════════════════╣
║  1. Create Account           ║
║  2. Deposit                  ║
║  3. Withdraw                 ║
║  4. Transfer                 ║
║  5. Check Balance            ║
║  6. Exit                     ║
╚══════════════════════════════╝""")


def get_amount(prompt: str) -> Optional[float]:
    """Prompt for a valid positive float amount. Returns None on invalid input."""
    try:
        amount = float(input(prompt))
        return amount
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None


def run_cli(bank: Bank) -> None:
    """Run the interactive command-line interface for the bank."""
    print_menu()

    while True:
        user_input = input("\nChoose an option (1-6): ").strip()

        if user_input == "1":
            name = input("Enter account holder's name: ").strip()
            success, msg = bank.create_account(name)
            print(msg)

        elif user_input == "2":
            acc_id = input("Enter account ID: ").strip()
            amount = get_amount("Enter deposit amount: ₹")
            if amount is not None:
                _, msg = bank.deposit(acc_id, amount)
                print(msg)

        elif user_input == "3":
            acc_id = input("Enter account ID: ").strip()
            amount = get_amount("Enter withdrawal amount: ₹")
            if amount is not None:
                _, msg = bank.withdraw(acc_id, amount)
                print(msg)

        elif user_input == "4":
            send_id = input("Enter sender account ID: ").strip()
            rec_id = input("Enter receiver account ID: ").strip()
            amount = get_amount("Enter transfer amount: ₹")
            if amount is not None:
                _, msg = bank.transfer(send_id, rec_id, amount)
                print(msg)

        elif user_input == "5":
            acc_id = input("Enter account ID: ").strip()
            _, msg = bank.check_balance(acc_id)
            print(msg)

        elif user_input == "6":
            print("Thank you for using Simple Bank. Goodbye!")
            break

        else:
            print("Invalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    bank = Bank()
    run_cli(bank)