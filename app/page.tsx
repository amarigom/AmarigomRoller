export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0a0a] flex flex-col items-center justify-center p-24">
      {/* Usamos el color hexadecimal directo para asegurar que funcione */}
      <h1 className="text-6xl font-serif mb-8" style={{ color: '#c9a961' }}>
        Andrea Roller
      </h1>
      
      <p className="text-[#c4c4b8] text-xl max-w-2xl text-center mb-12">
        Diseño de cortinas y ambientes exclusivos con  elegancia y distinción.
      </p>
      
      <div className="p-8 border border-[#c9a961] bg-[#1a1a1a] rounded-lg shadow-[0_0_20px_rgba(201,169,97,0.2)]">
        <button className="bg-[#c9a961] text-[#0a0a0a] px-8 py-3 rounded-md font-bold hover:bg-[#d4b574] transition-all">
          Solicitar Presupuesto
        </button>
      </div>
    </main>
  )
}