"""Regresión de cálculo: casos reales en regression_cases.json. Si un cambio altera un total, avisa cuál."""
import json
import os

import pytest

from extensions import db
from models import Supply, SupplyCategory
from tests.helpers import crear_receta

with open(os.path.join(os.path.dirname(__file__), "regression_cases.json"), encoding="utf-8") as f:
    DATOS = json.load(f)


def _sembrar():
    cat = SupplyCategory(name="Varios")
    db.session.add(cat)
    db.session.flush()
    insumos = {clave: Supply(categoria_id=cat.id, **campos) for clave, campos in DATOS["insumos"].items()}
    db.session.add_all(insumos.values())
    db.session.commit()
    for pid, items in DATOS["productos"].items():
        crear_receta(int(pid), [
            {**{k: v for k, v in i.items() if k != "insumo"},
             **({"id_insumo": insumos[i["insumo"]].id} if "insumo" in i else {})}
            for i in items
        ])


@pytest.mark.parametrize("caso", DATOS["casos"], ids=lambda c: c["nombre"])
def test_caso_de_regresion(client, auth, caso):
    _sembrar()
    r = client.get(f"/api/recipes/{caso['producto']}/explosion", headers=auth("admin"),
                   query_string={"w": caso["w"], "h": caso["h"], **caso["opciones"]})
    assert r.status_code == 200, r.get_json()
    datos = r.get_json()
    obtenidos = {e["componente"]: e["costo_parcial"] for e in datos["explosion"]}
    assert obtenidos == pytest.approx(caso["componentes"], abs=0.01), f"Cambió el costo por componente en '{caso['nombre']}'"
    assert datos["total_materiales"] == pytest.approx(caso["total_materiales"], abs=0.01), \
        f"Cambió el total de materiales en '{caso['nombre']}'"
    assert datos["total_minutos"] == caso.get("total_minutos", 30)
