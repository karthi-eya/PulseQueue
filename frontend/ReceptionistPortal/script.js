document.addEventListener('DOMContentLoaded', () => {

    // Login Form Logic
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        // Protect dashboard routing
        if(sessionStorage.getItem('receptionistAuth') === 'true'){
            window.location.href = 'dashboard.html';
        }

        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const user = document.getElementById('username').value;
            const pass = document.getElementById('password').value;
            const errMsg = document.getElementById('error-msg');

            if (user === '9948740002' && pass === 'Chinnu@123') {
                errMsg.style.color = 'var(--primary-dark)';
                errMsg.textContent = 'Login successful! Redirecting...';
                sessionStorage.setItem('receptionistAuth', 'true');
                
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 800);
            } else {
                errMsg.textContent = 'Invalid username or password.';
            }
        });
    }

    // Dashboard Logic
    const dashLayout = document.querySelector('.dashboard-layout');
    if (dashLayout) {
        // Enforce auth
        if(sessionStorage.getItem('receptionistAuth') !== 'true'){
            window.location.href = 'index.html';
            return;
        }

        // Tab Switching
        const navLinks = document.querySelectorAll('.nav-links li');
        const tabs = document.querySelectorAll('.tab-content');

        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navLinks.forEach(l => l.classList.remove('active'));
                tabs.forEach(t => t.classList.remove('active'));

                link.classList.add('active');
                const targetTab = document.getElementById(link.getAttribute('data-tab'));
                targetTab.classList.add('active');
            });
        });

        // Load Patient Data
        const listContainer = document.getElementById('appointmentList');
        
        // This simulates a live backend by reading local storage set by PatientPortal
        const aptNo = localStorage.getItem('appointmentNumber');
        
        if (!aptNo) {
            listContainer.innerHTML = `
                <div class="glass-card text-center" style="padding: 3rem;">
                    <h3 style="color: var(--text-light);">No appointments found for today.</h3>
                </div>
            `;
        } else {
            const pName = localStorage.getItem('patientName') || 'Unknown';
            const pAge = localStorage.getItem('patientAge') || 'N/A';
            const pPhone = localStorage.getItem('patientPhone') || 'N/A';
            const date = localStorage.getItem('appointmentDate') || 'N/A';
            const time = localStorage.getItem('appointmentTime') || 'N/A';
            
            // Generate a descriptive symptom string mocking the full questionnaire logic
            const genericSymptomText = "The patient recently filled out the detailed symptoms questionnaire in the patient portal indicating primary consultations regarding recurring symptoms.";

            listContainer.innerHTML = `
                <div class="appointment-card">
                    <div class="apt-header">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div class="apt-id">${aptNo}</div>
                            <label class="custom-checkbox">
                                <input type="checkbox" class="arrived-checkbox">
                                <span class="checkmark"></span>
                                <span class="label-text">Arrived?</span>
                            </label>
                        </div>
                        <div class="apt-time">${time}</div>
                    </div>
                    <div class="apt-body">
                        <div class="patient-info">
                            <h3>${pName}</h3>
                            <p><strong>Age:</strong> ${pAge}</p>
                            <p><strong>Phone:</strong> ${pPhone}</p>
                            <p><strong>Date:</strong> ${date}</p>
                        </div>
                        <div class="symptoms-box">
                            <h4>New Patient Details & Symptoms</h4>
                            <p>${genericSymptomText}</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }
});
