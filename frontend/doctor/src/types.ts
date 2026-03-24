export interface Patient {
  id: string;
  queueNumber: number;
  name: string;
  age: number;
  symptom: string;
  symptomDetail: string;
  appointmentTime: string;
  session: 'morning' | 'afternoon';
  status: 'scheduled' | 'arrived' | 'done';
}

export interface SessionSummary {
  morningCount: number;
  afternoonCount: number;
}
