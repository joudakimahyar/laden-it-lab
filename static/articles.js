const form = document.getElementById("product-form");
const idField = document.getElementById("product-id");
const nameField = document.getElementById("product-name");
const priceField = document.getElementById("product-price");
const formTitle = document.getElementById("form-title");
const submitButton = document.getElementById("submit-button");
const cancelButton = document.getElementById("cancel-button");
const message = document.getElementById("message");

async function loadProducts() {
  const response = await fetch("/api/products");
  const products = await response.json();

  const tableBody = document.getElementById("product-table-body");
  tableBody.innerHTML = "";

  for (const product of products) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${product.name}</td>
      <td>${product.price.toFixed(2)} €</td>
      <td>
        <button data-action="edit">Bearbeiten</button>
        <button data-action="delete">Löschen</button>
      </td>
    `;
    row.querySelector("[data-action='edit']").addEventListener("click", () => startEdit(product));
    row.querySelector("[data-action='delete']").addEventListener("click", () => deleteProduct(product.id));
    tableBody.appendChild(row);
  }
}

function startEdit(product) {
  idField.value = product.id;
  nameField.value = product.name;
  priceField.value = product.price;
  formTitle.textContent = "Artikel bearbeiten";
  submitButton.textContent = "Speichern";
  cancelButton.hidden = false;
}

function resetForm() {
  form.reset();
  idField.value = "";
  formTitle.textContent = "Neuer Artikel";
  submitButton.textContent = "Hinzufügen";
  cancelButton.hidden = true;
}

async function deleteProduct(id) {
  const response = await fetch(`/api/products/${id}`, { method: "DELETE" });
  if (!response.ok) {
    const error = await response.json();
    showMessage(`Fehler: ${error.detail}`, true);
    return;
  }
  showMessage("Artikel gelöscht.", false);
  loadProducts();
}

function showMessage(text, isError) {
  message.style.color = isError ? "red" : "green";
  message.textContent = text;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const body = JSON.stringify({
    name: nameField.value,
    price: parseFloat(priceField.value),
  });

  const isEdit = idField.value !== "";
  const url = isEdit ? `/api/products/${idField.value}` : "/api/products";
  const method = isEdit ? "PUT" : "POST";

  const response = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body,
  });

  if (!response.ok) {
    const error = await response.json();
    showMessage(`Fehler: ${error.detail}`, true);
    return;
  }

  showMessage(isEdit ? "Artikel gespeichert." : "Artikel hinzugefügt.", false);
  resetForm();
  loadProducts();
});

cancelButton.addEventListener("click", resetForm);

loadProducts();
