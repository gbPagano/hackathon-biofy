const label = document.querySelector("label");
const button = document.querySelector("button");
const form = document.querySelector("#uploadForm");
const result = document.querySelector("#resultado");
const input = document.querySelector('#imageInput');
const fileName = document.querySelector('#file-name');

input.addEventListener("change", function() {
    let string = this.value.split("\\");
    fileName.textContent = string[string.length-1];
    button.style.display = "block";
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