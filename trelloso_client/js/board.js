import User from "./users.js";
import Fetch from './fetch.js';
import Trocar from "./display.js";
import Modal from "./modal.js";

let listaQuadros = document.getElementById("quadros");
let quadrosFavoritos = document.getElementById("quadros-fav");

function exibirBoards(){
    User.myBoards().then((array)=>{
        listaQuadros.innerHTML = "";
      array.forEach(element => {
        let quadro = document.createElement("li");
        let id = element.id;
        
        quadro.innerHTML =  `
          <div class="board" id = "board-${id}">
            <span>${element.name}</span>
            <div class="board-icons">
              <i class="fa fa-star-o show" aria-hidden="true" id = "star-o-${id}"></i>
              <i class="fa fa-star no-show" aria-hidden="true" id = "star-${id}"></i>
              <i class="fa fa-trash-o" aria-hidden="true" id = "delete-${id}"></i>
            </div>
          </div>
        `;
    
        listaQuadros.appendChild(quadro);
        document.getElementById(`board-${id}`).style.backgroundColor = element.color;
        
        quadro.addEventListener("click", (event) => {
          event.preventDefault();
          localStorage.setItem("board-id", `board-${id}`);
        })
    
        // favoritarQuadro(element, id);
        if (element.favorite === true){
          quadrosFavoritos.appendChild(quadro);
        }
      });
    });
  }

// novo quadro

function novoQuadro(){
  let nome = document.querySelector('input[name="nome"]').value;
  let color = document.querySelector('input[name="color"]').value;
  const boardData = {
    name: nome,
    color: color,
    favorito: false
  };
  console.log(boardData);

  Fetch.request('/boards/', boardData, 'POST').then(newBoard => {
    console.log(newBoard);
    console.log(newBoard.id);
    exibirBoards();
    // favoritarQuadro(newBoard.id);
  })
  .catch(error => {
    console.error(error);
  });
}



function favoritarQuadro(id){

  let quadro = document.getElementById(`board-${id}`);
  let emptyStar = document.getElementById(`star-o-${id}`);
  let fullStar = document.getElementById(`star-${id}`);
  let del = document.getElementById(`delete-${id}`);

  emptyStar.addEventListener("click", (event) => {
      event.preventDefault();
      quadro.favorite = true;
      Trocar.mudarTela(emptyStar, fullStar);
  });

  fullStar.addEventListener("click", (event) => {
      event.preventDefault();
      quadro.favorite = false;
      Trocar.mudarTela(fullStar, emptyStar);
  });

  del.addEventListener("click", (event) =>{
    event.preventDefault();
    Fetch.request(`/boards/${id}`, id, 'DELETE').then(deleteBoard => {
      alert(`Quadro ${id} removido`);
    }).catch(error =>{
      console.log(error);
    })
  })
}

export default{novoQuadro,exibirBoards};
