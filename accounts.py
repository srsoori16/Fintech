from typing import Tuple
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
