document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.endsWith('index.html') && localStorage.getItem('appointmentNumber')) {
        window.location.href = 'success.html';
        return;
    }

    // Add simple input animations for focus states
    const inputs = document.querySelectorAll('input[type="text"], input[type="tel"], input[type="number"], textarea, input[type="date"], select');

    inputs.forEach(input => {
        input.addEventListener('focus', (e) => {
            const label = e.target.parentElement.querySelector('label');
            if (label) label.style.color = 'var(--primary-dark)';
        });

        input.addEventListener('blur', (e) => {
            const label = e.target.parentElement.querySelector('label');
            if (label) label.style.color = 'var(--text-dark)';
        });
    });

    // Populate name from local storage if navigating back
    const nameInput = document.getElementById('name');
    if (nameInput) {
        const savedName = localStorage.getItem('patientName');
        if (savedName) nameInput.value = savedName;
    }
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        const savedPhone = localStorage.getItem('patientPhone');
        if (savedPhone) phoneInput.value = savedPhone;
    }
    const ageInput = document.getElementById('age');
    if (ageInput) {
        const savedAge = localStorage.getItem('patientAge');
        if (savedAge) ageInput.value = savedAge;
    }

    // Toggle sub-options for symptoms
    const parentCheckboxes = document.querySelectorAll('.parent-checkbox');
    parentCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const targetId = e.target.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                if (e.target.checked) {
                    targetEl.classList.add('active');
                } else {
                    targetEl.classList.remove('active');
                    // Uncheck any inner checkboxes and clear numbers
                    const innerInputs = targetEl.querySelectorAll('input');
                    innerInputs.forEach(innerInput => {
                        if (innerInput.type === 'checkbox') innerInput.checked = false;
                        if (innerInput.type === 'number') innerInput.value = '';
                    });
                }
            }
        });
    });

    // Toggle sub-options for radio buttons
    const toggleRadios = document.querySelectorAll('.toggle-radio');
    toggleRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            const targetId = e.target.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                if (e.target.value === 'yes') {
                    targetEl.classList.add('active');
                } else {
                    targetEl.classList.remove('active');
                    const textInput = targetEl.querySelector('input[type="text"]');
                    if (textInput) textInput.value = '';
                }
            }
        });
    });

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = loginForm.querySelector('.submit-btn');

            btn.innerHTML = `
                <span>Proceeding...</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            `;

            // Save details to localStorage
            const name = document.getElementById('name').value;
            const phone = document.getElementById('phone').value;
            const age = document.getElementById('age').value;
            localStorage.setItem('patientName', name);
            localStorage.setItem('patientPhone', phone);
            localStorage.setItem('patientAge', age);

            // Redirect to symptoms page
            setTimeout(() => {
                window.location.href = 'symptoms.html';
            }, 300);
        });
    }

    const symptomsForm = document.getElementById('symptomsForm');
    if (symptomsForm) {
        symptomsForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = symptomsForm.querySelector('.submit-btn');

            btn.innerHTML = `
                <svg class="animate-spin" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10" stroke="white" stroke-width="3" stroke-dasharray="31.4 31.4" stroke-linecap="round"></circle>
                </svg>
                <span>Processing...</span>
            `;

            if (!document.getElementById('spin-style')) {
                const style = document.createElement('style');
                style.id = 'spin-style';
                style.textContent = '@keyframes spin { 100% { transform: rotate(360deg); } }';
                document.head.appendChild(style);
            }

            setTimeout(() => {
                window.location.href = 'appointment.html';
            }, 600);
        });
    }

    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        // Set minimum date and handle past time validations
        const dateInput = document.getElementById('appointment_date');
        const timeSelect = document.getElementById('appointment_time');
        if (dateInput && timeSelect) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('min', today);

            // Parse text like "03:00 PM" into minutes
            const getMinutesFromTimeStr = (timeStr) => {
                const parts = timeStr.trim().split(' ');
                if (parts.length < 2) return 0;
                let [hours, mins] = parts[0].split(':').map(Number);
                const period = parts[1].toUpperCase();

                if (period === 'PM' && hours !== 12) hours += 12;
                if (period === 'AM' && hours === 12) hours = 0;

                return hours * 60 + mins;
            };

            dateInput.addEventListener('change', (e) => {
                const selectedDate = e.target.value;
                const isToday = selectedDate === today;

                const now = new Date();
                const currentMinutes = now.getHours() * 60 + now.getMinutes();

                Array.from(timeSelect.options).forEach(opt => {
                    if (!opt.value || opt.value === "---") return;

                    const startTimeStr = opt.value.split('-')[0].trim();
                    const slotMinutes = getMinutesFromTimeStr(startTimeStr);

                    // Hide slot if Date is today AND slot time has already passed
                    if (isToday && currentMinutes >= slotMinutes) {
                        opt.style.display = 'none';
                        opt.disabled = true;
                    } else {
                        opt.style.display = '';
                        opt.disabled = false;
                    }
                });

                // Clear the selection if the currently selected option became hidden
                if (timeSelect.options[timeSelect.selectedIndex] && timeSelect.disabled) {
                    timeSelect.value = "";
                }
            });
        }

        appointmentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = appointmentForm.querySelector('.submit-btn');

            btn.innerHTML = `
                <svg class="animate-spin" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10" stroke="white" stroke-width="3" stroke-dasharray="31.4 31.4" stroke-linecap="round"></circle>
                </svg>
                <span>Booking...</span>
            `;

            if (!document.getElementById('spin-style')) {
                const style = document.createElement('style');
                style.id = 'spin-style';
                style.textContent = '@keyframes spin { 100% { transform: rotate(360deg); } }';
                document.head.appendChild(style);
            }

            const date = document.getElementById('appointment_date').value;
            const timeSelect = document.getElementById('appointment_time');
            const timeText = timeSelect.options[timeSelect.selectedIndex].text;

            localStorage.setItem('appointmentDate', date);
            localStorage.setItem('appointmentTime', timeText);

            // Construct payload
            const payload = {
                name: localStorage.getItem('patientName') || 'Patient',
                age: parseInt(localStorage.getItem('patientAge')) || 30,
                gender: 'Unspecified',
                symptoms: {
                    fever: null,
                    cough: null,
                    headache: null,
                    vomiting: null,
                    pregnancy: false
                },
                description: "Online booking"
            };

            fetch('http://localhost:8002/book', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
                .then(r => r.json())
                .then(data => {
                    localStorage.setItem('appointmentNumber', data.token);
                    // Also set an explicitly booked flag
                    localStorage.setItem('patientBooked', 'true');
                    setTimeout(() => {
                        window.location.href = 'success.html';
                    }, 800);
                })
                .catch(err => {
                    console.error('Error booking:', err);
                    alert('Server error while booking.');
                    btn.innerHTML = '<span>Book Appointment</span>';
                });
        });
    }
});
