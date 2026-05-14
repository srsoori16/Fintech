from flask import Flask, request, jsonify
from bank import Bank

bank = Bank()

def configure_routes(app):
    @app.route("/account/create", methods=["POST"])
    def create_account():
        data = request.get_json()   # gets JSON input
        name = data["name"]         # extracts name
        success, msg = bank.create_account(name)
        return jsonify({"success": success, "message": msg})

    @app.route("/account/deposit", methods=["POST"])
    def deposit():
        data = request.get_json()
        amount = data["amount"]
        acc_id = data["acc_id"]
        success, msg = bank.deposit(acc_id,amount)
        return jsonify({"success" : success,"message": msg})

    @app.route("/account/withdraw", methods=["POST"])
    def withdraw():
        data = request.get_json()
        amount = data["amount"]
        acc_id = data["acc_id"]
        success, msg = bank.withdraw(acc_id,amount)
        return jsonify({"success" : success,"message": msg})
    
    @app.route("/account/transfer", methods=["POST"])
    def transfer():
        data = request.get_json()
        rec_acc_id = data["reciever"]
        send_acc_id = data["sender"]
        amount = data["amount"]
        success, msg = bank.transfer(send_acc_id,rec_acc_id,amount)
        return jsonify({"success" : success,"message": msg})
    
    @app.route("/account/check_balance/<int:acc_id>", methods=["GET"])
    def Check_balance(acc_id):
        account = bank.find_account(acc_id)
        acc_id = account[0]
        success, msg = bank.check_balance(acc_id)
        return jsonify({"success" : success,"message": msg})