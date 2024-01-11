// importa os mmódulos user e token
import User from './users.js';
import Fetch from './fetch.js';
import Token from './token.js';
import Tela from './display.js';

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

let modal = document.getElementById("modal");

document.getElementById("create-board").addEventListener("click", (event) =>{
  event.preventDefault();
  modal.classList.remove("no-show");
  modal.classList.add("show");  
  modal.addEventListener("submit", (event)=>{
    event.preventDefault();
    let nome = document.querySelector('input[name="nome"]').value;

    const boardData = {
      name: nome,
      color: "#FFFFF",
      favorito: false
    };
    console.log(boardData);

    Fetch.request('/boards/', boardData, 'POST').then(newBoard => {
      console.log(newBoard);
    })
    .catch(error => {
      console.error(error);
    });

    
    

    // modal.classList.remove("show");
    // nome.value = "";
  })
});



