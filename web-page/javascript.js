const label = document.querySelector("label");
const button = document.querySelector("button");
const form = document.querySelector("#uploadForm");
const result = document.querySelector("#resultado");
const input = document.querySelector('#imageInput');
const preview = document.querySelector("#preview")
const bacteria = document.querySelectorAll('path');
const title = document.querySelector(".title");

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
        window.scrollTo({
            top: document.documentElement.scrollHeight || document.body.scrollHeight,
            behavior: 'smooth'
        });
    }
})

form.addEventListener("submit", function(event) {
    event.preventDefault();

    title.style.backgroundImage = `url(${URL.createObjectURL(form.files[0])})`;
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });

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

addEventListener('mousemove', function(event) {

    bacteria.forEach(bacterium => {
        const x = event.clientX / 200;
        const y = event.clientY / 200;

        bacterium.style.transform = `translate(${x}px, ${y}px)`;
    });  
});
