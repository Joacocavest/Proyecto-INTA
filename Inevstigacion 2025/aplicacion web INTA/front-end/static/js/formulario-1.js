function validarFormularioCompleto() {
    var nombre = document.getElementById('nombre').value.trim();
    var apellido = document.getElementById('apellido').value.trim();
    var cuit = document.getElementById('cuit').value.trim();
    var sexo = document.getElementById('sexo').value.trim();
    var email = document.getElementById('email').value.trim(); // ojo: id="correo"

    if (nombre === '' || apellido === '' || cuit === '' || sexo === '' || email === '') {
        alert('Por favor, complete todos los campos.');
    } else {
        // Redirigir a otra página manualmente
        window.location.href = './formulario-usuario-2.html';
    }
}
