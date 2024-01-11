function mudarTela(some, aparece){
  if (some.classList.contains("show")){
    some.classList.remove("show");
    some.classList.add("no-show");
  }
  if (aparece.classList.contains("no-show")){
    aparece.classList.remove("no-show");
    aparece.classList.add("show");
  }
}

export default {mudarTela};