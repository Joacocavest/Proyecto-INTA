function validarInicioSesion() {
    var nombre = document.getElementById('name').value.trim();
    var contraseña = document.getElementById('password').value.trim();

    if (nombre === '' || contraseña === '') {
        alert('Por favor, complete todos los campos.');
    } else {
        // alert('Campos llenos, redirigiendo...');
        // Redirigir a la página principal
        window.location.href = 'pagina_principal.html';  // Aquí colocas la ruta correcta a tu página principal
    }
}

//hola mundo
