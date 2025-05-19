const actividades = [
  {
    id: 1,
    inicio: "2025-03-28 12:00",
    termino: "2025-03-28 14:00",
    comuna: "Santiago",
    sector: "Beauchef 850",
    tema: "Boxeo",
    organizador: "Juan Pérez",
    fotos: ["img/boxeo.png", "img/boxeo.png", "img/boxeo.png"]
  },
  {
    id: 2,
    inicio: "2025-03-29 10:00",
    termino: "2025-03-29 12:00",
    comuna: "Santiago",
    sector: "Centro",
    tema: "Fútbol",
    organizador: "María López",
    fotos: ["img/frutas.png", "img/frutas.png"]
  },
];

function mostrarDetalle(id) {
  // Buscamos la actividad por id en el arreglo
  const actividad = actividades.find(a => a.id === id);
  if (!actividad) {
    alert('Actividad no encontrada');
    return;
  }

  // Generamos el contenido que mostrará el detalle de la actividad
  const contenido = `
    <p><strong>Inicio:</strong> ${actividad.inicio}</p>
    <p><strong>Término:</strong> ${actividad.termino}</p>
    <p><strong>Comuna:</strong> ${actividad.comuna}</p>
    <p><strong>Sector:</strong> ${actividad.sector}</p>
    <p><strong>Tema:</strong> ${actividad.tema}</p>
    <p><strong>Organizador:</strong> ${actividad.organizador}</p>
    <p><strong>Total de fotos:</strong> ${actividad.fotos.length}</p>
    <div class="galeria">
      ${actividad.fotos
        .map((foto, i) => `
          <div class="foto-contenedor" style="display: inline-block; position: relative;">
            <img id="foto-${i}" src="${foto}" width="320" height="240"
                 onclick="ampliarFoto(this)" alt="Foto de ${actividad.tema}">
          </div>
        `).join('')}
    </div>
  `;
  
  // Oculta el listado y muestra el detalle
  document.getElementById("listado-actividades").style.display = "none";
  document.getElementById("detalle-actividad").style.display = "block";
  document.getElementById("detalle-contenido").innerHTML = contenido;
}

function volverListado() {
  // Oculta el contenedor de detalle y muestra el listado nuevamente
  document.getElementById("detalle-actividad").style.display = "none";
  document.getElementById("listado-actividades").style.display = "block";
}

function ampliarFoto(img) {
  // Evita ampliar de nuevo si ya se encuentra ampliada
  if (img.getAttribute('data-enlarged') === "true") return;
  img.setAttribute('data-enlarged', "true");

  // Guarda el tamaño original de la imagen
  const originalWidth = img.width;
  const originalHeight = img.height;

  // Cambia el tamaño de la imagen a 800x600
  img.width = 800;
  img.height = 600;

  // Crea un botón para cerrar el modo ampliado
  const contenedor = img.parentElement;
  const botonCerrar = document.createElement("button");
  botonCerrar.textContent = "Cerrar";
  botonCerrar.onclick = function() {
    img.width = originalWidth;
    img.height = originalHeight;
    img.removeAttribute('data-enlarged');
    if (botonCerrar.parentElement) {
      botonCerrar.parentElement.removeChild(botonCerrar);
    }
  };
  botonCerrar.style.position = "absolute";
  botonCerrar.style.top = "5px";
  botonCerrar.style.right = "5px";
  contenedor.appendChild(botonCerrar);
}
