from extensions import db
from models import Product, Receta, Supply, SupplyCategory
from tests.helpers import crear_receta

CSV = (
    "producto;nombre;id_insumo;tipo_calculo;delta_ancho_cm;cantidad_base;merma_pct;condicion\n"
    "Roller Duo;Tubo;{tubo};perfil;-1,5;1;0;\n"
    "Roller Duo;Soporte central;{soporte};fijo;0;1;0;ancho > 200\n"
    "Roller Solar;Tubo;{tubo};perfil;-1,5;1;5;\n"
)


def _insumos():
    cat = SupplyCategory(name="Varios")
    db.session.add(cat)
    db.session.flush()
    tubo = Supply(categoria_id=cat.id, name="Tubo 4 mts", unidad_medida="cm", precio_costo_unitario=50,
                  stock_actual=2000, largo_pieza_cm=400)
    soporte = Supply(categoria_id=cat.id, name="Soporte", unidad_medida="unidad",
                     precio_costo_unitario=1000, stock_actual=20)
    db.session.add_all([tubo, soporte])
    db.session.commit()
    return tubo, soporte


def _items(tubo, soporte):
    return [
        {"id_insumo": tubo.id, "nombre": "Tubo", "tipo_calculo": "perfil", "delta_ancho_cm": -1.5},
        {"id_insumo": soporte.id, "nombre": "Soporte", "tipo_calculo": "fijo", "condicion": "ancho > 200"},
    ]


# --- Vista previa ---------------------------------------------------------------------------

def test_preview_calcula_sin_guardar(client, auth):
    tubo, soporte = _insumos()
    cuerpo = {"w": 250, "h": 200, "items": _items(tubo, soporte)}
    r = client.post("/api/recipes/preview", json=cuerpo, headers=auth("admin"))
    assert r.status_code == 200, r.get_json()
    datos = r.get_json()
    assert [e["componente"] for e in datos["explosion"]] == ["Tubo 4 mts", "Soporte", "Etiqueta"]
    assert datos["version"] is None
    assert Receta.query.count() == 0


def test_preview_valida_como_al_publicar(client, auth):
    tubo, soporte = _insumos()
    items = _items(tubo, soporte)
    items[1]["condicion"] = "ancho >"
    r = client.post("/api/recipes/preview", json={"items": items}, headers=auth("admin"))
    assert r.status_code == 400
    assert any("condicion" in d for d in r.get_json()["detalles"])


