const body = document.querySelector('body');
const button = document.querySelector('.button');
const word = document.createElement('h1');
const definition = document..createElement('p');

const randomWord = () => {
    fetch('https://random-word-api.herokuapp.com/word?number=1')
    .then(response => {
        return response.json();
    })
    .then(response => {
        word.textContent = response;
        body.appendChild(word);
        randomDefinition(word);
    })
    .catch (err => {
        console.log(err);
    })
}

const randomDefinition = (word) =>{
    fetch(`https://www.dictionaryapi.com/api/v3/references/collegiate/json/${word.textContent}?key=your-api-key`);
    .then(response => {
        return response.json();
    })
    .then(response => {
        console.log(response[0].shortdef[0]);
        if (response[0].shortdef !== undefined){
            definition.textContent = "Definition: " + response[0].shortdef;
        }
        else{
            definition.textContent = "Definition: " + response.shortdef;
        }
        body.appendChild(definition);
    })
    .catch (err => {
        console.log(err);
    })
}


button.addEventListener('click', function(){
    randomWord();
})
