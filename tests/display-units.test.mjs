import { strict as assert } from "node:assert"
import { test } from "node:test"
import { displayNumber, linearDisplay } from "../lib/display-units.ts"

test("convierte stock y precio de centímetros a metros sin cambiar su importe", () => {
  const result = linearDisplay(145, 12.5, "cm")
  assert.deepEqual(result, { quantity: 1.45, price: 1250, unit: "metro" })
  assert.equal(result.quantity * result.price, 145 * 12.5)
  assert.equal(displayNumber(linearDisplay(1450, 0, "cm").quantity, 2), "14,50")
})

test("conserva unidades distintas de centímetros", () => {
  assert.deepEqual(linearDisplay(14.5, 1200, "metro"), { quantity: 14.5, price: 1200, unit: "metro" })
  assert.deepEqual(linearDisplay(4, 200, "unidad"), { quantity: 4, price: 200, unit: "unidad" })
  assert.deepEqual(linearDisplay(4, 200, null), { quantity: 4, price: 200, unit: null })
  assert.equal(displayNumber(linearDisplay(0.0001, 0, "cm").quantity, 2), "0,000001")
})
