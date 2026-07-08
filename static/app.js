let products = [];
const cart = new Map(); // product_id -> quantity

async function loadProducts() {
  const response = await fetch("/api/products");
  products = await response.json();

  const list = document.getElementById("product-list");
  list.innerHTML = "";
  for (const product of products) {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${product.name} (${product.price.toFixed(2)} €)</span>
      <button data-id="${product.id}">In den Warenkorb</button>
    `;
    li.querySelector("button").addEventListener("click", () => addToCart(product.id));
    list.appendChild(li);
  }
}

function addToCart(productId) {
  cart.set(productId, (cart.get(productId) || 0) + 1);
  renderCart();
}

function renderCart() {
  const list = document.getElementById("cart-list");
  list.innerHTML = "";
  let total = 0;

  for (const [productId, quantity] of cart.entries()) {
    const product = products.find((p) => p.id === productId);
    const lineTotal = product.price * quantity;
    total += lineTotal;

    const li = document.createElement("li");
    li.textContent = `${product.name} x${quantity} = ${lineTotal.toFixed(2)} €`;
    list.appendChild(li);
  }

  document.getElementById("total").textContent = `${total.toFixed(2)} €`;
}

async function checkout() {
  const items = Array.from(cart.entries()).map(([productId, quantity]) => ({
    product_id: productId,
    quantity,
  }));

  if (items.length === 0) {
    return;
  }

  const response = await fetch("/api/sale", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });

  const message = document.getElementById("message");
  if (!response.ok) {
    const error = await response.json();
    message.style.color = "red";
    message.textContent = `Fehler: ${error.detail}`;
    return;
  }

  const result = await response.json();
  message.style.color = "green";
  message.innerHTML =
    `Verkauf gespeichert. Summe: ${result.total.toFixed(2)} € - ` +
    `<a href="/api/sale/${result.id}/receipt" target="_blank">Beleg (PDF) herunterladen</a>`;

  cart.clear();
  renderCart();
}

document.getElementById("checkout-button").addEventListener("click", checkout);
loadProducts();
