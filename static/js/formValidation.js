//ao carregar a página
window.onload = function () {
    formCadastro = document.querySelector("#formCadastro");
    for (const [key, value] of new FormData(formCadastro)) {
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

window.onload = function () {
    formLogin = document.querySelector("#formLogin");
    for (const [key, value] of new FormData(formLogin)) {
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

window.onload = function () {
    formCadastro = document.querySelector("#alterarSenha");
    for (const [key, value] of new FormData(formCadastro)) {
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