"use client";

import { useState, useEffect } from "react";
import {Cliente} from "@/lib/types/client";
import { Table, TableHeader, TableBody, TableRow, TableCell } from "@/components/ui/table"; 
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search, Phone, User } from "lucide-react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';


export default function ClientesPage() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [busqueda, setBusqueda] = useState("");
  const [cargando, setCargando] = useState(true);
  
  // 1. CARGAR DATOS DESDE EL BACKEND
  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/clients`);
        const data = await response.json();
        setClientes(data);
      } catch (error) {
        console.error("Error al obtener clientes:", error);
      } finally {
        setCargando(false);
      }
    };

    fetchClientes();
  }, []);

  // 2. LÓGICA DE FILTRADO (Buscador)
  const clientesFiltrados = clientes.filter((c) =>
    `${c.nombre}`.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6 bg-black min-h-screen text-white">
      {/* HEADER */}
      <div className="flex justify-between items-center border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-[#c9a961]">Clientes</h1>
          <p className="text-xs text-gray-500 uppercase tracking-widest mt-1">Base de Datos AMARIGOM DECO</p>
        </div>
        <Button className="bg-[#c9a961] hover:bg-[#b09452] text-black font-bold px-6">
          <Plus className="mr-2" size={18} /> Nuevo Cliente
        </Button>
      </div>

      {/* BUSCADOR */}
      <div className="relative group">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[#c9a961] transition-colors" size={20} />
        <Input 
          placeholder="Buscar por nombre, apellido o email..." 
          className="pl-10 bg-[#111] border-gray-800 focus:border-[#c9a961] text-gray-200 w-full lg:w-1/3"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      {/* TABLA DE RESULTADOS */}
      <div className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden shadow-2xl">
        {cargando ? (
          <div className="p-20 text-center text-gray-500 animate-pulse">Cargando clientes de Tandil...</div>
        ) : (
          <Table>
            <TableHeader className="bg-white/5">
              <TableRow className="border-b border-gray-800">
                <TableCell className="text-[#c9a961] font-semibold py-4">Cliente</TableCell>
                <TableCell className="text-[#c9a961] font-semibold py-4">Contacto WhatsApp</TableCell>
                <TableCell className="text-[#c9a961] font-semibold py-4">Dirección / Obra</TableCell>
                <TableCell className="text-[#c9a961] font-semibold py-4 text-right">Ficha</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {clientesFiltrados.length > 0 ? (
                clientesFiltrados.map((cliente) => (
                  <TableRow key={cliente.id} className="border-b border-gray-900 hover:bg-white/5 transition-all">
                    <TableCell className="py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-[#c9a961]">
                          <User size={16} />
                        </div>
                        <span className="font-medium">{cliente.nombre}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <a 
                        href={`https://wa.me/${cliente.telefono}`} 
                        target="_blank"
                        className="text-gray-400 hover:text-[#c9a961] flex items-center gap-2 transition-colors"
                      >
                        <Phone size={14} /> {cliente.telefono}
                      </a>
                    </TableCell>
                    <TableCell className="text-gray-400">{cliente.direccion || "No especificada"}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" className="text-gray-500 hover:text-[#c9a961]">Ver Detalles</Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="py-10 text-center text-gray-600">
                    No se encontraron clientes con ese nombre.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}