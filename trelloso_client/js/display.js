// import token from "./token";
// import user from "./users";

// Pega os dados do HTML
let form = document.getElementById("forms");
let telaHome = document.getElementById("home");
let telaLogin = document.getElementById("form-login");
let telaCadastro = document.getElementById("form-create-user");

// exibe apenas a tela de login inicialmente
telaHome.style.display = 'none';
telaLogin.style.display = 'flex';
telaCadastro.style.display = 'none';

document.getElementById('exibir-cadastro').addEventListener('click', function(event) {
  event.preventDefault();
  telaLogin.style.display = 'none';
  telaCadastro.style.display = 'flex';
  telaHome.style.display = 'none';
});

document.getElementById('exibir-login').addEventListener('click', function(event) {
  event.preventDefault();
  telaLogin.style.display = 'flex';
  telaCadastro.style.display = 'none';
  telaHome.style.display = 'none';
});

// Fazer autenticação do usuário para exibir a tela principal usando auth e token
telaLogin.addEventListener('submit', function(event) {
  event.preventDefault();
  form.style.display = "none"
  telaHome.style.display = 'grid';
});