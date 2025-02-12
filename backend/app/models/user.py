class User ():
    def __init__(
        self,
        first_name,
        last_name,
        email,
        password,
        is_admin=False,
    ) -> None:
        super().__init__()
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.password: str = password
        self.is_admin: bool = is_admin