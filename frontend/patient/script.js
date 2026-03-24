// -------------------------
// JWT GUARD — redirect to login if no token
// -------------------------
(function () {
    const token = localStorage.getItem('token');
    const onPatientPage = window.location.pathname.includes('symptoms') ||
        window.location.pathname.includes('success');
    if (onPatientPage && !token) {
        window.location.href = '/';
    }
})();

document.addEventListener('DOMContentLoaded', () => {

    // -------------------------
    // REDIRECT IF ALREADY REGISTERED
    // -------------------------
    if (window.location.pathname.endsWith('index.html') && localStorage.getItem('patientToken')) {
        window.location.href = 'success.html';
        return;
    }

    // -------------------------
    // INPUT ANIMATION
    // -------------------------
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', (e) => {
            const label = e.target.parentElement.querySelector('label');
            if (label) label.style.color = 'blue';
        });

        input.addEventListener('blur', (e) => {
            const label = e.target.parentElement.querySelector('label');
            if (label) label.style.color = 'black';
        });
    });

    // -------------------------
    // LOAD SAVED DATA
    // -------------------------
    const nameInput = document.getElementById('name');
    const ageInput = document.getElementById('age');

    if (nameInput) nameInput.value = localStorage.getItem('patientName') || '';
    if (ageInput) ageInput.value = localStorage.getItem('patientAge') || '';

    // -------------------------
    // LOGIN FORM (BASIC DETAILS)
    // -------------------------
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = document.getElementById('name').value;
            const age = document.getElementById('age').value;

            localStorage.setItem('patientName', name);
            localStorage.setItem('patientAge', age);

            window.location.href = 'symptoms.html';
        });
    }

    // -------------------------
    // SYMPTOMS FORM (MAIN LOGIC)
    // -------------------------
    const symptomsForm = document.getElementById('symptomsForm');

    if (symptomsForm) {
        symptomsForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const btn = symptomsForm.querySelector('.submit-btn');
            if (btn) btn.innerText = "Processing...";

            // -------------------------
            // BUILD PAYLOAD (MATCH BACKEND)
            // -------------------------
            const payload = {
                name: localStorage.getItem('patientName') || 'Patient',
                age: parseInt(localStorage.getItem('patientAge')) || 25,

                description: document.getElementById("description")?.value || "",

                symptoms: {
                    fever: {
                        temperature: parseFloat(document.getElementById("temp")?.value) || 0,
                        days: parseInt(document.getElementById("fever_days")?.value) || 0
                    },
                    cough: {
                        days: parseInt(document.getElementById("cough_days")?.value) || 0
                    },
                    vomiting: {
                        days: parseInt(document.getElementById("vomit_days")?.value) || 0
                    },
                    headache: document.getElementById("headache")?.checked || false,
                    pregnancy: document.getElementById("pregnancy")?.checked || false
                }
            };

            try {
                // -------------------------
                // API CALL (with JWT auth)
                // -------------------------
                const token = localStorage.getItem('token');
                const response = await fetch("http://127.0.0.1:8000/add_patient", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + token
                    },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                console.log("Server Response:", data);

                // Save patient ID
                localStorage.setItem("appointmentNumber", data.patient.id);

                alert("Patient Registered Successfully!");

                // Redirect to success page
                window.location.href = "success.html";

            } catch (error) {
                console.error("Error:", error);
                alert("Failed to register patient");
            }
        });
    }

});