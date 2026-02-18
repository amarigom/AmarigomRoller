// Estado global de la aplicación
let currentLang = document.documentElement.lang|| "es"
let cart = []

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
  loadCart()
  updateCartCount()
})

// Cambio de idioma
function toggleLanguage() {
  const newLang = currentLang === "es" ? "en" : "es"
  fetch(`/set-language/${newLang}`).then((response) => {
      if (response.ok) {
        currentLang = newLang
        window.location.reload()
      }
    })
    .catch((error) => {
      console.error("Error changing language:", error)
    })
}

// Toggle menú móvil
function toggleMobileMenu() {
  const mobileNav = document.getElementById("mobile-nav")
  mobileNav.classList.toggle("active")
}

// Toggle carrito
function toggleCart() {
  const cartModal = document.getElementById("cart-modal")
  cartModal.classList.toggle("active")
  if (cartModal.classList.contains("active")) {
    renderCart()
  }
}

// Cargar carrito desde el servidor
function loadCart() {
  fetch("/cart/get")
    .then((response) => response.json())
    .then((data) => {
      cart = data.items
      updateCartCount()
    })
    .catch((error) => console.error("[v0] Error loading cart:", error))
}

// Agregar al carrito
function addToCart(productId, name, price, image) {
  const data = {
    product_id: productId,
    name: name,
    price: price,
    image: image,
    quantity: 1,
  }

  fetch("/cart/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        loadCart()
        showNotification(data.message)
      }
    })
    .catch((error) => console.error("[v0] Error adding to cart:", error))
}

// Eliminar del carrito
function removeFromCart(productId) {
  fetch(`/cart/remove/${productId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        loadCart()
        renderCart()
      }
    })
    .catch((error) => console.error("[v0] Error removing from cart:", error))
}

// Actualizar contador del carrito
function updateCartCount() {
  const countElement = document.getElementById("cart-count")
  if (countElement) {
    countElement.textContent = cart.length
  }
}

// Renderizar carrito
function renderCart() {
  const cartItemsContainer = document.getElementById("cart-items")
  const cartTotalElement = document.getElementById("cart-total")

  if (cart.length === 0) {
    cartItemsContainer.innerHTML =
      '<p style="text-align: center; color: var(--color-text-secondary);">El carrito está vacío</p>'
    cartTotalElement.textContent = "$0"
    return
  }

  let total = 0
  let html = ""

  cart.forEach((item) => {
    const itemTotal = item.price * item.quantity
    total += itemTotal

    html += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;">
                <div style="flex: 1;">
                    <h4 style="font-size: 0.9rem; margin-bottom: 0.25rem;">${item.name}</h4>
                    <p style="color: var(--color-text-secondary); font-size: 0.85rem;">Cantidad: ${item.quantity}</p>
                    <p style="color: var(--color-accent-gold); font-weight: 500;">$${itemTotal.toLocaleString()}</p>
                </div>
                <button onclick="removeFromCart(${item.product_id})" style="background: transparent; border: none; color: var(--color-text-secondary); cursor: pointer; font-size: 1.5rem;">&times;</button>
            </div>
        `
  })

  cartItemsContainer.innerHTML = html
  cartTotalElement.textContent = `$${total.toLocaleString()}`
}

// Checkout
function checkout() {
  alert("Funcionalidad de checkout en desarrollo. Por favor contacta por WhatsApp para finalizar tu compra.")
  window.open("https://wa.me/5492494630750", "_blank")
}

// Notificaciones
function showNotification(message) {
  const notification = document.createElement("div")
  notification.textContent = message
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--color-accent-gold);
        color: var(--color-bg-primary);
        padding: 1rem 1.5rem;
        border-radius: 4px;
        z-index: 3000;
        animation: slideIn 0.3s ease;
    `

  document.body.appendChild(notification)

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease"
    setTimeout(() => notification.remove(), 300)
  }, 3000)
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute("href"))
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  })
})
