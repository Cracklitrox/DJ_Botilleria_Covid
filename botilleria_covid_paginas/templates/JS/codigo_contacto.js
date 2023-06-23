$("#contact-form").submit(function(event) {
  // Evita el envío del formulario por defecto
  event.preventDefault();

  // Obtenemos los valores de cada campo a válidar
  var name = $("#name").val();
  var email = $("#email").val();
  var phone = $("#phone").val();
  var city = $("#city").val();
  var message = $("#message").val();

  // Verifica si el nombre de usuario cumple con las reglas de longitud
  if (name.length < 8 || name.length > 30) {
    alert("Por favor, ingrese un nombre entre 8 y 30 caracteres.");
    return;
  }
  
  // Verifica si el nombre es válido según el patrón establecido
  if (!/^[a-zA-Z\s]{5,100}$/.test(name)) {
    alert("Por favor, ingrese un nombre válido.");
    return;
  }

  // Verifica si el nombre de usuario esta vacio
  if (name.trim() === "") {
    alert("Por favor, ingrese un nombre completo.");
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

  // Verifica si el número de teléfono cumple con las reglas de longitud
  if (phone.length < 9 || phone.length > 9) {
    alert("Por favor, ingrese un número teléfonico de 9 números.");
    return;
  }

  // Verifica si el número de teléfono es válido según el patrón establecido
  if (!/^\d{9}$/.test(phone)) {
    alert("Por favor, ingrese un número de teléfono válido de 9 dígitos.");
    return;
  }

  // Verifica si  el número de teléfono esta vacio
  if (phone.trim() === "") {
    alert("Por favor, ingrese un número teléfonico.");
    return;
  }

  // Verifica si la ciudad cumple con las reglas de longitud
  if (city.length < 10 || city.length > 50) {
    alert("Por favor, ingrese una ciudad entre 10 y 50 caracteres.");
    return;
  }

  // Verifica si la ciudad es válido según el patrón establecido
  if (!/^[a-zA-Z\s\-']+$/.test(city)) {
    alert("Por favor, ingrese una ciudad válido.");
    return;
  }

  // Verifica si la ciudad esta vacio
  if (city.trim() === "") {
    alert("Por favor, ingrese una ciudad.");
    return;
  }

  // Verifica si el mensaje cumple con las reglas de longitud
  if (message.length < 10 || message.length > 120) {
    alert("Por favor, ingrese un ciudad mensaje entre 10 y 120 caracteres.");
    return;
  }

  // Verifica si el mensaje es válido según el patrón establecido
  if (!/^[a-zA-Z0-9áéíóúÁÉÍÓÚ\s]+$/.test(message)) {
    alert("Por favor, ingrese un mensaje válido.");
    return;
  }

  // Verifica si el mensaje esta vacio
  if (message.trim() === "") {
    alert("Por favor, ingrese un mensaje.");
    return;
  }

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

// Ocultar mensaje de error al corregir el email
$("#email").on("input", function() {
  if ($("#email")[0].checkValidity()) {
    $("#email-error").hide();
  }
});

// Ocultar mensaje de error al corregir el teléfono
$("#phone").on("input", function() {
  if ($("#phone")[0].checkValidity()) {
    $("#phone-error").hide();
  }
});

// Ocultar mensaje de error al corregir la ciudad
$("#city").on("input", function() {
  if ($("#city")[0].checkValidity()) {
    $("#city-error").hide();
  }
});

// Ocultar mensaje de error al corregir la ciudad
$("#message").on("input", function() {
  if ($("#message")[0].checkValidity()) {
    $("#message-error").hide();
  }
});

$("#contact-form").validate({
  rules: {
    name: {
      required: true,
      minlength: 8,
      maxlength: 30,
      pattern: /^[a-zA-ZáéíóúÁÉÍÓÚ\s]+$/
    },
    email: {
      required: true,
      minlength: 10,
      maxlength: 40,
      email: true,
      pattern: /^([a-zA-Z0-9._%+-]+@(gmail|hotmail|yahoo)\.(com|cl|hotmail|yahoo))$/
    },
    phone: {
      required: true,
      minlength: 9,
      maxlength: 9,
      pattern: /^\d{9}$/
    },
    city: {
      required: true,
      minlength: 10,
      maxlength: 50,
      pattern: /^[a-zA-Z\s\-']+$/
    },
    message: {
      required: true,
      minlength: 10,
      maxlength: 120,
      pattern: /^[a-zA-Z0-9áéíóúÁÉÍÓÚ\s]+$/
    }
  },
  messages: {
    name: {
      required: "Por favor, ingrese su nombre completo",
      minlength: "El nombre completo debe tener al menos 8 caracteres",
      maxlength: "El nombre completo no puede tener más de 30 caracteres",
      pattern: "El nombre solo puede contener letras, espacios y acentos"
    },
    email: {
      required: "Por favor, ingrese su correo electrónico completo",
      minlength: "El correo electrónico debe tener al menos 10 caracteres",
      maxlength: "El correo electrónico no puede tener más de 40 caracteres",
      email: "Por favor ingrese un correo electrónico valido",
      pattern: "Por favor ingrese un correo electrónico con una extensión válida (.com, .cl, .hotmail, .yahoo)"
    },
    phone: {
      required: "Por favor, ingrese su número teléfonico completo",
      minlength: "El número teléfonico debe tener un minimo de 9 números",
      minlength: "El número teléfonico debe tener un máximo de 9 números",
      pattern: "El número teléfonico solo puede contener números"
    },
    city: {
      required: "Por favor, ingrese su ciudad",
      minlength: "La ciudad debe tener al menos 10 caracteres",
      maxlength: "La ciudad no puede tener más de 50 caracteres",
      pattern: "Por favor ingrese una ciudad válida"
    },
    message: {
      required: "Por favor, ingrese su mensaje",
      minlength: "El mensaje debe tener al menos 10 caracteres",
      maxlength: "El mensaje no puede tener más de 120 caracteres",
      pattern: "Por favor ingrese un mensaje válido"
    }
  },
  submitHandler: function(form) {
    alert("El formulario se ha enviado correctamente.");
    form.submit();
  }
});