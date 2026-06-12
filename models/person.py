class Person:
    """Base class for people in the system."""
    def __init__(self, name: str, email: str | None = None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name!r}, email={self.email!r})"
