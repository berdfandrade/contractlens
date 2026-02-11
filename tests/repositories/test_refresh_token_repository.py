import pytest

from app.repositories.refresh_token import RefreshTokenRepository


@pytest.mark.asyncio
async def test_save_and_get_token(test_db):
    repo = RefreshTokenRepository(test_db)
    await repo.save_token("user123", "token123")
    token = await repo.get_token("token123")
    assert token is not None
    assert token["user_id"] == "user123"
    assert token["token"] == "token123"


@pytest.mark.asyncio
async def test_delete_token(test_db):
    repo = RefreshTokenRepository(test_db)
    await repo.save_token("user123", "token_delete")
    await repo.delete_token("token_delete")
    token = await repo.get_token("token_delete")
    assert token is None


@pytest.mark.asyncio
async def test_rotate_token(test_db):
    repo = RefreshTokenRepository(test_db)
    await repo.save_token("user123", "old_token")
    await repo.rotate_token("old_token", "new_token")

    old = await repo.get_token("old_token")
    new = await repo.get_token("new_token")

    assert old is None
    assert new is not None
    assert new["token"] == "new_token"


@pytest.mark.asyncio
async def test_get_token_not_found(test_db):

    repo = RefreshTokenRepository(test_db)
    token = await repo.get_token("ghost_token")
    assert token is None
