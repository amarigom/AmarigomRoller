import os
import sys
from types import SimpleNamespace as NS

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from extensions import db
from models import PiezaStock, Supply, SupplyCategory
from tests.helpers import crear_receta
from services.costeo import calcular_explosion
from strategies.costing import ComponentInput, WidthLinearStrategy

PRECIO_CM = 50.0


def insumo(unidad='cm', precio=PRECIO_CM, name='Tubo 32 x 4 mts', largo=400):
    return NS(name=name, unidad_medida=unidad, precio_costo_unitario=precio, largo_pieza_cm=largo)


def componente(tipo, ins, id_insumo=1, dw=0, dh=0, base=1, merma=0, minutos=0):
    return NS(insumo=ins, id_insumo=id_insumo, nombre_producto='x', tipo_calculo=tipo,
              delta_ancho_cm=dw, delta_alto_cm=dh, cantidad_base=base,
              merma_pct=merma, minutos_mano_obra=minutos)


def sobrante(id_, largo):
    return NS(id=id_, longitud_actual_cm=largo)


# --- Unidades -------------------------------------------------------------------------

def test_espagueti_por_metro_consume_en_metros():
    ins = insumo('metro', 70, 'Espagueti', largo=20000)
    res, total = calcular_explosion([componente('lineal_ancho', ins, dw=1)], {}, 149, 200)
    assert res[0]['consumo_m_o_m2'] == 1.5
    assert total == 105.0


def test_cinta_por_rollo_de_50_m():
    ins = insumo('rollo', 18000, 'Cinta doble faz (50 mts)', largo=5000)
    res, total = calcular_explosion([componente('lineal_ancho', ins)], {}, 150, 200)
    assert res[0]['consumo_m_o_m2'] == 0.03
    assert total == 540.0


def test_rollo_sin_largo_de_pieza_da_error_claro():
    ins = insumo('rollo', 18000, 'Cinta', largo=None)
    with pytest.raises(Exception) as exc:
        WidthLinearStrategy().calculate(ComponentInput(
            nombre='Cinta', unidad='rollo', precio_unitario=1, ancho_corte=100, alto_corte=100))
    assert 'largo_pieza_cm' in str(exc.value)


# --- Perfiles ---------------------------------------------------------------------------

def test_perfil_corta_pieza_nueva_y_guarda_sobrante_reutilizable():
    res, total = calcular_explosion([componente('perfil', insumo())], {}, 148.5, 200)
    r = res[0]
    assert r['metodo'] == 'PERFIL'
    assert r['consumo_m_o_m2'] == 148.5
    assert total == round(148.5 * PRECIO_CM, 2)
    corte = r['cortes'][0]
    assert corte['origen'] == 'pieza_nueva'
    assert corte['sobrante'] == 251.5 and corte['reutilizable']


def test_perfil_sobrante_menor_al_minimo_se_descarta_y_se_cobra():
    res, total = calcular_explosion([componente('perfil', insumo())], {}, 350, 200)
    assert res[0]['cortes'][0]['reutilizable'] is False
    assert res[0]['consumo_m_o_m2'] == 400
    assert total == 400 * PRECIO_CM


def test_perfil_usa_sobrante_existente_antes_que_pieza_nueva():
    res, total = calcular_explosion(
        [componente('perfil', insumo())], {}, 148.5, 200,
        sobrantes_perfil={1: [sobrante(10, 300), sobrante(11, 160)]})
    corte = res[0]['cortes'][0]
    assert corte['origen'] == 'retazo' and corte['id_pieza'] == 11
    assert corte['sobrante'] == 11.5 and corte['reutilizable'] is False
    assert res[0]['consumo_m_o_m2'] == 160


def test_perfil_dos_componentes_reutilizan_el_sobrante_del_primero():
    comps = [componente('perfil', insumo()), componente('perfil', insumo())]
    res, total = calcular_explosion(comps, {}, 150, 200)
    assert res[0]['cortes'][0]['origen'] == 'pieza_nueva'
    assert res[1]['cortes'][0]['origen'] == 'retazo'
    assert res[1]['cortes'][0]['tok_origen'] == res[0]['cortes'][0]['tok_sobrante']


