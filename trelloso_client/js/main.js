// importa os mmódulos user e token
import User from './users.js';
import Token from './token.js';
import TelaHome from './display.js';

// pega os dados do html
let formLogin = document.getElementById("form-login");
let formCreateUser = document.getElementById("form-create-user");
let listUsers = document.getElementById("list-users");
let btnListUsers = document.getElementById("btn-users");
let spanMe = document.getElementById("me");


// captura o evento submit e envia os dados de login
formLogin.addEventListener("submit", (event) => {
  event.preventDefault();
  let formData = new FormData(formLogin);
  User.login(formData).then(token => {
    Token.saveToken(token);
    console.log("Usuario logado.");
    TelaHome.abrirHome();
  }).catch(error => {
    console.log(error);
    console.log("Algo deu errado.");
    alert("Algo deu errado. Tente Novamente.");
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
    formCreateUser.classList.remove("show");
    formCreateUser.classList.add("no-show");
    formLogin.classList.remove("no-show");
    formLogin.classList.add("show");
  }).catch(error => {
    console.log(error.message);
  });
});