"""
Tests for the Simple Bank System.
Run with: pytest test_bank.py -v
"""

import pytest
from main import Account, Bank


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def bank(tmp_path):
    """Provide a fresh Bank instance backed by a temporary file for each test."""
    return Bank(str(tmp_path / "test_accounts.json"))


@pytest.fixture
def funded_bank(bank):
    """Bank with two accounts, sender has ₹1000."""
    bank.create_account("Alice")   # 1001
    bank.create_account("Bob")     # 1002
    bank.deposit("1001", 1000)
    return bank


# ─────────────────────────────────────────────
# Account — deposit
# ─────────────────────────────────────────────

class TestAccountDeposit:
    def test_deposit_increases_balance(self):
        acc = Account("1001", "Test", 0)
        acc.deposit(200)
        assert acc.balance == 200

    def test_deposit_returns_success(self):
        acc = Account("1001", "Test", 0)
        success, _ = acc.deposit(100)
        assert success is True

    def test_deposit_zero_fails(self):
        acc = Account("1001", "Test", 0)
        success, _ = acc.deposit(0)
        assert success is False
        assert acc.balance == 0

    def test_deposit_negative_fails(self):
        acc = Account("1001", "Test", 100)
        success, _ = acc.deposit(-50)
        assert success is False
        assert acc.balance == 100


# ─────────────────────────────────────────────
# Account — withdraw
# ─────────────────────────────────────────────

class TestAccountWithdraw:
    def test_withdraw_decreases_balance(self):
        acc = Account("1001", "Test", 500)
        acc.withdraw(200)
        assert acc.balance == 300

    def test_withdraw_returns_success(self):
        acc = Account("1001", "Test", 500)
        success, _ = acc.withdraw(100)
        assert success is True

    def test_withdraw_insufficient_balance(self):
        acc = Account("1001", "Test", 100)
        success, msg = acc.withdraw(200)
        assert success is False
        assert acc.balance == 100
        assert "insufficient" in msg.lower()

    def test_withdraw_zero_fails(self):
        acc = Account("1001", "Test", 100)
        success, _ = acc.withdraw(0)
        assert success is False
        assert acc.balance == 100

    def test_withdraw_negative_fails(self):
        acc = Account("1001", "Test", 100)
        success, _ = acc.withdraw(-10)
        assert success is False
        assert acc.balance == 100

    def test_withdraw_exact_balance(self):
        """Withdrawing exactly the available balance should succeed."""
        acc = Account("1001", "Test", 300)
        success, _ = acc.withdraw(300)
        assert success is True
        assert acc.balance == 0


# ─────────────────────────────────────────────
# Bank — create_account
# ─────────────────────────────────────────────

class TestBankCreateAccount:
    def test_creates_first_account_with_id_1001(self, bank):
        bank.create_account("Alice")
        assert "1001" in bank.accounts

    def test_sequential_ids(self, bank):
        bank.create_account("Alice")
        bank.create_account("Bob")
        assert "1002" in bank.accounts

    def test_new_account_starts_with_zero_balance(self, bank):
        bank.create_account("Alice")
        assert bank.accounts["1001"].balance == 0

    def test_empty_name_fails(self, bank):
        success, _ = bank.create_account("   ")
        assert success is False
        assert len(bank.accounts) == 0


# ─────────────────────────────────────────────
# Bank — deposit
# ─────────────────────────────────────────────

class TestBankDeposit:
    def test_deposit_updates_balance(self, bank):
        bank.create_account("Alice")
        bank.deposit("1001", 500)
        assert bank.accounts["1001"].balance == 500

    def test_deposit_to_nonexistent_account(self, bank):
        success, msg = bank.deposit("9999", 100)
        assert success is False
        assert "not found" in msg.lower()

    def test_deposit_invalid_amount(self, bank):
        bank.create_account("Alice")
        success, _ = bank.deposit("1001", -100)
        assert success is False
        assert bank.accounts["1001"].balance == 0


# ─────────────────────────────────────────────
# Bank — withdraw
# ─────────────────────────────────────────────

class TestBankWithdraw:
    def test_withdraw_updates_balance(self, bank):
        bank.create_account("Alice")
        bank.deposit("1001", 500)
        bank.withdraw("1001", 200)
        assert bank.accounts["1001"].balance == 300

    def test_withdraw_from_nonexistent_account(self, bank):
        success, msg = bank.withdraw("9999", 100)
        assert success is False
        assert "not found" in msg.lower()

    def test_withdraw_insufficient_funds(self, bank):
        bank.create_account("Alice")
        bank.deposit("1001", 100)
        success, _ = bank.withdraw("1001", 500)
        assert success is False
        assert bank.accounts["1001"].balance == 100


# ─────────────────────────────────────────────
# Bank — transfer
# ─────────────────────────────────────────────

class TestBankTransfer:
    def test_transfer_moves_funds(self, funded_bank):
        funded_bank.transfer("1001", "1002", 300)
        assert funded_bank.accounts["1001"].balance == 700
        assert funded_bank.accounts["1002"].balance == 300

    def test_transfer_insufficient_funds(self, funded_bank):
        success, _ = funded_bank.transfer("1001", "1002", 5000)
        assert success is False
        assert funded_bank.accounts["1001"].balance == 1000
        assert funded_bank.accounts["1002"].balance == 0

    def test_transfer_same_account_fails(self, funded_bank):
        success, msg = funded_bank.transfer("1001", "1001", 100)
        assert success is False
        assert "same account" in msg.lower()

    def test_transfer_zero_amount_fails(self, funded_bank):
        success, _ = funded_bank.transfer("1001", "1002", 0)
        assert success is False

    def test_transfer_negative_amount_fails(self, funded_bank):
        success, _ = funded_bank.transfer("1001", "1002", -100)
        assert success is False

    def test_transfer_invalid_sender(self, funded_bank):
        success, msg = funded_bank.transfer("9999", "1002", 100)
        assert success is False
        assert "not found" in msg.lower()

    def test_transfer_invalid_receiver(self, funded_bank):
        success, msg = funded_bank.transfer("1001", "9999", 100)
        assert success is False
        assert "not found" in msg.lower()


# ─────────────────────────────────────────────
# Bank — check_balance
# ─────────────────────────────────────────────

class TestBankCheckBalance:
    def test_check_balance_returns_correct_amount(self, bank):
        bank.create_account("Alice")
        bank.deposit("1001", 750)
        _, msg = bank.check_balance("1001")
        assert "750" in msg

    def test_check_balance_nonexistent_account(self, bank):
        success, msg = bank.check_balance("9999")
        assert success is False
        assert "not found" in msg.lower()


# ─────────────────────────────────────────────
# Persistence
# ─────────────────────────────────────────────

class TestPersistence:
    def test_data_persists_across_instances(self, tmp_path):
        """Data saved by one Bank instance should be loadable by another."""
        file = str(tmp_path / "accounts.json")
        bank1 = Bank(file)
        bank1.create_account("Alice")
        bank1.deposit("1001", 999)

        bank2 = Bank(file)
        assert "1001" in bank2.accounts
        assert bank2.accounts["1001"].balance == 999
        assert bank2.accounts["1001"].name == "Alice"