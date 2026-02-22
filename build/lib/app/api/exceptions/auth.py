from fastapi import HTTPException, status


def invalid_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )


def user_already_exists():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already exists",
    )


def error_creating_user():
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error creating user",
    )


def unauthorized():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
