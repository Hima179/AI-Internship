// Mock Data for UAI Counsellor Insights Dashboard

export const coursesList = [
  "B.Sc. Agriculture",
  "B.Tech Biotechnology",
  "M.Sc. Horticulture",
  "B.Sc. Forestry",
  "MBA Agribusiness"
];

export const cohortsList = [
  "Batch 2025",
  "Batch 2024",
  "Batch 2023"
];

export const academicYearsList = [
  "2025-2026",
  "2024-2025"
];

export const riskLevelsList = [
  "All",
  "High",
  "Medium",
  "Low"
];

export const mockStudents = [
  {
    id: "UAI-2025-0012",
    name: "Rohan Sharma",
    course: "B.Sc. Agriculture",
    cohort: "Batch 2025",
    academicYear: "2025-2026",
    riskLevel: "High",
    wellnessScore: 42,
    lastContacted: "2026-05-18",
    email: "rohan.sharma@uai.edu.in",
    phone: "+91 98765 43210",
    avatar: "RS",
    gender: "Male",
    hosteller: "Yes (Hostel-A)",
    attendance: "58%",
    gpa: "6.2/10",
    riskFactors: {
      psychological: "Moderate to severe anxiety flagged on recent GAD-7 (Score: 14). Reports constant exam stress and difficulty concentrating.",
      academic: "Significant attendance drop from 85% to 58% over the last 4 weeks. Missed 2 continuous practical labs.",
      social: "Struggling with adjustment to hostel life away from home. Expressed feeling isolated and homesick."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-05-10", score: "11 (Moderate)", status: "Flagged" },
      { name: "GAD-7 (Anxiety)", date: "2026-05-12", score: "14 (Moderate-Severe)", status: "Critical" },
      { name: "Academic Stress Scale", date: "2026-04-15", score: "78/100 (High)", status: "Flagged" }
    ],
    interventions: [
      { date: "2026-05-14", type: "1-on-1 Counselling", notes: "First introductory session. Rohan was reserved. Focused on coping strategies for academic pressure and sleep routine.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" },
      { date: "2026-05-19", type: "Peer Mentor Assign", notes: "Assigned a senior peer mentor from B.Sc. Ag to help with lab files and campus familiarity.", counsellor: "Dr. Sarah Ahmed", status: "Completed" }
    ]
  },
  {
    id: "UAI-2025-0045",
    name: "Ananya Iyer",
    course: "B.Sc. Agriculture",
    cohort: "Batch 2025",
    academicYear: "2025-2026",
    riskLevel: "Medium",
    wellnessScore: 68,
    lastContacted: "2026-05-20",
    email: "ananya.iyer@uai.edu.in",
    phone: "+91 91234 56789",
    avatar: "AI",
    gender: "Female",
    hosteller: "No (Day Scholar)",
    attendance: "81%",
    gpa: "7.8/10",
    riskFactors: {
      psychological: "Mild depression flagged (PHQ-9 Score: 8). Expresses general lack of motivation.",
      academic: "Struggles with chemistry-related courses, but attendance and assignment submissions are mostly on time.",
      social: "Well-integrated socially, but feels pressured by parental expectations regarding government agri-exams."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-05-02", score: "8 (Mild)", status: "Monitor" },
      { name: "GAD-7 (Anxiety)", date: "2026-05-02", score: "6 (Mild)", status: "Normal" }
    ],
    interventions: [
      { date: "2026-05-05", type: "Group Therapy Session", notes: "Participated in the 'Coping with Academic Anxiety' workshop. Active participant.", counsellor: "Dr. Sarah Ahmed", status: "Completed" }
    ]
  },
  {
    id: "UAI-2025-0102",
    name: "Vikram Rathore",
    course: "B.Tech Biotechnology",
    cohort: "Batch 2025",
    academicYear: "2025-2026",
    riskLevel: "High",
    wellnessScore: 35,
    lastContacted: "2026-05-22",
    email: "vikram.rathore@uai.edu.in",
    phone: "+91 88990 11223",
    avatar: "VR",
    gender: "Male",
    hosteller: "Yes (Hostel-B)",
    attendance: "45%",
    gpa: "5.5/10",
    riskFactors: {
      psychological: "PHQ-9 score in the severe range (Score: 21). Reports insomnia, extreme fatigue, and severe feelings of worthlessness.",
      academic: "Failing in two core subjects. High risk of academic year-back. Attendance below critical 50% limit.",
      social: "Parents contacted; family under financial stress due to crop failure, compounding student's anxiety."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-05-18", score: "21 (Severe)", status: "Critical" },
      { name: "GAD-7 (Anxiety)", date: "2026-05-18", score: "16 (Severe)", status: "Critical" },
      { name: "Sleep & Fatigue Index", date: "2026-05-19", score: "88/100 (Severe)", status: "Critical" }
    ],
    interventions: [
      { date: "2026-05-20", type: "Clinical Referral", notes: "Referred to consulting campus psychiatrist Dr. Verma for pharmacological evaluation due to severity of depressive symptoms. Immediate emergency protocols activated.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" },
      { date: "2026-05-23", type: "Parental Counseling Session", notes: "Telephonic call with Vikram's father. Discussed academic status and well-being. Father was cooperative and is visiting campus next week.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" }
    ]
  },
  {
    id: "UAI-2025-0078",
    name: "Meera Sen",
    course: "M.Sc. Horticulture",
    cohort: "Batch 2024",
    academicYear: "2025-2026",
    riskLevel: "Low",
    wellnessScore: 89,
    lastContacted: "2026-05-15",
    email: "meera.sen@uai.edu.in",
    phone: "+91 76543 21098",
    avatar: "MS",
    gender: "Female",
    hosteller: "Yes (Hostel-C)",
    attendance: "94%",
    gpa: "9.1/10",
    riskFactors: {
      psychological: "All scores within normal baseline. Reports good resilience and occasional mild academic stress prior to presentations.",
      academic: "Excellent academic standing. Top of class in floriculture research.",
      social: "Strong friendship circle and positive relationship with research guide."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-04-10", score: "3 (Normal)", status: "Normal" },
      { name: "GAD-7 (Anxiety)", date: "2026-04-10", score: "2 (Normal)", status: "Normal" }
    ],
    interventions: []
  },
  {
    id: "UAI-2025-0156",
    name: "Aditya Verma",
    course: "B.Sc. Agriculture",
    cohort: "Batch 2025",
    academicYear: "2025-2026",
    riskLevel: "Medium",
    wellnessScore: 61,
    lastContacted: "2026-05-12",
    email: "aditya.verma@uai.edu.in",
    phone: "+91 99887 76655",
    avatar: "AV",
    gender: "Male",
    hosteller: "Yes (Hostel-A)",
    attendance: "78%",
    gpa: "7.0/10",
    riskFactors: {
      psychological: "Moderate stress flagged. Struggles with chronic sleep issues (averages 4-5 hours of sleep per night).",
      academic: "Exhibits signs of panic during practical exams, though theoretical assignments are solid.",
      social: "Struggles with public speaking and peer interactions in group projects."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-05-01", score: "7 (Mild)", status: "Monitor" },
      { name: "GAD-7 (Anxiety)", date: "2026-05-01", score: "10 (Moderate)", status: "Flagged" },
      { name: "Sleep & Fatigue Index", date: "2026-05-03", score: "62/100 (Moderate)", status: "Flagged" }
    ],
    interventions: [
      { date: "2026-05-06", type: "1-on-1 Counselling", notes: "Conducted cognitive restructuring session focusing on practical performance anxiety and sleep hygiene.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" }
    ]
  },
  {
    id: "UAI-2025-0211",
    name: "Sneha Reddy",
    course: "B.Sc. Forestry",
    cohort: "Batch 2023",
    academicYear: "2025-2026",
    riskLevel: "Low",
    wellnessScore: 84,
    lastContacted: "2026-05-10",
    email: "sneha.reddy@uai.edu.in",
    phone: "+91 94401 23456",
    avatar: "SR",
    gender: "Female",
    hosteller: "No (Day Scholar)",
    attendance: "89%",
    gpa: "8.5/10",
    riskFactors: {
      psychological: "Low stress. Positive outlook on careers in forestry department.",
      academic: "Highly consistent, regular submission of field projects.",
      social: "Active participant in NSS and university cultural committee."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-03-20", score: "2 (Normal)", status: "Normal" },
      { name: "GAD-7 (Anxiety)", date: "2026-03-20", score: "4 (Normal)", status: "Normal" }
    ],
    interventions: []
  },
  {
    id: "UAI-2025-0199",
    name: "Kabir Mehta",
    course: "MBA Agribusiness",
    cohort: "Batch 2024",
    academicYear: "2025-2026",
    riskLevel: "Medium",
    wellnessScore: 59,
    lastContacted: "2026-05-21",
    email: "kabir.mehta@uai.edu.in",
    phone: "+91 93322 11009",
    avatar: "KM",
    gender: "Male",
    hosteller: "No (Day Scholar)",
    attendance: "72%",
    gpa: "7.1/10",
    riskFactors: {
      psychological: "Elevated anxiety related to upcoming corporate summer placements.",
      academic: "Slight drop in finance assignments. Missed one presentations round.",
      social: "Reports high self-imposed pressure to secure high-paying placements due to education loan."
    },
    assessments: [
      { name: "GAD-7 (Anxiety)", date: "2026-05-15", score: "11 (Moderate)", status: "Flagged" },
      { name: "Academic Stress Scale", date: "2026-05-16", score: "68/100 (Moderate)", status: "Flagged" }
    ],
    interventions: [
      { date: "2026-05-18", type: "Placement Stress Coaching", notes: "Guided on mock interviews, stress-resilience framing, and deep breathing exercises.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" }
    ]
  },
  {
    id: "UAI-2025-0008",
    name: "Zoya Khan",
    course: "B.Tech Biotechnology",
    cohort: "Batch 2025",
    academicYear: "2025-2026",
    riskLevel: "Low",
    wellnessScore: 92,
    lastContacted: "2026-05-24",
    email: "zoya.khan@uai.edu.in",
    phone: "+91 90088 77665",
    avatar: "ZK",
    gender: "Female",
    hosteller: "Yes (Hostel-C)",
    attendance: "96%",
    gpa: "9.4/10",
    riskFactors: {
      psychological: "Excellent well-being. Enthusiastic about course curricula.",
      academic: "Top academic tier. Exemplary lab work.",
      social: "Peer-leader. Helps organize biotech department festivals."
    },
    assessments: [
      { name: "PHQ-9 (Depression)", date: "2026-05-05", score: "1 (Normal)", status: "Normal" },
      { name: "GAD-7 (Anxiety)", date: "2026-05-05", score: "2 (Normal)", status: "Normal" }
    ],
    interventions: []
  }
];

