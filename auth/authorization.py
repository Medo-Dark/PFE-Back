from fastapi import Depends, Request, HTTPException, status
from auth.authentication import get_current_user
from schemas.user import User, RolesEnum


def check_permissions(request: Request, user: User = Depends(get_current_user)):
    allowed_roles = get_allowed_roles(request)

    if user:
        if user.role in allowed_roles:
            return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have enough permissions"
    )


def get_allowed_roles(request: Request):
    path = request.url.path.lstrip('/')
    allowed_roles = []

    if path == 'users/all':
        allowed_roles = [RolesEnum.ADMIN]

    if path == 'users/me' or path == 'users/{resource_id}':
        allowed_roles = [RolesEnum.ADMIN, RolesEnum.SUPERVISEUR, RolesEnum.MANAGER, RolesEnum.ZONE_LEADER]

    # if path.startswith('users'):
    #     allowed_roles.append(RolesEnum.ADMIN)

    # if (
    #         path.startswith('rapport')
    # ):
    #     allowed_roles.append(RolesEnum.MANAGER)
    #     allowed_roles.append(RolesEnum.SUPERVISEUR)

    return allowed_roles
