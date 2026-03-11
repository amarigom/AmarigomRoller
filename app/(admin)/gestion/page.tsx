// app/(admin)/gestion/page.tsx (o /admin/page.tsx si renombraste la carpeta)

export default function GestionPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-serif text-[#c9a961] mb-6">
        Bienvenida al Panel de Control, Andrea
      </h1>
      <p className="text-gray-400">
        Selecciona una opción del menú lateral para comenzar a gestionar AMARIGOM.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div className="p-6 border border-[#c9a961]/20 bg-black/40 rounded-sm">
          <h3 className="text-[#c9a961] mb-2 uppercase text-xs tracking-widest">Estado de Stock</h3>
          <p className="text-2xl font-light">42 Rollos</p>
        </div>
        {/* Agrega más tarjetas de resumen aquí si quieres */}
      </div>
    </div>
  )
}