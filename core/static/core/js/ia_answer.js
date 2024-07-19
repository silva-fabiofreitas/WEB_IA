function mindMap(markdown) {
  const { markmap } = window;
  const { Transformer, Markmap, loadCSS, loadJS } = markmap;
  const transformer = new Transformer();

  const { root } = transformer.transform(markdown);

  localStorage.setItem('mindMap', markdown)

  Markmap.create("#mindmap", { autoFit: true }, root);
}

function removeMindMap(selector) {
  // Remove o mapa existente, se houver
  const container = document.querySelector(selector);
  if (container.firstChild) {
    container.innerHTML = ''
  }
}

function spinner() {
  const spinner = document.getElementsByClassName('js-load')
  for (const el of spinner) {
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


function saveMindMap() {
  saveButton = document.getElementById('saveMindMap');
  const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'))

  saveButton.addEventListener('click', (event) => {
    const form = document.getElementById("formMindMap");
    const mindMapMarkdown = localStorage.getItem('mindMap');

    const data = new FormData(form);
    data.append('content', mindMapMarkdown);

    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const url = '/mind-map/create/';

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken // Include the CSRF token in the header
      },
      body: data
    })
      .then(response => response.json())
      .then(data => {
        form.reset()
        myModal.hide()


      })
      .catch(error => {
        console.error('Error:', error);
      });


  })
}


submitForm();
saveMindMap();






// Consumir stream de dados 
async function readData(url) {
  const response = await fetch(url);
  for await (const chunk of response.body) {
    var string = new TextDecoder().decode(chunk);
    console.log(string)
    // Do something with each "chunk"
  }
  // Exit when done
  }

