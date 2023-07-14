// Variable para mantener el estado visible del carrito
var carritoVisible = false;

// Espera para que todos los elementos de la página se carguen para continuar el script
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}

function ready() {
    // A través de esta función agregaremos funcionalidad para los botones "eliminar" del carrito
    var botonesEliminarItem = document.getElementsByClassName('btn-eliminate');
    for (var i = 0; i < botonesEliminarItem.length; i++) {
        var button = botonesEliminarItem[i];
        button.addEventListener('click', eliminarItemCarrito);
    }

    // A través de esta función, el botón de "sumar cantidad" funcionará correctamente
    var botonesSumarCantidad = document.getElementsByClassName('add-quantity');
    for (var i = 0; i < botonesSumarCantidad.length; i++) {
        var button = botonesSumarCantidad[i];
        button.addEventListener('click', sumarCantidad);
    }

    // A través de esta función, el botón de "restar cantidad" funcionará correctamente
    var botonesRestarCantidad = document.getElementsByClassName('subtract-amount');
    for (var i = 0; i < botonesRestarCantidad.length; i++) {
        var button = botonesRestarCantidad[i];
        button.addEventListener('click', restarCantidad);
    }

    // A través de esta función, el botón de "Agregar al Carrito" funcionará correctamente
    var botonesAgregarAlCarrito = document.getElementsByClassName('button-item');
    for (var i = 0; i < botonesAgregarAlCarrito.length; i++) {
        var button = botonesAgregarAlCarrito[i];
        button.addEventListener('click', agregarAlCarritoClicked);
    }

    // A través de esta función, el botón de "Pagar" funcionará correctamente
    document.getElementsByClassName('btn-pay')[0].addEventListener('click', pagarClicked);
}

// Función para eliminar el item seleccionado del carrito
function eliminarItemCarrito(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.remove();

    // Llamamos la función 'actualizarTotalCarrito' para mostrar el monto total del carrito
    actualizarTotalCarrito();
    console.log("Actualizando el total del carrito...");

    // Llamamos la función 'ocultarCarrito' para determinar si existen elementos en el carrito una vez que se elimine
    // En caso contrario, se ocultará el carrito
    ocultarCarrito();
}

// Función para ocultar el carrito en caso que esté vacío de elementos
function ocultarCarrito() {
    var carritoItems = document.getElementsByClassName('shipping-items')[0];
    if (carritoItems.childElementCount == 0) {
        var carrito = document.getElementsByClassName('shipping')[0];
        carrito.style.marginRight = '-100%';
        carrito.style.opacity = '0';
        carritoVisible = false;

        // El siguiente código maximiza los productos una vez que se oculte el carrito
        var items = document.getElementsByClassName('container-items')[0];
        items.style.width = '100%';
    }
}

// Función para actualizar el total de precio del carrito
function actualizarTotalCarrito() {

    // Definimos el contenedor del carrito
    var carritoContenedor = document.getElementsByClassName('shipping')[0];
    var carritoItems = carritoContenedor.getElementsByClassName('shipping-item');
    var total = 0;

    // A través de este código, recorremos cada elemento del carrito para actualizar el total
    for (var i = 0; i < carritoItems.length; i++) {
        var item = carritoItems[i];
        var precioElemento = item.getElementsByClassName('shipping-item-price')[0];

        // Quitamos el símbolo peso y el punto de milesimo sobre el producto cliqueado
        var precio = parseFloat(precioElemento.innerText.replace('$', '').replace('.', ''));
        var cantidadItem = item.getElementsByClassName('shipping-item-quantity')[0];
        var cantidad = cantidadItem.value;
        total = total + (precio * cantidad);
    }

    // Realizamos las operaciones con variables previamente creadas para mostrar el resultado total al momento de quitar un producto
    total = Math.round(total * 100) / 100;
    document.getElementsByClassName('total-cart-price')[0].innerText = '$' + formatPrice(total);
}

// Esta función aumenta en 1 el elemento seleccionado
function sumarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    var cantidadActual = parseInt(selector.getElementsByClassName('shipping-item-quantity')[0].value);
    console.log(cantidadActual);

    // Aumenta en 1 la cantidad
    cantidadActual++;
    selector.getElementsByClassName('shipping-item-quantity')[0].value = cantidadActual;

    // Actualiza el total del carrito
    actualizarTotalCarrito();
}