export const mockAssessments = [
  {
    id: "asm-001",
    title: "PHQ-9 Well-being Assessment",
    description: "Standard clinical 9-question tool measuring severity of depressive symptomatology over the past 2 weeks.",
    questionsCount: 9,
    participationRate: "88%",
    averageScore: "6.2 (Mild)",
    activeTriggers: 4,
    frequency: "Monthly",
    status: "Active"
  },
  {
    id: "asm-002",
    title: "GAD-7 Anxiety Screening",
    description: "Generalized Anxiety Disorder 7-item clinical scale to screen for and evaluate severity of anxiety.",
    questionsCount: 7,
    participationRate: "91%",
    averageScore: "5.8 (Mild)",
    activeTriggers: 6,
    frequency: "Fortnightly",
    status: "Active"
  },
  {
    id: "asm-003",
    title: "UAi Sleep & Fatigue Index",
    description: "In-house lifestyle checkup evaluating sleep duration, hygiene, screen habits, and subjective exhaustion.",
    questionsCount: 12,
    participationRate: "76%",
    averageScore: "48/100 (Moderate)",
    activeTriggers: 9,
    frequency: "Term-wise",
    status: "Active"
  },
  {
    id: "asm-004",
    title: "Academic & Campus Adjustment Survey",
    description: "Evaluates transition difficulties, hostel adaptation, mentor connection, and curricular comfort level.",
    questionsCount: 15,
    participationRate: "95%",
    averageScore: "72/100 (High Adjustment)",
    activeTriggers: 2,
    frequency: "Post-induction",
    status: "Completed"
  }
];

