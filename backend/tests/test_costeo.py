import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.costeo import calcular_explosion
from strategies.costing import buscar_retazo


def insumo(unidad='metro', precio=15000, name='Blackout'):
    return NS(name=name, unidad_medida=unidad, precio_costo_unitario=precio)


def componente(tipo, ins, id_insumo=1, dw=0, dh=0, base=1):
    return NS(insumo=ins, id_insumo=id_insumo, nombre_producto='x', tipo_calculo=tipo,
              delta_ancho_cm=dw, delta_alto_cm=dh, cantidad_base=base)


def retazo(id_, ancho, largo):
    return NS(id=id_, ancho_cm=ancho, largo_cm=largo)


def test_tela_en_rollo_cuesta_por_metro():
    res, total = calcular_explosion([componente('lineal_alto', insumo())], {}, 150, 200)
    assert res[0]['metodo'] == 'ROLLO'
    assert res[0]['consumo_m_o_m2'] == 2.0
    assert total == 30000.0


def test_retazo_se_usa_y_no_suma_costo():
    retazos = {1: [retazo(7, 160, 210)]}
    res, total = calcular_explosion([componente('lineal_alto', insumo())], retazos, 150, 200)
    assert res[0]['metodo'] == 'RETAZO'
    assert res[0]['id_retazo'] == 7
    assert total == 0.0


def test_retazo_no_se_reutiliza_en_el_mismo_calculo():
    retazos = {1: [retazo(7, 160, 210)]}
    comps = [componente('lineal_alto', insumo()), componente('lineal_alto', insumo())]
    res, _ = calcular_explosion(comps, retazos, 150, 200)
    assert [r['metodo'] for r in res] == ['RETAZO', 'ROLLO']


def test_elige_el_retazo_mas_chico_que_alcanza():
    chico, grande = retazo(1, 160, 210), retazo(2, 300, 300)
    assert buscar_retazo([grande, chico], 150, 200).id == 1
    assert buscar_retazo([retazo(3, 100, 100)], 150, 200) is None


def test_deltas_barra_y_fijo():
    comps = [
        componente('lineal_ancho', insumo('metro', 1000, 'Tubo'), dw=-3),
        componente('fijo', insumo('unidad', 500, 'Cadena'), base=2),
    ]
    res, total = calcular_explosion(comps, {}, 150, 200)
    assert res[0]['metodo'] == 'BARRA'
    assert res[0]['consumo_m_o_m2'] == 1.47
    assert res[1]['costo_parcial'] == 1000.0
    assert total == 2470.0
