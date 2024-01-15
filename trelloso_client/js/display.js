function trocarAparicao(some, aparece){
  some.classList.remove("show");
  some.classList.add("no-show");

  aparece.classList.remove("no-show");
  aparece.classList.add("show");
}

function show(div){
  div.classList.remove("no-show");
  div.classList.add("show");
}

function hide(div){
  div.classList.remove("show");
  div.classList.add("no-show");
}

export default {trocarAparicao, show, hide};