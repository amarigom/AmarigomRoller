export function linearDisplay(quantity: number, price: number, unit: string | null | undefined) {
  if (unit === "cm") return { quantity: quantity / 100, price: price * 100, unit: "metro" }
  return { quantity, price, unit }
}

export function displayNumber(value: number, minimumFractionDigits = 0, maximumFractionDigits = 6) {
  return value.toLocaleString("es-AR", { minimumFractionDigits, maximumFractionDigits })
}