export const mockAlerts = [
  {
    id: "alt-001",
    studentId: "UAI-2025-0102",
    studentName: "Vikram Rathore",
    course: "B.Tech Biotechnology",
    riskLevel: "High",
    trigger: "Severe PHQ-9 Flag (Score: 21)",
    time: "2 days ago",
    details: "Student reported severe insomnia, persistent sadness, and complete loss of interest in academics in their monthly PHQ-9. Attendance is currently at 45%.",
    status: "Escalated",
    actionTaken: "Psychiatrist referral scheduled. Parents contacted."
  },
  {
    id: "alt-002",
    studentId: "UAI-2025-0012",
    studentName: "Rohan Sharma",
    course: "B.Sc. Agriculture",
    riskLevel: "High",
    trigger: "Sudden Attendance Drop & GAD-7 Score: 14",
    time: "4 days ago",
    details: "Attendance dropped by 27% in 30 days. Anxiety screen shows moderate-to-severe response. Indicated high homesickness and stress during labs.",
    status: "In Progress",
    actionTaken: "1-on-1 counseling initiated. Peer support assigned."
  },
  {
    id: "alt-003",
    studentId: "UAI-2025-0156",
    studentName: "Aditya Verma",
    course: "B.Sc. Agriculture",
    riskLevel: "Medium",
    trigger: "Elevated GAD-7 (Score: 10) & Fatigue Flag",
    time: "1 week ago",
    details: "Panic triggers reported during mock viva-voce. Averages under 5 hours of sleep due to night-studying.",
    status: "In Progress",
    actionTaken: "Counseling sessions started. Guidelines on sleep hygiene sent."
  },
  {
    id: "alt-004",
    studentId: "UAI-2025-0199",
    studentName: "Kabir Mehta",
    course: "MBA Agribusiness",
    riskLevel: "Medium",
    trigger: "Placement Stress Spike",
    time: "3 days ago",
    details: "Student requested urgent support due to placement-related stress, panic before mock interviews.",
    status: "Investigating",
    actionTaken: "Consultation set for tomorrow morning."
  }
];

