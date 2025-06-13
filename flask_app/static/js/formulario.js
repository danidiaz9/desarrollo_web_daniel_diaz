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
  const inicioInput = document.getElementById('fecha_inicio');
  const terminoInput = document.getElementById('fecha_termino');

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
  const telefono = document.getElementById('celular').value;
  if (telefono && !/^\+\d{3}\.\d{8}$/.test(telefono)) {
    alert('Formato de teléfono debe ser +NNN.NNNNNNNN');
    return false;
  }

  // Validar fechas: solo si 'termino' tiene valor
  const inicioVal = document.getElementById('fecha_inicio').value;
  const terminoVal = document.getElementById('fecha_termino').value;
  if (terminoVal) {
    const inicio = new Date(inicioVal);
    const termino = new Date(terminoVal);
    if (termino < inicio) {
      alert('La fecha de término no puede ser anterior a la de inicio');
      return false;
    }
  }

  // Validar fotos 
  const inputsFotos = document.querySelectorAll('#fotos-container input[type="file"]');
  let cantidadArchivos = 0;
  inputsFotos.forEach(input => {
    if (input.files) cantidadArchivos += input.files.length;
  });
  if (cantidadArchivos < 1 || cantidadArchivos > 5) {
    alert('Debe subir entre 1 y 5 fotos');
    return false;
  }

  // Validar temas
  const temaSelect = document.getElementById('tema');
  if (temaSelect.value === '') {
    alert('Debe seleccionar un tema');
    return false;
  }

  // Validar tema "otro"
  const temaOtro = document.getElementById('tema-otro');
  if (temaSelect.value === 'otro' && temaOtro.value.trim().length < 3) {
    alert('Debe describir el tema (mínimo 3 caracteres)');
    return false;
  }

  // Si todo está OK, muestra el modal de confirmación
  document.getElementById('modal-confirmacion').classList.add('mostrar');
  return false; // Evita el envío inmediato
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
document.querySelector('#modal-confirmacion .btn-confirm').addEventListener('click', () => {
  document.getElementById('modal-confirmacion').style.display = 'none';
  document.getElementById('modal-exito').style.display = 'block';
});
document.querySelector('#modal-confirmacion .btn-cancel').addEventListener('click', () => {
  document.getElementById('modal-confirmacion').style.display = 'none';
});

// Se asocia el evento de validación al formulario
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById('form-actividad');
  if (form) {
    form.addEventListener('submit', validarFormulario);
  }

  const confirmBtn = document.querySelector('#modal-confirmacion .btn-confirm');
  const cancelBtn = document.querySelector('#modal-confirmacion .btn-cancel');
  
  if (confirmBtn && cancelBtn) {
    confirmBtn.addEventListener('click', () => {
      document.getElementById('modal-confirmacion').classList.remove('mostrar');
      document.getElementById('modal-exito').classList.add('mostrar');
      setTimeout(() => {
        window.location.href = '/';
      }, 2000); // 2 segundos para leer el mensaje
    });
  
    cancelBtn.addEventListener('click', () => {
      document.getElementById('modal-confirmacion').classList.remove('mostrar');
    });
  }

  // Cargar comunas dinámicamente
  const regionSelect = document.getElementById('region');
  if (regionSelect) {
      regionSelect.addEventListener('change', function() {
          const regionId = this.value;
          fetch("/api/comunas?region_id=" + regionId)
              .then(response => response.json())
              .then(data => {
                  const comunaSelect = document.getElementById('comuna');
                  comunaSelect.innerHTML = '<option value="">Seleccione comuna...</option>';
                  data.forEach(comuna => {
                      const option = document.createElement('option');
                      option.value = comuna.id;
                      option.textContent = comuna.nombre;
                      comunaSelect.appendChild(option);
                  });
                  comunaSelect.disabled = false;
              });
      });
  }

  // Validación de tema "otro"
  const temaSelect = document.getElementById('tema');
  if (temaSelect) {
      temaSelect.addEventListener('change', function() {
          const temaOtro = document.getElementById('tema_otro');
          temaOtro.style.display = this.value === 'otro' ? 'block' : 'none';
          if (this.value !== 'otro') temaOtro.value = '';
      });
  }

  // Mostrar/ocultar inputs de contacto
  window.toggleContacto = function(checkbox) {
      const input = document.getElementById(checkbox.id + '-id');
      if (checkbox.checked) {
          input.style.display = 'block';
          input.required = true;
      } else {
          input.style.display = 'none';
          input.value = '';
          input.required = false;
      }
  };

  // Lógica para fotos
  let photoCount = document.querySelectorAll('#fotos-container input[type="file"]').length;
  const agregarFotoBtn = document.getElementById('agregar-foto');
  if (agregarFotoBtn) {
      agregarFotoBtn.addEventListener('click', function() {
          if (photoCount < 5) {
              const newInput = document.createElement('input');
              newInput.type = 'file';
              newInput.name = 'fotos';
              newInput.accept = 'image/*';
              newInput.className = 'form-control';
              newInput.style.marginTop = "5px";
              document.getElementById('fotos-container').appendChild(newInput);
              photoCount++;
          } else {
              alert("Solo puedes subir hasta 5 fotos.");
          }
      });
  }
});
