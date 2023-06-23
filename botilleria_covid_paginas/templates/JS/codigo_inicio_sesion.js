$("#form-login").submit(function(event) {
    // Evita el envío del formulario por defecto
    event.preventDefault();

    // Obtenemos los valores de cada campo a válidar
    var login_field = $("#login_field").val();
    var password = $("#password").val();

    // Verifica si el nombre de usuario cumple con las reglas de longitud
    if (login_field.length < 8 || login_field.length > 30) {
        alert("Por favor, ingrese un nombre de usuario entre 8 y 30 caracteres.");
        return;
    }

    // Verifica si el nombre de usuario es válido según el patrón establecido
    if (!/^[a-zA-Z0-9_]+$/.test(login_field)) {
        alert("Por favor, ingrese un nombre de usuario válido.");
        return;
    }
    
    // Verifica si el nombre de usuario esta vacio
    if (login_field.trim() === "") {
        alert("Por favor, ingrese un nombre de usuario.");
        return;
    }

    // Verifica si la contraseña cumple con la longitud mínima y máxima establecidas
    if (password.length < 8 || password.length > 40) {
        alert("Por favor, ingrese una contraseña que tenga entre 8 y 40 caracteres.");
        return;
    }

    // Verifica si la contraseña es válido según el patrón establecido
    if (!/^[a-zA-Z0-9\s]+$/.test(password)) {
        alert("Por favor, ingrese una contraseña válida.");
        return;
    }

    // Verifica si el campo está vacío
    if (password.trim() === "") {
        alert("Por favor, ingrese su contraseña.");
        return;
    }
    # Preguntar por que no funciona, y por que se ve en gris
    $.ajax({
        console.log("funciona");
        url: "/inicio_sesion/",
        type: "POST",
        data: {
            login_field: login_field,
            password: password
        },
        success: function(response) {
            window.location.href = "/";  // Redirige al usuario a la página de inicio
        },
        error: function(xhr, status, error) {
            alert("Error al iniciar sesión: " + error);
        }
    });    
});