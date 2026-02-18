import Hero from "@/components/sections/Hero"
import Products from "@/components/sections/Products"
import Gallery from "@/components/sections/Gallery"
import QuoteForm from "@/components/sections/QuoteForm"
import About from "@/components/sections/About"
import Contact from "@/components/sections/Contact"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0A0A0A]">
      <Hero />
      <About />
      <Products />
      <Gallery />
      <QuoteForm />
      <Contact />
    </main>
  )
}
