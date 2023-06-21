from jsondb import JSONDATABASE


class Data:
    def __init__(self):
        self.db = JSONDATABASE("jsons/data.json")

    def set_auth_token(self, token):
        tokens = self.db.get_field("user_tokens")
        if tokens is None:
            tokens = []
        tokens.append(token)
        self.db.save_field("user_tokens", tokens)

    def has_auth_token(self, token):
        tokens = self.db.get_field("user_tokens")
        if tokens is None:
            return False
        if token in tokens:
            return True
        else:
            return False

    def delete_auth_token(self, token):
        tokens = self.db.get_field("user_tokens")
        if tokens is not None:
            tokens.remove(token)
            self.db.save_field("user_tokens", tokens)
