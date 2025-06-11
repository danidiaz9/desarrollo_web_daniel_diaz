document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/estadisticas")
    .then(res => res.json())
    .then(data => {
      // Gráfico de líneas
      new Chart(document.getElementById("graficoLineas"), {
        type: "line",
        data: {
          labels: data.lineas.dias,
          datasets: [{
            label: "Actividades por día",
            data: data.lineas.cantidades,
            borderColor: "blue",
            fill: false
          }]
        }
      });

      // Gráfico de torta
      new Chart(document.getElementById("graficoTorta"), {
        type: "pie",
        data: {
          labels: data.torta.tipos,
          datasets: [{
            label: "Actividades por tipo",
            data: data.torta.cantidades,
            backgroundColor: ["#f87171", "#60a5fa", "#34d399", "#fbbf24", "#a78bfa", "#f472b6"]
          }]
        }
      });

      // Gráfico de barras
      new Chart(document.getElementById("graficoBarras"), {
        type: "bar",
        data: {
          labels: data.barras.meses,
          datasets: [
            {
              label: "Mañana",
              data: data.barras.manana,
              backgroundColor: "#60a5fa"
            },
            {
              label: "Mediodía",
              data: data.barras.mediodia,
              backgroundColor: "#fbbf24"
            },
            {
              label: "Tarde",
              data: data.barras.tarde,
              backgroundColor: "#34d399"
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    })
    .catch(error => {
      console.error("Error al cargar estadísticas:", error);
    });
});
