import Hero from "@/components/sections/Hero"
import About from "@/components/sections/About"
import Products from "@/components/sections/Products"
import Gallery from "@/components/sections/Gallery"
import QuoteForm from "@/components/sections/QuoteForm"
import ContactSection from "@/components/sections/ContactSection"
import Promotions from "@/app/(tienda)/products/[categorie]/Promotions"
// No importamos Gallery ni QuoteForm por ahora para ver si arranca

export default function Home() {
  return (
    <main className="bg-black min-h-screen">
      <Hero />
      <About />
      <Products />
      <Gallery/>
      <Promotions/>
      <QuoteForm/>
      <ContactSection/>
    </main>
  )
}