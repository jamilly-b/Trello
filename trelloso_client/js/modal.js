function abrirDialogo(action){
    let dialogo = document.getElementById("dialog");
    let form = document.getElementById("modal-newBoard");

    dialogo.classList.remove("no-show");
    dialogo.classList.add("show");  

    function handleSubmit(event){
        event.preventDefault();
        action();
        dialogo.classList.add("no-show");
        dialogo.classList.remove("show");
        form.removeEventListener("submit", handleSubmit);
    }

    form.addEventListener("submit", handleSubmit);

    form.addEventListener("reset", (event)=>{
        event.preventDefault();
        dialogo.classList.remove("show");
        dialogo.classList.add("no-show");
    });
}

export default {abrirDialogo};