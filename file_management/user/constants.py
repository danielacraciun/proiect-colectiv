class UserRoles(object):
    READER = 1
    CONTRIBUTOR = 2
    MANAGEMENT = 3
    ADMIN = 4

    USER_GROUPS_CHOICES = (
        (READER, 'Cititor'),
        (CONTRIBUTOR, 'Contribuitor'),
        (MANAGEMENT, 'Manager'),
        (ADMIN, 'Administrator')
    )