export const mockInsights = [
  {
    id: "ins-001",
    category: "Academic Stress",
    title: "Mid-Term Preparation Anxiety Spike",
    finding: "74% of freshman students in B.Sc. Agriculture Batch 2025 reported high academic stress levels leading into mid-terms, primarily due to practical lab journal backlogs.",
    actionableAdvice: "Organize cooperative peer study groups and clear labs timelines to ease compile strain.",
    intensity: "High"
  },
  {
    id: "ins-002",
    category: "Hostel Integration",
    title: "First-Year Isolation Trend",
    finding: "Out-of-state hostellers in Hostel-A have a 25% higher GAD-7 anxiety average than local day scholars during their first 90 days on campus.",
    actionableAdvice: "Introduce monthly hostel orientation mixers and stress-buster sports tournaments.",
    intensity: "Medium"
  },
  {
    id: "ins-003",
    category: "Sleep Deprivation Correlation",
    title: "Attendance & Exhaustion Nexus",
    finding: "A strong statistical correlation (r = -0.72) is shown between average sleep duration (< 6 hours) and attendance drop below 75% in B.Tech Biotechnology courses.",
    actionableAdvice: "Enforce strict 'light-out and screen-down' awareness seminars in Hostel-B.",
    intensity: "High"
  }
];

export const mockResources = [
  {
    category: "Anxiety & Panic",
    items: [
      { title: "Box Breathing Technique", type: "Interactive Guide", size: "2 pages PDF", link: "#" },
      { title: "Cognitive Distortion Worksheet", type: "Activity Sheet", size: "4 pages PDF", link: "#" },
      { title: "Managing Exam Stress Workshop Notes", type: "Slides", size: "12 slides PDF", link: "#" }
    ]
  },
  {
    category: "Depression & Motivation",
    items: [
      { title: "Behavioral Activation Chart", type: "Self-Monitor Log", size: "1 page PDF", link: "#" },
      { title: "Practicing Daily Gratitude", type: "Reflection Sheet", size: "2 pages PDF", link: "#" },
      { title: "Understanding Depression: Myths vs Facts", type: "Reading Guide", size: "6 pages PDF", link: "#" }
    ]
  },
  {
    category: "Sleep & Health",
    items: [
      { title: "Good Sleep Hygiene Protocol", type: "Checklist Card", size: "1 page PDF", link: "#" },
      { title: "Digital Detox Checklist", type: "Routine Builder", size: "2 pages PDF", link: "#" }
    ]
  },
  {
    category: "Crisis Hotlines (Emergency)",
    items: [
      { title: "UAi 24/7 Wellness Helpline", type: "In-Campus Call", size: "Ext: 4400 (Toll Free)", link: "#" },
      { title: "National Tele-MANAS helpline", type: "Govt. Initiative", size: "14416 (24 hours)", link: "#" },
      { title: "Vandrevala Foundation for Mental Health", type: "Independent NGO", size: "+91 9999 666 555", link: "#" }
    ]
  }
];

