import pandas


# This class stores user information in an easily accessible object, and generates their URL link
class User:
    def __init__(self, id, name, currency_thing = False):
        self.id         = int(id)
        self.name       = str(name)
        self.url        = f'<a href="/@{name}">{name}</a>'
        self.mention    = f'<@{id}>'
        self.avatar     = "www.avatar.com"

        # Currency Thing redirects back to the main page
        if currency_thing: self.url = f'<a href="/">{name}</a>'
    
    def __repr__(self):                                                                     # this is what gets output in the console when you print the object. cool! -> https://www.pythontutorial.net/python-oop/python-__repr__/
        return f'User: {self.id} | {self.name} | {self.url}'



# creates a dictionary to lookup a user value and replace it with another
def replace_thing(key, value):
    replace = {}
    for user in USERS:
        dict = {
        "id"        : user.id,
        "mention"   : user.mention,
        "name"      : user.name,
        "url"       : user.url
        }
        replace[dict[key]] = dict[value]
    
    return replace

# Gets a User object by name
def get_user(name: str):
        for user in USERS:
            if(user.name == name):
                return user


# Creates a User object for each user in the users.csv file
def create_users():
    users_df = pandas.read_csv('users.csv', index_col=0)
    users = []
    for id, row in users_df.iterrows():
        u = User(id, row['Username'])
        users.append(u)
    
    return users

# List of all User instances - hardcoding in the ID of the Currency Thing bot
USERS = [User(840976021687762955, 'Currency Thing', True)] + create_users()


# the thing
if (__name__ == "__main__"):
    print ("Executed when invoked directly")
    print(replace_thing("mention", "url"))
    print(USERS)
else:
    print ("[USERS.PY IMPORTED]")