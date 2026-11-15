from datetime import datetime, timedelta, timezone

import jwt
import pytest

from conftest import PASSWORD, _crear_usuario
from extensions import db
from models import Supply, User


def test_login_ok_devuelve_token_rol_y_permisos(client):
    _crear_usuario("ventas")
    r = client.post("/api/auth/login", json={"email": "VENTAS@example.com", "password": PASSWORD})
    data = r.get_json()
    assert r.status_code == 200
    assert data["user"]["rol"] == "ventas"
    assert "clients:write" in data["permissions"] and "users:manage" not in data["permissions"]
    assert "password_hash" not in str(data)


def test_login_fallido_mensaje_generico(client):
    _crear_usuario("admin")
    mala = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "otra"})
    inexistente = client.post("/api/auth/login", json={"email": "no@example.com", "password": "otra"})
    assert mala.status_code == inexistente.status_code == 401
    assert mala.get_json()["message"] == inexistente.get_json()["message"]


def test_bloqueo_por_intentos(client):
    _crear_usuario("admin")
    body = {"email": "admin@example.com", "password": "mala"}
    assert [client.post("/api/auth/login", json=body).status_code for _ in range(3)] == [401, 401, 401]
    assert client.post("/api/auth/login", json=body).status_code == 429
    buena = {"email": "admin@example.com", "password": PASSWORD}
    assert client.post("/api/auth/login", json=buena).status_code == 429

    u = User.query.filter_by(email="admin@example.com").first()
    u.bloqueado_hasta = datetime.utcnow() - timedelta(seconds=1)
    db.session.commit()
    assert client.post("/api/auth/login", json=buena).status_code == 200


def test_usuario_inactivo_no_entra(client, auth):
    _crear_usuario("taller")
    u = User.query.filter_by(email="taller@example.com").first()
    u.activo = False
    db.session.commit()
    r = client.post("/api/auth/login", json={"email": "taller@example.com", "password": PASSWORD})
    assert r.status_code == 401


@pytest.mark.parametrize("url", ["/api/inventory", "/api/categories", "/api/clients", "/api/recipes/1", "/api/users"])
def test_sin_token_401(client, url):
    assert client.get(url).status_code == 401


def test_token_manipulado_o_expirado(client, app):
    u = _crear_usuario("admin")
    ahora = datetime.now(timezone.utc)
    expirado = jwt.encode({"sub": str(u.id), "iat": ahora, "exp": ahora - timedelta(minutes=1)},
                          "test-secret-test-secret-test-secret-123", algorithm="HS256")
    firmado_mal = jwt.encode({"sub": str(u.id), "exp": ahora + timedelta(hours=1)}, "otra", algorithm="HS256")
    sin_firma = jwt.encode({"sub": str(u.id), "exp": ahora + timedelta(hours=1)}, None, algorithm="none")
    for t in (expirado, firmado_mal, sin_firma, "basura"):
        assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {t}"}).status_code == 401


# rol -> estados esperados de: GET inventario, POST inventario, DELETE inventario, GET clientes, POST clientes, GET receta, GET usuarios
MATRIZ = {
    "admin":  (200, 201, 200, 200, 201, 404, 200),
    "ventas": (200, 403, 403, 200, 201, 404, 403),
    "taller": (200, 403, 403, 403, 403, 404, 403),
}


@pytest.mark.parametrize("rol", MATRIZ)
def test_matriz_de_permisos(client, auth, rol):
    from models import SupplyCategory
    db.session.add(SupplyCategory(name="Telas"))
    existente = Supply(categoria_id=1, name="Existente")
    db.session.add(existente)
    db.session.commit()
    h = auth(rol)
    insumo = {"name": "T", "categoria_id": 1, "codigo_sku": "A1"}
    cliente = {"nombre": "A", "apellido": "B", "email": "a@b.com"}
    obtenido = (
        client.get("/api/inventory", headers=h).status_code,
        client.post("/api/inventory", json=insumo, headers=h).status_code,
        client.delete(f"/api/inventory/{existente.id}", headers=h).status_code,
        client.get("/api/clients", headers=h).status_code,
        client.post("/api/clients", json=cliente, headers=h).status_code,
        client.get("/api/recipes/1", headers=h).status_code,
        client.get("/api/users", headers=h).status_code,
    )
    assert obtenido == MATRIZ[rol]


def test_rol_cambiado_aplica_de_inmediato(client, auth):
    h = auth("admin")
    u = User.query.filter_by(email="admin@example.com").first()
    otro = _crear_usuario("taller", "otro@example.com")
    h_taller = {"Authorization": "Bearer " + client.post(
        "/api/auth/login", json={"email": "otro@example.com", "password": PASSWORD}).get_json()["token"]}
    assert client.get("/api/inventory", headers=h_taller).status_code == 200
    r = client.patch(f"/api/users/{otro.id}", json={"activo": False}, headers=h)
    assert r.status_code == 200
    assert client.get("/api/inventory", headers=h_taller).status_code == 401


def test_admin_gestiona_usuarios(client, auth):
    h = auth("admin")
    nuevo = {"email": "Nuevo@Example.com", "nombre": "Nuevo", "password": PASSWORD, "rol": "ventas"}
    r = client.post("/api/users", json=nuevo, headers=h)
    assert r.status_code == 201 and r.get_json()["email"] == "nuevo@example.com"
    assert client.post("/api/users", json=nuevo, headers=h).status_code == 409
    assert client.post("/api/users", json={**nuevo, "email": "x@example.com", "password": "corta"}, headers=h).status_code == 400
    assert client.post("/api/users", json={**nuevo, "email": "y@example.com", "rol": "root"}, headers=h).status_code == 400
    assert client.patch("/api/users/9999", json={"nombre": "Z"}, headers=h).status_code == 404


def test_no_se_puede_dejar_sin_admins(client, auth):
    h = auth("admin")
    admin_id = User.query.filter_by(email="admin@example.com").first().id
    assert client.patch(f"/api/users/{admin_id}", json={"activo": False}, headers=h).status_code == 409
    assert client.patch(f"/api/users/{admin_id}", json={"rol": "ventas"}, headers=h).status_code == 409
    segundo = _crear_usuario("admin", "admin2@example.com")
    assert client.patch(f"/api/users/{segundo.id}", json={"rol": "ventas"}, headers=h).status_code == 200


def test_cambiar_password(client, auth):
    h = auth("ventas")
    assert client.post("/api/auth/change-password", json={"actual": "mala", "nueva": "otra-clave-larga-1"}, headers=h).status_code == 401
    assert client.post("/api/auth/change-password", json={"actual": PASSWORD, "nueva": "corta"}, headers=h).status_code == 400
    assert client.post("/api/auth/change-password", json={"actual": PASSWORD, "nueva": "otra-clave-larga-1"}, headers=h).status_code == 200
    r = client.post("/api/auth/login", json={"email": "ventas@example.com", "password": "otra-clave-larga-1"})
    assert r.status_code == 200


