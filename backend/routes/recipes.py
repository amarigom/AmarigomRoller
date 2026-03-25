from flask import Blueprint, jsonify, request
from models.recipe_bom import RecipeBOM
from models import db

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/test-recipe/<int:product_id>', methods=['GET'])
def test_recipe(product_id):
    resultado = [] # Lo inicializamos arriba para que el except siempre lo encuentre
    try:
        components = RecipeBOM.query.filter_by(id_padre=product_id).all()
        if not components:
            return jsonify({"status": "error", "message": "No hay componentes"}), 404

        w_pedido = float(request.args.get('w', 150.0))
        h_pedido = float(request.args.get('h', 200.0))

        for item in components:
            # 1. Medidas
            d_w = float(item.delta_ancho_cm or 0)
            d_h = float(item.delta_alto_cm or 0)
            ancho_corte = w_pedido + d_w
            alto_corte = h_pedido + d_h
            
            # 2. Precio
            precio_unit_base = float(item.insumo.precio_costo_unitario or 0) if item.insumo else 0

            # Inicialización por defecto
            metodo = "NUEVO"
            id_pieza_usada = None
            mensaje_opt = ""
            consumo_final = alto_corte 

            # 3. Lógica de Selección
            if item.tipo_calculo == 'fijo':
                metodo = "UNIDAD"
                consumo_final = float(item.cantidad_base or 1.0)
            
            elif item.tipo_calculo in ['lineal_alto', 'lineal_ancho', 'superficie']:
                medida_necesaria = alto_corte if item.tipo_calculo in ['lineal_alto', 'superficie'] else ancho_corte
                
                # Intentar buscar retazo solo si es tela
                if item.tipo_calculo in ['lineal_alto', 'superficie']:
                    try:
                        from models import RetazoTela
                        # DEBUG en consola
                        print(f"\n--- DEBUG RETAZOS ---")
                        print(f"Buscando para Insumo ID: {item.id_insumo}")
                        print(f"Medida Necesaria: {ancho_corte}x{alto_corte}")

                        retazo = RetazoTela.query.filter(
                            RetazoTela.id_insumo_base == item.id_insumo,
                            RetazoTela.estado == 'disponible',
                            RetazoTela.ancho_cm >= ancho_corte,
                            RetazoTela.largo_cm >= alto_corte
                        ).order_by((RetazoTela.ancho_cm * RetazoTela.largo_cm).asc()).first()

                        if retazo:
                            print(f"¡ÉXITO! Encontrado Retazo ID: {retazo.id}")
                            metodo = "RETAZO"
                            id_pieza_usada = retazo.id
                            mensaje_opt = "Retazo hallado"
                            consumo_final = 1.0 
                        else:
                            print(f"FALLO: Sin retazos para esa medida.")
                            metodo = "ROLLO"
                            consumo_final = alto_corte
                    except Exception as err: # Cambiado 'e' por 'err' para evitar conflictos
                        print(f"ERROR EN BÚSQUEDA RETAZO: {str(err)}")
                        metodo = "ROLLO"
                        consumo_final = alto_corte
                else:
                    metodo = "BARRA"
                    consumo_final = ancho_corte
            
            # --- 4. SEGURO PARA TELA ---
            if consumo_final == 0 and precio_unit_base > 0:
                consumo_final = alto_corte

            # 5. COSTEO (Opción A: Cobrar siempre)
            if item.tipo_calculo in ['lineal_alto', 'superficie']:
                costo_parcial = round(alto_corte * precio_unit_base, 2)
            elif item.tipo_calculo == 'lineal_ancho':
                costo_parcial = round(ancho_corte * precio_unit_base, 2)
            else:
                costo_parcial = round(consumo_final * precio_unit_base, 2)

            resultado.append({
                "componente": item.nombre_producto,
                "consumo_real": round(consumo_final, 2),
                "unidad": "un" if metodo == "UNIDAD" else "cm",
                "medida_corte": f"{ancho_corte} x {alto_corte} cm",
                "precio_unitario": precio_unit_base,
                "costo_parcial": costo_parcial,
                "metodo": metodo,
                "id_pieza": id_pieza_usada,
                "mensaje": mensaje_opt
            })
            
        # --- EL RETURN VA AQUÍ (FUERA DEL FOR) ---
        total = round(sum(i['costo_parcial'] for i in resultado), 2)
        return jsonify({"status": "success", "explosion": resultado, "total_materiales": total})

    except Exception as e:
        print(f"ERROR GENERAL: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

#-------------------------------

