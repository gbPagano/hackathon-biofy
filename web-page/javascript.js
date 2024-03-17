const label = document.querySelector("label");
const button = document.querySelector("button");
const form = document.querySelector("#uploadForm");
const result = document.querySelector("#resultado");
const input = document.querySelector('#imageInput');
const preview = document.querySelector("#preview")

input.addEventListener("change", function() {
    preview.innerHTML = "";

    if (this.value == "") {
        label.textContent = "Nenhuma imagem selecionada";
        label.style.backgroundColor = "red";
        button.style.display = "none";
    }
    else {
        let string = this.value.split("\\");
        label.textContent = string[string.length-1];
        button.style.display = "block";
        label.style.backgroundColor = "green";

        let imagem = document.createElement('img');
        imagem.src = URL.createObjectURL(this.files[0]);
        imagem.style.maxWidth = '600px';

        preview.appendChild(imagem);
    }
})

form.addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("example.com/uploadimage", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        result.innerHTML = "Nome Bactéria: " + data.nomeBacteria;
    })
    .catch(error => {
        console.error("Ocorreu um erro", error);
        result.innerHTML = "Ocorreu um erro ao processar a solicitação.";
    });
})