function Explicacion(nivel){
    var nombreElemento = document.getElementsByName("nivel_administrador")[0];
    var explicacionElemento = document.getElementById("explicacion");

    if (nombreElemento.value == "1"){
        explicacionElemento.textContent = "El nivel de administrador 1 tiene permisos para realizar la creación, modificación, eliminación y busqueda del modelo 'Imagenes' a travez del panel de control.";
    } else if(nombreElemento.value == "2"){
        explicacionElemento.textContent = "El nivel de administrador 2 tiene permisos para realizar la creación, modificación, eliminación y busqueda de los modelos 'Imagenes' y 'Usuarios' a travez del panel de control."
    } else if(nombreElemento.value == "3"){
        explicacionElemento.textContent = "El nivel de administrador 3 tiene permisos para realizar la creación, modificación, eliminación y busqueda de todos los modelos del panel de control."
    } else {
        explicacionElemento.textContent = "";
    }
}