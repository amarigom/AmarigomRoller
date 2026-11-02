"""Permisos por rol. Los endpoints piden un permiso, nunca un rol concreto."""

INVENTORY_READ = 'inventory:read'
INVENTORY_WRITE = 'inventory:write'
INVENTORY_DELETE = 'inventory:delete'
CLIENTS_READ = 'clients:read'
CLIENTS_WRITE = 'clients:write'
RECIPES_READ = 'recipes:read'
USERS_MANAGE = 'users:manage'

ALL_PERMISSIONS = frozenset({
    INVENTORY_READ, INVENTORY_WRITE, INVENTORY_DELETE,
    CLIENTS_READ, CLIENTS_WRITE, RECIPES_READ, USERS_MANAGE,
})

ROLE_PERMISSIONS = {
    'admin': ALL_PERMISSIONS,
    'ventas': frozenset({INVENTORY_READ, CLIENTS_READ, CLIENTS_WRITE, RECIPES_READ}),
    'taller': frozenset({INVENTORY_READ, INVENTORY_WRITE, RECIPES_READ}),
}


def permissions_for(role):
    return ROLE_PERMISSIONS.get(role, frozenset())


def has_permission(role, permission):
    return permission in permissions_for(role)
