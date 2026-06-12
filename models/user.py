from .person import Person


class User(Person):
    _id_counter = 1

    def __init__(self, name: str, email: str | None = None, id: int | None = None):
        """Initialize a User.

        If `id` is omitted an auto-incremented id is assigned.
        """
        super().__init__(name, email)
        if id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = id

    def to_dict(self):
        """Serialize the user to a dictionary for JSON storage."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, d):
        """Create a User instance from a dictionary.

        Also ensures the class id counter is advanced when loading persisted ids.
        """
        u = cls(name=d.get("name"), email=d.get("email"), id=d.get("id"))
        if d.get("id") and d.get("id") >= cls._id_counter:
            cls._id_counter = d.get("id") + 1
        return u

    def __repr__(self):
        """Return a concise representation for CLI output."""
        return f"User(id={self.id}, name={self.name})"