export const mockSystemSettings = {
  highRiskThreshold: 15, // GAD-7 or PHQ-9
  mediumRiskThreshold: 8,
  attendanceAlertThreshold: 75, // Alert if attendance < 75%
  enableEmailAlerts: true,
  enableSmsEscalation: false,
  autoReferToPsychiatrist: false
};

// Common Pakistani Names arrays for generating realistic dataset
const firstNamesMale = ["Ali", "Ahmed", "Bilal", "Faisal", "Hassan", "Imran", "Tariq", "Usman", "Zain", "Hamza", "Junaid", "Asad", "Omar", "Fahad", "Saad", "Yasir", "Shehzad", "Babar", "Mustafa", "Haris", "Sufyan", "Zubair", "Adeel", "Waseem"];
const firstNamesFemale = ["Ayesha", "Fatima", "Sana", "Zara", "Nadia", "Sara", "Huma", "Layla", "Sidra", "Kiran", "Sadia", "Mariam", "Iqra", "Nida", "Hina", "Anam", "Rabia", "Mahnoor", "Zaynab", "Bushra", "Fiza", "Noreen", "Sobia", "Shazia"];
const lastNames = ["Khan", "Hassan", "Noor", "Raza", "Javed", "Malik", "Ahmed", "Mirza", "Qureshi", "Sheikh", "Baig", "Chaudhry", "Mahmood", "Akhtar", "Siddiqui", "Abbasi", "Yousuf", "Butt", "Dar", "Mughal", "Gillani", "Hashmi", "Latif", "Sharif"];

export const generateFollowUpStudents = () => {
  const list = [];
  const cohorts = ["Batch 2022", "Batch 2023", "Batch 2024", "Batch 2025"];

  for (let i = 1; i <= 200; i++) {
    const isMale = Math.random() > 0.5;
    const fName = isMale 
      ? firstNamesMale[Math.floor(Math.random() * firstNamesMale.length)]
      : firstNamesFemale[Math.floor(Math.random() * firstNamesFemale.length)];
    const lName = lastNames[Math.floor(Math.random() * lastNames.length)];
    const name = `${fName} ${lName}`;
    
    const regId = `REG-2025-${String(Math.floor(1000 + Math.random() * 9000))}`;
    const cohort = cohorts[Math.floor(Math.random() * cohorts.length)];
    
    // Controlled stress distribution: Severe=12%, High=18%, Moderate=35%, Low=35%
    let stress = "Low";
    const randStress = Math.random();
    if (randStress > 0.88) stress = "Severe";
    else if (randStress > 0.70) stress = "High";
    else if (randStress > 0.35) stress = "Moderate";
    
    // Controlled impulsivity: High=15%, Moderate=30%, Low=55%
    let impulsivity = "Low";
    const randImp = Math.random();
    if (randImp > 0.85) impulsivity = "High";
    else if (randImp > 0.55) impulsivity = "Moderate";
    
    // Controlled risk-taking: High=12%, Moderate=28%, Low=60%
    let risk = "Low";
    const randRisk = Math.random();
    if (randRisk > 0.88) risk = "High";
    else if (randRisk > 0.60) risk = "Moderate";
    
    // Intervention flag is "Yes" if stress is High/Severe or any level is High
    const intervention = (stress === "Severe" || stress === "High" || impulsivity === "High" || risk === "High") ? "Yes" : "No";
    
    list.push({
      id: i,
      name,
      regId,
      course: "B.Sc. Agriculture",
      cohort,
      stress,
      impulsivity,
      risk,
      intervention
    });
  }
  return list;
};

export const followUpStudentsList = generateFollowUpStudents();

