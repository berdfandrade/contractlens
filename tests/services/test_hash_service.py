from app.services.hash import HashService


def test_hash_password_generates_hash():
    service = HashService()

    password = "123456"
    hashed = service.hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)
    assert hashed.startswith("$argon2")


def test_verify_password_success():
    service = HashService()

    password = "123456"
    hashed = service.hash_password(password)

    result = service.verify_password(password, hashed)

    assert result is True


def test_verify_password_wrong_password():
    service = HashService()

    hashed = service.hash_password("correct")

    result = service.verify_password("wrong", hashed)

    assert result is False


def test_hash_password_generates_different_hashes_for_same_password():
    service = HashService()

    password = "123456"

    hash1 = service.hash_password(password)
    hash2 = service.hash_password(password)

    assert hash1 != hash2
