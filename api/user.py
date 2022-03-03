import yaml


def does_user_exist(user_id):
    with open('data.yaml', 'r') as f:
        loaded = yaml.load(f.read(), Loader=yaml.FullLoader)

    users = loaded['users']

    if int(user_id) in users:
        return True
    else:
        return False


def get_permissions(group):
    with open('permissions.yaml', 'r') as f:
        loaded = yaml.load(f.read(), Loader=yaml.FullLoader)

    groups = loaded['groups']

    if group in groups:
        return groups[group]
    else:
        return groups['default']


def get_user(user_id):
    with open('data.yaml', 'r') as f:
        loaded = yaml.load(f.read(), Loader=yaml.FullLoader)

    return loaded['users'][int(user_id)]


class User:
    id = None
    username = None
    discrim = None
    avatar = None
    permissions = []
    rank = None

    def __init__(self, user_id, user_data):
        self.id = user_id
        self.rank = get_user(user_id)['group']
        self.permissions = get_permissions(self.rank)
        self.username = user_data['username']
        self.discrim = user_data['discriminator']
        self.avatar = user_data['avatar']

    def has_permission(self, perm):

        for x in self.permissions:
            if x == "*":
                return True

            if (x == "litebans.*" or x == "coreprotect.*") and ("litebans" in perm or "coreprotect" in perm):
                return True

            if (x == "litebans.view.*" or x == "coreprotect.lookup.*") and (
                    "litebans.view" in perm or "coreprotect.lookup" in perm):
                return True

            if x == perm:
                return True

        return False

    def to_dict(self):
        data = {
            'username': self.username,
            'id': self.id,
            'discriminator': self.discrim,
            'avatar': self.avatar,
            'panel': {
                'rank': self.rank,
                'permissions': self.permissions
            }
        }
        return data