export const mockInstitutionalInfo = {
  universityName: "Universal AI University",
  chancellor: {
    name: "Mr. Tarun Anand",
    role: "Chancellor & Founder",
    bio: "Pioneer in AI education and leadership. Formerly Managing Director of Thomson Reuters South Asia, founding Universal AI University as India's first AI-focused university to prepare students for the future of work.",
    image: "https://www.universalai.in/wp-content/uploads/2023/05/Tarun-Anand.jpg",
    email: "chancellor@universalai.in",
    vision: "Integrating ethical AI, design thinking, and cognitive well-being into higher education to create compassionate, future-ready global leaders."
  },
  deans: [
    { name: "Dr. Ravichandran Nair", role: "Dean of Academics", department: "Academic Council", email: "dean.academics@uai.edu.in", phone: "+91 99881 22334" },
    { name: "Dr. Asha Prasuna", role: "Dean of Research & PG Programs", department: "Research & Development", email: "dean.research@uai.edu.in", phone: "+91 99881 22335" }
  ],
  hods: [
    { department: "B.Tech (AI & Biotech)", name: "Dr. Naveen Qureshi", email: "hod.btech@uai.edu.in", phone: "+91 99881 22340", room: "Block A - 402" },
    { department: "B.Sc (Agriculture)", name: "Dr. Farhan Malik", email: "hod.agriculture@uai.edu.in", phone: "+91 99881 22341", room: "Block C - 204" },
    { department: "BBA (Business Analytics)", name: "Prof. Aisha Khan", email: "hod.bba@uai.edu.in", phone: "+91 99881 22342", room: "Block B - 108" },
    { department: "MBA (Agribusiness)", name: "Dr. Sameer Butt", email: "hod.mba@uai.edu.in", phone: "+91 99881 22343", room: "Block B - 110" },
    { department: "Design Thinking", name: "Prof. Huma Raza", email: "hod.design@uai.edu.in", phone: "+91 99881 22344", room: "Innovation Lab" }
  ],
  counsellors: [
    { name: "Dr. Sarah Ahmed", role: "Lead Student Counsellor", email: "sarah.ahmed@uai.edu.in", phone: "+91 99881 22350", specialty: "Academic Anxiety & Cognitive Restructuring" },
    { name: "Mr. Bilal Hassan", role: "Associate Counsellor", email: "bilal.hassan@uai.edu.in", phone: "+91 99881 22351", specialty: "Hostel Adaptation & Social Well-being" },
    { name: "Dr. Kamran Verma", role: "Consulting Campus Psychiatrist", email: "kamran.verma@uai.edu.in", phone: "+91 99881 22352", specialty: "Pharmacotherapy & Crisis Intervention" }
  ],
  departments: [
    { code: "B.Tech", name: "AI & Biotechnology", hod: "Dr. Naveen Qureshi", facultyCount: 18, studentCount: 320, riskRatio: "12.4%" },
    { code: "B.Sc", name: "Agriculture", hod: "Dr. Farhan Malik", facultyCount: 22, studentCount: 410, riskRatio: "21.4%" },
    { code: "BBA", name: "Business Analytics", hod: "Prof. Aisha Khan", facultyCount: 12, studentCount: 250, riskRatio: "9.6%" },
    { code: "MBA", name: "Agribusiness & AI", hod: "Dr. Sameer Butt", facultyCount: 16, studentCount: 180, riskRatio: "15.8%" },
    { code: "Design Thinking", name: "Human-Centred Innovation", hod: "Prof. Huma Raza", facultyCount: 8, studentCount: 120, riskRatio: "7.2%" }
  ],
  faculty: [
    { name: "Prof. Tariq Mahmood", department: "B.Sc (Agriculture)", role: "Professor of Agronomy", email: "tariq.mahmood@uai.edu.in", phone: "+91 98112 00001" },
    { name: "Dr. Yasir Abbasi", department: "B.Sc (Agriculture)", role: "Associate Professor of Soil Science", email: "yasir.abbasi@uai.edu.in", phone: "+91 98112 00002" },
    { name: "Prof. Noreen Latif", department: "B.Sc (Agriculture)", role: "Professor of Horticulture", email: "noreen.latif@uai.edu.in", phone: "+91 98112 00003" },
    { name: "Dr. Haris Mirza", department: "B.Tech (AI & Biotech)", role: "Professor of Bioinformatics", email: "haris.mirza@uai.edu.in", phone: "+91 98112 00004" },
    { name: "Prof. Bushra Siddiqui", department: "B.Tech (AI & Biotech)", role: "Professor of Genetic Engineering", email: "bushra.siddiqui@uai.edu.in", phone: "+91 98112 00005" },
    { name: "Dr. Adeel Qureshi", department: "BBA (Business Analytics)", role: "Associate Professor of Data Science", email: "adeel.qureshi@uai.edu.in", phone: "+91 98112 00006" },
    { name: "Prof. Shazia Hashmi", department: "MBA (Agribusiness)", role: "Professor of Agri-Economics", email: "shazia.hashmi@uai.edu.in", phone: "+91 98112 00007" },
    { name: "Dr. Babar Sharif", department: "Design Thinking", role: "Professor of Product UX", email: "babar.sharif@uai.edu.in", phone: "+91 98112 00008" }
  ]
};
