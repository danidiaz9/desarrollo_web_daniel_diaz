document.addEventListener("DOMContentLoaded", function () {
    cargarActividades();
});

function cargarActividades() {
    fetch('/api/actividades/finalizadas')
        .then(res => res.json())
        .then(data => {
            // Ordenar por ID ascendente
            data.sort((a, b) => a.id - b.id);

            const tbody = document.getElementById('lista-actividades');
            tbody.innerHTML = '';

            data.forEach(act => {
                let tema = '-';
                if (Array.isArray(act.temas) && act.temas.length > 0) {
                    tema = act.temas.map(t =>
                        t.tema === 'otro' && t.glosaOtro ? `${t.tema} (${t.glosaOtro})` : t.tema
                    ).join(', ');
                }

                const promedio = Number.isFinite(act.promedioNotas)
                    ? act.promedioNotas.toFixed(2)
                    : '-';

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${act.id}</td>
                    <td>${formatearFecha(act.diaHoraInicio)}</td>
                    <td>${act.sector || '-'}</td>
                    <td>${act.nombre}</td>
                    <td>${tema}</td>
                    <td class="nota">${promedio} 
                        <button onclick="evaluar(${act.id}, this)" style="margin-left: 10px;">Evaluar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error("Error al cargar actividades:", err);
            alert("No se pudieron cargar las actividades.");
        });
}

function formatearFecha(fechaISO) {
    if (!fechaISO) return '-';
    try {
        const d = new Date(fechaISO);
        return d.toLocaleDateString('es-CL', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
    } catch (e) {
        return fechaISO;
    }
}

function evaluar(actividadId, btn) {
    const nota = prompt("Ingrese una nota entre 1 y 7 (solo números enteros):");
    if (nota === null) return;

    const valor = Number(nota.trim());

    if (isNaN(valor) || !Number.isInteger(valor) || valor < 1 || valor > 7) {
        alert("Nota inválida. Solo se permiten números enteros entre 1 y 7.");
        return;
    }

    btn.disabled = true;

    fetch(`/api/actividad/${actividadId}/nota`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ valor: valor })
    })
        .then(res => res.json())
        .then(resp => {
            if (resp.error) {
                alert(resp.error);
            } else {
                // Recarga toda la tabla para reflejar los cambios
                cargarActividades();
            }
        })
        .catch(err => {
            console.error("Error al guardar la nota:", err);
            alert("No se pudo guardar la nota.");
        })
        .finally(() => {
            btn.disabled = false;
        });
}
