class Account:
    def __init__(self, name, account_id):
        self.name = name
        self.account_id = account_id

    def __repr__(self):
        return f"{self.name} ({self.account_id})"
