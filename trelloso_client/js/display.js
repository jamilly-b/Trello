// Pega os dados do HTML
let divform = document.getElementById("forms");
let telaHome = document.getElementById("home");
let telaLogin = document.getElementById("tela-login");
let formLogin = document.getElementById("form-login")
let telaCadastro = document.getElementById("tela-cadastro");
let body = document.getElementsByTagName("body");

// exibir a tela de cadastro
document.getElementById('exibir-cadastro').addEventListener('click', function(event) {
  event.preventDefault();
  telaLogin.classList.remove("show");
  telaLogin.classList.add("no-show");
  telaCadastro.classList.add("show");
  telaCadastro.classList.remove("no-show");
});

// exibir a tela de login
document.getElementById('exibir-login').addEventListener('click', function(event) {
  event.preventDefault();
  telaCadastro.classList.add("no-show");
  telaCadastro.classList.remove("show");
  telaLogin.classList.remove("no-show");
  telaLogin.classList.add("show");
});

// Fazer autenticação do usuário para exibir a tela principal
function abrirHome(){
  divform.classList.add("no-show");
  telaLogin.classList.remove("show");
  telaLogin.classList.add("no-show");
  telaHome.classList.remove("no-show");
  telaHome.classList.add("show");
  // consertar o estilo do body
  // document.style.backgroundColor("#282827");
  // body.style.backgroundColor("#282827");
  // body.style.backgroundImage("none");
};

export default {abrirHome};