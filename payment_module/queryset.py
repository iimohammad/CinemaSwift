from db.database_manager import DatabaseManager

database_manager = DatabaseManager()


def check_bank_account_query(account_userid, account_name):
    query = f"""SELECT count(id) FROM bankaccounts
                    WHERE
                    user_id = '{account_userid}' AND name = '{account_name}'; """
    result = database_manager.execute_query_select(query)
    return result


def add_bank_account_query(data):
    query = """INSERT INTO `bankaccounts` (`user_id`, `name`, `balance`, `cvv2`, `password`)
                    VALUES
                    (%(user_id)s, %(name)s, %(balance)s, %(cvv2)s, %(password)s);"""
    database_manager.execute_query(query, data)


def get_bank_accounts_query(user_id):
    query = f"""SELECT name FROM cinemaswift.bankaccounts
                    WHERE
                    user_id = '{user_id}';"""
    r = database_manager.execute_query_select(query)


def get_bank_accounts_balance_query(user_id, account_name):
    query = f"""SELECT cvv2,password,name,balance FROM bankaccounts
                    WHERE user_id = '{user_id}' AND name = '{account_name}';"""
    result = database_manager.execute_query_select(query)
    return result


def deposit_to_bank_account_query(user_id, account_name):
    query = f"""SELECT id,balance FROM bankaccounts
                    WHERE
                    user_id = '{user_id}' AND name = '{account_name}';"""
    result = database_manager.execute_query_select(query)
    return result


def update_balance_query(id_bank,balance,amount):
    query = f"""UPDATE `bankaccounts` SET `balance` = '{
    balance + amount}' WHERE (`id` = '{id_bank}');"""
    database_manager.execute_query(query)


def harvest_from_account(account_name, user_id):
    query = f"""SELECT * FROM bankaccounts
                    WHERE user_id = '{user_id}' AND name = '{account_name}';"""
    result = database_manager.execute_query_select(query)
    return result


def update_new_balance_query(id, balance, amount):
    query = f"""UPDATE `bankaccounts` SET `balance` = '{
    balance - amount}'
                    WHERE
                    (`id` = '{id}');"""
    database_manager.execute_query(query)


def get_wallet_query(user_id):
    query = f"SELECT * FROM wallets WHERE user_id = '{user_id}'"
    result = database_manager.execute_query_select(query)
    return result


def select_wallet_query(user_id):
    query = f"SELECT id FROM wallets WHERE user_id = '{user_id}'"
    r = database_manager.execute_query_select(query)


def add_wallet_query(user_id):
    query = f"INSERT INTO wallets  (user_id, balance) VALUES ('{
    user_id}', 0);"
    database_manager.execute_query(query)


def update_wallet(balance, wallet_id):
    query = f"UPDATE `wallets` SET `balance` = '{
    balance}' WHERE (`id` = '{wallet_id}');"
    database_manager.execute_query(query)