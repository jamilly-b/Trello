// importa os mmódulos user e token
import User from './users.js';
import Fetch from './fetch.js';
import Token from './token.js';
import Tela from './display.js';
import Modal from './modal.js';



let formLogin = document.getElementById("form-login");
let formCreateUser = document.getElementById("form-create-user");
let telaLogin = document.getElementById("tela-login");
let telaCadastro = document.getElementById("tela-cadastro");
let listUsers = document.getElementById("list-users");
let btnListUsers = document.getElementById("btn-users");
let telaHome = document.getElementById("home");
let spanMe = document.getElementById("me");

// captura o evento submit e envia os dados de login
formLogin.addEventListener("submit", (event) => {
  event.preventDefault();
  let formData = new FormData(formLogin);
  User.login(formData).then(token => {
    Token.saveToken(token);
    console.log("Usuario logado.");
    Tela.mudarTela(telaLogin, telaHome);
  }).catch(error => {
    console.log(error);
    alert("Usuário ou senha incorretos. Tente Novamente.");
  });
});

// captura o evento click e lista os usuários cadastrados
btnListUsers.addEventListener("click", (event) => {
  listUsers.innerHTML = "";
  User.getAll().then(users=>{
    for (let user of users) {
      const li = document.createElement("li");
      li.innerHTML = user.name;
      listUsers.appendChild(li);
    }
  })
})

// captura o evento de submit para cadastrar um usuário
formCreateUser.addEventListener("submit", (event) => {
  event.preventDefault();

  const name = document.getElementById("new-name").value;
  const username = document.getElementById("new-username").value;
  const password = document.getElementById("new-password").value;
  const avatar = document.getElementById("new-avatar").value;
  console.log(name, username, password, avatar);

  // cria um novo usuário com os dados do form
  User.create(name, username, password, avatar).then(user=>{
    console.log(user);
    alert("Usuário " + username + " cadastrado com sucesso!");
    Tela.mudarTela(telaCadastro, telaLogin);
  }).catch(error => {
    console.log(error.message);
  });
});


// troca a tela de login pela de cadastro
document.getElementById("exibir-login").addEventListener("click", (event) => {
  event.preventDefault();
  Tela.mudarTela(telaCadastro, telaLogin);
})
document.getElementById("exibir-cadastro").addEventListener("click", (event) => {
  event.preventDefault();
  Tela.mudarTela(telaLogin, telaCadastro);
})

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
  })
  .catch(error => {
    console.error(error);
  });
}
Modal.abrirDialogo(novoQuadro);


//mostra todos os quadros

let listaQuadros = document.getElementById("quadros");
let quadrosFavoritos = document.getElementById("quadros-fav");
User.myBoards().then((array)=>{
  array.forEach(element => {
    let quadro = document.createElement("li");
    
    quadro.innerHTML =  `
      <div class="board" id = "board-${element.id}">
        <span>${element.name}</span>
        <div class="board-icons">
          <i class="fa fa-star-o show" aria-hidden="true"></i>
          <i class="fa fa-star no-show" aria-hidden="true"></i>
          <i class="fa fa-trash-o" aria-hidden="true"></i>
        </div>
      </div>
    `;
    listaQuadros.appendChild(quadro);

    let div = document.querySelector(".board");
    div.style.backgroundColor = element.color;

    if (element.favorite === true){
      quadrosFavoritos.appendChild(quadro);
    }
  });
})


// favoritar quadro

// let emptyStar = document.getElementsByClassName("fa fa-star-o show");
// let fullStar = document.getElementsByClassName("fa fa-star no-show");

// emptyStar.addEventListener("click", (event) => {
//   let board = document.getElementsByClassName("board");
//   board.favorite = true;
//   emptyStar.Tela.mudarTela(emptyStar, fullStar);
// });