export default function Footer() {
  return (
    <footer className="footer bg-[#0a0a0a] text-[#f5f5f0] py-12 border-t border-[#c9a961]/20">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          
          {/* Sección 1: Marca */}
          <div className="footer-section">
            <h3 className="text-[#c9a961] text-xl font-serif mb-4">AMARIGOM DECO</h3>
            <p className="text-sm text-[#c4c4b8]">
              Diseño de cortinas y ambientes exclusivos con elegancia y distinción.
            </p>
          </div>

          {/* Sección 2: Links Rápidos */}
          <div className="footer-section">
            <h4 className="font-bold mb-4">Enlaces</h4>
            <ul className="space-y-2 text-sm text-[#c4c4b8]">
              <li><a href="#about" className="hover:text-[#c9a961]">Nosotros</a></li>
              <li><a href="#products" className="hover:text-[#c9a961]">Productos</a></li>
              <li><a href="#gallery" className="hover:text-[#c9a961]">Galería</a></li>
              <li><a href="#contact" className="hover:text-[#c9a961]">Contacto</a></li>
            </ul>
          </div>

          {/* Sección 3: Legal */}
          <div className="footer-section">
            <h4 className="font-bold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-[#c4c4b8]">
              <li><a href="#privacy" className="hover:text-[#c9a961]">Privacidad</a></li>
              <li><a href="#terms" className="hover:text-[#c9a961]">Términos</a></li>
              <li><a href="#warranty" className="hover:text-[#c9a961]">Garantía</a></li>
            </ul>
          </div>

          {/* Sección 4: Contacto */}
          <div className="footer-section">
            <h4 className="font-bold mb-4">Contacto</h4>
            <div className="flex gap-4 mb-4">
              <a href="https://wa.me/5492494630750" target="_blank" className="text-[#c9a961] hover:underline">WhatsApp</a>
              <a href="https://instagram.com/amarigom" target="_blank" className="text-[#c9a961] hover:underline">Instagram</a>
            </div>
            <p className="text-sm text-[#c4c4b8]">
              Andrea Marigomez<br />
              +54 9 2494630750
            </p>
          </div>
        </div>

        <div className="footer-bottom mt-12 pt-8 border-t border-gray-800 text-center text-xs text-gray-500">
          <p>&copy; 2026 AMARIGOM DECO. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  )
}