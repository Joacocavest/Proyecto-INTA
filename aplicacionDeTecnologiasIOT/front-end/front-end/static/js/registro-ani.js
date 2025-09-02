
document.getElementById("registro-animal").addEventListener("submit", function(event) {
    var cuig = document.getElementById('cuig').value.trim();
    var carabana = document.getElementById('carabana').value.trim();
    var especie = document.getElementById('especie').value.trim();
    var raza = document.getElementById('raza').value.trim();
    var cuidador = document.getElementById('cuidador').value.trim();
    
    if (cuig === '' || carabana === '' || especie === ''|| raza === ''|| cuidador === '' ) 
    {
        event.preventDefault(); 
        alert("Por favor, complete todos los campos.");
    }
});
