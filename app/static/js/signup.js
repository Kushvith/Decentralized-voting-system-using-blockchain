initMultiStepForm();

function initMultiStepForm() {
    const progressNumber = document.querySelectorAll(".step").length;
    const slidePage = document.querySelector(".slide-page");
    const submitBtn = document.querySelector(".submit");
    const progressText = document.querySelectorAll(".step p");
    const progressCheck = document.querySelectorAll(".step .check");
    const bullet = document.querySelectorAll(".step .bullet");
    const pages = document.querySelectorAll(".page");
    const nextButtons = document.querySelectorAll(".next");
    const prevButtons = document.querySelectorAll(".prev");
    const stepsNumber = pages.length;

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture');
    const captureNextButton = document.getElementById('captureNext');
    const registerButton = document.querySelector('.submit');
    let captureEnabled = false;
    let photoCount = 0;  
    if (progressNumber !== stepsNumber) {
        console.warn(
            "Error, number of steps in progress bar do not match number of pages"
        );
    }

    document.documentElement.style.setProperty("--stepNumber", stepsNumber);

    let current = 1;

    for (let i = 0; i < nextButtons.length; i++) {
        nextButtons[i].addEventListener("click", function (event) {
            event.preventDefault();

            inputsValid = validateInputs(this);
            // inputsValid = true;

            if (inputsValid) {
                slidePage.style.marginLeft = `-${
                    (100 / stepsNumber) * current
                }%`;
                bullet[current - 1].classList.add("active");
                progressCheck[current - 1].classList.add("active");
                progressText[current - 1].classList.add("active");
                current += 1;
            }
            if(current == 6){
                step5()
            }
        });
    }

    for (let i = 0; i < prevButtons.length; i++) {
        prevButtons[i].addEventListener("click", function (event) {
            event.preventDefault();
            slidePage.style.marginLeft = `-${
                (100 / stepsNumber) * (current - 2)
            }%`;
            bullet[current - 2].classList.remove("active");
            progressCheck[current - 2].classList.remove("active");
            progressText[current - 2].classList.remove("active");
            current -= 1;
        });
    }
    // submitBtn.addEventListener("click", function () {
    //     bullet[current - 1].classList.add("active");
    //     progressCheck[current - 1].classList.add("active");
    //     progressText[current - 1].classList.add("active");
    //     current += 1;
    //     setTimeout(function () {
    //         alert("Your Form Successfully Signed up");
    //         location.reload();
    //     }, 800);
    // });

    function validateInputs(ths) {
        let inputsValid = true;

        const inputs =
            ths.parentElement.parentElement.querySelectorAll("input");
        for (let i = 0; i < inputs.length; i++) {
            const valid = inputs[i].checkValidity();
            if (!valid) {
                inputsValid = false;
                inputs[i].classList.add("invalid-input");
            } else {
                inputs[i].classList.remove("invalid-input");
            }
        }
        return inputsValid;
    }
    function step5(){
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            alert('Error accessing webcam:', err);
        });
    }
  

captureButton.addEventListener('click', () => {
    captureEnabled = true;
});

video.addEventListener('click', () => {
    captureEnabled = true;
});

video.addEventListener('play', () => {
    const canvasContext = canvas.getContext('2d');
    setInterval(() => {
        if (captureEnabled) {
            canvasContext.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL('image/jpeg');
            document.getElementById(`image_data_${photoCount}`).value = imageData;
            captureEnabled = false;
            photoCount++;
            if (photoCount < 4) {
                captureButton.style.display = 'none';
                captureNextButton.style.display = 'block';
            } else {
                captureButton.style.display = 'none';
                captureNextButton.style.display = 'none';
                registerButton.style.display = 'block';
            }
        }
    }, 100);
});

captureNextButton.addEventListener('click', () => {
    captureButton.style.display = 'block';
    captureNextButton.style.display = 'none';
});
    // Calculate age based on date of birth
    document.getElementById('dob').addEventListener('change', function() {
    const dob = new Date(this.value);
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
        age--;
    }
    document.getElementById('age').value = age;
});
}
