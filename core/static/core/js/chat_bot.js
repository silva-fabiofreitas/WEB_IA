function spinner() {
  const spinner = document.getElementsByClassName('js-load')
  for (const el of spinner) {
    el.classList.toggle('d-none')
  }
}

async function setAnswer(answer, element){
  const elementAnswer = document.getElementById('answer')
  elementAnswer.append(element)
  element.innerHTML +=answer
} 


function setQuestion(question){
  const paragraphText = document.createElement('p')
  const elementAnswer = document.getElementById('answer')
  paragraphText.classList.add('border', 'rounded-1', 'p-2', 'text-bg-light', 'shadow-sm')
  paragraphText.innerHTML = question
  elementAnswer.append(paragraphText)

}

function submitForm() {
  const form = document.getElementById("assistente-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new URLSearchParams(new FormData(form));
    setQuestion(data.get('question'))
    spinner()
    readData(`/chatbot/?${data}`)
    spinner()
  });
}

submitForm();


// Consumir stream de dados 
async function readData(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
    "X-Requested-With": "XMLHttpRequest",
    }
  });

  const paragraphText = document.createElement('p')
  const iconIA = document.createElement('i')
  iconIA.className = 'bi-back pe-2'
  paragraphText.append(iconIA)
  paragraphText.classList.add('p-2', 'bg-white')
  
  for await (const chunk of response.body) {
    var string = new TextDecoder().decode(chunk);
    setAnswer(string, paragraphText)
    // Do something with each "chunk"
  }
  // Exit when done
  }



