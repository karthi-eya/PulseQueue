/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useMemo, useEffect } from 'react';
import {
  Stethoscope,
  User,
  Lock,
  LogOut,
  Sun,
  Moon,
  Users,
  Clock,
  ChevronRight,
  Activity,
  Search,
  X,
  FileText,
  Info
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Patient } from './types';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => sessionStorage.getItem('doctorAuth') === 'true');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [showArrivedOnly, setShowArrivedOnly] = useState(true);
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [completedCount, setCompletedCount] = useState(0);

  // Read doctor specialty from sessionStorage (set by unified login)
  const doctorSpecialty = sessionStorage.getItem('doctorSpecialty') || "General Physician";

  useEffect(() => {
    if (!isLoggedIn) return;

    const fetchQueue = async () => {
      try {
        const res = await fetch(`http://localhost:8001/queue/${doctorSpecialty}`);
        const data = await res.json();

        if (data && Array.isArray(data.queue)) {
          const mappedPatients: Patient[] = data.queue.map((p: any) => {
            // Extract primary symptom string
            let primarySymptom = "Consultation / Follow-up";
            if (p.symptoms && typeof p.symptoms === 'object') {
              const active = Object.entries(p.symptoms).find(([k, v]) => v !== null && v !== false);
              if (active) primarySymptom = active[0].charAt(0).toUpperCase() + active[0].slice(1);
            }

            return {
              id: p.token,
              queueNumber: p.queue_number || p.position,
              name: p.name,
              age: p.age || 0,
              symptom: primarySymptom,
              symptomDetail: JSON.stringify(p.symptoms) + (p.description ? ` | Desc: ${p.description}` : ''),
              priority: p.priority || 0,
              appointmentTime: new Date((p.arrival_time || (Date.now() / 1000)) * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }),
              session: new Date().getHours() < 14 ? 'morning' : 'afternoon',
              status: 'arrived' as const
            };
          });

          setPatients(mappedPatients);
        }
      } catch (err) {
        console.error("Error fetching live queue data:", err);
      }
    };

    fetchQueue();
    const interval = setInterval(fetchQueue, 3000);
    return () => clearInterval(interval);
  }, [isLoggedIn]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username.trim().toLowerCase() === 'general' && password === 'doc@123') {
      sessionStorage.setItem('doctorAuth', 'true');
      sessionStorage.setItem('doctorSpecialty', 'General Physician');
      setIsLoggedIn(true);
      setLoginError('');
    } else {
      setLoginError('Invalid credentials. Try "doc" and "doc@123"');
    }
  };

  const handleDemoLogin = () => {
    setUsername('general');
    setPassword('doc@123');
    sessionStorage.setItem('doctorAuth', 'true');
    sessionStorage.setItem('doctorSpecialty', 'General Physician');
    setIsLoggedIn(true);
    setLoginError('');
  };

  const callNextPatient = async (id: string) => {
    try {
      const res = await fetch(`http://localhost:8001/next/${doctorSpecialty}`, { method: 'POST' });
      const data = await res.json();
      if (data.message) {
        setCompletedCount(prev => prev + 1);
        setPatients(prev => prev.filter(p => p.id !== id));
        if (selectedPatient && selectedPatient.id === id) {
          setSelectedPatient(null);
        }
      }
    } catch (err) {
      console.error("Failed to dismiss patient", err);
    }
  };

  const morningPatients = useMemo(() =>
    patients.filter(p => p.session === 'morning' && p.status !== 'done'),
    [patients]);

  const afternoonPatients = useMemo(() =>
    patients.filter(p => p.session === 'afternoon' && p.status !== 'done'),
    [patients]);

  const parseTime = (timeStr: string) => {
    const [time, modifier] = timeStr.split(' ');
    let [hours, minutes] = time.split(':').map(Number);
    if (modifier === 'PM' && hours < 12) hours += 12;
    if (modifier === 'AM' && hours === 12) hours = 0;
    return hours * 60 + minutes;
  };

  const filteredPatients = useMemo(() => {
    return [...patients]
      .filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          p.symptom.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesArrivedFilter = showArrivedOnly ? p.status === 'arrived' : true;
        return matchesSearch && matchesArrivedFilter && p.status !== 'done';
      })
      .sort((a, b) => a.queueNumber - b.queueNumber);
  }, [searchTerm, patients, showArrivedOnly]);

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-hospital-bg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-hospital-blue/10 text-hospital-blue mb-4">
              <Stethoscope size={32} />
            </div>
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Pulse Queue</h1>
            <p className="text-slate-500 mt-2">Doctor Portal Login</p>
          </div>

          <div className="medical-card p-8">
            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Doctor ID / Username</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                    <User size={18} />
                  </span>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-hospital-blue focus:border-transparent outline-none transition-all"
                    placeholder="Enter doc"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                    <Lock size={18} />
                  </span>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-hospital-blue focus:border-transparent outline-none transition-all"
                    placeholder="••••••••"
                    required
                  />
                </div>
              </div>

              {loginError && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-red-500 text-sm text-center"
                >
                  {loginError}
                </motion.p>
              )}

              <button
                type="submit"
                className="w-full bg-hospital-blue hover:bg-hospital-blue/90 text-white font-semibold py-3 rounded-xl transition-all shadow-lg shadow-hospital-blue/20 active:scale-[0.98]"
              >
                Sign In
              </button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-slate-200"></span>
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-slate-400">Or use demo</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleDemoLogin}
                className="w-full bg-slate-100 hover:bg-slate-200 text-slate-600 font-semibold py-3 rounded-xl transition-all active:scale-[0.98]"
              >
                Demo Login
              </button>
            </form>
          </div>

          <p className="text-center text-slate-400 text-sm mt-8">
            &copy; 2026 Pulse Queue Healthcare Systems
          </p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-hospital-bg">
      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="bg-hospital-blue text-white p-1.5 rounded-lg">
                <Activity size={20} />
              </div>
              <span className="text-xl font-bold text-slate-900 tracking-tight">Pulse Queue</span>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-3 mr-4 pr-4 border-r border-slate-200">
                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-900">Dr. {doctorSpecialty}</p>
                  <p className="text-xs text-slate-500">{doctorSpecialty}</p>
                </div>
                <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-hospital-blue">
                  <User size={20} />
                </div>
              </div>
              <button
                onClick={() => {
                  sessionStorage.removeItem('doctorAuth');
                  setIsLoggedIn(false);
                }}
                className="text-slate-500 hover:text-red-500 transition-colors flex items-center gap-2 text-sm font-medium"
              >
                <LogOut size={18} />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900">Dashboard Overview</h2>
          <p className="text-slate-500">Welcome back, here is your patient live queue.</p>
        </div>

        {/* Session Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <motion.div
            whileHover={{ y: -4 }}
            className="medical-card p-6 flex items-center gap-6"
          >
            <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-500 flex items-center justify-center">
              <Sun size={28} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Morning Session</p>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-slate-900">{morningPatients.length}</span>
                <span className="text-slate-400 text-sm">Patients</span>
              </div>
              <p className="text-xs text-slate-400 mt-1">Live Updating</p>
            </div>
          </motion.div>

          <motion.div
            whileHover={{ y: -4 }}
            className="medical-card p-6 flex items-center justify-between"
          >
            <div className="flex items-center gap-6">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-indigo-500 flex items-center justify-center">
                <Moon size={28} />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">Afternoon Session</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-slate-900">{afternoonPatients.length}</span>
                  <span className="text-slate-400 text-sm">Patients</span>
                </div>
                <p className="text-xs text-slate-400 mt-1">Live Updating</p>
              </div>
            </div>

            <div className="text-right border-l border-slate-100 pl-6">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Completed</p>
              <div className="flex items-center justify-end gap-2">
                <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center">
                  <Activity size={16} />
                </div>
                <span className="text-2xl font-bold text-emerald-600">{completedCount}</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Patient Queue List */}
        <div className="medical-card">
          <div className="p-6 border-b border-slate-100 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="flex items-center gap-2">
                <Users className="text-hospital-blue" size={20} />
                <h3 className="font-bold text-slate-900">Live Active Queue</h3>
              </div>

              <div className="flex bg-slate-100 p-1 rounded-lg">
                <button
                  onClick={() => setShowArrivedOnly(true)}
                  className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${showArrivedOnly ? 'bg-white text-hospital-blue shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                >
                  Arrived Only
                </button>
                <button
                  disabled
                  title="Offline schedules are managed locally or via Reception"
                  className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-all ${!showArrivedOnly ? 'bg-white text-hospital-blue shadow-sm' : 'text-slate-300'}`}
                >
                  All Scheduled
                </button>
              </div>
            </div>

            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
              <input
                type="text"
                placeholder="Search patients..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-200 text-sm focus:ring-2 focus:ring-hospital-blue outline-none transition-all"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="medical-table-header w-20">Queue</th>
                  <th className="medical-table-header">Patient Name</th>
                  <th className="medical-table-header w-24">Age</th>
                  <th className="medical-table-header w-28">Priority</th>
                  <th className="medical-table-header w-32">Time</th>
                  <th className="medical-table-header w-32">Status</th>
                  <th className="medical-table-header w-32 text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                <AnimatePresence mode='popLayout'>
                  {filteredPatients.length > 0 ? (
                    filteredPatients.map((patient) => (
                      <motion.tr
                        key={patient.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        layout
                        className="hover:bg-slate-50/50 transition-colors group"
                      >
                        <td className="medical-table-cell">
                          <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-slate-100 text-slate-600 font-bold text-xs">
                            {patient.queueNumber}
                          </span>
                        </td>
                        <td className="medical-table-cell">
                          <button
                            onClick={() => setSelectedPatient(patient)}
                            className="font-semibold text-slate-900 hover:text-hospital-blue transition-colors text-left"
                          >
                            {patient.name}
                          </button>
                        </td>
                        <td className="medical-table-cell text-slate-500">
                          {patient.age} yrs
                        </td>
                        <td className="medical-table-cell">
                          <span className="font-bold text-hospital-blue">{patient.priority.toFixed(2)}</span>
                        </td>
                        <td className="medical-table-cell text-slate-500">
                          <div className="flex items-center gap-1.5">
                            <Clock size={14} />
                            {patient.appointmentTime}
                          </div>
                        </td>
                        <td className="medical-table-cell">
                          <span className="inline-flex items-center gap-1 text-emerald-600 text-xs font-bold uppercase tracking-wider">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            Waiting
                          </span>
                        </td>
                        <td className="medical-table-cell text-right">
                          <button
                            onClick={() => callNextPatient(patient.id)}
                            className="bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold py-1.5 px-3 rounded-lg transition-all active:scale-95"
                          >
                            Check In / Next
                          </button>
                        </td>
                      </motion.tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={6} className="py-12 text-center text-slate-400">
                        <div className="flex flex-col items-center gap-2">
                          <Users size={40} className="opacity-20" />
                          <p>No patients currently in the live queue for your specialty.</p>
                        </div>
                      </td>
                    </tr>
                  )}
                </AnimatePresence>
              </tbody>
            </table>
          </div>

          <div className="p-4 bg-slate-50 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-400">
              Showing {filteredPatients.length} patients waiting in Live Queue
            </p>
          </div>
        </div>

        {/* Patient Detail Modal */}
        <AnimatePresence>
          {selectedPatient && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="medical-card w-full max-w-lg overflow-hidden"
              >
                <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-hospital-blue/10 text-hospital-blue flex items-center justify-center">
                      <User size={20} />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900">{selectedPatient.name}</h3>
                      <p className="text-xs text-slate-500">Patient Token: {selectedPatient.id}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedPatient(null)}
                    className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition-all"
                  >
                    <X size={20} />
                  </button>
                </div>

                <div className="p-6 space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                      <p className="text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Age</p>
                      <p className="text-sm font-semibold text-slate-700">{selectedPatient.age} Years</p>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                      <p className="text-[10px] uppercase tracking-wider font-bold text-slate-400 mb-1">Primary Symptom</p>
                      <p className="text-sm font-semibold text-slate-700">{selectedPatient.symptom}</p>
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <FileText size={16} className="text-hospital-blue" />
                      <h4 className="text-sm font-bold text-slate-900 uppercase tracking-tight">Detailed Symptoms</h4>
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 min-h-[100px]">
                      <p className="text-sm text-slate-600 leading-relaxed">
                        {selectedPatient.symptomDetail}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="p-6 bg-slate-50/50 border-t border-slate-100 flex justify-end">
                  <button
                    onClick={() => setSelectedPatient(null)}
                    className="px-6 py-2 bg-slate-900 text-white text-sm font-bold rounded-xl hover:bg-slate-800 transition-all active:scale-95"
                  >
                    Close Details
                  </button>
                </div>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
