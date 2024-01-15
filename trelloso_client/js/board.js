import User from "./users.js";
import Fetch from './fetch.js';
import Display from "./display.js";
import Modal from "./modal.js";
import display from "./display.js";

let home = document.getElementById("main-content");
let listPage = document.getElementById("list-page");
let listaQuadros = document.getElementById("quadros");
let quadrosFavoritos = document.getElementById("quadros-fav");

// exibe os quadros

function exibirBoards(){
  User.myBoards().then((array)=>{
    listaQuadros.innerHTML = "";
    quadrosFavoritos.innerHTML = "";

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

          Display.trocarAparicao(home, listPage);

          let divListas = document.getElementById("div-lists");
          localStorage.setItem("board-id", id);
   
          // chamarPaginaLista(localStorage.getItem("board-id"));

          exibirListasDoCard(id);
          function exibirListasDoCard(id){

            let todasListasUl = document.getElementById(`board-${id}-lists`);
            if (!todasListasUl) {
              todasListasUl = document.createElement('ul');
              todasListasUl.id = `board-${id}-lists`;
              todasListasUl.classList.add("all-lists");
              divListas.appendChild(todasListasUl);
            }

            let addNovaLista = document.createElement('div');
            addNovaLista.innerHTML = `
              <div id="create-new-list-${id}" class="create-new-list">
                <i class="fa fa-plus-square-o" aria-hidden="true"></i>
              </div>
            `;

            
            divListas.innerHTML = "";
            
            Fetch.request(`/boards/${id}/lists`, id).then(listas => {
              listas.forEach(lista => {
                console.log("Lista: ", lista);
                let nomeLista = lista.name;
                let listaID = lista.id;
                let cards = lista.cards;
  
                let novalista = document.createElement('li');
  
                
                novalista.innerHTML =
                `
                <li class="list" id="${listaID}">
                    <div class="list-content" id="list-content-${listaID}">
                        <div class="list-info"> 
                            <span class="list-Name">${nomeLista}</span>
                            <div class="list-icons">
                                <i class="fa fa-trash-o" aria-hidden="true"></i>
                                <span></span>
                            </div>
                        </div>
    
                        <div class="create-new-card">
                            <i class="fa fa-plus-circle" aria-hidden="true"></i>
                            <span class="new-card">Adicionar um cartão</span>
                        </div>
                    </div>
                </li>
                `

                todasListasUl.appendChild(novalista);
                divListas.appendChild(todasListasUl);

                exibirCards(cards, listaID);
              })
              
              divListas.append(addNovaLista);
            })

            
          }
          event.stopPropagation();
        })

        let nofav = document.getElementById(`star-o-${id}`);
        let fav = document.getElementById(`star-${id}`);
        
        favoritarBoard(id, element);
        desfavoritarBoard(id, element);
        deletarBoard(id);

        if (element.favorito === true){
          quadrosFavoritos.appendChild(quadro);
          Display.trocarAparicao(nofav, fav);
        }
        else {
          Display.trocarAparicao(fav, nofav);
        }

      });
  });
}

// exibir cards

function exibirCards(cards, listaID) {
  console.log("Cards: \n", cards);
  if(cards !== null && cards.length > 0) {
    console.log(cards);
    
      console.log(cards);
      console.log("tamanho do array cards: ",cards.length);
  
      let divCards = document.createElement('div');
      divCards.classList.add("show-cards");
  
      let todosCardsUl = document.createElement('ul');
      todosCardsUl.classList.add("all-cards");
  
      if (!divCards.querySelector(".all-cards")) {
        divCards.appendChild(todosCardsUl);
      }
  
      cards.forEach(card => {
        let nome = card.name;
        let cardID = card.id;
        let comments = card.cardcomments_count;
        let members = card.cardmembers_count;
        let tags = card.tags;
  
        let cardLista = document.createElement('li');
  
        cardLista.innerHTML =
          `
          <li class="card">
            <div class="tags-board">
                <ul class="tags">
                  <li class="tag"></li>
                  <li class="tag"></li>
                  <li class="tag"></li>
                </ul>
                <div class="delete-card" id="delete-card-${cardID}">
                  <i class="fa fa-trash-o" aria-hidden="true"></i>
                </div>
            </div>
            <div class="card-data"> 
                <span id="card-description">${nome}</span> 
                <div class="card-icons">
                  <i class="fa fa-users" aria-hidden="true"> ${members} </i>
                  <i class="fa fa-comments" aria-hidden="true"> ${comments} </i>
                </div>
            </div>
          </li>
        `;
  
        todosCardsUl.appendChild(cardLista);
      });
  
      let div = document.getElementById(`list-content-${listaID}`);
      if (div) {
        div.appendChild(divCards);
      } else {
        console.error(`Elemento com ID 'list-content-${listaID}' não encontrado.`);
      }
  }
  else {
    
  }
 
}

// adicionar nova lista

// NovaLista.addEventListener("click", (event) => {
//   event.preventDefault();
//   Modal.abrirDialogo(criarLista);
// });


function criarLista(boardID){

  let nome = document.querySelector('input[name="nome"]').value;

  const newlist = {
    name: nome,
    board_id: boardID,
    position: 0
  }

  let createList = document.getElementById(`create-new-list-${listId}`);

  Fetch.request('/lists/', newlist, 'POST').then(event=>{
    console.log(event);
  })
}



// novo quadro

function novoQuadro(){
  let nome = document.querySelector('input[name="nome"]').value;
  let color = document.querySelector('input[name="color"]').value;
  const boardData = {
    name: nome,
    color: color
  }; 

  Fetch.request('/boards/', boardData, 'POST').then(newBoard => {
    console.log(newBoard);
    exibirBoards();
  })
  .catch(error => {
    console.error(error);
  });
  
}


// função para deletar um board 

function deletarBoard(id){

  let del = document.getElementById(`delete-${id}`);

  del.addEventListener("click", (event) =>{
    event.preventDefault();
    Fetch.request(`/boards/${id}`, id, 'DELETE').then(deleteBoard => {
      alert(`Quadro removido.`);
      exibirBoards();
    }).catch(error =>{
      console.log(error);
    })
    event.stopPropagation();
  })
}

// desfavoritar board

function desfavoritarBoard(id, element){
  let nofav = document.getElementById(`star-o-${id}`);
  let fav = document.getElementById(`star-${id}`);
  fav.addEventListener("click", (event) => {
    event.preventDefault();
    element.favorito = false;
    Fetch.request(`/boards/${id}`, element, 'PATCH').then(favBoard => {
      exibirBoards();
    }).catch(error =>{
      console.log(error);
    })
    event.stopPropagation();
  });
}

// favoritar um board
function favoritarBoard(id, element){
  let nofav = document.getElementById(`star-o-${id}`);
  let fav = document.getElementById(`star-${id}`);
  
  nofav.addEventListener("click", (event) => {
    event.preventDefault();
    element.favorito = true;
    Fetch.request(`/boards/${element.id}`, element, 'PATCH').then(favBoard => {
      exibirBoards();
    }).catch(error =>{
      console.log(error);
    })
    event.stopPropagation();
  });
}

export default{novoQuadro,exibirBoards};
