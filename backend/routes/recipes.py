from flask import Blueprint, jsonify, request
from models.recipe_bom import RecipeBOM
from models import db

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/test-recipe/<int:product_id>', methods=['GET'])
def test_recipe(product_id):
    resultado = [] 
    try:
        # 1. Inicio y búsqueda de componentes
        print(f"--- INICIANDO CALCULO PARA PRODUCTO ID: {product_id} ---")
        
        components = RecipeBOM.query.filter_by(id_padre=product_id).all()
        if not components:
            return jsonify({"status": "error", "message": f"No hay receta para el ID {product_id}","message": f"El producto {product_id} aún no tiene definida su explosión de materiales."}), 404

        # 2. Captura de medidas desde la URL
        try:
            w_pedido = float(request.args.get('w', 100.0))
            h_pedido = float(request.args.get('h', 100.0))
        except ValueError:
            return jsonify({"status": "error", "message": "Medidas inválidas"}), 400

        for item in components:
            # --- DATOS DEL INSUMO (Compatibilidad con Neon 'name') ---
            insumo_obj = getattr(item, 'insumo', None)
            nombre_visual = getattr(insumo_obj, 'name', None) or \
                            getattr(item, 'nombre_producto', "Insumo sin nombre")
            precio_unit_base = float(getattr(insumo_obj, 'precio_costo_unitario', 0) or 0)

            # --- CÁLCULO DE MEDIDAS CON DELTAS ---
            d_w = float(item.delta_ancho_cm or 0)
            d_h = float(item.delta_alto_cm or 0)
            ancho_corte = w_pedido + d_w
            alto_corte = h_pedido + d_h
            
            # Inicialización por defecto
            metodo = "ROLLO"
            id_pieza_usada = None
            mensaje_opt = ""
            consumo_final = alto_corte # Por defecto es lineal de alto

            # --- 3. LÓGICA DE OPTIMIZACIÓN (Búsqueda de Retazos) ---
            # Solo buscamos retazos si es tela (lineal_alto o superficie)
            if item.tipo_calculo in ['lineal_alto', 'superficie']:
                try:
                    from models import RetazoTela
                    print(f"DEBUG: Buscando retazo para Insumo {item.id_insumo} (Req: {ancho_corte}x{alto_corte})")
                    
                    retazo = RetazoTela.query.filter(
                        RetazoTela.id_insumo_base == item.id_insumo,
                        RetazoTela.estado == 'disponible',
                        RetazoTela.ancho_cm >= ancho_corte,
                        RetazoTela.largo_cm >= alto_corte
                    ).order_by((RetazoTela.ancho_cm * RetazoTela.largo_cm).asc()).first()

                    if retazo:
                        print(f"  > ¡RETAZO ENCONTRADO! ID: {retazo.id}")
                        metodo = "RETAZO"
                        id_pieza_usada = retazo.id
                        mensaje_opt = f"Usar retazo de {int(retazo.ancho_cm)}x{int(retazo.largo_cm)} cm"
                        consumo_final = 1.0 # En el frontend se muestra como 1 unidad de descarte
                    else:
                        print(f"  > No hay retazos suficientes. Usando ROLLO.")
                        metodo = "ROLLO"
                        consumo_final = alto_corte
                except Exception as e_ret:
                    print(f"  > Error en búsqueda de retazos: {str(e_ret)}")
                    metodo = "ROLLO"
                    consumo_final = alto_corte
            
            # --- 4. OTROS TIPOS DE CÁLCULO ---
            elif item.tipo_calculo == 'lineal_ancho':
                metodo = "BARRA"
                consumo_final = ancho_corte
            elif item.tipo_calculo == 'fijo':
                metodo = "UNIDAD"
                consumo_final = float(item.cantidad_base or 1.0)

            # --- 5. COSTEO FINAL ---
            # Si es lineal (alto/ancho), trabajamos en cm para multiplicar por el precio unitario
            if item.tipo_calculo in ['lineal_alto', 'lineal_ancho', 'superficie']:
                costo_parcial = round((alto_corte if item.tipo_calculo != 'lineal_ancho' else ancho_corte) * precio_unit_base, 2)
            else:
                costo_parcial = round(consumo_final * precio_unit_base, 2)

            # --- 6. MAPEO PARA CUTTINGCALCULATOR.TSX ---
            resultado.append({
                "componente": nombre_visual,
                "consumo_cm": round(consumo_final, 2),
                "medida_corte": f"{ancho_corte} x {alto_corte} cm",
                "precio_unitario": precio_unit_base,
                "costo_parcial": costo_parcial,
                "metodo": metodo,
                "id_retazo": id_pieza_usada, # Esta key activa el banner en React
                "mensaje": mensaje_opt
            })

        # Sumatoria final
        total = round(sum(i['costo_parcial'] for i in resultado), 2)
        
        return jsonify({
            "status": "success", 
            "explosion": resultado, 
            "total_materiales": total
        })

    except Exception as e:
        import traceback
        print(f"--- ERROR CRÍTICO  ---\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    
@recipes_bp.route('/recipes/<int:product_id>', methods=['GET'])
def get_recipe_base(product_id):
    try:
        # 1. Buscamos los componentes en la tabla RecipeBOM
        components = RecipeBOM.query.filter_by(id_padre=product_id).all()
        
        if not components:
            return jsonify({
                "status": "error", 
                "message": f"El producto {product_id} no tiene una receta definida en la base de datos."
            }), 404

        # 2. Mapeamos los datos para que el Frontend los reciba limpios
        resultado = []
        for item in components:
            # Usamos getattr por seguridad, igual que en tu test_recipe
            insumo_obj = getattr(item, 'insumo', None)
            nombre = getattr(insumo_obj, 'name', None) or getattr(item, 'nombre_producto', "Insumo")
            
            resultado.append({
                "id": item.id,
                "componente": nombre,
                "cantidad_base": float(item.cantidad_base or 0.0)
            })

        return jsonify(resultado), 200

    except Exception as e:
        import traceback
        print(f"--- ERROR EN GET_RECIPE ---\n{traceback.format_exc()}")
        return jsonify({"status": "error", "message": str(e)}), 500    