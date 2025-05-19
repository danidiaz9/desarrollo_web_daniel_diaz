// Cargar regiones y comunas
fetch('region_comuna.json')
  .then(response => response.json())
  .then(data => {
    const regionSelect = document.getElementById('region');
    data.regiones.forEach(region => {
      const option = document.createElement('option');
      option.value = region.id;
      option.textContent = region.nombre;
      regionSelect.appendChild(option);
    });

    regionSelect.addEventListener('change', (e) => {
      const comunaSelect = document.getElementById('comuna');
      comunaSelect.innerHTML = '<option value="">Seleccione comuna</option>';
      const regionId = parseInt(e.target.value);
      const region = data.regiones.find(r => r.id === regionId);
      if (region && region.comunas) {
        region.comunas.forEach(comuna => {
          const option = document.createElement('option');
          option.value = comuna.id;
          option.textContent = comuna.nombre;
          comunaSelect.appendChild(option);
        });
      }
      comunaSelect.disabled = false;
    });
  });

// Función que muestra o esconde el input asociado al método de contacto
function revisaCheck(element) {
  const targetInput = document.getElementById(element.name);
  if (targetInput) {
    targetInput.style.display = element.checked ? "block" : "none";
  }
}

// Asignar evento para mostrar el campo "otro tema"
document.getElementById('tema').addEventListener('change', function(e) {
  const temaOtro = document.getElementById('tema-otro');
  if(e.target.value === 'otro'){
    temaOtro.hidden = false;
    temaOtro.required = true;
  } else {
    temaOtro.hidden = true;
    temaOtro.required = false;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const inicioInput = document.getElementById('inicio');
  const terminoInput = document.getElementById('termino');

  // Función para la fecha
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  };

  // Fecha y hora actual para el inicio
  const ahora = new Date();
  inicioInput.value = formatDate(ahora);

  // Fecha y hora para el término (inicio + 3 horas)
  const tresHorasDespues = new Date(ahora.getTime() + 3 * 60 * 60 * 1000);
  terminoInput.value = formatDate(tresHorasDespues);
});


// Función principal de validación del formulario
const validarFormulario = (e) => {
  e.preventDefault();
  
  // Validar email
  const email = document.getElementById('email').value;
  if (!/^\S+@\S+\.\S+$/.test(email)) {
    alert('Formato de email inválido');
    return false;
  }

  // Validar teléfono
  const telefono = document.getElementById('telefono').value;
  if (telefono && !/^\+\d{3}\.\d{8}$/.test(telefono)) {
    alert('Formato de teléfono debe ser +NNN.NNNNNNNN');
    return false;
  }

  // Validar fechas: solo si 'termino' tiene valor
  const inicioVal = document.getElementById('inicio').value;
  const terminoVal = document.getElementById('termino').value;
  if (terminoVal) {
    const inicio = new Date(inicioVal);
    const termino = new Date(terminoVal);
    if (termino < inicio) {
      alert('La fecha de término no puede ser anterior a la de inicio');
      return false;
    }
  }

  // Validar fotos 
  const fotos = document.querySelectorAll('#fotos-container input[type="file"]');
  if (fotos.length < 1 || fotos.length > 5) {
    alert('Debe subir entre 1 y 5 fotos');
    return false;
  }

  // Validar tema "otro"
  const temaSelect = document.getElementById('tema');
  const temaOtro = document.getElementById('tema-otro');
  if (temaSelect.value === 'otro' && temaOtro.value.trim().length < 3) {
    alert('Debe describir el tema (mínimo 3 caracteres)');
    return false;
  }

  // Si todas las validaciones pasan, mostrar el modal de confirmación.
  document.getElementById('confirmation-modal').hidden = false;

  return false; // Evitamos que el formulario se envíe inmediatamente.
};

function validarContactos() {
  // Obtener todos los checkboxes seleccionados
  const checkboxes = document.querySelectorAll('input[type="checkbox"][name]:checked');
  const contactos = [];

  // 1. Validar cantidad máxima (5)
  if (checkboxes.length > 5) {
      alert("Máximo 5 métodos de contacto permitidos.");
      return false;
  }

  // 2. Validar cada input asociado
  for (const checkbox of checkboxes) {
      const nombreContacto = checkbox.name;
      const inputId = nombreContacto + "-input";
      const inputTexto = document.getElementById(inputId);

      // Si el input no existe o está oculto, ignorar
      if (!inputTexto || inputTexto.style.display === "none") continue;

      const valor = inputTexto.value.trim();

      // Validar longitud del texto (4-50 caracteres)
      if (valor.length < 4 || valor.length > 50) {
          alert(`El ID/URL de ${nombreContacto} debe tener entre 4 y 50 caracteres.`);
          inputTexto.focus();
          return false;
      }

      // Validar formato si es necesario
      if (nombreContacto === "instagram" && !valor.startsWith("@")) {
          alert("El usuario de Instagram debe comenzar con @.");
          return false;
      }
  }

  return true;
}

// Configurar eventos para los botones de confirmación
document.getElementById('confirmar-si').addEventListener('click', () => {
  document.getElementById('confirmation-modal').hidden = true;
  document.getElementById('success-modal').hidden = false;
});
document.getElementById('confirmar-no').addEventListener('click', () => {
  document.getElementById('confirmation-modal').hidden = true;
});

// Se asocia el evento de validación al formulario
document.getElementById('form-actividad').addEventListener('submit', validarFormulario);
