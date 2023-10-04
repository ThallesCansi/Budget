//ao carregar a página
window.onload = function () {
    form = document.querySelector("form");
    for (const [key, value] of new FormData(form)) {
        campo = document.getElementById(key);
        textoErro = campo.parentElement.querySelector("span");
        if (textoErro) {
            textoErro.textContent = "";
            textoErro.classList.add("d-none");
            campo.classList.remove("is-invalid");
            campo.classList.remove("is-valid");
        }
    }

    if (fieldValues) {
        for (const [key, value] of Object.entries(fieldValues)) {
            campo = document.getElementById(key);
            campo.value = value;
            campo.classList.add("is-valid");
        }
    }
    
    if (validationErrors) {
        for (const [key, value] of Object.entries(validationErrors)) {
            campo = document.getElementById(key);
            textoErro = campo.parentElement.querySelector("span");
            if (textoErro) {
                textoErro.textContent = value[0];
                textoErro.classList.remove("d-none");
                campo.classList.remove("is-valid");
                campo.classList.add("is-invalid");
            }
        }
    }
}