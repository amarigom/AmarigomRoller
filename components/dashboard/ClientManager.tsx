// app/gestion/clientes/page.tsx
"use client";

import { useState, useEffect } from "react";
import { Table, TableHeader, TableBody, TableRow, TableCell } from "@/components/ui/table"; // Ajustá la ruta según tu carpeta
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search, Phone } from "lucide-react";

export default function ClientesPage() {
  const [clientes, setClientes] = useState([]);
  const [busqueda, setBusqueda] = useState("");

  // 1. RESPONSABILIDAD: Cargar datos (Fetch)
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/clients`)
      .then(res => res.json())
      .then(data => setClientes(data))
      .catch(err => console.error("Error cargando clientes:", err));
  }, []);

  // 2. RESPONSABILIDAD: Filtrar (Lógica de UI)
  const clientesFiltrados = clientes.filter(c => 
    c.nombre.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* HEADER: Título y Acción de agregar */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-[#c9a961]">Gestión de Clientes</h1>
          <p className="text-xs text-gray-500 uppercase tracking-widest">AMARIGOM DECO - Tandil</p>
        </div>
        <Button className="bg-[#c9a961] hover:bg-[#b09452] text-black gap-2">
          <Plus size={16} /> Nuevo Cliente
        </Button>
      </div>

      {/* BUSCADOR: Componente Atómico de búsqueda */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
        <Input 
          placeholder="Buscar por nombre o apellido..." 
          className="pl-10 bg-black/20 border-gray-800"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      {/* TABLA: Usando tus componentes de 'sections' */}
      <div className="border border-gray-800 rounded-xl overflow-hidden bg-black/40 backdrop-blur-sm">
        <Table>
          <TableHeader className="bg-white/5">
            <TableRow>
              <TableCell className="font-bold text-gray-400">Nombre</TableCell>
              <TableCell className="font-bold text-gray-400">WhatsApp</TableCell>
              <TableCell className="font-bold text-gray-400">Dirección</TableCell>
              <TableCell className="font-bold text-gray-400 text-right">Acciones</TableCell>
            </TableRow>
          </TableHeader>
          <TableBody>
            {clientesFiltrados.map((cliente) => (
              <TableRow key={cliente.id} className="hover:bg-white/5 transition-colors">
                <TableCell className="font-medium text-gray-200">{cliente.nombre}</TableCell>
                <TableCell>
                  <a href={`https://wa.me/${cliente.telefono}`} className="flex items-center gap-2 text-[#c9a961] hover:underline">
                    <Phone size={14} /> {cliente.telefono}
                  </a>
                </TableCell>
                <TableCell className="text-gray-400 text-sm">{cliente.direccion}</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" className="text-xs text-gray-500 hover:text-white">Ver Ficha</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}