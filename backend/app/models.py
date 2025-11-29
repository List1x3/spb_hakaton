class User():
    id: int = 0
    username: str
    email: str
    password: int
    avatar: str
    def __init__(self, username, email, password, avatar = "default_avatar.jpg"):
        self.id = hash(username) ^ hash(email) ^ hash(password) ^ hash(avatar) #needed only without normal data base
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar