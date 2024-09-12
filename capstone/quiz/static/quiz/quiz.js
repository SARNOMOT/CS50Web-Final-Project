document.addEventListener('DOMContentLoaded', function() {
    console.log('quiz.js called')

    // Get the current URL and extract the quiz ID from it
    const url = window.location.href;
    const quiz_id = window.location.pathname.split('/').filter(Boolean).pop();

    // Get various DOM elements
    const quizBox = document.getElementById('quiz-box');
    
    const timerBox = document.getElementById('timer-box')

    const activateTimer = (time) => {
        
        // Function to activate the timer
        if (time.toString().length < 2) {
            timerBox.innerHTML = `
                <b>0${time}:00</b>
            `
        } 
        else{
            timerBox.innerHTML = `
                <b>${time}:00</b>
            `
        }

        let minutes = time - 1
        let seconds = 60
        let displaySeconds
        let displayMinutes

        const timer = setInterval(()=> {
            seconds --
            if (seconds < 0) {
                seconds = 59
                minutes --
            }
            if (minutes.toString().length < 2) {
                displayMinutes = '0'+minutes
            }
            else {
                displayMinutes = minutes
            }
            if (seconds.toString().length < 2) {
                displaySeconds = '0'+seconds
            }
            else {
                displaySeconds = seconds
            }
            if (minutes === 0 && seconds === 0) {
                console.log('time over')
                timerBox.innerHTML = "<b>00:00</b>"
                setTimeout(() =>{
                    clearInterval(timer)
                    alert('Time Over')
                    sendData()
                    window.location.href = `/results/${quiz_id}`;
                }, 500)
                
            }

            timerBox.innerHTML = `
                <b>${displayMinutes}:${displaySeconds}</b>
            `
        }, 1000)
    }

    // Fetch quiz data from the server
    fetch(`/data/${quiz_id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(response => {
            const data = response.data;

            // Process the quiz data and render it in the quizBox element
            data.forEach(el => {
                for (const [question, answers] of Object.entries(el)) {
                    quizBox.innerHTML += `
                        <hr>
                        <div class="mb-2">
                            <b>${question}</b>
                        </div>`;
                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                            <div>
                                <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}">${answer}</label>
                            </div>
                        `
                    })
                }
            });
            // Activate the timer using the specified time
            activateTimer(response.time)

            // Log the quiz data to the console
            console.log('Quiz Data:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    // Get form and CSRF token elements
    const quizForm = document.getElementById('quiz-form');
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const elements = [...document.getElementsByClassName('ans')];

    // Function to send quiz data to the server
    const sendData = () => {
        const elements = [...document.getElementsByClassName('ans')];
        const data = {};
        data['csrfmiddlewaretoken'] = csrf[0].value;
        elements.forEach(el => {
            if (el.checked) {
                data[el.name] = el.value;
            } else {
                if (!data[el.name]) {
                    data[el.name] = null;
                }
            }
        });

        console.log('Sending Data:', data);

        fetch(`/save/${quiz_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf[0].value
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(response => {
            console.log(response);
            
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    // Add an event listener for form submission
    quizForm.addEventListener('submit', e => {
        // Prevent the default form submission behavior
        e.preventDefault();
        // Send quiz data to the server
        sendData();

        // Redirect to results page
        window.location.href = `/results/${quiz_id}`;
    });
});
