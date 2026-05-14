from db import conn,cursor
class Bank:
    def __init__(self):
        pass
    def create_account (self,name):
        name = name.strip()
        if not name:
            return False, "Name cannot be empty."
        cursor.execute("Insert into accounts(name,balance) values(%s,%s)",(name,0.00))
        conn.commit()
        acc_id = cursor.lastrowid
        return True,f"Account created successfully.Account ID: {acc_id}" 

    def find_account(self,acc_id):
        if not acc_id:
            return None
        cursor.execute("Select * from accounts where acc_id = %s",(acc_id,))
        result = cursor.fetchone()
        return result
    
    def deposit(self,acc_id,amount):
        if amount <= 0:
            return False,"Amount must be greater than zero"
        account = self.find_account(acc_id)
        if account is None:
            return False,f"Account {acc_id} not found"
        new_balance = account[2] + amount
        cursor.execute("Update accounts set balance = %s where acc_id = %s",(new_balance,acc_id))
        cursor.execute("Insert into transactions (trans_acc_id,type,amount) values(%s,%s,%s)",(acc_id,"deposit",amount))
        conn.commit()
        return True,f"Amount {amount} deposited successfully.Current Balance: {new_balance}"

    def withdraw(self,acc_id,amount):
        if amount <= 0:
            return False,"Amount must be greater than 0"
        account = self.find_account(acc_id)
        if account is None:
            return False,f"Account {acc_id} not found"
        if amount > account[2]:
            return False,"Insufficient Balance"
        new_balance = account[2] - amount
        cursor.execute("Update accounts set balance = %s where acc_id = %s",(new_balance,acc_id))
        cursor.execute("Insert into transactions(trans_acc_id,type,amount) values(%s,%s,%s)",(acc_id,"withdraw",amount))
        conn.commit()
        return True,f"Amount {amount} withdrawn successfully.Current Balance:{new_balance}"
    
    def transfer(self,send_id,rec_id,amount):
        if amount <= 0:
            return False,"Amount should be greater than 0"
        if send_id == rec_id:
            return False,"Cannot transfer to the same account"
        sender= self.find_account(send_id)
        reciever = self.find_account(rec_id)
        if sender is None:
            return False,f"Sender Account{send_id} not found"
        if reciever is None:
            return False,f"Reciever Account{rec_id} not found"
        if amount>sender[2]:
            return False,"Insufficient Balance!"
        sender_balance = sender[2] - amount
        reciever_balance = reciever[2] + amount
        cursor.execute("Update accounts set balance = %s where acc_id = %s",(sender_balance,send_id))
        cursor.execute("Update accounts set balance = %s where acc_id = %s",(reciever_balance,rec_id))
        cursor.execute("Insert into transactions(trans_acc_id,related_acc_id,type,amount) values (%s,%s,%s,%s)",(send_id,rec_id,"transfer",amount))
        conn.commit()
        return True,f"Transferred Successfully!"
    
    def check_balance(self,acc_id):
        account = self.find_account(acc_id)
        if account is None:
            return False,f"Account {acc_id} doesnt exist"
        return True,f"Account: {account[0]} | Name: {account[1]} | Balance: {account[2]} "
        