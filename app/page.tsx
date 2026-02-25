import Hero from "@/components/sections/Hero"
import About from "@/components/sections/About"
import Products from "@/components/sections/Products"
// No importamos Gallery ni QuoteForm por ahora para ver si arranca

export default function Home() {
  return (
    <main className="bg-black min-h-screen">
      <Hero />
      <About />
      <Products />
    </main>
  )
}