// Esta función resta en 1 el elemento seleccionado
function restarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    var cantidadActual = parseInt(selector.getElementsByClassName('shipping-item-quantity')[0].value);
    console.log(cantidadActual);

    // Resta en 1 la cantidad
    cantidadActual--;

    // Validación para comprobar que el valor no sea menor a 1
    if (cantidadActual >= 1) {
        selector.getElementsByClassName('shipping-item-quantity')[0].value = cantidadActual;

        // Actualiza el total del carrito
        actualizarTotalCarrito();
    }
}

// Esta función al momento de cliquear se sumará el producto al carrito
function agregarAlCarritoClicked(event) {
    var button = event.target;
    var item = button.parentElement;
    var titulo = item.getElementsByClassName('tittle-item')[0].innerText;
    console.log(titulo);
    var precio = item.getElementsByClassName('price-item')[0].innerText;
    var imagenSrc = item.getElementsByClassName('img-item')[0].src;
    console.log(imagenSrc);

    // La siguiente función agregará el elemento al carrito. Por lo tanto, se mandarán por parámetro los valores.
    agregarItemAlCarrito(titulo, precio, imagenSrc);
    actualizarTotalCarrito();

    // Llamamos a la función para hacer visible el carrito cuando agregamos un producto por primera vez
    hacerVisibleCarrito();
}

// Función para agregar el producto al carrito
function agregarItemAlCarrito(titulo, precio, imagenSrc) {
    var item = document.createElement('div');
    item.classList.add('shipping-item');
    var itemsCarrito = document.getElementsByClassName('shipping-items')[0];

    // Validación para comprobar que dicho item ya está ingresado en el carrito
    var nombresItemsCarrito = itemsCarrito.getElementsByClassName('shipping-item-tittle');
    for (var i = 0; i < nombresItemsCarrito.length; i++) {
        if (nombresItemsCarrito[i].innerText == titulo) {
            alert("El producto ya se encuentra agregado al carrito");
            return;
        }
    }

    // Este código agrega la imagen, titulo y el precio al carrito
    var itemsCarritoContenido = `
    <div class="shipping-item">
      <img src="${imagenSrc}" alt="" width="80px">
      <div class="shipping-item-details">
        <span class="shipping-item-tittle">${titulo}</span>
        <div class="selector-quantity">
          <i class="fa fa-minus subtract-amount"></i>
          <input type="text" value="1" class="shipping-item-quantity" disabled>
          <i class="fa fa-plus add-quantity"></i>
        </div>
        <span class="shipping-item-price">${formatPrice(precio)}</span>
      </div>
      <span class="btn-eliminate">
        <i class="fa fa-trash eliminate"></i>
      </span>
    </div>
  `;
    item.innerHTML = itemsCarritoContenido;
    itemsCarrito.append(item);

    // Agregamos la función de eliminar el nuevo item que agregamos al carrito
    item.getElementsByClassName('btn-eliminate')[0].addEventListener('click', eliminarItemCarrito);

    // Agregamos la función de sumar el nuevo item que agregamos al carrito
    var botonSumarCantidad = item.getElementsByClassName('add-quantity')[0];
    botonSumarCantidad.addEventListener('click', sumarCantidad);

    // Agregamos la función de restar el nuevo item que agregamos al carrito
    var botonRestarCantidad = item.getElementsByClassName('subtract-amount')[0];
    botonRestarCantidad.addEventListener('click', restarCantidad);
}

// Función para cuando el usuario realiza la compra
function pagarClicked(event) {
    alert("Gracias por su compra");

    // Elimina todos los elementos del carrito para aparentar el pago
    var carritoItems = document.getElementsByClassName('shipping-items')[0];
    while (carritoItems.hasChildNodes()) {
        carritoItems.removeChild(carritoItems.firstChild);
    }
    actualizarTotalCarrito();

    // Llamar a la función para ocultar el carrito
    ocultarCarrito();
}

// Función para hacer visible al carrito por primera vez
function hacerVisibleCarrito() {
    carritoVisible = true;
    var carrito = document.getElementsByClassName('shipping')[0];
    carrito.style.marginRight = '0';
    carrito.style.opacity = '1';

    var items = document.getElementsByClassName('shipping-items')[0];
    items.style.width = '100%';
}

// Función para formatear el precio en el formato deseado
function formatPrice(price) {
    return price.toLocaleString('en', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    });
}