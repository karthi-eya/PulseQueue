import { Patient } from './types';

export const MOCK_PATIENTS: Patient[] = [
  // Morning Session (10:00 - 11:30, 11:45 - 13:15)
  { id: '1', queueNumber: 1, name: 'John Doe', age: 45, symptom: 'Persistent Cough', symptomDetail: 'Patient reports a dry cough for the past 2 weeks, worsening at night. No fever but mild chest tightness.', appointmentTime: '10:00 AM', session: 'morning', status: 'arrived' },
  { id: '2', queueNumber: 2, name: 'Jane Smith', age: 32, symptom: 'Severe Headache', symptomDetail: 'Migraine-like symptoms, sensitivity to light and sound. Duration: 24 hours.', appointmentTime: '10:30 AM', session: 'morning', status: 'scheduled' },
  { id: '3', queueNumber: 3, name: 'Robert Brown', age: 58, symptom: 'Chest Pain', symptomDetail: 'Sharp pain on the left side, radiates to the shoulder. History of hypertension.', appointmentTime: '11:15 AM', session: 'morning', status: 'scheduled' },
  { id: '4', queueNumber: 4, name: 'Emily Davis', age: 24, symptom: 'Fever', symptomDetail: 'Temperature 101.5F, body aches, and fatigue. Started yesterday evening.', appointmentTime: '11:45 AM', session: 'morning', status: 'scheduled' },
  { id: '5', queueNumber: 5, name: 'Michael Wilson', age: 67, symptom: 'Back Pain', symptomDetail: 'Chronic lower back pain, acute flare-up after lifting heavy objects.', appointmentTime: '12:30 PM', session: 'morning', status: 'scheduled' },
  { id: '6', queueNumber: 6, name: 'Sarah Miller', age: 29, symptom: 'Sore Throat', symptomDetail: 'Difficulty swallowing, swollen tonsils, mild fever.', appointmentTime: '01:00 PM', session: 'morning', status: 'scheduled' },
  
  // Afternoon Session (03:00 - 04:00, 04:15 - 05:15, 05:30 - 06:30, 07:00 - 08:00)
  { id: '7', queueNumber: 1, name: 'David Garcia', age: 41, symptom: 'Abdominal Pain', symptomDetail: 'Sharp pain in the lower right quadrant, nausea, loss of appetite.', appointmentTime: '03:00 PM', session: 'afternoon', status: 'scheduled' },
  { id: '8', queueNumber: 2, name: 'Linda Martinez', age: 53, symptom: 'Dizziness', symptomDetail: 'Vertigo symptoms when standing up quickly, occasional ringing in ears.', appointmentTime: '03:45 PM', session: 'afternoon', status: 'scheduled' },
  { id: '9', queueNumber: 3, name: 'James Taylor', age: 38, symptom: 'Joint Pain', appointmentTime: '04:15 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Swelling and stiffness in both knees, worse in the morning.' },
  { id: '10', queueNumber: 4, name: 'Susan Clark', age: 47, symptom: 'Eye Irritation', appointmentTime: '05:00 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Redness and itching in both eyes, watery discharge.' },
  { id: '11', queueNumber: 5, name: 'Kevin Baker', age: 31, symptom: 'Skin Rash', appointmentTime: '05:30 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Red, itchy patches on arms and legs, possible allergic reaction.' },
  { id: '12', queueNumber: 6, name: 'Nancy Hill', age: 62, symptom: 'High Blood Pressure', appointmentTime: '06:15 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Regular check-up, history of hypertension, currently on medication.' },
  { id: '13', queueNumber: 7, name: 'Paul Adams', age: 55, symptom: 'Fatigue', appointmentTime: '07:00 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Persistent low energy for 3 weeks, poor sleep quality.' },
  { id: '14', queueNumber: 8, name: 'Karen Wright', age: 28, symptom: 'Allergy', appointmentTime: '07:45 PM', session: 'afternoon', status: 'scheduled', symptomDetail: 'Seasonal allergy symptoms: sneezing, runny nose, itchy eyes.' },
];
