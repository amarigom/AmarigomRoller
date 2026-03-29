"use client";

import { useState, useEffect } from "react";
import { Cliente } from "@/lib/types/client";
import { Table, TableHeader, TableBody, TableRow, TableCell } from "@/components/ui/table"; 
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search, Phone, User } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog"; 
import { Label } from "@/components/ui/label";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

export default function ClientesPage() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [busqueda, setBusqueda] = useState("");
  const [cargando, setCargando] = useState(true);

  // --- ESTADOS PARA EL MODAL Y NUEVO CLIENTE ---
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nuevoCliente, setNuevoCliente] = useState({ 
    nombre: '',
    apellido: '', 
    telefono: '', 
    direccion: '' ,
    email: ''
  });

  const fetchClientes = async () => {
    setCargando(true);
    try {
      const response = await fetch(`/api/clients`);
      if (!response.ok) throw new Error("Error al obtener datos");
      const data = await response.json();
      setClientes(data);
    } catch (error) {
      console.error("Error al obtener clientes:", error);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    fetchClientes();
  }, []);

  // --- LÓGICA PARA GUARDAR (Sincronizada con el comando OK) ---
  const handleGuardar = async () => {
    // 1. Limpiamos los datos de espacios accidentales
    const clienteData = {
      nombre: nuevoCliente.nombre.trim(),
      apellido: nuevoCliente.apellido.trim(),
      email: nuevoCliente.email.trim(),
      telefono: nuevoCliente.telefono.trim(),
      direccion: nuevoCliente.direccion.trim()
    };

    // 2. Validación de campos obligatorios
    if (!clienteData.nombre || !clienteData.apellido || !clienteData.email) {
      return alert("Nombre, Apellido y Email son obligatorios.");
    }

    try {
      console.log("Enviando datos a:", `${API_BASE_URL}/api/clients`);
      
      const response = await fetch(`${API_BASE_URL}/api/clients`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(clienteData),
      });

      if (response.ok) {
        setIsModalOpen(false); 
        setNuevoCliente({ nombre: '', apellido: '', telefono: '', direccion: '', email: '' }); 
        fetchClientes(); // Recarga la tabla de AMARIGOM DECO
      } else {
        const errorMsg = await response.json();
        alert(`Error: ${errorMsg.message || "No se pudo guardar el cliente"}`);
      }
    } catch (error) {
      console.error("Error en la petición:", error);
      alert("Error de conexión. Verificá que el backend esté corriendo y el CORS configurado.");
    }
  };

  const clientesFiltrados = clientes.filter((c) =>
    `${c.nombre} ${c.apellido}`.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6 bg-black min-h-screen text-white">
      {/* HEADER */}
      <div className="flex justify-between items-center border-b border-gray-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-[#c9a961]">Clientes</h1>
          <p className="text-xs text-gray-500 uppercase tracking-widest mt-1">Base de Datos AMARIGOM DECO</p>
        </div>

        {/* --- MODAL DE NUEVO CLIENTE --- */}
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button className="bg-[#c9a961] hover:bg-[#b09452] text-black font-bold px-6">
              <Plus className="mr-2" size={18} /> Nuevo Cliente
            </Button>
          </DialogTrigger>
          
          <DialogContent className="bg-[#0a0a0a] border border-gray-800 text-white sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle className="text-[#c9a961] text-xl">Registrar Cliente</DialogTitle>
            </DialogHeader>
            
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="nombre" className="text-gray-400 text-sm font-medium">Nombre</Label>
                  <Input 
                    id="nombre" 
                    value={nuevoCliente.nombre}
                    onChange={(e) => setNuevoCliente({...nuevoCliente, nombre: e.target.value})}
                    className="bg-white/5 border-gray-800 focus:border-[#c9a961] text-white"
                    placeholder="Andrea"
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="apellido" className="text-gray-400 text-sm font-medium">Apellido</Label>
                  <Input 
                    id="apellido" 
                    value={nuevoCliente.apellido}
                    onChange={(e) => setNuevoCliente({...nuevoCliente, apellido: e.target.value})}
                    className="bg-white/5 border-gray-800 focus:border-[#c9a961] text-white"
                    placeholder="Marigomez"
                  />
                </div>
              </div>

              <div className="grid gap-2">
                <Label htmlFor="email" className="text-gray-400 text-sm font-medium">Correo Electrónico</Label>
                <Input 
                  id="email" 
                  type="email"
                  value={nuevoCliente.email}
                  onChange={(e) => setNuevoCliente({...nuevoCliente, email: e.target.value})}
                  className="bg-white/5 border-gray-800 focus:border-[#c9a961] text-white"
                  placeholder="ejemplo@correo.com"
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="telefono" className="text-gray-400 text-sm font-medium">WhatsApp / Teléfono</Label>
                <Input 
                  id="telefono" 
                  value={nuevoCliente.telefono}
                  onChange={(e) => setNuevoCliente({...nuevoCliente, telefono: e.target.value})}
                  className="bg-white/5 border-gray-800 focus:border-[#c9a961] text-white"
                  placeholder="2494XXXXXX"
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="direccion" className="text-gray-400 text-sm font-medium">Dirección / Obra</Label>
                <Input 
                  id="direccion" 
                  value={nuevoCliente.direccion}
                  onChange={(e) => setNuevoCliente({...nuevoCliente, direccion: e.target.value})}
                  className="bg-white/5 border-gray-800 focus:border-[#c9a961] text-white"
                  placeholder="Calle 123, Tandil"
                />
              </div>
            </div>

            <DialogFooter>
              <Button 
                onClick={handleGuardar}
                className="w-full bg-[#c9a961] hover:bg-[#b09452] text-black font-bold h-12"
              >
                Guardar Cliente
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* BUSCADOR */}
      <div className="relative group">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-[#c9a961] transition-colors" size={20} />
        <Input 
          placeholder="Buscar por nombre o apellido..." 
          className="pl-10 bg-[#111] border-gray-800 focus:border-[#c9a961] text-gray-200 w-full lg:w-1/3"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      {/* TABLA DE RESULTADOS */}
      <div className="rounded-xl border border-gray-800 bg-[#0a0a0a] overflow-hidden shadow-2xl">
        {cargando ? (
          <div className="p-20 text-center text-gray-500 animate-pulse font-mono tracking-widest uppercase">
            Sincronizando con base de datos...
          </div>
        ) : (
          <Table>
            <TableHeader className="bg-white/5">
              <TableRow className="border-b border-gray-800 hover:bg-transparent">
                <TableCell className="text-[#c9a961] font-semibold py-4">Cliente</TableCell>
                <TableCell className="text-[#c9a961] font-semibold py-4">Contacto</TableCell>
                <TableCell className="text-[#c9a961] font-semibold py-4">Dirección</TableCell>
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
                        <span className="font-medium text-gray-200">{cliente.nombre} {cliente.apellido}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        <a 
                          href={`https://wa.me/${cliente.telefono}`} 
                          target="_blank"
                          className="text-gray-400 hover:text-[#c9a961] flex items-center gap-2 transition-colors text-sm"
                        >
                          <Phone size={14} /> {cliente.telefono}
                        </a>
                        <p className="text-xs text-gray-600">{cliente.email}</p>
                      </div>
                    </TableCell>
                    <TableCell className="text-gray-400 text-sm italic">{cliente.direccion || "Sin dirección"}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" className="text-gray-500 hover:text-[#c9a961] text-xs uppercase font-bold tracking-tighter">Detalles</Button>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={4} className="py-20 text-center text-gray-600 italic">
                    No se encontraron clientes en Tandil.
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