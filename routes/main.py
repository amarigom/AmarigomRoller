from flask import Blueprint, render_template, session, request
from utils.translations import get_translations

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal con hero, productos y galería"""
    lang = session.get('language', 'es')
    translations = get_translations()
    return render_template('index.html', translations=translations, lang=lang)

@main_bp.route('/set-language/<lang>')
def set_language(lang):
    """Cambiar idioma de la aplicación"""
    if lang in ['es', 'en']:
        session['language'] = lang
        session.modified = True
    from flask import jsonify
    return jsonify({'success': True, 'language': lang}), 200 # No content response
