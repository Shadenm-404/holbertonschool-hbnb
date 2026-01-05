from app.models.user import User
from app.models.base_model import BaseModel
def test_user():
    user = User("sondos", "alrubaish", "sondos@example.com")
    assert user.first_name == "sondos"
    assert user.email == "sondos@example.com"
    assert user.is_admin is False
    print("User test passed")

if __name__ == "__main__":
    test_user()
