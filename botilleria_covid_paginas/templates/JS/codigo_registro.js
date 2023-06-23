$("#form-register").submit(function(event) {
  // Evita el envío del formulario por defecto
  event.preventDefault();

  // Obtenemos los valores de cada campo a válidar
  var name = $("#name").val();
  var email = $("#email").val();
  var password = $("#password").val();
  var confirm_password = $("#confirm_password").val();

  // Verifica si el nombre de usuario cumple con las reglas de longitud
  if (name.length < 8 || name.length > 30) {
    alert("Por favor, ingrese un nombre de usuario entre 8 y 30 caracteres.");
    return;
  }

  // Verifica si el nombre de usuario es válido según el patrón establecido
  if (!/^[a-zA-Z0-9_]+$/.test(name)) {
    alert("Por favor, ingrese un nombre de usuario válido.");
    return;
  }

  // Verifica si el nombre de usuario esta vacio
  if (name.trim() === "") {
    alert("Por favor, ingrese un nombre de usuario.");
    return;
  }

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

  // Verifica si la contraseña cumple con las reglas de longitud
  if (password.length < 8 || password.length > 40) {
    alert("Por favor, ingrese una contraseña entre 8 y 40 caracteres.");
    return;
  }

  // Verifica si la contraseña es válido según el patrón establecido
  if (!/^[a-zA-Z0-9\s]+$/.test(password)) {
    alert("Por favor, ingrese una contraseña válida.");
    return;
  }

  // Verifica si la contraseña esta vacio
  if (password.trim() === "") {
    alert("Por favor, ingrese una contraseña.");
    return;
  }

  // Verifica si el confirmar contraseña cumple con las reglas de longitud
  if (confirm_password.length < 8 || confirm_password.length > 40) {
    alert("Por favor, ingrese una contraseña entre 8 y 40 caracteres.");
    return;
  }

  // Verifica si el confirmar contraseña es válido según el patrón establecido
  if (!/^[a-zA-Z0-9\s]+$/.test(confirm_password)) {
    alert("Por favor, ingrese una contraseña válida.");
    return;
  }

  // Verifica si el confirmar contraseña esta vacio
  if (confirm_password.trim() === "") {
    alert("Por favor, ingrese una contraseña.");
    return;
  }

  // Verifica si el confirmar contraseña ingresada es igual a la contraseña
  if (confirm_password !== password) {
    alert("Las contraseñas no coinciden.");
    return;
  };

  // Si los campos son validos, envía el formulario
  alert("El formulario se ha enviado correctamente.");
  this.submit();
});

// Ocultar mensaje de error al corregir el nombre
$("#name").on("input", function() {
  if ($("#name")[0].checkValidity()) {
      $("#name-error").hide();
  }
});

// Ocultar mensaje de error al corregir el nombre
$("#email").on("input", function() {
  if ($("#email")[0].checkValidity()) {
      $("#email-error").hide();
  }
});

// Ocultar mensaje de error al corregir el nombre
$("#password").on("input", function() {
  if ($("#password")[0].checkValidity()) {
      $("#password-error").hide();
  }
});

// Ocultar mensaje de error al corregir el nombre
$("#confirm_password").on("input", function() {
  if ($("#confirm_password")[0].checkValidity()) {
      $("#confirm_password-error").hide();
  }
});

$("#form-register").validate({
  rules: {
    name: {
      required: true,
      minlength: 8,
      maxlength: 30,
      pattern: /^[a-zA-Z0-9_]+$/
    },
    email: {
      required: true,
      minlength: 10,
      maxlength: 40,
      pattern: /^[a-zA-Z0-9._%+-]+@(gmail|hotmail|yahoo|)[.]com|cl$/
    },
    password: {
      required: true,
      minlength: 8,
      maxlength: 40,
      pattern: /^[a-zA-Z0-9\s]+$/
    },
    confirm_password: {
      required: true,
      minlength: 8,
      maxlength: 40,
      pattern: /^[a-zA-Z0-9\s]+$/
    }
  },
  messages: {
    name: {
      required: "Por favor, ingrese su nombre de usuario completo",
      minlength: "El nombre de usuario debe tener al menos 8 caracteres",
      maxlength: "El nombre de usuario no puede tener más de 30 caracteres",
      pattern: "El nombre de usuario solo puede contener letras, números y guiones bajos"
    },
    email: {
      required: "Por favor, ingrese su correo electrónico completo",
      minlength: "El correo electrónico debe tener al menos 10 caracteres",
      maxlength: "El correo electrónico no puede tener más de 40 caracteres",
      pattern: "El correo electrónico solo puede contener letras, espacios, acentos, letras y números"
    },
    password: {
      required: "Por favor, ingrese su contraseña completa",
      minlength: "La contraseña debe tener al menos 8 caracteres",
      maxlength: "La contraseña no puede tener más de 40 caracteres",
      pattern: "La contraseña solo puede contener letras y números"
    },
    confirm_password: {
      required: "Por favor, ingrese su contraseña completa",
      minlength: "La contraseña debe tener al menos 8 caracteres",
      maxlength: "La contraseña no puede tener más de 40 caracteres",
      pattern: "La contraseña solo puede contener letras y números"
    }
  },
  submitHandler: function(form) {
    alert("El formulario se ha enviado correctamente.");
    form.submit();
  }
});