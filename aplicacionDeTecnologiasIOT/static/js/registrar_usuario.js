



document.addEventListener("DOMContentLoaded", () => {
    const cuigInput = document.querySelector("#id_CUIG");
    const cuigContainer = document.querySelector("#cuig-container");
    const radioSenasa = document.querySelector("#radioSenasa");
    const radioParticular = document.querySelector("#radioParticular");
    const opcionesParticular = document.querySelector("#opciones-particular");
    const selectAuxiliar = document.querySelector("#selectAuxiliar");
    const btnCrearAuxiliar = document.querySelector("#btnCrearAuxiliar");
    const nuevoAuxiliarNombre = document.querySelector("#nuevoAuxiliarNombre");

    // --- Inicialmente ocultar CUIG y opciones particulares ---
    cuigContainer.style.display = "none";
    opcionesParticular.style.display = "none";

    // --- Función para mostrar según tipo de productor ---
    function actualizarVistaTipoProductor() {
        if (radioSenasa.checked) {
            cuigContainer.style.display = "flex";
            opcionesParticular.style.display = "none";
            cuigInput.disabled = false;
            cuigInput.value = "";
        } else if (radioParticular.checked) {
            cuigContainer.style.display = "none";
            opcionesParticular.style.display = "flex";
            cuigInput.disabled = false;
            cuigInput.value = "";
            cargarAuxiliares(); // Mostrar lista al elegir particular
        }
    }

    radioSenasa.addEventListener("change", actualizarVistaTipoProductor);
    radioParticular.addEventListener("change", actualizarVistaTipoProductor);

    // --- Cargar establecimientos AUX existentes ---
    function cargarAuxiliares() {
        fetch("/listar_establecimientos_auxiliares/")
            .then(res => res.json())
            .then(data => {
                selectAuxiliar.innerHTML = `<option value="">-- Elegir existente --</option>`;
                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(aux => {
                        const opt = document.createElement("option");
                        opt.value = aux.CUIG;
                        opt.textContent = `${aux.CUIG} - ${aux.nombre}`;
                        selectAuxiliar.appendChild(opt);
                    });
                } else {
                    const opt = document.createElement("option");
                    opt.disabled = true;
                    opt.textContent = "No hay establecimientos particulares aún";
                    selectAuxiliar.appendChild(opt);
                }
            })
            .catch(err => console.error("Error al cargar auxiliares:", err));
    }

    // --- Al seleccionar un auxiliar existente ---
    selectAuxiliar.addEventListener("change", () => {
        const selected = selectAuxiliar.value;
        cuigInput.value = selected || "";
    });

    // --- Crear nuevo auxiliar ---
    btnCrearAuxiliar.addEventListener("click", () => {
        const nombre = nuevoAuxiliarNombre.value.trim();
        if (!nombre) {
            alert("⚠️ Por favor, indique un nombre para el nuevo establecimiento particular.");
            return;
        }

        fetch("/crear_establecimiento_auxiliar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: `nombre=${encodeURIComponent(nombre)}`
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`✅ Establecimiento creado: ${data.CUIG}`);
                cuigInput.value = data.CUIG;
                nuevoAuxiliarNombre.value = "";
                cargarAuxiliares(); // recargar lista
            } else {
                alert("❌ Error al crear el establecimiento.");
            }
        })
        .catch(err => console.error("Error al crear auxiliar:", err));
    });

    // --- Helper para CSRF ---
    function getCSRFToken() {
        const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfInput ? csrfInput.value : "";
    }
});
