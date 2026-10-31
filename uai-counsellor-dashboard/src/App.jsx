import React, { useState, useMemo, useEffect } from 'react';
import {
  LayoutDashboard,
  Users,
  ClipboardCheck,
  AlertTriangle,
  TrendingUp,
  HeartHandshake,
  FileBarChart,
  BookOpen,
  Settings as SettingsIcon,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  Search,
  Download,
  User,
  Plus,
  PhoneCall,
  ExternalLink,
  X,
  Clock,
  Activity,
  CheckCircle,
  FileText,
  AlertCircle,
  ChevronDown,
  Sparkles,
  Award,
  Send,
  HelpCircle as FaqIcon,
  Check,
  Flag,
  Heart,
  GraduationCap
} from 'lucide-react';
import {
  mockStudents,
  mockAssessments,
  mockAlerts,
  mockInsights,
  mockResources,
  mockSystemSettings,
  coursesList,
  cohortsList,
  academicYearsList,
  riskLevelsList,
  followUpStudentsList as mockFollowUpStudentsList,
  mockInstitutionalInfo
} from './mockData';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  LineChart,
  Line,
  LabelList,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

// Universal AI University Logos
const FullLogo = () => (
  <svg viewBox="0 0 320 95" width="100%" height="100%" style={{ color: 'white' }}>
    {/* Map Grid (4 small squares with organic green paths representing continents) */}
    {/* Top-Left */}
    <rect x="5" y="5" width="22" height="22" fill="#19539D" rx="3" />
    <path d="M 8,15 C 10,13 14,13 16,11 C 18,9 20,12 23,10 C 24,12 23,14 24,16 Z" fill="#769D3E" />
    <path d="M 10,20 C 12,22 14,19 16,21 C 18,23 21,20 22,22 Z" fill="#769D3E" />

    {/* Top-Right */}
    <rect x="31" y="5" width="22" height="22" fill="#12284C" rx="3" />
    <path d="M 33,10 C 35,8 37,11 40,9 C 42,7 45,9 47,11 C 46,14 44,12 43,15 Z" fill="#769D3E" />
    <path d="M 37,18 C 39,20 41,17 43,19 Z" fill="#769D3E" />

    {/* Bottom-Left */}
    <rect x="5" y="31" width="22" height="22" fill="#19539D" rx="3" />
    <path d="M 7,37 C 9,35 11,38 13,36 C 15,34 18,37 20,35 C 19,39 17,38 16,41 Z" fill="#769D3E" />

    {/* Bottom-Right */}
    <rect x="31" y="31" width="22" height="22" fill="#19539D" rx="3" />
    <path d="M 33,41 C 35,39 38,42 40,40 C 42,38 45,41 47,39 C 45,44 42,43 40,46 Z" fill="#769D3E" />

    {/* Stylized geometric double-stroke A */}
    <path d="M 72,5 L 58,50 L 66,50 L 68,41 L 83,41 L 85,50 L 93,50 L 79,5 Z" fill="#19539D" />
    {/* Inner white inlay to create a high-fidelity double-line vector look */}
    <path d="M 75.5,10 L 64,46 M 75.5,10 L 87,46 M 68,36 L 83,36" fill="none" stroke="#FFFFFF" strokeWidth="2.2" strokeLinecap="round" />

    {/* Stylized geometric green i */}
    {/* Square dot */}
    <rect x="100" y="5" width="11" height="11" fill="#769D3E" rx="1.5" />
    {/* horizontal bar */}
    <rect x="100" y="19" width="11" height="5" fill="#769D3E" rx="1" />
    {/* vertical column */}
    <path d="M 100,27 L 111,27 L 111,50 L 100,50 Z" fill="#769D3E" />

    {/* Elegant typography */}
    <text x="130" y="30" font-family="'Georgia', serif" font-size="28" font-weight="bold" fill="#FFFFFF">Universal</text>
    <text x="130" y="53" font-family="'Georgia', serif" font-size="28" font-weight="bold" fill="#769D3E">University</text>

    {/* Footer: The future is here */}
    <line x1="5" y1="72" x2="115" y2="72" stroke="rgba(255,255,255,0.2)" strokeWidth="1" />
    <text x="160" y="76" font-family="'Georgia', serif" font-size="12" font-style="italic" fill="#FFFFFF" text-anchor="middle">The future is here</text>
    <line x1="205" y1="72" x2="315" y2="72" stroke="rgba(255,255,255,0.2)" strokeWidth="1" />
  </svg>
);

const CollapsedLogo = () => (
  <svg viewBox="0 0 115 50" width="100%" height="100%">
    {/* Map Grid */}
    {/* Top-Left */}
    <rect x="2" y="2" width="14" height="14" fill="#19539D" rx="2" />
    <path d="M 4,8 C 5,7 7,7 8,6 Z" fill="#769D3E" />
    
    {/* Top-Right */}
    <rect x="19" y="2" width="14" height="14" fill="#12284C" rx="2" />
    <path d="M 20,5 C 21,4 23,5 24,4 Z" fill="#769D3E" />

    {/* Bottom-Left */}
    <rect x="2" y="19" width="14" height="14" fill="#19539D" rx="2" />
    
    {/* Bottom-Right */}
    <rect x="19" y="19" width="14" height="14" fill="#19539D" rx="2" />

    {/* Stylized geometric A */}
    <path d="M 46,2 L 35,38 L 41,38 L 43,31 L 53,31 L 55,38 L 61,38 L 50,2 Z" fill="#19539D" />
    <path d="M 48,6 L 39,34 M 48,6 L 57,34 M 41.5,27 L 54.5,27" fill="none" stroke="#FFFFFF" strokeWidth="1.5" strokeLinecap="round" />

    {/* Stylized geometric green i */}
    {/* Square dot */}
    <rect x="67" y="2" width="7" height="7" fill="#769D3E" rx="1" />
    {/* horizontal bar */}
    <rect x="67" y="11" width="7" height="3" fill="#769D3E" rx="0.5" />
    {/* vertical column */}
    <path d="M 67,16 L 74,16 L 74,38 L 67,38 Z" fill="#769D3E" />
  </svg>
);

// Dynamic followUpStudentsList connected to the Flask SQLite database data if available
const followUpStudentsList = (typeof window !== 'undefined' && window.__FLASK_FLAGGED_STUDENTS__ && window.__FLASK_FLAGGED_STUDENTS__.length > 0)
  ? window.__FLASK_FLAGGED_STUDENTS__.map((s, index) => {
      // Handle ID cleaning
      const rawId = String(s.id || s.regId || '');
      const shortId = rawId.includes('-') ? rawId.split('-').pop() : rawId;
      const cleanRegId = rawId.startsWith("REG-") ? rawId : `REG-2025-${shortId.slice(-4)}`;
      
      return {
        id: s.id || `std-${index}`,
        profile_id: s.profile_id || null,
        name: s.name,
        regId: cleanRegId,
        course: s.course || "B.Sc. Agriculture",
        cohort: s.cohort || "Batch 2025",
        stress: s.stress || "Low",
        impulsivity: s.impulsivity || "Low",
        risk: s.risk_taking || s.risk || "Low",
        intervention: s.flag === "Yes" ? "Yes" : "No"
      };
    })
  : mockFollowUpStudentsList;

