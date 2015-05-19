# Dummy stub until a proper authentication/authorization schema surfaces

USERS = {'admin': 'admin',
         'listener': 'viewer'}
GROUPS = {'admin': ['group:admins']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
