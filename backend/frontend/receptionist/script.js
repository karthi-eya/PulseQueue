document.addEventListener('DOMContentLoaded', () => {
    // Dashboard Logic
    const dashLayout = document.querySelector('.dashboard-layout');
    if (dashLayout) {
        // Enforce auth
        if (sessionStorage.getItem('receptionistAuth') !== 'true') {
            window.location.href = '/';
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

        // Live polling for appointments and queue
        function fetchAppointments() {
            fetch('http://localhost:8003/patients')
                .then(r => r.json())
                .then(data => {
                    const listContainer = document.getElementById('appointmentList');
                    if (!data || data.length === 0) {
                        listContainer.innerHTML = `
                            <div class="glass-card text-center" style="padding: 3rem;">
                                <h3 style="color: var(--text-light);">No appointments found for today.</h3>
                            </div>
                        `;
                        return;
                    }

                    // Only show patients who haven't arrived yet
                    const pending = data.filter(p => !p.arrived);

                    if (pending.length === 0) {
                        listContainer.innerHTML = `
                            <div class="glass-card text-center" style="padding: 3rem;">
                                <h3 style="color: var(--text-light);">No pending appointments. All patients have arrived.</h3>
                            </div>
                        `;
                        return;
                    }

                    listContainer.innerHTML = pending.map(p => `
                        <div class="appointment-card">
                            <div class="apt-header">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <div class="apt-id">${p.token}</div>
                                    <button onclick="markArrived('${p.token}')" class="submit-btn" style="padding: 0.5rem 1rem; width: auto; margin-top: 0;">Mark Arrived</button>
                                </div>
                                <div class="apt-time">${new Date(p.arrival_time ? p.arrival_time * 1000 : Date.now()).toLocaleTimeString()}</div>
                            </div>
                            <div class="apt-body">
                                <div class="patient-info">
                                    <h3>${p.name}</h3>
                                    <p><strong>Age:</strong> ${p.age}</p>
                                    <p><strong>Base Score:</strong> ${p.base_score || p.priority}</p>
                                    <p><strong>Assigned Doctor:</strong> ${p.doctor}</p>
                                </div>
                                <div class="symptoms-box">
                                    <h4>Symptoms Data</h4>
                                    <p>${JSON.stringify(p.symptoms)}</p>
                                </div>
                            </div>
                        </div>
                    `).join('');
                })
                .catch(err => console.error("Error fetching patients:", err));
        }

        function fetchQueue() {
            fetch('http://localhost:8003/queue')
                .then(r => r.json())
                .then(data => {
                    const queueContainer = document.getElementById('queueList');
                    if (!data || data.length === 0) {
                        queueContainer.innerHTML = `
                            <div class="glass-card full-width text-center" style="padding: 3rem;">
                                <h3 style="color: var(--text-light);">No patients currently in queue.</h3>
                            </div>
                        `;
                        return;
                    }

                    queueContainer.innerHTML = data.map(p => `
                        <div class="appointment-card" style="border-left: 5px solid var(--primary);">
                            <div class="apt-header">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <div class="apt-id">#${p.queue_number || p.position} &mdash; ${p.token}</div>
                                </div>
                                <div class="apt-time">Priority: ${p.priority.toFixed(2)}</div>
                            </div>
                            <div class="apt-body">
                                <div class="patient-info">
                                    <h3>${p.name}</h3>
                                    <p><strong>Assigned to:</strong> ${p.doctor}</p>
                                </div>
                            </div>
                        </div>
                    `).join('');
                })
                .catch(err => console.error("Error fetching queue:", err));
        }

        window.markArrived = function (token) {
            fetch(`http://localhost:8003/arrive/${token}`, { method: 'POST' })
                .then(r => r.json())
                .then(d => {
                    alert(`${token} marked as arrived!`);
                    fetchAppointments();
                    fetchQueue();
                })
                .catch(err => console.error("Error marking arrival:", err));
        }

        // Add Appointment form handling
        const addForm = document.getElementById('addPatientForm');
        if (addForm) {
            addForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const payload = {
                    name: document.getElementById('walkinName').value,
                    age: parseInt(document.getElementById('walkinAge').value) || 30,
                    gender: "Unspecified",
                    symptoms: {
                        fever: null, cough: null, headache: null, vomiting: null, pregnancy: false
                    },
                    description: document.getElementById('walkinDesc').value
                };

                fetch('http://localhost:8003/add-patient', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                })
                    .then(r => r.json())
                    .then(d => {
                        alert('Walk-in patient added to queue! Token: ' + d.token);
                        document.getElementById('walkinModal').style.display = 'none';
                        addForm.reset();
                        fetchAppointments();
                        fetchQueue();
                    })
                    .catch(err => alert("Error adding patient"));
            });
        }

        window.openAddModal = function () {
            document.getElementById('walkinModal').style.display = 'flex';
        }
        window.closeAddModal = function () {
            document.getElementById('walkinModal').style.display = 'none';
        }

        fetchAppointments();
        fetchQueue();
        setInterval(() => {
            fetchAppointments();
            fetchQueue();
        }, 3000);
    }
});