export default function App() {
  // Navigation & UI States
  const [activeTab, setActiveTab] = useState("Dashboard");
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null); // For student detail modal
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Interactive Live Data States
  const [students, setStudents] = useState(mockStudents);

  // Generate reactive alert lists from our 200 Pakistani-named students
  const initialAlerts = useMemo(() => {
    return followUpStudentsList
      .filter(s => s.intervention === 'Yes')
      .map((s, index) => {
        let severity = "Moderate";
        let trigger = "Moderate Anxiety Flag";
        if (s.stress === "Severe") {
          severity = "Severe";
          trigger = "Severe DASS-21 Stress Flag";
        } else if (s.stress === "High") {
          severity = "High";
          trigger = "High DASS-21 Stress Flag";
        } else if (s.impulsivity === "High") {
          severity = "High";
          trigger = "High BIS-11 Impulsivity Flag";
        } else if (s.risk === "High") {
          severity = "High";
          trigger = "High BRIS Behavioural Risk Flag";
        } else if (s.stress === "Moderate") {
          severity = "Moderate";
          trigger = "Moderate DASS-21 Stress Flag";
        } else if (s.impulsivity === "Moderate") {
          severity = "Moderate";
          trigger = "Moderate BIS-11 Impulsivity Flag";
        } else if (s.risk === "Moderate") {
          severity = "Moderate";
          trigger = "Moderate BRIS Behavioural Risk Flag";
        }

        const daysAgo = (index % 12) + 1;
        const dateStr = `${daysAgo} days ago`;
        const actualDate = new Date();
        actualDate.setDate(actualDate.getDate() - daysAgo);
        const dateFormatted = actualDate.toISOString().split('T')[0];

        return {
          id: `alt-2025-${s.id}`,
          studentId: s.id,
          regId: s.regId,
          studentName: s.name,
          course: s.course,
          cohort: s.cohort,
          riskLevel: severity === "Severe" || severity === "High" ? "High" : "Medium",
          severity: severity, // Severe / High / Moderate
          trigger: trigger,
          time: dateStr,
          date: dateFormatted,
          details: `Student reported flagged clinical indexes on recent screening: Stress (${s.stress}), Impulsivity (${s.impulsivity}), Risk-Taking (${s.risk}). Faculty advisor has requested immediate counsellor checkup.`,
          status: "Active",
          actionTaken: ""
        };
      });
  }, []);

  const [alerts, setAlerts] = useState(initialAlerts);

  // Generate reactive interventions lists from the 27 flagged students
  const initialInterventions = useMemo(() => {
    return followUpStudentsList
      .filter(s => s.intervention === 'Yes')
      .map((s, index) => {
        const statuses = ["In Progress", "Completed", "Pending"];
        const status = statuses[index % statuses.length];
        const counsellorsList = ["Dr. Sarah Ahmed", "Mr. Bilal Hassan", "Dr. Kamran Verma"];
        const counsellor = counsellorsList[index % counsellorsList.length];
        
        const daysOut = (index * 3) % 15 + 1;
        const nextSession = status === "Completed" ? "N/A" : `2026-06-${String(daysOut).padStart(2, '0')}`;

        return {
          id: `int-${index}`,
          studentId: s.id,
          regId: s.regId,
          studentName: s.name,
          course: s.course,
          cohort: s.cohort,
          status: status, // Pending / In Progress / Completed
          counsellor: counsellor,
          nextSessionDate: nextSession,
          notes: `Active intervention plan created. Initial screening revealed elevated ${s.stress} stress levels. Plan includes bi-weekly cognitive behavioral therapy (CBT) and academic adjustment profiling.`,
          date: `2026-05-${String(daysOut).padStart(2, '0')}`
        };
      });
  }, []);

  const [interventions, setInterventions] = useState(initialInterventions);
  const [profile, setProfile] = useState({
    name: "Dr. Sarah Ahmed",
    role: "Lead Student Counsellor",
    department: "Counselling Services • UAi",
    avatar: "SA"
  });
  const [systemSettings, setSystemSettings] = useState(mockSystemSettings);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  
  // Export report states
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportStep, setExportStep] = useState(1);

  // Global Filters
  const [selectedCourse, setSelectedCourse] = useState("B.Sc. Agriculture");
  const [selectedCohort, setSelectedCohort] = useState("Batch 2025");
  const [selectedAcademicYear, setSelectedAcademicYear] = useState("2025-2026");
  const [selectedRiskLevel, setSelectedRiskLevel] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");

  // Browser Tab Title & Mobile Responsive Sidebar Collapse Effect
  useEffect(() => {
    document.title = "Counsellor Insights Dashboard | UAi";

    const handleResize = () => {
      if (window.innerWidth < 768) {
        setIsSidebarCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize(); // Call initially on mount
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Toast trigger helper
  const triggerToast = (msg) => {
    setToastMessage(msg);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  // Filtered Students based on search term & dropdown selectors
  const filteredStudents = useMemo(() => {
    return students.filter(student => {
      const matchesCourse = selectedCourse === "All" || student.course === selectedCourse;
      const matchesCohort = selectedCohort === "All" || student.cohort === selectedCohort;
      const matchesYear = selectedAcademicYear === "All" || student.academicYear === selectedAcademicYear;
      const matchesRisk = selectedRiskLevel === "All" || student.riskLevel === selectedRiskLevel;
      
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = student.name.toLowerCase().includes(searchLower) ||
                            student.id.toLowerCase().includes(searchLower) ||
                            student.email.toLowerCase().includes(searchLower);

      return matchesCourse && matchesCohort && matchesYear && matchesRisk && matchesSearch;
    });
  }, [students, selectedCourse, selectedCohort, selectedAcademicYear, selectedRiskLevel, searchTerm]);

  // Global Dynamic Filter for all 200 students based on global filter bar dropdowns & search bar
  const filteredFollowUpStudents = useMemo(() => {
    return followUpStudentsList.filter(student => {
      // Course filter
      const matchesCourse = selectedCourse === "All" || student.course === selectedCourse;
      // Cohort filter
      const matchesCohort = selectedCohort === "All" || student.cohort === selectedCohort;
      
      // Risk filter mapping (High/Medium/Low/All global values mapped to DASS-21, BIS-11, BRIS variables)
      let matchesRisk = true;
      if (selectedRiskLevel !== "All") {
        if (selectedRiskLevel === "High") {
          matchesRisk = student.stress === "High" || student.stress === "Severe" ||
                        student.impulsivity === "High" || student.risk === "High";
        } else if (selectedRiskLevel === "Medium") {
          matchesRisk = student.stress === "Moderate" || student.impulsivity === "Moderate" || student.risk === "Moderate";
        } else if (selectedRiskLevel === "Low") {
          matchesRisk = student.stress === "Low" && student.impulsivity === "Low" && student.risk === "Low";
        }
      }
      
      // Search matches name or registration ID
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = student.name.toLowerCase().includes(searchLower) ||
                            student.regId.toLowerCase().includes(searchLower);

      return matchesCourse && matchesCohort && matchesRisk && matchesSearch;
    });
  }, [selectedCourse, selectedCohort, selectedRiskLevel, searchTerm]);

  // Export report handler showing custom loading-state modal popup
  const handleExportReport = () => {
    setShowExportModal(true);
    setExportStep(1);
    setTimeout(() => {
      setExportStep(2);
    }, 1200);
  };

  // Interactive Log Intervention Note
  const handleAddIntervention = (studentId, type, notes) => {
    const student = students.find(s => s.id === studentId);
    if (!student) return;

    const newIntervention = {
      date: new Date().toISOString().split('T')[0],
      type,
      notes,
      counsellor: "Dr. Sarah Ahmed",
      status: "Ongoing"
    };

    // Update Students State
    setStudents(prev => prev.map(s => {
      if (s.id === studentId) {
        return {
          ...s,
          interventions: [newIntervention, ...s.interventions],
          lastContacted: newIntervention.date,
          wellnessScore: Math.min(100, s.wellnessScore + 5) // intervention improves wellness score slightly
        };
      }
      return s;
    }));

    // Update Interventions Flat State
    setInterventions(prev => [
      { ...newIntervention, studentId: student.id, studentName: student.name, course: student.course },
      ...prev
    ]);

    triggerToast(`Intervention logged successfully for ${student.name}.`);
  };

  // Acknowledge or Modify Risk Alerts State
  const handleUpdateAlertStatus = (alertId, newStatus) => {
    setAlerts(prev => prev.map(alt => {
      if (alt.id === alertId) {
        return { ...alt, status: newStatus, actionTaken: `Marked as ${newStatus} by Dr. Sarah Ahmed.` };
      }
      return alt;
    }));
    triggerToast(`Alert status updated to ${newStatus}.`);
  };

  return (
    <div className={`app-container ${isDarkMode ? 'dark-theme' : ''}`}>
      {/* Toast Alert popup */}
      {showToast && (
        <div style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          backgroundColor: '#1B3A6B',
          color: 'white',
          padding: '12px 20px',
          borderRadius: '8px',
          boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
          zIndex: 2000,
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          borderLeft: '4px solid #27AE60',
          animation: 'fadeIn 0.2s ease-out'
        }}>
          <CheckCircle size={18} color="#27AE60" />
          <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{toastMessage}</span>
        </div>
      )}

      {/* Sidebar Navigation */}
      <aside className={`sidebar ${isSidebarCollapsed ? 'collapsed' : ''}`}>
        <div>
          <div className="sidebar-brand" style={{ padding: isSidebarCollapsed ? '8px 4px 20px 4px' : '8px 0 20px 0', borderBottom: 'none', display: 'block', overflow: 'hidden' }}>
            {isSidebarCollapsed ? <CollapsedLogo /> : <FullLogo />}
          </div>

          <nav className="sidebar-nav">
            {[
              { id: "Dashboard", icon: LayoutDashboard },
              { id: "Students", icon: Users },
              { id: "Assessments", icon: ClipboardCheck },
              { id: "Risk Alerts", icon: AlertTriangle },
              { id: "Insights", icon: TrendingUp },
              { id: "Interventions", icon: HeartHandshake },
              { id: "Reports", icon: FileBarChart },
              { id: "Resources", icon: BookOpen },
              { id: "Institution", icon: GraduationCap },
              { id: "Settings", icon: SettingsIcon },
              { id: "Help & Support", icon: HelpCircle }
            ].map(item => {
              const IconComponent = item.icon;
              return (
                <div
                  key={item.id}
                  className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(item.id)}
                  data-label={item.id}
                >
                  <IconComponent className="nav-item-icon" />
                  <span className="nav-item-text">{item.id}</span>
                </div>
              );
            })}
          </nav>
        </div>

        <div className="sidebar-footer">
          <button className="collapse-btn" onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}>
            {isSidebarCollapsed ? <ChevronRight size={18} /> : (
              <>
                <ChevronLeft size={18} />
                <span className="collapse-text">Collapse Menu</span>
              </>
            )}
          </button>
        </div>
      </aside>

      {/* Main Layout Area */}
      <div className={`main-wrapper ${isSidebarCollapsed ? 'expanded' : ''}`}>
        
        {/* Top Header */}
        <header className="top-header">
          <div className="header-title-section">
            <h1>Counsellor Insights Dashboard</h1>
            <p>Student Well-Being Monitoring & Early Support</p>
          </div>
          <div className="header-profile-section">
            <div className="profile-avatar">{profile.avatar}</div>
            <div className="profile-info">
              <span className="profile-name">{profile.name}</span>
              <span className="profile-title">{profile.role} • {profile.department}</span>
            </div>
          </div>
        </header>

        {/* Filter Bar */}
        <section className="filter-bar">
          <div className="filters-group">
            <div className="filter-select-wrapper">
              <label>Course</label>
              <select
                className="filter-select"
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
              >
                <option value="All">All Courses</option>
                {coursesList.map(course => <option key={course} value={course}>{course}</option>)}
              </select>
            </div>

            <div className="filter-select-wrapper">
              <label>Cohort/Batch</label>
              <select
                className="filter-select"
                value={selectedCohort}
                onChange={(e) => setSelectedCohort(e.target.value)}
              >
                <option value="All">All Batches</option>
                {cohortsList.map(cohort => <option key={cohort} value={cohort}>{cohort}</option>)}
              </select>
            </div>

            <div className="filter-select-wrapper">
              <label>Academic Year</label>
              <select
                className="filter-select"
                value={selectedAcademicYear}
                onChange={(e) => setSelectedAcademicYear(e.target.value)}
              >
                <option value="All">All Years</option>
                {academicYearsList.map(ay => <option key={ay} value={ay}>{ay}</option>)}
              </select>
            </div>

            <div className="filter-select-wrapper">
              <label>Risk Level</label>
              <select
                className="filter-select"
                value={selectedRiskLevel}
                onChange={(e) => setSelectedRiskLevel(e.target.value)}
              >
                {riskLevelsList.map(risk => <option key={risk} value={risk}>{risk === "All" ? "All Risks" : `${risk} Risk`}</option>)}
              </select>
            </div>
          </div>

          <div className="search-export-group">
            <div className="search-input-wrapper">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Search students..."
                className="search-input"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <button className="export-btn" onClick={handleExportReport}>
              <Download size={15} />
              Export Report
            </button>
          </div>
        </section>

        {/* Dynamic Page Container */}
        <main className="page-container page-fade-in" key={activeTab}>
          {activeTab === "Dashboard" && (
            <DashboardPage
              students={filteredStudents}
              alerts={alerts}
              interventions={interventions}
              setActiveTab={setActiveTab}
              setSelectedStudent={setSelectedStudent}
              followUpStudents={filteredFollowUpStudents}
              selectedCohort={selectedCohort}
            />
          )}

          {activeTab === "Students" && (
            <StudentsPage
              students={filteredStudents}
              setSelectedStudent={setSelectedStudent}
              course={selectedCourse}
              cohort={selectedCohort}
              followUpStudents={filteredFollowUpStudents}
            />
          )}

          {activeTab === "Assessments" && (
            <AssessmentsPage
              triggerToast={triggerToast}
              students={students}
            />
          )}

          {activeTab === "Risk Alerts" && (
            <RiskAlertsPage
              alerts={alerts}
              onUpdateStatus={handleUpdateAlertStatus}
              setSelectedStudent={setSelectedStudent}
              students={students}
            />
          )}

          {activeTab === "Insights" && (
            <InsightsPage triggerToast={triggerToast} />
          )}

          {activeTab === "Interventions" && (
            <InterventionsPage
              interventions={interventions}
              students={students}
              onAddIntervention={handleAddIntervention}
            />
          )}

          {activeTab === "Reports" && (
            <ReportsPage students={filteredStudents} course={selectedCourse} cohort={selectedCohort} />
          )}

          {activeTab === "Resources" && (
            <ResourcesPage triggerToast={triggerToast} />
          )}

          {activeTab === "Settings" && (
            <SettingsPage
              settings={systemSettings}
              setSettings={setSystemSettings}
              triggerToast={triggerToast}
              isDarkMode={isDarkMode}
              setIsDarkMode={setIsDarkMode}
            />
          )}

          {activeTab === "Institution" && (
            <InstitutionPage triggerToast={triggerToast} />
          )}

          {activeTab === "Help & Support" && (
            <HelpPage />
          )}
        </main>

        {/* Universal premium responsive footer */}
        <footer className="dashboard-footer-bar">
          <p>© 2025 University of Agriculture (UAi). All rights reserved.</p>
          <div className="footer-links">
            <a href="#privacy">Privacy Policy</a>
            <span>|</span>
            <a href="#terms">Terms of Use</a>
            <span>|</span>
            <a href="#support">Contact Support</a>
          </div>
        </footer>
      </div>

      {/* Comprehensive Student Details Modal (Drilldown) */}
      {selectedStudent && (
        <StudentDetailsModal
          student={selectedStudent}
          onClose={() => setSelectedStudent(null)}
          onAddIntervention={handleAddIntervention}
        />
      )}

      {/* Export Report Loading State & Custom Modal Popup */}
      {showExportModal && (
        <div className="modal-overlay" onClick={() => setShowExportModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '400px', textAlign: 'center', padding: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '-16px', marginRight: '-16px' }}>
              <button className="modal-close-btn" onClick={() => setShowExportModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            {exportStep === 1 ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
                <div className="export-spinner"></div>
                <h3 style={{ fontFamily: 'Outfit', fontSize: '1.25rem', color: '#1B3A6B' }}>Exporting Report</h3>
                <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Compiling dashboard insights, student charts, and clinical logs into PDF format...</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
                <div style={{
                  width: '60px',
                  height: '60px',
                  borderRadius: '50%',
                  backgroundColor: '#E8F8F0',
                  color: '#27AE60',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 10px rgba(39, 174, 96, 0.15)'
                }}>
                  <CheckCircle size={36} />
                </div>
                <h3 style={{ fontFamily: 'Outfit', fontSize: '1.25rem', color: '#27AE60' }}>Export Complete!</h3>
                <p style={{ fontSize: '0.85rem', color: '#1E293B', fontWeight: 600 }}>Done! Report_May2025.pdf downloaded</p>
                <p style={{ fontSize: '0.78rem', color: '#64748B' }}>The clinical report has been successfully compiled and saved to your downloads folder.</p>
                <button className="submit-btn" onClick={() => setShowExportModal(false)} style={{ padding: '8px 24px', width: '100%', marginTop: '8px' }}>
                  Acknowledge
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/* ==========================================
   COMPONENT: DashboardPage
   ========================================== */
function DashboardPage({ students, alerts, interventions, setActiveTab, setSelectedStudent, followUpStudents, selectedCohort }) {
  // Aggregate KPIs based on current filtered student set
  const totalStudents = students.length;
  const highRiskCount = students.filter(s => s.riskLevel === "High").length;
  const mediumRiskCount = students.filter(s => s.riskLevel === "Medium").length;
  const lowRiskCount = students.filter(s => s.riskLevel === "Low").length;

  const averageWellnessScore = useMemo(() => {
    if (students.length === 0) return 0;
    const sum = students.reduce((acc, curr) => acc + curr.wellnessScore, 0);
    return Math.round(sum / students.length);
  }, [students]);

  const activeInterventions = interventions.filter(i => i.status === "Ongoing").length;
  const activeAlerts = alerts.filter(a => a.status === "In Progress" || a.status === "Investigating").length;

  // Chart 1 Data: Pie/Donut Chart for Overall Risk Distribution
  const chart1Data = (typeof window !== 'undefined' && window.__FLASK_CHART_DATA__ && window.__FLASK_CHART_DATA__.overall_risk)
    ? [
        { name: "Low Risk", value: window.__FLASK_CHART_DATA__.overall_risk.data[0], color: "#27AE60", percentage: window.__FLASK_CHART_DATA__.overall_risk.percentages[0] },
        { name: "Moderate Risk", value: window.__FLASK_CHART_DATA__.overall_risk.data[1], color: "#F2C94C", percentage: window.__FLASK_CHART_DATA__.overall_risk.percentages[1] },
        { name: "High Risk", value: window.__FLASK_CHART_DATA__.overall_risk.data[2], color: "#DD6B20", percentage: window.__FLASK_CHART_DATA__.overall_risk.percentages[2] },
        { name: "Severe Risk", value: window.__FLASK_CHART_DATA__.overall_risk.data[3], color: "#EB5757", percentage: window.__FLASK_CHART_DATA__.overall_risk.percentages[3] }
      ]
    : [
        { name: "Low Risk", value: 69, color: "#27AE60", percentage: "54.8%" },
        { name: "Moderate Risk", value: 31, color: "#F2C94C", percentage: "24.6%" },
        { name: "High Risk", value: 17, color: "#DD6B20", percentage: "13.5%" },
        { name: "Severe Risk", value: 9, color: "#EB5757", percentage: "7.1%" }
      ];

  // Chart 4 Data: Flagged Cases Over Time (Line Chart)
  const chart4Data = (typeof window !== 'undefined' && window.__FLASK_CHART_DATA__ && window.__FLASK_CHART_DATA__.trend)
    ? window.__FLASK_CHART_DATA__.trend.labels.map((lbl, idx) => ({
        name: lbl,
        value: window.__FLASK_CHART_DATA__.trend.data[idx]
      }))
    : [
        { name: "Dec '24", value: 14 },
        { name: "Jan '25", value: 16 },
        { name: "Feb '25", value: 18 },
        { name: "Mar '25", value: 21 },
        { name: "Apr '25", value: 23 },
        { name: "May '25", value: 27 }
      ];

  // Follow-up Table state
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState('name');
  const [sortDirection, setSortDirection] = useState('asc');

  // Sorting handler
  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  // Sorted follow-up students
  const sortedStudents = useMemo(() => {
    const list = [...followUpStudents];
    if (!sortColumn) return list;
    
    list.sort((a, b) => {
      let aVal = a[sortColumn];
      let bVal = b[sortColumn];
      
      // Handle casing
      if (typeof aVal === 'string') aVal = aVal.toLowerCase();
      if (typeof bVal === 'string') bVal = bVal.toLowerCase();
      
      // Handle hierarchy for Stress / Impulsivity / Risk levels: Low < Moderate < High < Severe
      const hierarchy = { Low: 1, Moderate: 2, High: 3, Severe: 4 };
      if (['stress', 'impulsivity', 'risk'].includes(sortColumn)) {
        aVal = hierarchy[a[sortColumn]] || 0;
        bVal = hierarchy[b[sortColumn]] || 0;
      }
      
      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
    return list;
  }, [followUpStudents, sortColumn, sortDirection]);

  const itemsPerPage = 20;
  const totalPages = Math.ceil(sortedStudents.length / itemsPerPage);
  
  const paginatedStudents = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return sortedStudents.slice(startIndex, startIndex + itemsPerPage);
  }, [sortedStudents, currentPage]);

  const handleViewReport = (student) => {
    const detailedStudent = {
      id: student.regId,
      profile_id: student.profile_id,
      name: student.name,
      course: student.course,
      cohort: student.cohort,
      academicYear: "2025-2026",
      riskLevel: student.stress === "Severe" || student.stress === "High" ? "High" : student.stress === "Moderate" ? "Medium" : "Low",
      wellnessScore: student.stress === "Severe" ? 28 : student.stress === "High" ? 44 : student.stress === "Moderate" ? 65 : 88,
      lastContacted: "2026-05-20",
      email: `${student.name.toLowerCase().replace(/\s+/g, '.')}@uai.edu.in`,
      phone: "+92 300 1234567",
      avatar: student.name.split(' ').map(n=>n[0]).join(''),
      gender: Math.random() > 0.5 ? "Male" : "Female",
      hosteller: Math.random() > 0.3 ? "Yes (Hostel-A)" : "No (Day Scholar)",
      attendance: `${Math.floor(55 + Math.random() * 40)}%`,
      gpa: `${(6.0 + Math.random() * 3.5).toFixed(1)}/10`,
      riskFactors: {
        psychological: `Stress Level (DASS-21) is flagged as ${student.stress}. Impulsivity (BIS-11) is ${student.impulsivity}.`,
        academic: `Attendance stands at acceptable baseline. Course engagement remains steady.`,
        social: `Struggling with exam preparation pressure and cohort adjustments.`
      },
      assessments: [
        { name: "DASS-21 Stress Level", date: "2026-05-10", score: student.stress, status: student.stress === "Severe" || student.stress === "High" ? "Critical" : "Normal" },
        { name: "BIS-11 Impulsivity", date: "2026-05-12", score: student.impulsivity, status: student.impulsivity === "High" ? "Flagged" : "Normal" },
        { name: "BRIS Risk-Taking", date: "2026-05-14", score: student.risk, status: student.risk === "High" ? "Flagged" : "Normal" }
      ],
      interventions: []
    };
    setSelectedStudent(detailedStudent);
  };

  // Chart 2 Data: Grouped Bar Chart for Domain Overview
  const chart2Data = (typeof window !== 'undefined' && window.__FLASK_CHART_DATA__ && window.__FLASK_CHART_DATA__.domain_overview_by_cohort)
    ? (window.__FLASK_CHART_DATA__.domain_overview_by_cohort[selectedCohort] || window.__FLASK_CHART_DATA__.domain_overview_by_cohort["All"])
    : [
        { name: "Stress", "DASS-21": 1.85, "BIS-11": 1.62, "Behavioural Risk": null },
        { name: "Anxiety", "DASS-21": null, "BIS-11": 1.39, "Behavioural Risk": null },
        { name: "Depression", "DASS-21": null, "BIS-11": null, "Behavioural Risk": null },
        { name: "Impulsivity", "DASS-21": 2.11, "BIS-11": null, "Behavioural Risk": null },
        { name: "Non-Planning", "DASS-21": null, "BIS-11": 2.32, "Behavioural Risk": null },
        { name: "Risk-Taking", "DASS-21": 1.78, "BIS-11": null, "Behavioural Risk": null },
        { name: "Aggression", "DASS-21": null, "BIS-11": 1.46, "Behavioural Risk": null }
      ];

  // Chart 3 Data: Stacked Bar 100% for Risk Distribution by Cohort
  const chart3Data = (typeof window !== 'undefined' && window.__FLASK_CHART_DATA__ && window.__FLASK_CHART_DATA__.cohort_risk)
    ? window.__FLASK_CHART_DATA__.cohort_risk.labels.map((lbl, idx) => {
        const cleanName = lbl.split('\n')[0];
        return {
          name: cleanName,
          Low: window.__FLASK_CHART_DATA__.cohort_risk.low[idx],
          Moderate: window.__FLASK_CHART_DATA__.cohort_risk.moderate[idx],
          High: window.__FLASK_CHART_DATA__.cohort_risk.high[idx],
          Severe: window.__FLASK_CHART_DATA__.cohort_risk.severe[idx]
        };
      })
    : [
        { name: "Batch 2022", Low: 56, Moderate: 24, High: 13, Severe: 7 },
        { name: "Batch 2023", Low: 52, Moderate: 27, High: 14, Severe: 7 },
        { name: "Batch 2024", Low: 50, Moderate: 26, High: 15, Severe: 9 },
        { name: "Batch 2025", Low: 55, Moderate: 25, High: 13, Severe: 6 }
      ];

  return (
    <div>
      {/* Dynamic Welcome Heading */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Welcome Back, Dr. Ahmed</h2>
          <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Here is the student well-being snapshot matching your active filters.</p>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span className="badge badge-pill-light">
            <Sparkles size={13} style={{ marginRight: '5px' }} />
            AI-Engine Active
          </span>
        </div>
      </div>

      {/* 5 Stat Cards Row */}
      <section className="stat-cards-container">
        {/* Card 1: Blue icon (people) | Total Students Assessed | 126 | 100% of 126 enrolled */}
        <div className="dashboard-stat-card">
          <div className="stat-icon-circle blue">
            <Users size={20} />
          </div>
          <div className="stat-text-side">
            <span className="stat-card-title">Total Students Assessed</span>
            <div className="stat-card-number">126</div>
            <span className="stat-card-subtitle">100% of 126 enrolled</span>
          </div>
        </div>

        {/* Card 2: Red flag icon | Flagged for Intervention | 27 | 21.4% of assessed */}
        <div className="dashboard-stat-card" style={{ cursor: 'pointer' }} onClick={() => setActiveTab("Risk Alerts")}>
          <div className="stat-icon-circle red">
            <Flag size={20} />
          </div>
          <div className="stat-text-side">
            <span className="stat-card-title">Flagged for Intervention</span>
            <div className="stat-card-number red">27</div>
            <span className="stat-card-subtitle">21.4% of assessed</span>
          </div>
        </div>

        {/* Card 3: Orange heart icon | Moderate Stress / Anxiety | 38 | 30.2% of assessed */}
        <div className="dashboard-stat-card" style={{ cursor: 'pointer' }} onClick={() => setActiveTab("Insights")}>
          <div className="stat-icon-circle orange">
            <Heart size={20} />
          </div>
          <div className="stat-text-side">
            <span className="stat-card-title">Moderate Stress / Anxiety</span>
            <div className="stat-card-number orange">38</div>
            <span className="stat-card-subtitle">30.2% of assessed</span>
          </div>
        </div>

        {/* Card 4: Purple pulse icon | High Impulsivity (BIS-11) | 22 | 17.5% of assessed */}
        <div className="dashboard-stat-card" style={{ cursor: 'pointer' }} onClick={() => setActiveTab("Assessments")}>
          <div className="stat-icon-circle purple">
            <Activity size={20} />
          </div>
          <div className="stat-text-side">
            <span className="stat-card-title">High Impulsivity (BIS-11)</span>
            <div className="stat-card-number purple">22</div>
            <span className="stat-card-subtitle">17.5% of assessed</span>
          </div>
        </div>

        {/* Card 5: Orange warning icon | Behavioural Risk Cases | 15 | 11.9% of assessed */}
        <div className="dashboard-stat-card" style={{ cursor: 'pointer' }} onClick={() => setActiveTab("Students")}>
          <div className="stat-icon-circle orange">
            <AlertTriangle size={20} />
          </div>
          <div className="stat-text-side">
            <span className="stat-card-title">Behavioural Risk Cases</span>
            <div className="stat-card-number orange">15</div>
            <span className="stat-card-subtitle">11.9% of assessed</span>
          </div>
        </div>
      </section>

      {/* Visual Recharts Row */}
      <section className="dashboard-charts-row">
        
        {/* CHART 1: Overall Risk Distribution (Pie/Donut, left) */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Overall Risk Distribution</h2>
          </div>
          <div className="chart-area" style={{ flexDirection: 'column', paddingBottom: '10px' }}>
            <div style={{ position: 'relative', width: '100%', height: '175px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chart1Data}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={70}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {chart1Data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value, name, props) => [`${value} Students (${props.payload.percentage})`, 'Count']} />
                </PieChart>
              </ResponsiveContainer>
              <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center',
                pointerEvents: 'none'
              }}>
                <div style={{ fontSize: '1.4rem', fontWeight: '700', color: '#1B3A6B', fontFamily: 'Outfit, sans-serif', lineHeight: 1 }}>126</div>
                <div style={{ fontSize: '0.6rem', color: '#64748B', fontWeight: '600', textTransform: 'uppercase', marginTop: '2px', letterSpacing: '0.5px' }}>Students</div>
              </div>
            </div>

            {/* Custom Pie Chart Legend */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px 8px', width: '100%', padding: '0 5px', marginTop: '10px' }}>
              {chart1Data.map((item, idx) => (
                <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.7rem', fontWeight: '500' }}>
                  <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: item.color, display: 'inline-block', flexShrink: 0 }}></span>
                  <span style={{ color: '#1E293B', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{item.name}</span>
                </div>
              ))}
            </div>
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94A3B8', marginTop: 'auto', borderTop: '1px solid #F1F5F9', paddingTop: '8px' }}>
            Data as of 18 May 2025
          </div>
        </div>

        {/* CHART 2: Domain Overview (Average Score) (Grouped Bar, center) */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Domain Overview (Average Score)</h2>
          </div>
          <div className="chart-area" style={{ flexDirection: 'column' }}>
            <div style={{ width: '100%', height: '175px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chart2Data} margin={{ top: 10, right: 5, left: -30, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                  <XAxis dataKey="name" tick={{ fontSize: 7, fill: '#64748B', fontWeight: 600 }} interval={0} stroke="#E2E8F0" />
                  <YAxis domain={[0, 3]} ticks={[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]} tick={{ fontSize: 8, fill: '#64748B' }} stroke="#E2E8F0" />
                  <Tooltip formatter={(value) => [value, 'Avg Score']} />
                  <Legend iconSize={6} iconType="circle" wrapperStyle={{ fontSize: '8px', paddingTop: '5px' }} />
                  <Bar dataKey="DASS-21" fill="#1B3A6B" radius={[1, 1, 0, 0]} barSize={6} />
                  <Bar dataKey="BIS-11" fill="#27AE60" radius={[1, 1, 0, 0]} barSize={6} />
                  <Bar dataKey="Behavioural Risk" fill="#DD6B20" radius={[1, 1, 0, 0]} barSize={6} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ fontSize: '0.65rem', color: '#64748B', fontWeight: '500', textAlign: 'center', marginTop: '10px' }}>
              0 (None) – 3 (Severe) | Higher scores = greater concern
            </div>
          </div>
        </div>

        {/* CHART 3: Risk Distribution by Cohort (Stacked Bar 100%, right) */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Risk Distribution by Cohort</h2>
          </div>
          <div className="chart-area" style={{ flexDirection: 'column' }}>
            <div style={{ width: '100%', height: '175px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chart3Data} margin={{ top: 10, right: 5, left: -30, bottom: 5 }} stackOffset="expand">
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                  <XAxis dataKey="name" tick={{ fontSize: 7, fill: '#64748B', fontWeight: 600 }} stroke="#E2E8F0" />
                  <YAxis tickFormatter={(v) => `${Math.round(v * 100)}%`} tick={{ fontSize: 8, fill: '#64748B' }} stroke="#E2E8F0" />
                  <Tooltip formatter={(value) => [`${Math.round(value)}%`, 'Percentage']} />
                  <Legend iconSize={6} iconType="circle" wrapperStyle={{ fontSize: '8px', paddingTop: '5px' }} />
                  <Bar dataKey="Low" stackId="a" fill="#27AE60" />
                  <Bar dataKey="Moderate" stackId="a" fill="#F2C94C" />
                  <Bar dataKey="High" stackId="a" fill="#DD6B20" />
                  <Bar dataKey="Severe" stackId="a" fill="#EB5757" radius={[1, 1, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0 5px', fontSize: '7px', color: '#94A3B8', fontWeight: 700, marginTop: '2px', textTransform: 'uppercase' }}>
              <span>n=120</span>
              <span>n=120</span>
              <span>n=118</span>
              <span>n=126</span>
            </div>
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94A3B8', marginTop: 'auto', borderTop: '1px solid #F1F5F9', paddingTop: '8px' }}>
            Based on latest assessments
          </div>
        </div>
      </section>

      {/* Row 2: 2 Charts + 1 Info Panel */}
      <section className="dashboard-charts-row">
        
        {/* CHART 4: Trend: Flagged Cases Over Time (Line chart, left) */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Trend: Flagged Cases Over Time</h2>
          </div>
          <div className="chart-area" style={{ flexDirection: 'column' }}>
            <div style={{ width: '100%', height: '175px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chart4Data} margin={{ top: 15, right: 15, left: -30, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                  <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748B', fontWeight: 600 }} stroke="#E2E8F0" />
                  <YAxis domain={[0, 40]} ticks={[0, 10, 20, 30, 40]} tick={{ fontSize: 8, fill: '#64748B' }} stroke="#E2E8F0" />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#1B3A6B" strokeWidth={2.5} dot={{ r: 4, fill: '#1B3A6B' }} activeDot={{ r: 6 }}>
                    <LabelList dataKey="value" position="top" style={{ fontSize: 9, fill: '#1B3A6B', fontWeight: 700 }} />
                  </Line>
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div style={{ fontSize: '0.65rem', color: '#94A3B8', marginTop: 'auto', borderTop: '1px solid #F1F5F9', paddingTop: '8px' }}>
            Based on latest assessments each month
          </div>
        </div>

        {/* PANEL: Course / Cohort Overview (center, card) */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Course / Cohort Overview</h2>
          </div>
          <div className="chart-area">
            <div className="overview-panel-grid">
              
              {/* Left half GREEN - Key Strengths */}
              <div className="overview-half green">
                <h3>Key Strengths</h3>
                <ul className="overview-list">
                  <li>
                    <span style={{ color: '#27AE60' }}>✅</span>
                    <span>Majority (54.8%) in low-risk category</span>
                  </li>
                  <li>
                    <span style={{ color: '#27AE60' }}>✅</span>
                    <span>Stress levels within manageable range</span>
                  </li>
                  <li>
                    <span style={{ color: '#27AE60' }}>✅</span>
                    <span>Strong engagement in assessments</span>
                  </li>
                  <li>
                    <span style={{ color: '#27AE60' }}>✅</span>
                    <span>Consistent improvement in support seeking</span>
                  </li>
                </ul>
              </div>

              {/* Right half ORANGE - Key Concerns */}
              <div className="overview-half orange">
                <h3>Key Concerns</h3>
                <ul className="overview-list">
                  <li>
                    <span style={{ color: '#DD6B20' }}>⚠️</span>
                    <span>21.4% students need intervention</span>
                  </li>
                  <li>
                    <span style={{ color: '#DD6B20' }}>⚠️</span>
                    <span>Impulsivity (Non-Planning) scores high</span>
                  </li>
                  <li>
                    <span style={{ color: '#DD6B20' }}>⚠️</span>
                    <span>Behavioural risk cases require follow-up</span>
                  </li>
                  <li>
                    <span style={{ color: '#DD6B20' }}>⚠️</span>
                    <span>Stress levels rising in recent months</span>
                  </li>
                </ul>
              </div>

            </div>
          </div>
        </div>

        {/* RIGHT SIDE PANEL: HawkAi Insight (fixed right column, navy border card) */}
        <div className="hawkai-card">
          <div className="hawkai-header">
            <span className="heart-icon">❤️</span>
            <span>HawkAi Insight</span>
          </div>
          
          <div className="hawkai-mascot-container">
            <img src="/uai_bird_mascot.png" alt="HawkAi Mascot" className="hawkai-mascot" />
          </div>

          <div className="hawkai-bold-text">
            Early support enables better outcomes.
          </div>

          <div className="hawkai-subtext">
            You have 27 students flagged for intervention. Timely outreach can reduce risk and build resilience.
          </div>

          <div className="hawkai-actions">
            <div className="hawkai-actions-title">Recommended Actions</div>
            <ul className="hawkai-actions-list">
              <li>
                <span style={{ color: '#27AE60' }}>✅</span>
                <span>Review flagged student reports</span>
              </li>
              <li>
                <span style={{ color: '#27AE60' }}>✅</span>
                <span>Schedule follow-up sessions</span>
              </li>
              <li>
                <span style={{ color: '#27AE60' }}>✅</span>
                <span>Track intervention outcomes</span>
              </li>
              <li>
                <span style={{ color: '#27AE60' }}>✅</span>
                <span>Monitor trends weekly</span>
              </li>
            </ul>
          </div>

          <button className="hawkai-btn" onClick={() => setActiveTab("Risk Alerts")}>
            View All Alerts
          </button>
        </div>

      </section>

      {/* SECTION: Students Requiring Follow-Up (27) */}
      <section className="table-card" style={{ marginTop: '24px', marginBottom: '24px' }}>
        <div className="table-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <AlertCircle size={20} color="#EB5757" />
            <h2 style={{ fontFamily: 'Outfit', fontWeight: 700, fontSize: '1.2rem', color: '#1B3A6B' }}>
              Students Requiring Follow-Up (27)
            </h2>
            <span title="Clinical monitoring indicators: Stress, Impulsivity, and Behavioural Risk scores flagging active concerns." style={{ cursor: 'pointer', display: 'inline-flex', alignItems: 'center' }}>
              <HelpCircle size={14} color="#64748B" />
            </span>
          </div>
          <span className="badge badge-high">27 Flagged Intervention Cases</span>
        </div>

        <div className="table-responsive">
          <table className="custom-table">
            <thead>
              <tr>
                {[
                  { label: "Student Name", key: "name" },
                  { label: "Registration ID", key: "regId" },
                  { label: "Course", key: "course" },
                  { label: "Cohort", key: "cohort" },
                  { label: "Stress Level (DASS-21)", key: "stress" },
                  { label: "Impulsivity (BIS-11)", key: "impulsivity" },
                  { label: "Risk-Taking (BRIS)", key: "risk" },
                  { label: "Intervention Flag", key: "intervention" }
                ].map(col => (
                  <th 
                    key={col.key} 
                    onClick={() => handleSort(col.key)} 
                    style={{ cursor: 'pointer', userSelect: 'none' }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      {col.label}
                      {sortColumn === col.key ? (
                        sortDirection === 'asc' ? ' ▲' : ' ▼'
                      ) : (
                        <span style={{ opacity: 0.3 }}> ↕</span>
                      )}
                    </div>
                  </th>
                ))}
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {paginatedStudents.map(student => (
                <tr key={student.id} onClick={() => handleViewReport(student)}>
                  <td>
                    <div style={{ fontWeight: 600, color: '#1E293B' }}>{student.name}</div>
                  </td>
                  <td>
                    <span style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600 }}>{student.regId}</span>
                  </td>
                  <td>{student.course}</td>
                  <td>{student.cohort}</td>
                  <td>
                    <span className={`badge ${
                      student.stress === 'Severe' ? 'badge-high' :
                      student.stress === 'High' ? 'badge-high' :
                      student.stress === 'Moderate' ? 'badge-medium' : 'badge-low'
                    }`} style={{
                      backgroundColor: student.stress === 'Severe' ? '#EB5757' : student.stress === 'High' ? '#DD6B20' : student.stress === 'Moderate' ? '#F2C94C' : '#27AE60',
                      color: 'white',
                      fontWeight: 700
                    }}>
                      {student.stress}
                    </span>
                  </td>
                  <td>
                    <span className="badge" style={{
                      backgroundColor: student.impulsivity === 'High' ? 'rgba(221, 107, 32, 0.15)' : student.impulsivity === 'Moderate' ? 'rgba(242, 201, 76, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                      color: student.impulsivity === 'High' ? '#DD6B20' : student.impulsivity === 'Moderate' ? '#B7791F' : '#27AE60',
                      fontWeight: 700
                    }}>
                      {student.impulsivity}
                    </span>
                  </td>
                  <td>
                    <span className="badge" style={{
                      backgroundColor: student.risk === 'High' ? 'rgba(221, 107, 32, 0.15)' : student.risk === 'Moderate' ? 'rgba(242, 201, 76, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                      color: student.risk === 'High' ? '#DD6B20' : student.risk === 'Moderate' ? '#B7791F' : '#27AE60',
                      fontWeight: 700
                    }}>
                      {student.risk}
                    </span>
                  </td>
                  <td>
                    <span className="badge" style={{
                      backgroundColor: student.intervention === 'Yes' ? 'rgba(235, 87, 87, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                      color: student.intervention === 'Yes' ? '#EB5757' : '#27AE60',
                      fontWeight: 700
                    }}>
                      {student.intervention === 'Yes' ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button 
                        className="action-btn"
                        style={{ 
                          display: 'inline-flex', 
                          alignItems: 'center', 
                          gap: '4px', 
                          backgroundColor: 'rgba(27, 58, 107, 0.08)',
                          color: '#1B3A6B',
                          border: '1px solid rgba(27, 58, 107, 0.2)',
                          fontWeight: 700,
                          padding: '6px 8px',
                          fontSize: '0.72rem',
                          whiteSpace: 'nowrap'
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          window.location.href = `/counsellor/student/${student.profile_id || student.id}/report`;
                        }}
                      >
                        <FileText size={11} />
                        View Report
                      </button>
                      <button 
                        className="action-btn"
                        style={{ 
                          display: 'inline-flex', 
                          alignItems: 'center', 
                          gap: '4px', 
                          backgroundColor: '#1B3A6B',
                          color: 'white',
                          border: 'none',
                          fontWeight: 700,
                          padding: '6px 8px',
                          fontSize: '0.72rem',
                          whiteSpace: 'nowrap'
                        }}
                        onClick={(e) => {
                          e.stopPropagation();
                          window.open(`/api/counsellor/student/${student.profile_id || student.id}/report/pdf`, '_blank');
                        }}
                      >
                        <Download size={11} />
                        Download PDF
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Table Footer Controls (Pagination & View All link) */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '16px 24px',
          borderTop: '1px solid #E2E8F0',
          backgroundColor: '#F8FAFC'
        }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600 }}>
              Page {currentPage} of {totalPages} (Showing {paginatedStudents.length} of 200 students)
            </span>
          </div>

          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <button 
              className="action-btn" 
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              style={{ padding: '6px 12px', opacity: currentPage === 1 ? 0.5 : 1 }}
            >
              Previous
            </button>
            <button 
              className="action-btn" 
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              style={{ padding: '6px 12px', opacity: currentPage === totalPages ? 0.5 : 1 }}
            >
              Next
            </button>
          </div>

          <div>
            <span 
              onClick={() => {
                setActiveTab("Risk Alerts");
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              style={{ 
                fontSize: '0.85rem', 
                color: '#1B3A6B', 
                fontWeight: 700, 
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}
            >
              View all 27 students &rarr;
            </span>
          </div>
        </div>
      </section>

      {/* Alerts Feed and Student Activity Lists */}
      <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        
        {/* Critical Alerts panel */}
        <div className="activity-feed-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h2>Urgent Clinical Risk Alerts</h2>
            <span style={{ fontSize: '0.75rem', color: '#1B3A6B', fontWeight: 600, cursor: 'pointer' }} onClick={() => setActiveTab("Risk Alerts")}>
              View All Alerts &rarr;
            </span>
          </div>
          <div className="feed-list">
            {alerts.filter(a => a.status !== "Closed").slice(0, 3).map(alert => (
              <div key={alert.id} className={`feed-item ${alert.riskLevel}`} style={{ cursor: 'pointer' }} onClick={() => {
                const s = mockStudents.find(st => st.id === alert.studentId);
                if (s) setSelectedStudent(s);
              }}>
                <div className="feed-avatar" style={{ backgroundColor: alert.riskLevel === 'High' ? '#EB5757' : '#F2C94C' }}>
                  {alert.studentName.split(' ').map(n=>n[0]).join('')}
                </div>
                <div className="feed-body">
                  <div className="feed-title">
                    {alert.studentName} <span className={`badge ${alert.riskLevel === 'High' ? 'badge-high' : 'badge-medium'}`} style={{ fontSize: '0.6rem', padding: '1px 5px' }}>{alert.riskLevel}</span>
                  </div>
                  <div className="feed-desc"><strong>Trigger:</strong> {alert.trigger}</div>
                  <div className="feed-desc" style={{ fontSize: '0.7rem' }}><strong>Latest:</strong> {alert.details}</div>
                  <div className="feed-time">{alert.time}</div>
                </div>
              </div>
            ))}
            {alerts.filter(a => a.status !== "Closed").length === 0 && (
              <div style={{ textAlign: 'center', color: '#94A3B8', fontSize: '0.8rem', padding: '20px' }}>No active urgent clinical alerts! All clear.</div>
            )}
          </div>
        </div>

        {/* Live Active Student List */}
        <div className="activity-feed-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h2>Students Under Watch ({students.length})</h2>
            <span style={{ fontSize: '0.75rem', color: '#1B3A6B', fontWeight: 600, cursor: 'pointer' }} onClick={() => setActiveTab("Students")}>
              Full Directory &rarr;
            </span>
          </div>
          
          <div className="feed-list">
            {students.slice(0, 4).map(student => (
              <div key={student.id} className={`feed-item`} style={{ cursor: 'pointer', borderLeft: '3px solid #1B3A6B' }} onClick={() => setSelectedStudent(student)}>
                <div className="feed-avatar">
                  {student.avatar}
                </div>
                <div className="feed-body">
                  <div className="feed-title" style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{student.name}</span>
                    <span className={`badge badge-${student.riskLevel.toLowerCase()}`} style={{ fontSize: '0.65rem', padding: '2px 6px' }}>{student.riskLevel} Risk</span>
                  </div>
                  <div className="feed-desc">Course: {student.course} ({student.cohort})</div>
                  <div className="feed-desc" style={{ fontWeight: 600 }}>Wellness Score: {student.wellnessScore}%</div>
                  <div className="feed-time">Last session: {student.lastContacted}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

/* ==========================================
   COMPONENT: StudentsPage
   ========================================== */
function StudentsPage({ setSelectedStudent, followUpStudents }) {
  const [currentPage, setCurrentPage] = useState(1);
  const [sortColumn, setSortColumn] = useState("name");
  const [sortDirection, setSortDirection] = useState("asc");

  // Reset pagination on filter change
  useEffect(() => {
    setCurrentPage(1);
  }, [followUpStudents]);

  // Sort student set
  const sortedStudents = useMemo(() => {
    const list = [...followUpStudents];
    if (!sortColumn) return list;

    list.sort((a, b) => {
      let aVal = a[sortColumn];
      let bVal = b[sortColumn];

      if (typeof aVal === 'string') aVal = aVal.toLowerCase();
      if (typeof bVal === 'string') bVal = bVal.toLowerCase();

      // Hierarchy sorting for stress / impulsivity / risk levels
      const hierarchy = { Low: 1, Moderate: 2, High: 3, Severe: 4 };
      if (["stress", "impulsivity", "risk"].includes(sortColumn)) {
        aVal = hierarchy[a[sortColumn]] || 0;
        bVal = hierarchy[b[sortColumn]] || 0;
      }

      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
    return list;
  }, [followUpStudents, sortColumn, sortDirection]);

  // Paginated student set (25 per page)
  const itemsPerPage = 25;
  const totalPages = Math.ceil(sortedStudents.length / itemsPerPage);
  
  const paginatedStudents = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return sortedStudents.slice(startIndex, startIndex + itemsPerPage);
  }, [sortedStudents, currentPage]);

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const handleViewReport = (student) => {
    const detailedStudent = {
      id: student.regId,
      profile_id: student.profile_id,
      name: student.name,
      course: student.course,
      cohort: student.cohort,
      academicYear: "2025-2026",
      riskLevel: student.stress === "Severe" || student.stress === "High" ? "High" : student.stress === "Moderate" ? "Medium" : "Low",
      wellnessScore: student.stress === "Severe" ? 28 : student.stress === "High" ? 44 : student.stress === "Moderate" ? 65 : 88,
      lastContacted: "2026-05-20",
      email: `${student.name.toLowerCase().replace(/\s+/g, '.')}@uai.edu.in`,
      phone: "+92 300 1234567",
      avatar: student.name.split(' ').map(n=>n[0]).join(''),
      gender: Math.random() > 0.5 ? "Male" : "Female",
      hosteller: Math.random() > 0.3 ? "Yes (Hostel-A)" : "No (Day Scholar)",
      attendance: `${Math.floor(55 + Math.random() * 40)}%`,
      gpa: `${(6.0 + Math.random() * 3.5).toFixed(1)}/10`,
      riskFactors: {
        psychological: `Stress Level (DASS-21) is flagged as ${student.stress}. Impulsivity (BIS-11) is ${student.impulsivity}.`,
        academic: `Attendance stands at acceptable baseline. Course engagement remains steady.`,
        social: `Struggling with exam preparation pressure and cohort adjustments.`
      },
      assessments: [
        { name: "DASS-21 Stress Level", date: "2026-05-10", score: student.stress, status: student.stress === "Severe" || student.stress === "High" ? "Critical" : "Normal" },
        { name: "BIS-11 Impulsivity", date: "2026-05-12", score: student.impulsivity, status: student.impulsivity === "High" ? "Flagged" : "Normal" },
        { name: "BRIS Risk-Taking", date: "2026-05-14", score: student.risk, status: student.risk === "High" ? "Flagged" : "Normal" }
      ],
      interventions: []
    };
    setSelectedStudent(detailedStudent);
  };

  return (
    <div className="table-card">
      {/* Total Students Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 24px', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--card-bg)' }}>
        <div>
          <h2 style={{ fontFamily: 'Outfit', fontWeight: 800, fontSize: '1.4rem', color: '#1B3A6B' }}>Total: 200 Students</h2>
          <p style={{ fontSize: '0.8rem', color: '#64748B', marginTop: '2px' }}>
            Interactive full directory of all enrolled UAI students under clinical monitoring.
          </p>
        </div>
        <span className="badge badge-high" style={{ padding: '6px 12px', fontSize: '0.8rem', fontWeight: 700 }}>
          {followUpStudents.length} Matching Records
        </span>
      </div>

      {/* Table grid */}
      <div className="table-responsive">
        <table className="custom-table">
          <thead>
            <tr>
              {[
                { label: "Student Name", key: "name" },
                { label: "Registration ID", key: "regId" },
                { label: "Course", key: "course" },
                { label: "Cohort", key: "cohort" },
                { label: "Stress (DASS-21)", key: "stress" },
                { label: "Impulsivity (BIS-11)", key: "impulsivity" },
                { label: "Risk-Taking (BRIS)", key: "risk" },
                { label: "Intervention", key: "intervention" }
              ].map(col => (
                <th key={col.key} onClick={() => handleSort(col.key)} style={{ cursor: 'pointer', userSelect: 'none' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    {col.label}
                    {sortColumn === col.key ? (sortDirection === 'asc' ? ' ▲' : ' ▼') : <span style={{ opacity: 0.3 }}> ↕</span>}
                  </div>
                </th>
              ))}
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {paginatedStudents.map(student => (
              <tr key={student.id} onClick={() => handleViewReport(student)}>
                <td>
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{student.name}</div>
                </td>
                <td>
                  <span style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600 }}>{student.regId}</span>
                </td>
                <td>{student.course}</td>
                <td>{student.cohort}</td>
                <td>
                  <span className="badge" style={{
                    backgroundColor: student.stress === 'Severe' ? '#EB5757' : student.stress === 'High' ? '#DD6B20' : student.stress === 'Moderate' ? '#F2C94C' : '#27AE60',
                    color: 'white',
                    fontWeight: 700
                  }}>
                    {student.stress}
                  </span>
                </td>
                <td>
                  <span className="badge" style={{
                    backgroundColor: student.impulsivity === 'High' ? 'rgba(221, 107, 32, 0.15)' : student.impulsivity === 'Moderate' ? 'rgba(242, 201, 76, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                    color: student.impulsivity === 'High' ? '#DD6B20' : student.impulsivity === 'Moderate' ? '#B7791F' : '#27AE60',
                    fontWeight: 700
                  }}>
                    {student.impulsivity}
                  </span>
                </td>
                <td>
                  <span className="badge" style={{
                    backgroundColor: student.risk === 'High' ? 'rgba(221, 107, 32, 0.15)' : student.risk === 'Moderate' ? 'rgba(242, 201, 76, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                    color: student.risk === 'High' ? '#DD6B20' : student.risk === 'Moderate' ? '#B7791F' : '#27AE60',
                    fontWeight: 700
                  }}>
                    {student.risk}
                  </span>
                </td>
                <td>
                  <span className="badge" style={{
                    backgroundColor: student.intervention === 'Yes' ? 'rgba(235, 87, 87, 0.15)' : 'rgba(39, 174, 96, 0.15)',
                    color: student.intervention === 'Yes' ? '#EB5757' : '#27AE60',
                    fontWeight: 700
                  }}>
                    {student.intervention}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button 
                      className="action-btn"
                      style={{ 
                        display: 'inline-flex', 
                        alignItems: 'center', 
                        gap: '4px', 
                        backgroundColor: 'rgba(27, 58, 107, 0.08)',
                        color: '#1B3A6B',
                        border: '1px solid rgba(27, 58, 107, 0.2)',
                        fontWeight: 700,
                        padding: '6px 8px',
                        fontSize: '0.72rem',
                        whiteSpace: 'nowrap'
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        window.location.href = `/counsellor/student/${student.profile_id || student.id}/report`;
                      }}
                    >
                      <FileText size={11} />
                      View Report
                    </button>
                    <button 
                      className="action-btn"
                      style={{ 
                        display: 'inline-flex', 
                        alignItems: 'center', 
                        gap: '4px', 
                        backgroundColor: '#1B3A6B',
                        color: 'white',
                        border: 'none',
                        fontWeight: 700,
                        padding: '6px 8px',
                        fontSize: '0.72rem',
                        whiteSpace: 'nowrap'
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        window.open(`/api/counsellor/student/${student.profile_id || student.id}/report/pdf`, '_blank');
                      }}
                    >
                      <Download size={11} />
                      Download PDF
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            
            {sortedStudents.length === 0 && (
              <tr>
                <td colSpan="9">
                  <div className="empty-state" style={{ padding: '40px 0', textAlign: 'center' }}>
                    <AlertCircle size={36} color="#94A3B8" style={{ marginBottom: '10px' }} />
                    <h3 style={{ fontSize: '1rem', color: '#1B3A6B' }}>No students found</h3>
                    <p style={{ fontSize: '0.8rem', color: '#64748B' }}>Modify your keyword or dropdown filters above.</p>
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--card-bg)' }}>
          <span style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600 }}>
            Showing page {currentPage} of {totalPages} ({followUpStudents.length} students total)
          </span>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="action-btn" disabled={currentPage === 1} onClick={() => setCurrentPage(prev => prev - 1)} style={{ opacity: currentPage === 1 ? 0.5 : 1 }}>
              Previous
            </button>
            <button className="action-btn" disabled={currentPage === totalPages} onClick={() => setCurrentPage(prev => prev + 1)} style={{ opacity: currentPage === totalPages ? 0.5 : 1 }}>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ==========================================
   COMPONENT: AssessmentsPage
   ========================================== */
function AssessmentsPage({ triggerToast, students }) {
  const [selectedAsm, setSelectedAsm] = useState(null);
  const [assignStudentId, setAssignStudentId] = useState("");

  const handleAssign = (e) => {
    e.preventDefault();
    if (!assignStudentId) return;
    const std = followUpStudentsList.find(s => String(s.id) === String(assignStudentId));
    if (!std) return;
    triggerToast(`Sent "${selectedAsm.title}" successfully to student ${std.name}! Notified via portal.`);
    setSelectedAsm(null);
    setAssignStudentId("");
  };

  const assessmentsList = [
    {
      name: "DASS-21 (Stress/Anxiety/Depression)",
      totalAssessed: 126,
      averageScore: "1.62/3.0 (Moderate)",
      completionRate: "88%",
      color: "#1B3A6B",
      desc: "validated 21-item clinical scale measuring core symptoms of negative emotional states."
    },
    {
      name: "BIS-11 (Impulsivity Scale)",
      totalAssessed: 126,
      averageScore: "2.11/3.0 (High)",
      completionRate: "91%",
      color: "#27AE60",
      desc: "Standard 30-item clinical framework evaluating motor, cognitive, and non-planning impulsiveness."
    },
    {
      name: "BRIS (Risk-Taking & Aggression)",
      totalAssessed: 126,
      averageScore: "1.78/3.0 (Moderate)",
      completionRate: "76%",
      color: "#DD6B20",
      desc: "Behavioral Risk Index measuring thrill-seeking, safety negligence, and verbal hostility tendencies."
    }
  ];

  // Domain score Recharts data
  const chartData = [
    { domain: "Stress", "DASS-21": 1.85 },
    { domain: "Anxiety", "DASS-21": 1.39 },
    { domain: "Depression", "DASS-21": 1.10 },
    { domain: "Cognitive Imp.", "BIS-11": 2.11 },
    { domain: "Motor Imp.", "BIS-11": 2.32 },
    { domain: "Non-Planning", "BIS-11": 1.90 },
    { domain: "Risk-Taking", "BRIS": 1.78 },
    { domain: "Aggression", "BRIS": 1.46 }
  ];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Psychological Assessments Hub</h2>
        <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Deploy and review standard screening assessments for UAI students.</p>
      </div>

      {/* 3 Cards */}
      <div className="assessment-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        {assessmentsList.map((asm, idx) => (
          <div key={idx} className="asm-card" style={{ borderTop: `4px solid ${asm.color}`, padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '230px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className="badge badge-pill-light" style={{ fontSize: '0.65rem' }}>Active Term</span>
                <span className="badge badge-low" style={{ fontSize: '0.65rem', backgroundColor: 'rgba(39, 174, 96, 0.12)', color: '#27AE60' }}>{asm.completionRate} Complete</span>
              </div>
              <h3 className="asm-title" style={{ fontFamily: 'Outfit', fontWeight: 700, fontSize: '1.05rem', color: '#1B3A6B' }}>{asm.name}</h3>
              <p className="asm-desc" style={{ fontSize: '0.75rem', color: '#64748B', lineHeight: 1.3, margin: '6px 0 12px 0' }}>{asm.desc}</p>
            </div>

            <div>
              <div className="asm-meta-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '14px', borderTop: '1px solid #F1F5F9', paddingTop: '8px' }}>
                <div className="asm-meta-item" style={{ fontSize: '0.65rem', display: 'flex', flexDirection: 'column' }}>
                  Total Assessed
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-primary)' }}>{asm.totalAssessed} Students</span>
                </div>
                <div className="asm-meta-item" style={{ fontSize: '0.65rem', display: 'flex', flexDirection: 'column' }}>
                  Average Score
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: asm.color }}>{asm.averageScore}</span>
                </div>
              </div>

              <button
                className="submit-btn"
                style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '0.8rem', padding: '8px' }}
                onClick={() => setSelectedAsm({ id: `asm-${idx}`, title: asm.name })}
              >
                <Send size={12} />
                Deploy Assessment
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Bar chart showing assessment scores by domain */}
      <div className="chart-card" style={{ marginBottom: '24px' }}>
        <div className="chart-header">
          <h2>Clinical Domains Score Analysis (Average Index)</h2>
        </div>
        <div className="chart-area" style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 20, left: -25, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
              <XAxis dataKey="domain" tick={{ fontSize: 9, fill: '#64748B', fontWeight: 600 }} stroke="var(--border-color)" />
              <YAxis domain={[0, 3]} ticks={[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]} tick={{ fontSize: 9, fill: '#64748B' }} stroke="var(--border-color)" />
              <Tooltip formatter={(value) => [value, "Score"]} contentStyle={{ backgroundColor: 'var(--card-bg)', color: 'var(--text-primary)', border: '1px solid var(--border-color)', borderRadius: '6px' }} />
              <Legend iconSize={8} iconType="circle" wrapperStyle={{ fontSize: '10px' }} />
              <Bar dataKey="DASS-21" fill="#1B3A6B" radius={[2, 2, 0, 0]} barSize={25} />
              <Bar dataKey="BIS-11" fill="#27AE60" radius={[2, 2, 0, 0]} barSize={25} />
              <Bar dataKey="BRIS" fill="#DD6B20" radius={[2, 2, 0, 0]} barSize={25} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div style={{ fontSize: '0.7rem', color: '#64748B', fontWeight: 500, textAlign: 'center', marginTop: '10px' }}>
          Clinical score representation: 0 (No Symtomatology) - 3 (Severe Clinical Concern)
        </div>
      </div>

      {/* Modal overlay to assign assessment */}
      {selectedAsm && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '460px' }}>
            <div className="modal-header">
              <h2>Deploy Clinical Assessment</h2>
              <button className="modal-close-btn" onClick={() => setSelectedAsm(null)}>
                <X size={18} />
              </button>
            </div>
            <div className="modal-scroll-area">
              <p style={{ fontSize: '0.8rem', color: '#64748B', marginBottom: '16px' }}>
                Select a student below to send the <strong>{selectedAsm.title}</strong> directly to their UAI portal.
              </p>
              
              <form className="logger-form" onSubmit={handleAssign}>
                <div className="form-group">
                  <label>Target Student</label>
                  <select
                    className="form-control"
                    required
                    value={assignStudentId}
                    onChange={(e) => setAssignStudentId(e.target.value)}
                  >
                    <option value="">-- Choose Student --</option>
                    {followUpStudentsList.map(s => (
                      <option key={s.id} value={s.id}>{s.name} ({s.regId})</option>
                    ))}
                  </select>
                </div>
                <div style={{ display: 'flex', gap: '10px', marginTop: '14px' }}>
                  <button type="button" className="action-btn" style={{ flexGrow: 1 }} onClick={() => setSelectedAsm(null)}>Cancel</button>
                  <button type="submit" className="submit-btn" style={{ flexGrow: 1 }}>Confirm & Send</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ==========================================
   COMPONENT: RiskAlertsPage
   ========================================== */
function RiskAlertsPage({ alerts, onUpdateStatus, setSelectedStudent, students }) {
  const [filterSeverity, setFilterSeverity] = useState("All");

  const filteredAlerts = useMemo(() => {
    if (filterSeverity === "All") return alerts;
    return alerts.filter(a => a.severity === filterSeverity);
  }, [alerts, filterSeverity]);

  const activeAlertsCount = useMemo(() => {
    return alerts.filter(a => a.status === "Active").length;
  }, [alerts]);

  const handleViewClinicalCard = (alert) => {
    const matched = followUpStudentsList.find(s => s.id === alert.studentId);
    if (!matched) return;
    const detailedStudent = {
      id: matched.regId,
      name: matched.name,
      course: matched.course,
      cohort: matched.cohort,
      academicYear: "2025-2026",
      riskLevel: matched.stress === "Severe" || matched.stress === "High" ? "High" : matched.stress === "Moderate" ? "Medium" : "Low",
      wellnessScore: matched.stress === "Severe" ? 28 : matched.stress === "High" ? 44 : matched.stress === "Moderate" ? 65 : 88,
      lastContacted: "2026-05-20",
      email: `${matched.name.toLowerCase().replace(/\s+/g, '.')}@uai.edu.in`,
      phone: "+92 300 1234567",
      avatar: matched.name.split(' ').map(n=>n[0]).join(''),
      gender: Math.random() > 0.5 ? "Male" : "Female",
      hosteller: Math.random() > 0.3 ? "Yes (Hostel-A)" : "No (Day Scholar)",
      attendance: `${Math.floor(55 + Math.random() * 40)}%`,
      gpa: `${(6.0 + Math.random() * 3.5).toFixed(1)}/10`,
      riskFactors: {
        psychological: `Stress Level (DASS-21) is flagged as ${matched.stress}. Impulsivity (BIS-11) is ${matched.impulsivity}.`,
        academic: `Attendance stands at acceptable baseline. Course engagement remains steady.`,
        social: `Struggling with exam preparation pressure and cohort adjustments.`
      },
      assessments: [
        { name: "DASS-21 Stress Level", date: "2026-05-10", score: matched.stress, status: matched.stress === "Severe" || matched.stress === "High" ? "Critical" : "Normal" },
        { name: "BIS-11 Impulsivity", date: "2026-05-12", score: matched.impulsivity, status: matched.impulsivity === "High" ? "Flagged" : "Normal" },
        { name: "BRIS Risk-Taking", date: "2026-05-14", score: matched.risk, status: matched.risk === "High" ? "Flagged" : "Normal" }
      ],
      interventions: []
    };
    setSelectedStudent(detailedStudent);
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '10px' }}>
        <div>
          <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Real-time Risk Alerts</h2>
          <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Critical mental health or academic alerts generated by assessment thresholds or attendance logs.</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge badge-high" style={{ padding: '6px 12px', fontWeight: 700, fontSize: '0.75rem' }}>
            {activeAlertsCount} Unreviewed Alerts
          </span>
        </div>
      </div>

      {/* Severity Filter tabs */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
        {["All", "Severe", "High", "Moderate"].map(sev => (
          <button
            key={sev}
            onClick={() => setFilterSeverity(sev)}
            className={`action-btn ${filterSeverity === sev ? 'active' : ''}`}
            style={{
              padding: '6px 14px',
              fontSize: '0.8rem',
              fontWeight: 700,
              backgroundColor: filterSeverity === sev ? '#1B3A6B' : 'var(--card-bg)',
              color: filterSeverity === sev ? 'white' : 'var(--text-primary)',
              borderColor: filterSeverity === sev ? '#1B3A6B' : 'var(--border-color)'
            }}
          >
            {sev} Severity
          </button>
        ))}
      </div>

      <div className="alerts-list-wrapper" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {filteredAlerts.map(alert => (
          <div 
            key={alert.id} 
            className={`alert-item-card ${alert.severity === 'Severe' ? 'Severe' : alert.severity === 'High' ? 'High' : 'Medium'}`}
            style={{
              borderLeft: `4px solid ${alert.severity === 'Severe' ? '#EB5757' : alert.severity === 'High' ? '#DD6B20' : '#F2C94C'}`,
              opacity: alert.status === "Closed" ? 0.6 : 1,
              transition: 'opacity 0.2s'
            }}
          >
            <div className="alert-main-info" style={{ flexGrow: 1 }}>
              <div className="alert-student-header" style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '8px', marginBottom: '6px' }}>
                <span className="alert-student-name" style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{alert.studentName}</span>
                <span style={{ fontSize: '0.75rem', color: '#64748B' }}>({alert.regId}) • {alert.course} • {alert.cohort}</span>
                <span className="badge" style={{
                  backgroundColor: alert.severity === 'Severe' ? '#EB5757' : alert.severity === 'High' ? '#DD6B20' : '#F2C94C',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '0.65rem'
                }}>
                  {alert.trigger}
                </span>
              </div>
              <p className="alert-details-text" style={{ fontSize: '0.8rem', color: 'var(--text-primary)', lineHeight: 1.4, margin: '6px 0' }}>{alert.details}</p>
              <div className="alert-action-summary" style={{ fontSize: '0.75rem', color: '#64748B', display: 'flex', alignItems: 'center', gap: '5px', marginTop: '10px' }}>
                <Clock size={12} />
                <strong>Status:</strong> 
                <span style={{
                  fontWeight: 700,
                  color: alert.status === "Active" ? "#EB5757" : "#27AE60"
                }}>
                  {alert.status === "Active" ? "Active Care Trigger" : "Reviewed & Acknowledged"}
                </span>
                {alert.actionTaken && <span style={{ fontStyle: 'italic' }}>({alert.actionTaken})</span>}
              </div>
            </div>

            <div className="alert-side-controls" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', justifyContent: 'space-between', minWidth: '150px' }}>
              <span className="alert-time-stamp" style={{ fontSize: '0.7rem', color: '#94A3B8', fontWeight: 600, marginBottom: '10px' }}>{alert.time}</span>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="action-btn" onClick={() => handleViewClinicalCard(alert)} style={{ fontSize: '0.75rem', padding: '6px 10px' }}>
                  Clinical Card
                </button>
                {alert.status === "Active" && (
                  <button 
                    className="submit-btn" 
                    style={{ backgroundColor: '#1B3A6B', padding: '6px 10px', fontSize: '0.75rem', border: 'none' }}
                    onClick={() => onUpdateStatus(alert.id, "Closed")}
                  >
                    Mark as Reviewed
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}

        {filteredAlerts.length === 0 && (
          <div className="empty-state" style={{ textAlign: 'center', padding: '40px 0' }}>
            <CheckCircle size={40} color="#27AE60" style={{ marginBottom: '10px' }} />
            <h3 style={{ fontSize: '1rem', color: '#1B3A6B' }}>No active alerts in this category</h3>
            <p style={{ fontSize: '0.8rem', color: '#64748B' }}>All alerts of this severity have been processed.</p>
          </div>
        )}
      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: InsightsPage
   ========================================== */
function InsightsPage({ triggerToast }) {
  // Line charts datasets
  const timelineData = [
    { name: "Dec '24", stress: 1.62, impulsivity: 2.25, risk: 1.95, success: 78 },
    { name: "Jan '25", stress: 1.65, impulsivity: 2.22, risk: 1.90, success: 80 },
    { name: "Feb '25", stress: 1.58, impulsivity: 2.30, risk: 1.85, success: 82 },
    { name: "Mar '25", stress: 1.74, impulsivity: 2.18, risk: 1.82, success: 85 },
    { name: "Apr '25", stress: 1.82, impulsivity: 2.20, risk: 1.80, success: 89 },
    { name: "May '25", stress: 1.85, impulsivity: 2.11, risk: 1.78, success: 91 }
  ];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>AI & Statistical Well-being Insights</h2>
        <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Cross-data correlations, predictive risk indicators, and batch intervention guidance.</p>
      </div>

      {/* Summary Row */}
      <div className="stat-cards-container" style={{ marginBottom: '24px' }}>
        {[
          { title: "Average Stress Level", value: "1.85 / 3.0", trend: "+1.6% increase", color: "#EB5757", bg: "rgba(235, 87, 87, 0.08)" },
          { title: "Impulsivity Score", value: "2.11 / 3.0", trend: "-4.1% decrease", color: "#27AE60", bg: "rgba(39, 174, 96, 0.08)" },
          { title: "Behavioral Risks", value: "1.78 / 3.0", trend: "-1.1% decrease", color: "#27AE60", bg: "rgba(39, 174, 96, 0.08)" },
          { title: "Intervention Success", value: "91.0%", trend: "+2.2% increase", color: "#1B3A6B", bg: "rgba(27, 58, 107, 0.08)" }
        ].map((item, idx) => (
          <div key={idx} className="dashboard-stat-card" style={{ display: 'flex', flexDirection: 'column', gap: '4px', alignItems: 'flex-start', padding: '16px 20px' }}>
            <span style={{ fontSize: '0.75rem', color: '#64748B', fontWeight: 600 }}>{item.title}</span>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)', margin: '4px 0' }}>{item.value}</div>
            <span className="badge" style={{ backgroundColor: item.bg, color: item.color, fontWeight: 700, fontSize: '0.65rem' }}>{item.trend} vs last month</span>
          </div>
        ))}
      </div>

      {/* 4 Line Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '24px' }}>
        
        {/* Stress Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Average Stress Index Over Time (DASS-21)</h2>
          </div>
          <div className="chart-area" style={{ height: '200px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData} margin={{ top: 10, right: 10, left: -30, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748B', fontWeight: 600 }} stroke="var(--border-color)" />
                <YAxis domain={[1.0, 2.0]} tick={{ fontSize: 9, fill: '#64748B' }} stroke="var(--border-color)" />
                <Tooltip />
                <Line type="monotone" dataKey="stress" stroke="#EB5757" strokeWidth={2.5} dot={{ r: 4, fill: '#EB5757' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Impulsivity Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Average Impulsivity Trend (BIS-11)</h2>
          </div>
          <div className="chart-area" style={{ height: '200px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData} margin={{ top: 10, right: 10, left: -30, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748B', fontWeight: 600 }} stroke="var(--border-color)" />
                <YAxis domain={[2.0, 2.5]} tick={{ fontSize: 9, fill: '#64748B' }} stroke="var(--border-color)" />
                <Tooltip />
                <Line type="monotone" dataKey="impulsivity" stroke="#27AE60" strokeWidth={2.5} dot={{ r: 4, fill: '#27AE60' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk-Taking Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Behavioral Risk-Taking Indices (BRIS)</h2>
          </div>
          <div className="chart-area" style={{ height: '200px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData} margin={{ top: 10, right: 10, left: -30, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748B', fontWeight: 600 }} stroke="var(--border-color)" />
                <YAxis domain={[1.5, 2.1]} tick={{ fontSize: 9, fill: '#64748B' }} stroke="var(--border-color)" />
                <Tooltip />
                <Line type="monotone" dataKey="risk" stroke="#DD6B20" strokeWidth={2.5} dot={{ r: 4, fill: '#DD6B20' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Intervention Success Rate Chart */}
        <div className="chart-card">
          <div className="chart-header">
            <h2>Counselling Mitigation Success Rate (%)</h2>
          </div>
          <div className="chart-area" style={{ height: '200px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timelineData} margin={{ top: 10, right: 10, left: -30, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748B', fontWeight: 600 }} stroke="var(--border-color)" />
                <YAxis domain={[70, 100]} tick={{ fontSize: 9, fill: '#64748B' }} stroke="var(--border-color)" />
                <Tooltip formatter={(value) => [`${value}%`, 'Mitigation Rate']} />
                <Line type="monotone" dataKey="success" stroke="#1B3A6B" strokeWidth={2.5} dot={{ r: 4, fill: '#1B3A6B' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: InterventionsPage
   ========================================== */
function InterventionsPage({ interventions, students, onAddIntervention }) {
  const [selectStudent, setSelectStudent] = useState("");
  const [intType, setIntType] = useState("1-on-1 Counselling");
  const [intNotes, setIntNotes] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectStudent || !intNotes) return;
    onAddIntervention(parseInt(selectStudent), intType, intNotes);
    
    // reset form
    setSelectStudent("");
    setIntNotes("");
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Student Interventions Manager</h2>
        <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Add care notes, schedule psychiatry recommendations, or monitor assigned peer mentor milestones.</p>
      </div>

      <div className="intervention-layout" style={{ display: 'grid', gridTemplateColumns: '1fr 1.3fr', gap: '24px', alignItems: 'start' }}>
        {/* Logger Form */}
        <div className="logger-panel" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
          <h2>Log Student Support Activity</h2>
          <form className="logger-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Select Student</label>
              <select
                className="form-control"
                required
                value={selectStudent}
                onChange={(e) => setSelectStudent(e.target.value)}
              >
                <option value="">-- Choose Student --</option>
                {followUpStudentsList.map(s => (
                  <option key={s.id} value={s.id}>{s.name} ({s.regId}) - {s.stress} Stress</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Intervention Type</label>
              <select
                className="form-control"
                value={intType}
                onChange={(e) => setIntType(e.target.value)}
              >
                <option value="1-on-1 Counselling">1-on-1 Counselling Session</option>
                <option value="Group Therapy Session">Group Therapy Session</option>
                <option value="Peer Mentor Assign">Peer Mentor Assignment</option>
                <option value="Clinical Referral">Psychiatry/Clinical Referral</option>
                <option value="Parental Counseling Session">Parental Call/Counseling</option>
              </select>
            </div>

            <div className="form-group">
              <label>Clinical Notes</label>
              <textarea
                className="form-control form-textarea"
                placeholder="Document notes regarding student's mood, attendance reason, academic coping strategies, etc..."
                required
                value={intNotes}
                onChange={(e) => setIntNotes(e.target.value)}
                style={{ height: '110px' }}
              />
            </div>

            <button type="submit" className="submit-btn" style={{ marginTop: '6px', width: '100%' }}>
              Log Support Session
            </button>
          </form>
        </div>

        {/* Flat interventions timeline */}
        <div className="activity-feed-card" style={{ display: 'flex', flexDirection: 'column', backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)', margin: 0 }}>
          <h2 style={{ marginBottom: '16px' }}>Active Case Support Listing ({interventions.length})</h2>
          
          <div className="table-responsive" style={{ maxHeight: '420px', overflowY: 'auto' }}>
            <table className="custom-table" style={{ fontSize: '0.75rem' }}>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Status</th>
                  <th>Counsellor</th>
                  <th>Next Session</th>
                </tr>
              </thead>
              <tbody>
                {interventions.map((item, idx) => (
                  <tr key={idx}>
                    <td>
                      <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{item.studentName}</div>
                      <div style={{ fontSize: '0.65rem', color: '#64748B' }}>{item.course}</div>
                    </td>
                    <td>
                      <span className="badge" style={{
                        backgroundColor: item.status === 'Completed' ? 'rgba(39, 174, 96, 0.15)' : item.status === 'In Progress' ? 'rgba(27, 58, 107, 0.15)' : 'rgba(242, 201, 76, 0.15)',
                        color: item.status === 'Completed' ? '#27AE60' : item.status === 'In Progress' ? '#1B3A6B' : '#B7791F',
                        fontWeight: 700,
                        fontSize: '0.65rem'
                      }}>
                        {item.status}
                      </span>
                    </td>
                    <td>{item.counsellor}</td>
                    <td>
                      <span style={{ fontWeight: 600, color: item.nextSessionDate === "N/A" ? "#94A3B8" : "var(--text-primary)" }}>
                        {item.nextSessionDate}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: ReportsPage
   ========================================== */
function ReportsPage({ students, course, cohort }) {
  const [loadingCard, setLoadingCard] = useState(null);

  const handleAction = (reportTitle, type) => {
    setLoadingCard(reportTitle + "-" + type);
    setTimeout(() => {
      setLoadingCard(null);
      alert(`${type === 'gen' ? 'Generated' : 'Downloaded'} successfully: ${reportTitle}!`);
    }, 1000);
  };

  const reportCards = [
    {
      title: "Monthly Summary Report",
      desc: "Aggregated review of student wellness indexes, alerts resolved, and counselling sessions completed during the month."
    },
    {
      title: "Cohort Comparison Report",
      desc: "Cross-analytical comparison of cognitive anxiety, impulsivity indicators, and academic risk across academic batches."
    },
    {
      title: "Individual Student Report",
      desc: "Compile all confidential counseling diaries, assessments history, and clinical referrals for a single student portfolio."
    },
    {
      title: "Risk Analysis Report",
      desc: "AI-driven hotspot analysis identifying key concerns across day scholars, hostellers, gender, and course structures."
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Executive Counseling Report Hub</h2>
        <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Generate and compile comprehensive academic and psychiatric well-being report documents.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        {reportCards.map((report, idx) => (
          <div key={idx} className="chart-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: '200px', backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)', margin: 0 }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className="badge badge-pill-light" style={{ fontSize: '0.65rem' }}>PDF / CSV</span>
                <span style={{ fontSize: '0.7rem', color: '#27AE60', fontWeight: 600 }}>Ready</span>
              </div>
              <h3 style={{ fontFamily: 'Outfit', fontSize: '1.05rem', fontWeight: 700, color: '#1B3A6B' }}>{report.title}</h3>
              <p style={{ fontSize: '0.78rem', color: '#64748B', lineHeight: 1.4, margin: '8px 0 16px 0' }}>{report.desc}</p>
            </div>

            <div style={{ display: 'flex', gap: '8px' }}>
              <button 
                className="submit-btn" 
                style={{ flexGrow: 1, padding: '8px 10px', fontSize: '0.75rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                onClick={() => handleAction(report.title, 'gen')}
                disabled={loadingCard !== null}
              >
                {loadingCard === report.title + "-gen" ? "Generating..." : "Generate Report"}
              </button>
              <button 
                className="action-btn" 
                style={{ flexGrow: 1, padding: '8px 10px', fontSize: '0.75rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}
                onClick={() => handleAction(report.title, 'dl')}
                disabled={loadingCard !== null}
              >
                {loadingCard === report.title + "-dl" ? "Downloading..." : "Download PDF"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: ResourcesPage
   ========================================== */
function ResourcesPage({ triggerToast }) {
  const resourcesList = [
    {
      title: "Assessment Guidelines",
      desc: "Standard operating protocols for administering GAD-7, PHQ-9, and sleep metrics.",
      category: "Guidelines"
    },
    {
      title: "Crisis Protocol",
      desc: "Emergency step-by-step diagnostic workflow for self-harm or high behavioral risks.",
      category: "Emergency"
    },
    {
      title: "Counselling Handbook",
      desc: "Modern evidence-based CBT and cognitive restructuring therapies manual.",
      category: "Clinical"
    },
    {
      title: "CBT Worksheets",
      desc: "Print-ready activity logs, gratitude lists, and thought logs to share with students.",
      category: "Activity"
    },
    {
      title: "Self-Help Guides",
      desc: "Audio/slides on box breathing, sleep hygiene protocols, and exam-resilience guidelines.",
      category: "Student Guides"
    },
    {
      title: "Hostel Adaptation Materials",
      desc: "Guidance files to help out-of-state hostellers transition into residential campus life.",
      category: "Adjustment"
    }
  ];

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Counselling Resource Library</h2>
        <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Printable CBT worksheets, panic guides, and emergency hotlines to share with students.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        {resourcesList.map((res, idx) => (
          <div 
            key={idx} 
            className="chart-card" 
            style={{ 
              padding: '20px', 
              display: 'flex', 
              flexDirection: 'column', 
              justifyContent: 'space-between', 
              minHeight: '190px', 
              backgroundColor: 'var(--card-bg)', 
              border: '1px solid var(--border-color)', 
              borderTop: `4px solid ${res.category === 'Emergency' ? '#EB5757' : '#1B3A6B'}`,
              margin: 0 
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className="badge badge-pill-light" style={{ fontSize: '0.65rem' }}>{res.category}</span>
                <span style={{ fontSize: '0.7rem', color: '#64748B' }}>PDF File</span>
              </div>
              <h3 style={{ fontFamily: 'Outfit', fontSize: '1.05rem', fontWeight: 700, color: '#1B3A6B' }}>{res.title}</h3>
              <p style={{ fontSize: '0.78rem', color: '#64748B', lineHeight: 1.4, margin: '6px 0 14px 0' }}>{res.desc}</p>
            </div>

            <button 
              className="action-btn" 
              style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', fontSize: '0.75rem', padding: '8px' }}
              onClick={() => triggerToast(`Opening resource file: "${res.title}"...`)}
            >
              <ExternalLink size={12} />
              View Resource Document
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: SettingsPage
   ========================================== */
function SettingsPage({ settings, setSettings, triggerToast, isDarkMode, setIsDarkMode }) {
  // Dr Sarah Ahmed profile editing state
  const [profileName, setProfileName] = useState("Dr. Sarah Ahmed");
  const [profileRole, setProfileRole] = useState("Lead Student Counsellor");
  const [profileDept, setProfileDept] = useState("Counselling Services • UAi");

  const handleToggleEmail = () => {
    setSettings(prev => ({ ...prev, enableEmailAlerts: !prev.enableEmailAlerts }));
    triggerToast("Email alert triggers updated!");
  };

  const handleSliderChange = (e) => {
    const val = parseInt(e.target.value);
    setSettings(prev => ({ ...prev, highRiskThreshold: val }));
  };

  const handleSaveProfile = (e) => {
    e.preventDefault();
    triggerToast("Counsellor Profile information updated successfully!");
  };

  return (
    <div className="settings-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
      
      {/* 1. Profile Section */}
      <div className="settings-card" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
        <h2>Counsellor Profile Configuration</h2>
        
        <form onSubmit={handleSaveProfile} className="logger-form" style={{ marginTop: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
            <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#1B3A6B', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', fontWeight: 800 }}>
              SA
            </div>
            <div>
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>{profileName}</h3>
              <p style={{ fontSize: '0.75rem', color: '#64748B' }}>Primary Account Holder</p>
            </div>
          </div>

          <div className="form-group">
            <label>Name</label>
            <input 
              type="text" 
              className="form-control" 
              value={profileName} 
              onChange={(e) => setProfileName(e.target.value)} 
            />
          </div>

          <div className="form-group">
            <label>Role</label>
            <input 
              type="text" 
              className="form-control" 
              value={profileRole} 
              onChange={(e) => setProfileRole(e.target.value)} 
            />
          </div>

          <div className="form-group">
            <label>Department</label>
            <input 
              type="text" 
              className="form-control" 
              value={profileDept} 
              onChange={(e) => setProfileDept(e.target.value)} 
            />
          </div>

          <button type="submit" className="submit-btn" style={{ width: '100%' }}>
            Save Profile Settings
          </button>
        </form>
      </div>

      {/* 2. Theme Toggle & Alerts configuration */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
        {/* Theme Settings Card */}
        <div className="settings-card" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
          <h2>Dashboard Display Settings</h2>
          
          <div className="toggle-group" style={{ marginTop: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0' }}>
            <div className="toggle-info">
              <span className="toggle-label" style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-primary)' }}>Dark Mode Appearance</span>
              <span className="toggle-sub" style={{ fontSize: '0.75rem', color: '#64748B', display: 'block', marginTop: '2px' }}>Convert dashboard to rich premium dark color palette.</span>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={isDarkMode}
                onChange={() => {
                  setIsDarkMode(!isDarkMode);
                  triggerToast(`Switched theme to ${!isDarkMode ? 'Dark Mode' : 'Light Mode'}!`);
                }}
              />
              <span className="slider"></span>
            </label>
          </div>
        </div>

        {/* Clinical Thresholds */}
        <div className="settings-card" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
          <h2>Clinical Alerts Cut-off Tuning</h2>
          
          <div className="range-slider-group" style={{ marginTop: '10px' }}>
            <div className="range-slider-labels">
              <span>High Risk Triage Score (PHQ/GAD)</span>
              <span style={{ color: '#EB5757', fontWeight: 700 }}>&gt;={settings.highRiskThreshold}</span>
            </div>
            <input
              type="range"
              min="10"
              max="20"
              className="slider-input"
              value={settings.highRiskThreshold}
              onChange={handleSliderChange}
              onMouseUp={() => triggerToast(`High risk cutoff score tuned to ${settings.highRiskThreshold}`)}
            />
            <p style={{ fontSize: '0.65rem', color: '#94A3B8', marginTop: '4px' }}>
              Scores at or above this threshold on GAD-7 or PHQ-9 will immediately trigger severe warnings.
            </p>
          </div>

          <div className="range-slider-group" style={{ marginTop: '16px' }}>
            <div className="range-slider-labels">
              <span>Attendance Warning Limit</span>
              <span style={{ color: '#DD6B20', fontWeight: 700 }}>&lt;={settings.attendanceAlertThreshold}%</span>
            </div>
            <input
              type="range"
              min="60"
              max="85"
              className="slider-input"
              value={settings.attendanceAlertThreshold}
              onChange={(e) => setSettings(prev => ({ ...prev, attendanceAlertThreshold: parseInt(e.target.value) }))}
              onMouseUp={() => triggerToast(`Attendance alert limit configured at ${settings.attendanceAlertThreshold}%`)}
            />
            <p style={{ fontSize: '0.65rem', color: '#94A3B8', marginTop: '4px' }}>
              Triggers alerts if class attendance falls below this threshold within 30 days.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ==========================================
   COMPONENT: HelpPage (FAQ Accordion)
   ========================================== */
function HelpPage() {
  const faqs = [
    {
      q: "How does the UAI Insights Dashboard calculate the student well-being index?",
      a: "The dashboard aggregates objective factors (lecture attendance trends, grade spikes, or drops) alongside subjective clinical indicators (validated clinical tests like GAD-7 for anxiety and PHQ-9 for depression) to calculate a normalized percentage-based Wellness score for each student."
    },
    {
      q: "Who is notified when a High-Risk alert triggers?",
      a: "Depending on your settings, an automatic encrypted clinical notification is sent directly to Dr. Sarah Ahmed's UAI dashboard and secure mail. If SMS escalation is active, an emergency SMS token is pushed to the chief counselor's registered emergency line."
    },
    {
      q: "Can I customize the clinical survey tools or add custom questions?",
      a: "Yes! By navigating to the 'Assessments' page and using the Advanced Creator option, you can customize existing metrics or construct in-house adjustment scales tailored to campus hostellers or department curriculums."
    },
    {
      q: "Are clinical reports HIPAA / FERPA compliant?",
      a: "Absolutely. Student mental health reports are encrypted at rest and in transit. Only authorized clinical counselors logged in through official campus credentials can access student psychological portfolios and clinical histories."
    },
    {
      q: "What is the emergency hotline protocol for immediate crises?",
      a: "In the event of active suicidal ideation, self-harm gestures, or severe psychological breakdown, counsellors are prompted to follow the Red-Borders emergency protocol: contact UAi Student Helpline Ext 4400, trigger emergency medical services, and page the on-campus consulting psychiatrist."
    }
  ];

  const [openIdx, setOpenIdx] = useState(null);
  const [supportName, setSupportName] = useState("");
  const [supportEmail, setSupportEmail] = useState("");
  const [supportMsg, setSupportMsg] = useState("");

  const toggleFaq = (idx) => {
    setOpenIdx(openIdx === idx ? null : idx);
  };

  const handleSupportSubmit = (e) => {
    e.preventDefault();
    alert(`Support request submitted successfully! Ticket logged for ${supportName}.`);
    setSupportName("");
    setSupportEmail("");
    setSupportMsg("");
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* emergency Contacts Header red card */}
      <div className="chart-card" style={{ border: '2px solid #EB5757', backgroundColor: 'rgba(235, 87, 87, 0.05)', padding: '20px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '16px', margin: 0 }}>
        <div style={{ backgroundColor: '#EB5757', color: 'white', width: '45px', height: '45px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <PhoneCall size={20} />
        </div>
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#EB5757', fontFamily: 'Outfit' }}>EMERGENCY CLINICAL PROTOCOL RED HELPLINE</h3>
          <p style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '2px', lineHeight: 1.3 }}>
            Immediate 24/7 on-campus crisis lines: <strong>UAi Wellness Helpline Ext: 4400</strong> | Government Mental Health Helpline: <strong>14416 (Tele-MANAS)</strong> | Vandrevala Foundation: <strong>+91 9999 666 555</strong>
          </p>
        </div>
      </div>

      <div>
        <div style={{ marginBottom: '20px' }}>
          <h2 style={{ fontFamily: 'Outfit', fontSize: '1.5rem', fontWeight: 700, color: '#1B3A6B' }}>Help Centre & FAQs</h2>
          <p style={{ fontSize: '0.85rem', color: '#64748B' }}>Find clinical tutorials, explore dashboard parameters, or review student support logs compliance.</p>
        </div>

        <div className="help-faq-list" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {faqs.map((faq, idx) => (
            <div key={idx} className="faq-item" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
              <div 
                className="faq-question" 
                onClick={() => toggleFaq(idx)} 
                style={{ padding: '16px 20px', cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-primary)' }}
              >
                <span>{faq.q}</span>
                <ChevronDown size={16} style={{
                  transform: openIdx === idx ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.2s',
                  color: '#64748B'
                }} />
              </div>
              {openIdx === idx && (
                <div className="faq-answer" style={{ padding: '0 20px 16px 20px', fontSize: '0.8rem', color: '#64748B', lineHeight: 1.5, borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
                  <p>{faq.a}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Support ticket creation form */}
      <div className="settings-card" style={{ backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
        <h2 style={{ marginBottom: '14px' }}>Create Secure IT/Clinical Support Ticket</h2>
        <form onSubmit={handleSupportSubmit} className="logger-form" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div className="form-group" style={{ gridColumn: 'span 1' }}>
            <label>Full Name</label>
            <input 
              type="text" 
              className="form-control" 
              required 
              value={supportName} 
              onChange={(e) => setSupportName(e.target.value)} 
            />
          </div>
          <div className="form-group" style={{ gridColumn: 'span 1' }}>
            <label>Campus Email</label>
            <input 
              type="email" 
              className="form-control" 
              required 
              value={supportEmail} 
              onChange={(e) => setSupportEmail(e.target.value)} 
            />
          </div>
          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label>Support Query / Message</label>
            <textarea 
              className="form-control form-textarea" 
              required 
              value={supportMsg} 
              onChange={(e) => setSupportMsg(e.target.value)} 
              placeholder="Describe dashboard syncing issues, clinical assessment glitches, or database bugs..."
              style={{ height: '90px' }}
            />
          </div>
          <button type="submit" className="submit-btn" style={{ gridColumn: 'span 2', padding: '10px' }}>
            Submit Support Request
          </button>
        </form>
      </div>

    </div>
  );
}

/* ==========================================
   COMPONENT: InstitutionPage (Directory Page)
   ========================================== */
function InstitutionPage() {
  const [facultySearch, setFacultySearch] = useState("");
  const [deptFilter, setDeptFilter] = useState("All");

  const filteredFaculty = useMemo(() => {
    return mockInstitutionalInfo.faculty.filter(f => {
      const matchesSearch = f.name.toLowerCase().includes(facultySearch.toLowerCase()) || 
                            f.role.toLowerCase().includes(facultySearch.toLowerCase());
      const matchesDept = deptFilter === "All" || f.department === deptFilter;
      return matchesSearch && matchesDept;
    });
  }, [facultySearch, deptFilter]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Chancellor Tarun Anand Profile Card */}
      <div className="chart-card" style={{ padding: '24px', display: 'flex', flexDirection: 'row', gap: '24px', alignItems: 'center', flexWrap: 'wrap', backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)', margin: 0 }}>
        <div style={{
          width: '100px',
          height: '100px',
          borderRadius: '50%',
          backgroundColor: '#1B3A6B',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '2rem',
          fontWeight: 800,
          boxShadow: '0 4px 10px rgba(0,0,0,0.1)'
        }}>
          TA
        </div>
        <div style={{ flex: 1, minWidth: '250px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h2 style={{ fontFamily: 'Outfit', fontWeight: 800, fontSize: '1.4rem', color: '#1B3A6B' }}>{mockInstitutionalInfo.chancellor.name}</h2>
            <span className="badge badge-pill-light">{mockInstitutionalInfo.chancellor.role}</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: '#64748B', fontStyle: 'italic', marginTop: '2px' }}>"{mockInstitutionalInfo.chancellor.vision}"</p>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: 1.4, marginTop: '8px' }}>
            {mockInstitutionalInfo.chancellor.bio}
          </p>
          <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '8px', fontWeight: 600 }}>
            Contact: {mockInstitutionalInfo.chancellor.email}
          </div>
        </div>
      </div>

      {/* Leadership Row: Deans & Counsellors */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '20px' }}>
        
        {/* Academic Deans directory */}
        <div className="activity-feed-card" style={{ margin: 0, backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
          <h2 style={{ marginBottom: '14px', fontFamily: 'Outfit', fontWeight: 700 }}>Academic Leadership Deans</h2>
          <div className="feed-list">
            {mockInstitutionalInfo.deans.map((d, idx) => (
              <div key={idx} className="feed-item" style={{ borderLeft: '3px solid #1B3A6B', padding: '10px' }}>
                <div className="feed-body">
                  <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.85rem' }}>{d.name}</div>
                  <div style={{ fontSize: '0.72rem', color: '#1B3A6B', fontWeight: 600 }}>{d.role}</div>
                  <div style={{ fontSize: '0.72rem', color: '#64748B', marginTop: '2px' }}>Dept: {d.department} | Tel: {d.phone}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Campus Counsellors Team */}
        <div className="activity-feed-card" style={{ margin: 0, backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)' }}>
          <h2 style={{ marginBottom: '14px', fontFamily: 'Outfit', fontWeight: 700 }}>Campus Clinical Counseling Team</h2>
          <div className="feed-list">
            {mockInstitutionalInfo.counsellors.map((c, idx) => (
              <div key={idx} className="feed-item" style={{ borderLeft: '3px solid #27AE60', padding: '10px' }}>
                <div className="feed-body">
                  <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.85rem' }}>{c.name}</div>
                  <div style={{ fontSize: '0.72rem', color: '#27AE60', fontWeight: 600 }}>{c.role}</div>
                  <div style={{ fontSize: '0.72rem', color: '#64748B', marginTop: '2px' }}>Specialty: {c.specialty} | Email: {c.email}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Departments Grid */}
      <div>
        <h2 style={{ fontFamily: 'Outfit', fontSize: '1.25rem', fontWeight: 700, color: '#1B3A6B', marginBottom: '14px' }}>Academic Programs & Departments</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          {mockInstitutionalInfo.departments.map((d, idx) => (
            <div key={idx} className="chart-card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', backgroundColor: 'var(--card-bg)', border: '1px solid var(--border-color)', margin: 0 }}>
              <div>
                <span className="badge badge-pill-light" style={{ fontSize: '0.65rem', marginBottom: '6px' }}>{d.code}</span>
                <h3 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#1B3A6B', fontFamily: 'Outfit' }}>{d.name}</h3>
                <div style={{ fontSize: '0.72rem', color: '#64748B', marginTop: '6px' }}>
                  <strong>HOD:</strong> {d.hod}
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: '#64748B', borderTop: '1px solid #F1F5F9', paddingTop: '8px', marginTop: '12px' }}>
                <span>Faculty: <strong>{d.facultyCount}</strong></span>
                <span>Students: <strong>{d.studentCount}</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Searchable Faculty Table */}
      <div className="table-card" style={{ margin: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid var(--border-color)', backgroundColor: 'var(--card-bg)', flexWrap: 'wrap', gap: '10px' }}>
          <div>
            <h2 style={{ fontFamily: 'Outfit', fontWeight: 700, fontSize: '1.1rem', color: '#1B3A6B' }}>Faculty Directory Directory</h2>
            <p style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '2px' }}>
              Academic advisors, mentors, and professors assisting in student support.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <select 
              className="filter-select" 
              value={deptFilter} 
              onChange={(e) => setDeptFilter(e.target.value)}
              style={{ fontSize: '0.75rem' }}
            >
              <option value="All">All Departments</option>
              <option value="B.Sc (Agriculture)">B.Sc (Agriculture)</option>
              <option value="B.Tech (AI & Biotech)">B.Tech (AI & Biotech)</option>
              <option value="BBA (Business Analytics)">BBA</option>
              <option value="MBA (Agribusiness)">MBA</option>
              <option value="Design Thinking">Design Thinking</option>
            </select>
            <input 
              type="text" 
              className="search-input" 
              placeholder="Search faculty name..."
              value={facultySearch}
              onChange={(e) => setFacultySearch(e.target.value)}
              style={{ fontSize: '0.75rem', padding: '4px 10px', height: 'auto', border: '1px solid var(--border-color)', borderRadius: '6px' }}
            />
          </div>
        </div>

        <div className="table-responsive">
          <table className="custom-table" style={{ fontSize: '0.8rem' }}>
            <thead>
              <tr>
                <th>Professor Name</th>
                <th>Academic Department</th>
                <th>Instructional Role</th>
                <th>Campus Email</th>
                <th>Academic Advisors</th>
              </tr>
            </thead>
            <tbody>
              {filteredFaculty.map((f, idx) => (
                <tr key={idx}>
                  <td>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{f.name}</div>
                  </td>
                  <td>{f.department}</td>
                  <td>{f.role}</td>
                  <td>{f.email}</td>
                  <td>
                    <span className="badge badge-low" style={{ backgroundColor: 'rgba(39, 174, 96, 0.12)', color: '#27AE60', fontWeight: 700, fontSize: '0.65rem' }}>
                      Assigned Advisor
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}

/* ==========================================
   COMPONENT: StudentDetailsModal
   ========================================== */
function StudentDetailsModal({ student, onClose, onAddIntervention }) {
  const [intType, setIntType] = useState("1-on-1 Counselling");
  const [intNotes, setIntNotes] = useState("");

  const handleSubmitNote = (e) => {
    e.preventDefault();
    if (!intNotes) return;
    onAddIntervention(student.id, intType, intNotes);
    setIntNotes("");
  };

  // Supplement timeline to ensure exactly 3 fake entries are always rendered
  const visualInterventions = useMemo(() => {
    const list = [...(student.interventions || [])];
    if (list.length < 3) {
      const remaining = 3 - list.length;
      const fakeEntries = [
        { date: "2026-05-18", type: "1-on-1 Counselling Session", notes: "Conducted cognitive restructuring session focusing on practical performance anxiety and sleep hygiene.", counsellor: "Dr. Sarah Ahmed", status: "Ongoing" },
        { date: "2026-05-12", type: "Peer Mentor Assignment", notes: "Assigned a senior peer mentor from Agriculture Batch 2023 to help with lab reports and residential adaptation.", counsellor: "Dr. Sarah Ahmed", status: "Completed" },
        { date: "2026-05-04", type: "Parental Call/Counselling", notes: "Telephonic call with student's parents. Discussed academic status and well-being. Parents were highly cooperative.", counsellor: "Dr. Sarah Ahmed", status: "Completed" }
      ];
      for (let i = 0; i < remaining; i++) {
        list.push(fakeEntries[i % fakeEntries.length]);
      }
    }
    return list.slice(0, 3); // Bound strictly to exactly 3 entries
  }, [student]);

  // Determine progress bar percentages based on student scores
  const getStressPercent = () => {
    if (student.stress === "Severe") return 92;
    if (student.stress === "High") return 75;
    if (student.stress === "Moderate") return 50;
    return 20;
  };

  const getImpulsivityPercent = () => {
    if (student.impulsivity === "High") return 80;
    if (student.impulsivity === "Moderate") return 55;
    return 25;
  };

  const getRiskPercent = () => {
    if (student.risk === "High") return 85;
    if (student.risk === "Moderate") return 50;
    return 18;
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Clinical Student Profile Card</h2>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-scroll-area" style={{ maxHeight: 'calc(80vh - 130px)', overflowY: 'auto' }}>
          {/* Profile summary banner */}
          <div className="modal-profile-summary">
            {/* Photo Placeholder */}
            <div className="modal-avatar-large" style={{ 
              backgroundColor: 'var(--sidebar-bg)', 
              color: 'white', 
              fontSize: '1.8rem', 
              fontWeight: 800,
              boxShadow: '0 4px 10px rgba(0,0,0,0.12)',
              border: '3px solid white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {student.avatar || "SA"}
            </div>
            
            <div className="modal-profile-meta">
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <h3>{student.name}</h3>
                <span className={`badge badge-${student.riskLevel.toLowerCase()}`}>{student.riskLevel} Risk</span>
              </div>
              
              <div className="modal-meta-grid">
                <div className="meta-field">ID: <span>{student.id}</span></div>
                <div className="meta-field">Course: <span>{student.course}</span></div>
                <div className="meta-field">Batch: <span>{student.cohort}</span></div>
                <div className="meta-field">Gender: <span>{student.gender || "Male"}</span></div>
                <div className="meta-field">Hosteller: <span>{student.hosteller}</span></div>
                <div className="meta-field">Attendance: <span>{student.attendance}</span></div>
                <div className="meta-field">GPA: <span>{student.gpa}</span></div>
                <div className="meta-field">Wellness Score: <span style={{ color: student.wellnessScore < 50 ? '#EB5757' : '#27AE60' }}>{student.wellnessScore}%</span></div>
              </div>
            </div>
          </div>

          {/* Scores shown as dynamic progress bars */}
          <div className="modal-section" style={{ backgroundColor: 'var(--border-light)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', marginBottom: '20px' }}>
            <h4 style={{ fontSize: '0.85rem', fontWeight: 800, color: '#1B3A6B', marginBottom: '14px', fontFamily: 'Outfit' }}>Clinical Assessment Ratios</h4>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {/* Stress */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                  <span>Stress / Depression Level (DASS-21)</span>
                  <span style={{ color: student.stress === 'Severe' || student.stress === 'High' ? '#EB5757' : '#27AE60', fontWeight: 700 }}>
                    {student.stress}
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(0,0,0,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${getStressPercent()}%`,
                    height: '100%',
                    backgroundColor: student.stress === 'Severe' ? '#EB5757' : student.stress === 'High' ? '#DD6B20' : student.stress === 'Moderate' ? '#F2C94C' : '#27AE60',
                    borderRadius: '4px',
                    transition: 'width 0.5s ease-out'
                  }}></div>
                </div>
              </div>

              {/* Impulsivity */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                  <span>Impulsivity Indicators (BIS-11)</span>
                  <span style={{ color: student.impulsivity === 'High' ? '#DD6B20' : '#27AE60', fontWeight: 700 }}>
                    {student.impulsivity}
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(0,0,0,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${getImpulsivityPercent()}%`,
                    height: '100%',
                    backgroundColor: student.impulsivity === 'High' ? '#DD6B20' : student.impulsivity === 'Moderate' ? '#F2C94C' : '#27AE60',
                    borderRadius: '4px',
                    transition: 'width 0.5s ease-out'
                  }}></div>
                </div>
              </div>

              {/* Risk-Taking */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                  <span>Behavioural Risk Index (BRIS)</span>
                  <span style={{ color: student.risk === 'High' ? '#DD6B20' : '#27AE60', fontWeight: 700 }}>
                    {student.risk}
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(0,0,0,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${getRiskPercent()}%`,
                    height: '100%',
                    backgroundColor: student.risk === 'High' ? '#DD6B20' : student.risk === 'Moderate' ? '#F2C94C' : '#27AE60',
                    borderRadius: '4px',
                    transition: 'width 0.5s ease-out'
                  }}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Risk Factors breakdown */}
          <div className="modal-section">
            <h4 className="modal-section-title">Risk Factor Diagnostics</h4>
            <div className="risk-analysis-grid">
              <div className="risk-factor-box">
                <h4>
                  <Activity size={14} color="#EB5757" />
                  Psychological Risk
                </h4>
                <p>{student.riskFactors.psychological}</p>
              </div>

              <div className="risk-factor-box">
                <h4>
                  <Award size={14} color="#1B3A6B" />
                  Academic Risk
                </h4>
                <p>{student.riskFactors.academic}</p>
              </div>

              <div className="risk-factor-box">
                <h4>
                  <Users size={14} color="#27AE60" />
                  Social & Environment
                </h4>
                <p>{student.riskFactors.social}</p>
              </div>
            </div>
          </div>

          {/* Supplemented clinical history (exactly 3 fake entries) */}
          <div className="modal-section">
            <h4 className="modal-section-title">Support Activity History (3 Case Records)</h4>
            <div className="timeline-list">
              {visualInterventions.map((item, idx) => (
                <div key={idx} className="timeline-item active">
                  <div className="timeline-dot"></div>
                  <div className="timeline-content-box" style={{ padding: '10px 14px' }}>
                    <div className="timeline-date-type" style={{ fontSize: '0.72rem', display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span className="timeline-type" style={{ fontWeight: 700, color: '#1B3A6B' }}>{item.type}</span>
                      <span className="timeline-date" style={{ fontWeight: 600, color: '#64748B' }}>{item.date}</span>
                    </div>
                    <p className="timeline-notes" style={{ fontSize: '0.75rem', color: 'var(--text-primary)', lineHeight: 1.4 }}>{item.notes}</p>
                    <div className="timeline-counsellor" style={{ fontSize: '0.68rem', color: '#64748B', fontStyle: 'italic', marginTop: '4px' }}>
                      Counsellor: {item.counsellor} ({item.status})
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick logger action note form */}
          <div className="modal-section" style={{ borderTop: '1px dashed var(--border-color)', paddingTop: '20px' }}>
            <h4 className="modal-section-title">Log New Care Note</h4>
            <form className="logger-form" onSubmit={handleSubmitNote} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div className="form-group" style={{ gridColumn: 'span 1' }}>
                <label>Intervention Action</label>
                <select
                  className="form-control"
                  value={intType}
                  onChange={(e) => setIntType(e.target.value)}
                >
                  <option value="1-on-1 Counselling">1-on-1 Counselling</option>
                  <option value="Group Therapy Session">Group Therapy Session</option>
                  <option value="Peer Mentor Assign">Peer Mentor Assign</option>
                  <option value="Clinical Referral">Clinical Referral</option>
                  <option value="Parental Counseling Session">Parental Call/Counseling</option>
                </select>
              </div>
              <div className="form-group" style={{ gridColumn: 'span 2' }}>
                <label>Counselor Session Notes</label>
                <textarea
                  className="form-control form-textarea"
                  placeholder="Enter confidential notes..."
                  required
                  value={intNotes}
                  onChange={(e) => setIntNotes(e.target.value)}
                  style={{ minHeight: '80px', width: '100%' }}
                />
              </div>
              <button type="submit" className="submit-btn" style={{ gridColumn: 'span 2', padding: '8px' }}>Log Care Note</button>
            </form>
          </div>
        </div>

        {/* Modal Footer Actions (Close + Schedule Session) */}
        <div className="modal-header" style={{ borderTop: '1px solid var(--border-color)', borderBottom: 'none', justifyContent: 'flex-end', gap: '12px', padding: '16px 24px' }}>
          {student.profile_id && (
            <button
              className="submit-btn"
              onClick={() => {
                window.location.href = `/counsellor/student/${student.profile_id}/report`;
              }}
              style={{ padding: '8px 16px', fontWeight: 700, backgroundColor: '#10b981', borderColor: '#10b981' }}
            >
              View Detailed Report
            </button>
          )}
          <button className="action-btn" onClick={onClose} style={{ padding: '8px 16px', fontWeight: 700 }}>
            Close
          </button>
          <button 
            className="submit-btn" 
            onClick={() => {
              alert(`Appointment session scheduled successfully for ${student.name} with Dr. Sarah Ahmed.`);
            }} 
            style={{ padding: '8px 16px', fontWeight: 700 }}
          >
            Schedule Session
          </button>
        </div>
      </div>
    </div>
  );
}
