$("#form-restore-password").submit(function(event) {
  // Evita el envío del formulario por defecto
  event.preventDefault();

  var email = $("#email").val();

  // Verifica si el correo electrónico cumple con las reglas de longitud
  if (email.length < 10 || email.length > 40) {
    alert("Por favor, ingrese un correo electrónico entre 10 y 40 caracteres.");
    return;
  }

  // Verifica si el correo electrónico es válido según el patrón establecido
  if (!/^[a-zA-Z0-9._%+-]+@(gmail|hotmail|yahoo|)[.]com|cl$/.test(email)) {
    alert("Por favor, ingrese un correo electrónico válido.");
    return;
  }

  // Verifica si el correo electrónico esta vacio
  if (email.trim() === "") {
    alert("Por favor, ingrese un correo electrónico.");
    return;
  }

  // Si los campos son validos, envía el formulario
  alert("El formulario se ha enviado correctamente.");
  this.submit();
});

// Ocultar mensaje de error al corregir el nombre
$("#email").on("input", function() {
  if ($("#email")[0].checkValidity()) {
      $("#email-error").hide();
  }
});

$("#form-restore-password").validate({
  rules: {
    email: {
      required: true,
      minlength: 10,
      maxlength: 40,
      pattern: /^[a-zA-Z0-9._%+-]+@(gmail|hotmail|yahoo|)[.]com|cl$/
    }
  },
  messages: {
    email: {
      required: "Por favor, ingrese su correo electrónico completo",
      minlength: "El correo electrónico debe tener al menos 10 caracteres",
      maxlength: "El correo electrónico no puede tener más de 40 caracteres",
      pattern: "El correo electrónico solo puede contener letras, espacios, acentos, letras y números"
    }
  },
  submitHandler: function(form) {
    alert("El formulario se ha enviado correctamente.");
    form.submit();
  }
});