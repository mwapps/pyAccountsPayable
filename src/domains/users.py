
class User:
    def __init__(self, user_id, user_name, user_email, user_pass):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_pass = user_pass

    def __str__(self):
        return '{"' \
        + 'user_id' + '": ' + str(self.user_id) + ', "' \
        + 'user_name' + '": ' + str(self.user_name) + ',"' \
        + 'user_email' + '": "' + str(self.user_email) + '", "' \
        + 'user_pass' + '": "' + self.user_pass + '"}'

    def jsonObject(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_email': self.user_email
        }
