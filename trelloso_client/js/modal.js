let modal = document.getElementById("modal");

function abrirDialogo(action){
    document.getElementById("create-board").addEventListener("click", (event) =>{
        event.preventDefault();
        modal.classList.remove("no-show");
        modal.classList.add("show");  
        modal.addEventListener("submit", (event)=>{
          event.preventDefault();
          action();
        })
        modal.addEventListener("reset", (event)=>{
            event.preventDefault();
            modal.classList.remove("show");
            modal.classList.add("no-show");
        });
    });
}

export default {abrirDialogo};