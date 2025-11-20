document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/estadisticas")
    .then(res => res.json())
    .then(data => {
      // Gráfico de líneas (Actividades por día)
      Highcharts.chart('graficoLineas', {
        chart: { type: 'line', height: 200, width: 400 },
        title: { text: null },
        xAxis: { categories: data.lineas.dias },
        yAxis: { title: { text: 'Cantidad' }, min: 0 },
        series: [{
          name: 'Actividades por día',
          data: data.lineas.cantidades,
          color: 'blue'
        }],
        credits: { enabled: false }
      });

      // Gráfico de torta (Actividades por tipo)
      Highcharts.chart('graficoTorta', {
        chart: { type: 'pie', height: 300, width: 300 },
        title: { text: null },
        series: [{
          name: 'Cantidad',
          colorByPoint: true,
          data: data.torta.tipos.map((tipo, i) => ({
            name: tipo,
            y: data.torta.cantidades[i],
            color: ["#f87171", "#60a5fa", "#34d399", "#fbbf24", "#a78bfa", "#f472b6"][i % 6]
          }))
        }],
        credits: { enabled: false }
      });

      // Gráfico de barras (Actividades por horario y mes)
      Highcharts.chart('graficoBarras', {
        chart: { type: 'column', height: 200, width: 400 },
        title: { text: null },
        xAxis: { categories: data.barras.meses },
        yAxis: { min: 0, title: { text: 'Cantidad' } },
        series: [
          {
            name: 'Mañana',
            data: data.barras.manana,
            color: '#60a5fa'
          },
          {
            name: 'Mediodía',
            data: data.barras.mediodia,
            color: '#fbbf24'
          },
          {
            name: 'Tarde',
            data: data.barras.tarde,
            color: '#34d399'
          }
        ],
        credits: { enabled: false }
      });
    })
    .catch(error => {
      console.error("Error al cargar estadísticas:", error);
    });
});
