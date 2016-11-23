class UserRoles(object):
    READER = 1
    CONTRIBUTOR = 2
    MANAGEMENT = 3

    USER_GROUPS_CHOICES = (
        (READER, 'Cititor'),
        (CONTRIBUTOR, 'Contributor'),
        (MANAGEMENT, 'Manager'),
    )