def test_perfil_varios_cortes_por_componente():
    res, _ = calcular_explosion([componente('perfil', insumo(), base=2)], {}, 150, 200)
    origenes = [c['origen'] for c in res[0]['cortes']]
    assert origenes == ['pieza_nueva', 'retazo']


def test_perfil_mas_largo_que_la_pieza_usa_varias_piezas():
    res, _ = calcular_explosion([componente('perfil', insumo(largo=200))], {}, 250, 200)
    corte = res[0]['cortes'][0]
    assert corte['largo_origen'] == 400 and corte['sobrante'] == 150


def test_perfil_respeta_largos_de_2_4_y_6_metros():
    for largo in (200, 400, 600):
        res, _ = calcular_explosion([componente('perfil', insumo(largo=largo))], {}, 150, 200)
        assert res[0]['cortes'][0]['largo_origen'] == largo


# --- Merma y mano de obra ---------------------------------------------------------------

def test_merma_aumenta_consumo_y_costo():
    ins = insumo('metro', 1000, 'Tela', largo=None)
    res, total = calcular_explosion([componente('lineal_alto', ins, merma=5)], {}, 150, 200)
    assert res[0]['consumo_m_o_m2'] == 2.1
    assert total == 2100.0


def test_mano_de_obra_se_informa_por_componente():
    ins = insumo('unidad', 0, 'Armado', largo=None)
    res, total = calcular_explosion([componente('mano_obra', ins, id_insumo=None, minutos=25)], {}, 150, 200)
    assert res[0]['minutos'] == 25 and total == 0.0


# --- API ------------------------------------------------------------------------------------

def _seed_perfil(stock_cm=1200):
    cat = SupplyCategory(name="Perfiles")
    db.session.add(cat)
    db.session.flush()
    tubo = Supply(categoria_id=cat.id, name="Tubo 32 x 4 mts", unidad_medida="cm",
                  precio_costo_unitario=PRECIO_CM, stock_actual=stock_cm, largo_pieza_cm=400)
    db.session.add(tubo)
    db.session.flush()
    crear_receta(1, [
        dict(id_insumo=tubo.id, nombre="Tubo", tipo_calculo="perfil", delta_ancho_cm=-1.5),
        dict(id_insumo=None, nombre="Armado", tipo_calculo="mano_obra", minutos_mano_obra=30),
    ])
    return tubo


def test_explosion_incluye_mano_de_obra_y_total(client, auth, app):
    app.config['COSTO_MINUTO_MANO_OBRA'] = 10
    _seed_perfil()
    r = client.get("/api/test-recipe/1?w=150&h=200", headers=auth("ventas"))
    assert r.status_code == 200, r.get_json()
    body = r.get_json()
    assert body['total_minutos'] == 30
    assert body['total_mano_obra'] == 300.0
    assert body['total'] == body['total_materiales'] + 300.0


def test_producir_perfil_guarda_sobrante_y_la_siguiente_lo_aprovecha(client, auth):
    tubo = _seed_perfil()
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert r.status_code == 200, r.get_json()
    assert r.get_json()['retazos_perfil_generados'] == 1
    db.session.expire_all()
    # corte de 148.5 con sobrante reutilizable: solo se descuenta lo cortado
    assert float(db.session.get(Supply, tubo.id).stock_actual) == 1200 - 148.5
    sobrantes = PiezaStock.query.filter_by(es_retazo=True).all()
    assert len(sobrantes) == 1 and float(sobrantes[0].longitud_actual_cm) == 251.5

    again = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert again.status_code == 200
    assert again.get_json()['retazos_perfil_generados'] == 0
    db.session.expire_all()
    sobrantes = PiezaStock.query.filter_by(es_retazo=True).all()
    assert len(sobrantes) == 1 and float(sobrantes[0].longitud_actual_cm) == 103.0


def test_producir_perfil_sin_stock_no_guarda_sobrantes(client, auth):
    _seed_perfil(stock_cm=100)
    r = client.post("/api/recipes/1/produce", json={"w": 150, "h": 200}, headers=auth("taller"))
    assert r.status_code == 409
    assert PiezaStock.query.count() == 0
