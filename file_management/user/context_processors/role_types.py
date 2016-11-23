from user.constants import UserRoles


def user_roles(request):
    return {
        'READER': UserRoles.READER,
        'CONTRIBUTOR': UserRoles.CONTRIBUTOR,
        'MANAGEMENT': UserRoles.MANAGEMENT,
        'ADMIN': UserRoles.ADMIN,
    }
