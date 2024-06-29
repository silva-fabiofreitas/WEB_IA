function mindMap(markdown) {
  const { markmap } = window;
  const { Transformer, Markmap, loadCSS, loadJS } = markmap;
  const transformer = new Transformer();

  const { root } = transformer.transform(markdown);
 
    Markmap.create("#mindmap", { autoFit: true }, root);
}

function removeMindMap(selector){
       // Remove o mapa existente, se houver
       const container = document.querySelector(selector);
       if (container.firstChild) {
         container.innerHTML=''
       }
}

function spinner(){
    const spinner = document.getElementsByClassName('js-load')
    for (const el of spinner){
        el.classList.toggle('d-none')
    }
}

function submitForm() {
  const form = document.getElementById("assistente-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new URLSearchParams(new FormData(form));
    
    removeMindMap('#mindmap')
    spinner()

    fetch(`/virtual-assistant/answer/?${data}`, {
      method: "GET",
    })
      .then((resp) => resp.json())
      .then((resp) => {
        spinner()
        mindMap(resp.answer);
      });
  });
}


submitForm();