def test_publicacion_rechaza_unidades_y_formas_de_calculo_incompatibles(client, auth):
    tubo, soporte = _insumos()
    tubo.unidad_medida = 'unidad'
    tela = Supply(categoria_id=tubo.categoria_id, name='Tela', unidad_medida='metro',
                  precio_costo_unitario=100, stock_actual=10, ancho_cm=220, es_tela=True)
    db.session.add(tela)
    db.session.commit()
    crear_receta(1, [{'id_insumo': soporte.id, 'nombre': 'Soporte', 'tipo_calculo': 'fijo'}])
    h = auth('admin')
    for item in (
        {'id_insumo': tubo.id, 'nombre': 'Tubo', 'tipo_calculo': 'perfil'},
        {'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'superficie'},
        {'id_insumo': tela.id, 'nombre': 'Tela', 'tipo_calculo': 'lineal_alto', 'cantidad_base': 2},
    ):
        response = client.post('/api/recipes/1/versions', json={'items': [item]}, headers=h)
        assert response.status_code == 400, response.get_json()
    assert Receta.query.count() == 1


def test_duplicar_receta_historica_invalida_no_crea_producto(client, auth):
    _, soporte = _insumos()
    crear_receta(1, [{'id_insumo': soporte.id, 'nombre': 'Antiguo', 'tipo_calculo': 'superficie'}])
    response = client.post('/api/recipes/1/duplicate', headers=auth('admin'), json={'nombre': 'Copia inválida'})
    assert response.status_code == 400
    assert Product.query.filter_by(nombre='Copia inválida').first() is None


def test_preview_solo_admin(client, auth):
    tubo, soporte = _insumos()
    r = client.post("/api/recipes/preview", json={"items": _items(tubo, soporte)}, headers=auth("ventas"))
    assert r.status_code == 403


# --- Productos y detalle --------------------------------------------------------------------

def test_listado_de_productos_con_version_vigente(client, auth):
    tubo, soporte = _insumos()
    crear_receta(1, _items(tubo, soporte))
    db.session.add(Product(id=2, nombre="Sin receta"))
    db.session.commit()
    r = client.get("/api/recipes/products", headers=auth("ventas"))
    por_id = {p["id"]: p for p in r.get_json()}
    assert por_id[1]["version_vigente"] == 1 and por_id[1]["items"] == 2
    assert por_id[2]["version_vigente"] is None


def test_crear_producto_y_rechazar_nombre_repetido(client, auth):
    h = auth("admin")
    assert client.post("/api/recipes/products", json={"nombre": "Roller Nuevo"}, headers=h).status_code == 201
    r = client.post("/api/recipes/products", json={"nombre": "roller nuevo"}, headers=h)
    assert r.status_code == 409


def test_detalle_devuelve_todos_los_campos_editables(client, auth):
    tubo, soporte = _insumos()
    crear_receta(1, _items(tubo, soporte))
    items = client.get("/api/recipes/1/detail", headers=auth("ventas")).get_json()
    assert items[1]["condicion"] == "ancho > 200" and items[0]["insumo"] == "Tubo 4 mts"
    assert items[0]["delta_ancho_cm"] == -1.5


# --- Duplicar -------------------------------------------------------------------------------

def test_duplicar_crea_producto_con_la_misma_receta(client, auth):
    tubo, soporte = _insumos()
    crear_receta(1, _items(tubo, soporte))
    r = client.post("/api/recipes/1/duplicate", json={"nombre": "Roller Blackout"}, headers=auth("admin"))
    assert r.status_code == 201, r.get_json()
    nuevo = r.get_json()["producto"]["id"]
    copia = client.get(f"/api/recipes/{nuevo}/detail", headers=auth("admin")).get_json()
    assert [(i["nombre"], i["condicion"]) for i in copia] == [("Tubo", None), ("Soporte", "ancho > 200")]


def test_duplicar_con_nombre_existente_o_sin_receta(client, auth):
    tubo, soporte = _insumos()
    crear_receta(1, _items(tubo, soporte))
    h = auth("admin")
    assert client.post("/api/recipes/1/duplicate", json={"nombre": "Producto 1"}, headers=h).status_code == 409
    assert client.post("/api/recipes/99/duplicate", json={"nombre": "X"}, headers=h).status_code == 404


# --- Importación CSV ------------------------------------------------------------------------

def _csv(tubo, soporte):
    return CSV.format(tubo=tubo.id, soporte=soporte.id)


def test_importar_sin_aplicar_solo_valida(client, auth):
    tubo, soporte = _insumos()
    r = client.post("/api/recipes/import", json={"csv": _csv(tubo, soporte)}, headers=auth("admin"))
    assert r.status_code == 200, r.get_json()
    datos = r.get_json()
    assert datos["aplicado"] is False
    assert {p["producto"]: p["items"] for p in datos["productos"]} == {"Roller Duo": 2, "Roller Solar": 1}
    assert Product.query.count() == 0


def test_importar_aplicando_crea_productos_y_versiona_existentes(client, auth):
    tubo, soporte = _insumos()
    h = auth("admin")
    cuerpo = {"csv": _csv(tubo, soporte), "aplicar": True}
    assert client.post("/api/recipes/import", json=cuerpo, headers=h).status_code == 200
    duo = Product.query.filter_by(nombre="Roller Duo").one()
    items = client.get(f"/api/recipes/{duo.id}/detail", headers=h).get_json()
    assert items[0]["delta_ancho_cm"] == -1.5 and items[1]["condicion"] == "ancho > 200"

    r = client.post("/api/recipes/import", json=cuerpo, headers=h).get_json()
    assert {p["producto"]: p["version"] for p in r["productos"]} == {"Roller Duo": 2, "Roller Solar": 2}
    assert [v["version"] for v in client.get(f"/api/recipes/{duo.id}/versions", headers=h).get_json()] == [2, 1]


def test_importar_es_todo_o_nada(client, auth):
    tubo, soporte = _insumos()
    malo = _csv(tubo, soporte) + f"Roller Roto;Tubo;{tubo.id};inventado;0;1;0;\n"
    r = client.post("/api/recipes/import", json={"csv": malo, "aplicar": True}, headers=auth("admin"))
    assert r.status_code == 400
    assert any("Roller Roto" in d and "inventado" in d for d in r.get_json()["detalles"])
    assert Product.query.count() == 0 and Receta.query.count() == 0


def test_importar_informa_fila_y_columna_con_error(client, auth):
    csv = "producto;nombre;tipo_calculo;merma_pct\nRoller;Tubo;perfil;150\n"
    r = client.post("/api/recipes/import", json={"csv": csv}, headers=auth("admin"))
    assert r.status_code == 400
    assert any(d.startswith("Fila 2, merma_pct") for d in r.get_json()["detalles"])


def test_importar_rechaza_columnas_desconocidas_o_faltantes(client, auth):
    h = auth("admin")
    r = client.post("/api/recipes/import", json={"csv": "producto;nombre\nA;B\n"}, headers=h)
    assert "Faltan columnas" in r.get_json()["detalles"][0]
    r = client.post("/api/recipes/import", json={"csv": "producto;nombre;tipo_calculo;precio\nA;B;fijo;3\n"}, headers=h)
    assert "desconocidas" in r.get_json()["detalles"][0]


def test_importar_acepta_comas_y_bom(client, auth):
    tubo, soporte = _insumos()
    csv = f"\ufeffproducto,nombre,id_insumo,tipo_calculo\nRoller,Soporte,{soporte.id},fijo\n"
    r = client.post("/api/recipes/import", json={"csv": csv}, headers=auth("admin"))
    assert r.status_code == 200, r.get_json()


def test_plantilla_y_permisos(client, auth):
    assert client.get("/api/recipes/import/template", headers=auth("ventas")).get_json()["csv"].startswith("producto;")
    r = client.post("/api/recipes/import", json={"csv": "x"}, headers=auth("taller"))
    assert r.status_code == 403
