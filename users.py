from jsondb import JSONDATABASE


class Settings:
    admin = False
    channel_id: int = 0
    valid_user = False
    hours = 0

    def __init__(self, settings: dict):
        if 'admin' in settings:
            self.admin = settings['admin']
        if 'channel_id' in settings:
            self.channel_id = settings['channel_id']
        if 'valid_user' in settings:
            self.valid_user = settings['valid_user']
        if 'hours' in settings:
            self.hours = settings['hours']

    def dump(self):
        return {
            'admin': self.admin,
            'channel_id': self.channel_id,
            'valid_user': self.valid_user,
            'hours': self.hours
        }


class User:
    settings: Settings = None

    def __init__(self, user_id: str, database: JSONDATABASE):
        self.user_id = user_id
        self.database = database
        user = self.database.get_field(user_id)
        if user is None:
            user = {}
        if 'settings' in user:
            self.settings = Settings(user['settings'])
        else:
            self.settings = Settings({})

    def save(self):
        user = {
            'settings': self.settings.dump()
        }
        self.database.save_field(self.user_id, user)


class Users:
    def __init__(self):
        self.db = JSONDATABASE("jsons/users.json")

    def user(self, user_id: str | int):
        return User(str(user_id), self.db)

    def get_all_users(self):
        users = []
        for user_id in self.db.read().keys():
            users.append(User(str(user_id), self.db))
        return users
