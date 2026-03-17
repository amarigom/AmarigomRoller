// app/(tienda)/layout.tsx
import Header from "@/components/ui/header"
import Footer from "@/components/ui/footer"

export default function TiendaLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex flex-col min-h-screen">
      {/* AQUÍ ES DONDE APARECE EL MENÚ PARA EL CLIENTE */}
      <Header />
      
      <main className="flex-grow">
        {children}
      </main>

      <Footer />
    </div>
  )
}