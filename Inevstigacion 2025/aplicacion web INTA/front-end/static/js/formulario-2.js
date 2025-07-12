
document.getElementById("formulario-2").addEventListener("submit", function(event) {
    var cuig = document.getElementById('cuig').value.trim();
    var usuario = document.getElementById('usuario').value.trim();
    var password = document.getElementById('password').value.trim();

    if (cuig === '' || usuario === '' || password === '' ) {
        event.preventDefault(); // ⛔ Detiene el envío del formulario
        alert("Por favor, complete todos los campos.");
    }
});
