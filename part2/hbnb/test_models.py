#!/usr/bin/python3
from app.models.user import User

# --- Robust imports (handles BaseModel.py vs base_model.py) ---
try:
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
except ModuleNotFoundError as e:
    raise SystemExit(f"Import error. Check your package structure and file names.\nDetails: {e}")


def print_section(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_user_creation():
    print_section("TEST 1: User creation")
    u = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert u.first_name == "John"
    assert u.last_name == "Doe"
    assert u.email == "john.doe@example.com"
    assert u.is_admin is False
    assert isinstance(u.id, str) and len(u.id) > 0
    print("✅ User creation passed")
    return u


def test_amenity_creation():
    print_section("TEST 2: Amenity creation")
    a = Amenity(name="Wi-Fi")
    assert a.name == "Wi-Fi"
    assert isinstance(a.id, str) and len(a.id) > 0
    print("✅ Amenity creation passed")
    return a


def test_place_creation(owner):
    print_section("TEST 3: Place creation")
    p = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=24.7136,
        longitude=46.6753,
        owner=owner
    )
    assert p.title == "Cozy Apartment"
    assert p.price == 100.0
    assert p.owner is owner
    assert isinstance(p.reviews, list) and len(p.reviews) == 0
    assert isinstance(p.amenities, list) and len(p.amenities) == 0
    print("✅ Place creation passed")
    return p


def test_review_creation(place, user):
    print_section("TEST 4: Review creation + add_review relationship")
    r = Review(text="Great stay!", rating=5, place=place, user=user)
    assert r.text == "Great stay!"
    assert r.rating == 5
    assert r.place is place
    assert r.user is user

    # Check updated_at changes after adding a review
    old_updated = place.updated_at
    sleep(0.01)  # tiny delay so timestamp changes reliably
    place.add_review(r)
    assert len(place.reviews) == 1
    assert place.reviews[0] is r
    assert place.updated_at > old_updated
    print("✅ Review creation + place.add_review passed")
    return r


def test_amenity_relationship(place, amenity):
    print_section("TEST 5: Amenity relationship + add_amenity")
    old_updated = place.updated_at
    sleep(0.01)
    place.add_amenity(amenity)

    assert len(place.amenities) == 1
    assert place.amenities[0] is amenity
    assert place.updated_at > old_updated

    # If your Place.add_amenity avoids duplicates, this should stay 1
    place.add_amenity(amenity)
    assert len(place.amenities) == 1
    print("✅ place.add_amenity passed (and duplicate check if implemented)")


def test_to_dict_outputs(user, place, review, amenity):
    print_section("TEST 6: to_dict outputs")
    ud = user.to_dict()
    pd = place.to_dict()
    rd = review.to_dict()
    ad = amenity.to_dict()

    # User dict
    assert "id" in ud and "created_at" in ud and "updated_at" in ud

    # Place dict
    assert pd["owner_id"] == user.id
    assert amenity.id in pd["amenity_ids"]
    assert review.id in pd["review_ids"]
    assert "created_at" in pd and "updated_at" in pd

    # Review dict
    assert rd["user_id"] == user.id
    assert rd["place_id"] == place.id
    assert "created_at" in rd and "updated_at" in rd

    # Amenity dict
    assert "created_at" in ad and "updated_at" in ad

    print("✅ to_dict checks passed")


def test_validation_errors():
    print_section("TEST 7: Validation errors (expected failures)")

    # Invalid email
    try:
        User(first_name="A", last_name="B", email="not-email")
        raise AssertionError("❌ Expected ValueError for invalid email")
    except ValueError:
        print("✅ invalid email rejected")

    # Invalid rating
    u = User(first_name="A", last_name="B", email="a@b.com")
    p = Place(title="T", description="", price=10, latitude=0, longitude=0, owner=u)
    try:
        Review(text="ok", rating=10, place=p, user=u)
        raise AssertionError("❌ Expected ValueError for invalid rating")
    except ValueError:
        print("✅ invalid rating rejected")

    # Invalid price
    try:
        Place(title="T", description="", price=0, latitude=0, longitude=0, owner=u)
        raise AssertionError("❌ Expected ValueError for non-positive price")
    except ValueError:
        print("✅ non-positive price rejected")


def main():
    owner = test_user_creation()
    amenity = test_amenity_creation()
    place = test_place_creation(owner)
    review = test_review_creation(place, owner)
    test_amenity_relationship(place, amenity)
    test_to_dict_outputs(owner, place, review, amenity)
    test_validation_errors()

    print_section("ALL TESTS PASSED ✅")


if __name__ == "__main__":
    main()
