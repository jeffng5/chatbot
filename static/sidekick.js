

async function renderDOM() {
    let button = document.getElementsByClassName('bttn')
    button.addEventListener('click', function(e) {e.preventDefault(); hideDOM() })

}

function hideDOM() {
    let questionElement = document.getElementsByClassName('question')
    questionElement.style.display = 'none'
}

renderDOM()