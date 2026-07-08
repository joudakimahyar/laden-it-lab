const dateInput = document.getElementById("date-input");
const message = document.getElementById("message");

async function loadReport(date) {
  const url = date ? `/api/report?date=${date}` : "/api/report";
  const response = await fetch(url);

  if (!response.ok) {
    const error = await response.json();
    message.style.color = "red";
    message.textContent = `Fehler: ${error.detail}`;
    return;
  }

  const report = await response.json();
  message.textContent = "";
  document.getElementById("report-date").textContent = report.date;
  document.getElementById("report-count").textContent = report.count;
  document.getElementById("report-total").textContent = `${report.total.toFixed(2)} €`;
  dateInput.value = report.date;
}

document.getElementById("date-form").addEventListener("submit", (event) => {
  event.preventDefault();
  loadReport(dateInput.value);
});

loadReport();
