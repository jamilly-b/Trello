// pega os dados do html
let formularios = document.querySelectorAll('form')
let formLogin = document.getElementById("form-login");
let formCreateUser = document.getElementById("form-create-user");
let telaPrincipal = document.getElementById("tela-pricipal");

function ExibirTela(){
  telaPrincipal.style.display = 'none';
  formLogin.style.display = 'none';
  formCreateUser.style.display = 'none';

  if(Token.getToken() !== null){
    telaPrincipal.style.display = 'grid';
    formLogin.style.display = 'none';
    formCreateUser.style.display = 'none';
  }
  else if(formLogin.style.display === 'grid'){
    formCreateUser.style.display = 'none';
    telaPrincipal.style.display = 'none';
  }
  else if(formCreateUser.style.display === 'grid'){
    formLogin.style.display = 'none';
    telaPrincipal.style.display = 'none';
  }
}

ExibirTela();