function DetalleActividad(id) {
  fetch(`/api/actividad/${id}`)
    .then(response => {
      if (!response.ok) throw new Error('No se pudo obtener el detalle');
      return response.text();
    })
    .then(html => {
      document.getElementById("listado-actividades").style.display = "none";
      document.getElementById("detalle-actividad").style.display = "block";
      document.getElementById("detalle-contenido").innerHTML = html;
    })
    .catch(error => alert(error));
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

  // Guarda los estilos originales de la imagen
  const originalWidth = img.style.width;
  const originalHeight = img.style.height;
  const originalMaxWidth = img.style.maxWidth;
  const originalMaxHeight = img.style.maxHeight;
  const originalBoxShadow = img.style.boxShadow;
  const originalPosition = img.style.position;
  const originalZIndex = img.style.zIndex;
  const originalBackground = img.style.background;

  // Cambia los estilos para ampliar la imagen
  img.style.width = "auto";
  img.style.height = "auto";
  img.style.maxWidth = "90vw";
  img.style.maxHeight = "90vh";
  img.style.boxShadow = "0 0 20px #000";
  img.style.position = "relative";
  img.style.zIndex = "1000";
  img.style.background = "#fff";

  // Crea un botón para cerrar el modo ampliado
  const contenedor = img.parentElement;
  const botonCerrar = document.createElement("button");
  botonCerrar.textContent = "Cerrar";
  botonCerrar.onclick = function() {
    img.style.width = originalWidth;
    img.style.height = originalHeight;
    img.style.maxWidth = originalMaxWidth;
    img.style.maxHeight = originalMaxHeight;
    img.style.boxShadow = originalBoxShadow;
    img.style.position = originalPosition;
    img.style.zIndex = originalZIndex;
    img.style.background = originalBackground;
    img.removeAttribute('data-enlarged');
    if (botonCerrar.parentElement) {
      botonCerrar.parentElement.removeChild(botonCerrar);
    }
  };
  botonCerrar.style.position = "absolute";
  botonCerrar.style.top = "5px";
  botonCerrar.style.right = "5px";
  botonCerrar.style.zIndex = "1001";
  contenedor.appendChild(botonCerrar);
}
