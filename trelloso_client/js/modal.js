let dialogo = document.getElementById("dialog");
let form = document.getElementById("modal-newBoard");

function abrirDialogo(action){
    dialogo.classList.remove("no-show");
    dialogo.classList.add("show");  
    form.addEventListener("submit", (event)=>{
        event.preventDefault();
        action();
        dialogo.classList.add("no-show");
        dialogo.classList.remove("show");
    })
    form.addEventListener("reset", (event)=>{
        event.preventDefault();
        dialogo.classList.remove("show");
        dialogo.classList.add("no-show");
    });
}

export default {abrirDialogo};