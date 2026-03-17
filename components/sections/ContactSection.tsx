import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Instagram, MessageCircle } from "lucide-react"

export default function ContactSection() {
  return (
    <section className="py-24 bg-black" id="contact">
      <div className="container mx-auto px-6 max-w-5xl">
        
        {/* Encabezado de la sección */}
        <div className="text-center mb-16">
          <h2 className="text-[#c9a961] text-3xl font-serif uppercase tracking-[0.3em] mb-4">
            Contacto
          </h2>
          <p className="text-gray-500 italic tracking-widest text-sm">
            Estamos aquí para ayudarte
          </p>
        </div>

        {/* Grid de Tarjetas de Contacto */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Tarjeta WhatsApp */}
          <Card className="group">
            <CardHeader className="text-center pt-10">
              <div className="w-16 h-16 bg-zinc-900 border border-[#c9a961]/20 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:border-[#c9a961]/50 transition-colors">
                <MessageCircle className="w-8 h-8 text-[#c9a961]" />
              </div>
              <CardTitle className="text-[#F5F5F0] tracking-widest uppercase text-xl">WhatsApp</CardTitle>
            </CardHeader>
            <CardContent className="text-center pb-10">
              <p className="text-[#C4C4B8] mb-6">+54 9 249 4630750</p>
              <a 
                href="https://wa.me/5492494630750" 
                target="_blank"
                className="inline-block px-8 py-3 border border-[#c9a961] text-[#c9a961] text-xs uppercase tracking-[0.2em] hover:bg-[#c9a961] hover:text-black transition-all duration-300"
              >
                Enviar mensaje
              </a>
            </CardContent>
          </Card>

          {/* Tarjeta Instagram */}
          <Card className="group">
            <CardHeader className="text-center pt-10">
              <div className="w-16 h-16 bg-zinc-900 border border-[#c9a961]/20 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:border-[#c9a961]/50 transition-colors">
                <Instagram className="w-8 h-8 text-[#c9a961]" />
              </div>
              <CardTitle className="text-[#F5F5F0] tracking-widest uppercase text-xl">Instagram</CardTitle>
            </CardHeader>
            <CardContent className="text-center pb-10">
              <p className="text-[#C4C4B8] mb-6">@amarigom.deco</p>
              <a 
                href="https://instagram.com/amarigom/" 
                target="_blank"
                className="inline-block px-8 py-3 border border-[#c9a961] text-[#c9a961] text-xs uppercase tracking-[0.2em] hover:bg-[#c9a961] hover:text-black transition-all duration-300"
              >
                Seguir
              </a>
            </CardContent>
          </Card>

        </div>
      </div>
    </section>
  )
}