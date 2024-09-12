document.addEventListener('DOMContentLoaded', function() {
    console.log('index.js called')

    // Get an array of all elements with the class 'modal-button'
    const modalBtns = [...document.getElementsByClassName('modal-button')]
    // Get the element with the ID 'modal-body-confirm'
    const modalBody = document.getElementById('modal-body-confirm')
    // Get the element with the ID 'start-button'
    const startBtn = document.getElementById('start-button')

    // Get the current URL
    const url = window.location.href

    // Add an event listener to each modal button
    modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
        // Retrieve data attributes from the clicked modal button
        const pk = modalBtn.getAttribute('data-pk')
        const name = modalBtn.getAttribute('data-quiz')
        const numQuestions = modalBtn.getAttribute('data-questions')
        const difficulty = modalBtn.getAttribute('data-difficulty')
        const scoreToPass = modalBtn.getAttribute('data-pass')
        const time = modalBtn.getAttribute('data-time')

        // Populate the modal body with quiz details
        modalBody.innerHTML = `
            <div class="h5 mb-3">Quiz Details</div>
            <div class="text-muted">
                <ul>
                    <li>Difficulty: <b>${difficulty}</b></li>
                    <li>Number of Questions: <b>${numQuestions}</b></li>
                    <li>Score to Pass: <b>${scoreToPass}</b>%</li>
                    <li>Time: <b>${time}</b>min</li>
                </ul>
            </div>
        `

        // Add an event listener to the start button within the modal
        startBtn.addEventListener('click', ()=>{
            // Redirect the user to the quiz page with the specified quiz ID
            window.location.href = `quiz/${pk}` 
        })
    }))
});