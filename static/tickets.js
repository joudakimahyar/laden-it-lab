async function loadTickets() {
    const response = await fetch("/api/tickets");
    const tickets = await response.json();

    const list = document.getElementById("ticket-list");
    list.innerHTML = "";

    for (const ticket of tickets) {
        const item = document.createElement("li");

        const statusOptions = ["offen", "in Bearbeitung", "gelöst"]
            .map(s => `<option value="${s}" ${s === ticket.status ? "selected" : ""}>${s}</option>`)
            .join("");

        item.innerHTML = `
            <strong>${ticket.title}</strong> (Priorität: ${ticket.priority})<br>
            ${ticket.description}<br>
            Status:
            <select data-id="${ticket.id}" class="status-select">
                ${statusOptions}
            </select>
        `;
        list.appendChild(item);
    }

    document.querySelectorAll(".status-select").forEach(select => {
        select.addEventListener("change", async (event) => {
            const ticketId = event.target.dataset.id;
            const newStatus = event.target.value;

            await fetch(`/api/tickets/${ticketId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status: newStatus }),
            });

            loadTickets();
        });
    });
}

document.getElementById("ticket-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const priority = document.getElementById("priority").value;

    const response = await fetch("/api/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description, priority }),
    });

    const message = document.getElementById("message");

    if (response.ok) {
        message.textContent = "Ticket erfolgreich erstellt!";
        document.getElementById("ticket-form").reset();
        loadTickets();
    } else {
        const error = await response.json();
        message.textContent = "Fehler: " + error.detail;
    }
});

loadTickets();
