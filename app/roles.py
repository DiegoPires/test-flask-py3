from flask import g
from flask.ext.principal import Principal, Identity, Permission, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, ActionNeed
from collections import namedtuple
from functools import partial


# Needs
be_admin = RoleNeed('admin')
be_desktop_client = RoleNeed('desktop_client')
be_online_client = RoleNeed('online_client')
to_sign_in = ActionNeed('sign in')

# Permissions
user = Permission(to_sign_in)
user.description = "User's permissions"
admin = Permission(be_admin)
admin.description = "Admin's permissions"
desktop_client = Permission(be_desktop_client)
desktop_client.description = "Desktop client's permission"
online_client = Permission(be_online_client)
online_client.description = "Online client's permissions"

apps_needs = [be_admin, be_desktop_client, be_online_client, to_sign_in]
apps_permissions = [user, admin, desktop_client, online_client]

#Permissions for more granular access control
modifyUser = namedtuple('user', ['method', 'value'])
modifyUserNeed = partial(modifyUser, 'modifyUser')


class modifyUserPermission(Permission):
    def __init__(self, id):
        need = modifyUser(unicode(id))
        super(modifyUserPermission, self).__init__(need)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    needs = []

    if identity.id in ('user', 'desktop_client', 'online_client', 'admin'):
        needs.append(to_sign_in)

    if identity.id in ('desktop_client', 'admin'):
        needs.append(be_desktop_client)

    if identity.id in ('online_client', 'admin'):
        needs.append(be_online_client)

    if identity.id == 'admin':
        needs.append(be_admin)

    # if the user has the attribute Id (it always has, but it's an example, a better example
    # could by addresses, for exemple.. if the user has adresses, then secury then...
    #if hasattr(g.current_user, 'id'):
        # lets just this user modify those guys, in this case, himself
    #    needs.append(modifyUser(unicode(g.current_user.id)))

    for n in needs:
        g.identity.provides.add(n)