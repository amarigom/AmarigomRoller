"use client"

import { useState } from "react"
import { Package, Filter, Ruler, Tag, Search, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface InventoryItem {
  id: number
  code: string
  name: string
  category: string
  metersLeft: number
  widthCm: number
  unit: string
  price: number
  lastUpdate: string
}

interface InventoryViewProps {
  items: InventoryItem[]
}

export default function InventoryView({ items }: InventoryViewProps) {
  const [filterCategory, setFilterCategory] = useState<string>("all")
  const [searchQuery, setSearchQuery] = useState("")

  // 1. Obtenemos categorías únicas
  const categories = ["all", ...new Set(items.map(item => item.category))]

  // 2. Lógica de filtrado combinada (Categoría + Búsqueda)
  const filtered = items.filter((item) => {
    const matchesCategory = filterCategory === "all" || item.category === filterCategory
    const matchesSearch = 
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.code.toLowerCase().includes(searchQuery.toLowerCase())
    
    return matchesCategory && matchesSearch
  })

  return (
    <div className="flex flex-col gap-6">
      {/* Header & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="font-serif text-2xl text-[#f5f0e8]">Inventario General</h2>
          <p className="text-sm text-[#6b6560] mt-1">
            {filtered.length} de {items.length} insumos
          </p>
        </div>

        {/* Buscador */}
        <div className="relative w-full md:w-72 group">
          <Search 
            size={16} 
            className="absolute left-3 top-1/2 -translate-y-1/2 text-[#6b6560] group-focus-within:text-[#c9a961] transition-colors" 
          />
          <input
            type="text"
            placeholder="Buscar por nombre o SKU..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#111111] border border-[#2a2520] rounded-lg py-2 pl-10 pr-10 text-sm text-[#f5f0e8] focus:outline-none focus:border-[#c9a961]/50 transition-all"
          />
          {searchQuery && (
            <button 
              onClick={() => setSearchQuery("")}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-[#6b6560] hover:text-[#f5f0e8]"
            >
              <X size={14} />
            </button>
          )}
        </div>
      </div>

      {/* Dynamic Filters */}
      <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">
        <Filter size={14} className="text-[#6b6560] flex-shrink-0" />
        <div className="flex gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={cn(
                "px-3 py-1.5 rounded-md text-[11px] border transition-all whitespace-nowrap uppercase tracking-wider font-medium",
                filterCategory === cat
                  ? "bg-[#c9a961]/10 text-[#c9a961] border-[#c9a961]/30"
                  : "text-[#6b6560] border-[#2a2520] hover:border-[#3a3530]"
              )}
            >
              {cat === "all" ? "Todos" : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Inventory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map((item) => (
          <div
            key={item.id}
            className="bg-[#111111] border border-[#2a2520] rounded-lg p-5 flex flex-col gap-4 hover:border-[#c9a961]/30 transition-all hover:shadow-[0_0_20px_rgba(201,169,97,0.05)] relative group"
          >
            {/* SKU Badge */}
            <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
               <span className="text-[9px] bg-[#2a2520] text-[#6b6560] px-2 py-0.5 rounded uppercase tracking-tighter">
                 {item.code}
               </span>
            </div>

            {/* Info */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center bg-[#c9a961]/5 border border-[#c9a961]/10 text-[#c9a961]">
                <Package size={18} />
              </div>
              <div className="flex-1 pr-8">
                <h3 className="text-sm font-medium text-[#f5f0e8] leading-snug line-clamp-1">{item.name}</h3>
                <p className="text-[10px] text-[#6b6560] mt-0.5 flex items-center gap-1">
                  <Tag size={10} /> {item.category}
                </p>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4 border-y border-[#2a2520]/50 py-4 my-1">
              <div>
                <p className="text-[9px] text-[#6b6560] uppercase tracking-widest mb-1">Stock</p>
                <div className="flex items-baseline gap-1">
                  <span className="text-xl font-serif text-[#f5f0e8]">{item.metersLeft}</span>
                  <span className="text-[10px] text-[#6b6560] lowercase">{item.unit}</span>
                </div>
              </div>
              <div className="text-right border-l border-[#2a2520]/50 pl-4">
                <p className="text-[9px] text-[#6b6560] uppercase tracking-widest mb-1">Precio</p>
                <p className="text-lg text-[#7a9b76] font-medium">
                  ${item.price.toLocaleString('es-AR')}
                </p>
              </div>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between mt-auto">
              {item.widthCm > 0 ? (
                <div className="flex items-center gap-1.5 text-[#6b6560]">
                  <Ruler size={12} />
                  <span className="text-xs">{item.widthCm} cm ancho</span>
                </div>
              ) : <div />}
              <span className="text-[9px] text-[#2a2520] font-mono">{item.lastUpdate}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filtered.length === 0 && (
        <div className="flex flex-col items-center justify-center py-20 text-center bg-[#111111]/50 border border-dashed border-[#2a2520] rounded-xl">
          <Search size={32} className="text-[#2a2520] mb-4" />
          <p className="text-[#f5f0e8] font-serif text-lg">No hay coincidencias</p>
          <p className="text-[#6b6560] text-sm max-w-[250px] mt-2">
            No encontramos nada que coincida con "{searchQuery}" en {filterCategory === "all" ? "el inventario" : filterCategory}.
          </p>
        </div>
      )}
    </div>
  )
}