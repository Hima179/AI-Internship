import requests
from bs4 import BeautifulSoup
import json
import re
import sys

BASE_URL = "http://127.0.0.1:5000"

def get_csrf_token(session, url):
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Try meta tag
    meta = soup.find('meta', {'name': 'csrf-token'})
    if meta:
        return meta.get('content')
        
    # Try hidden input
    hidden = soup.find('input', {'name': 'csrf_token'})
    if hidden:
        return hidden.get('value')
        
    return None

def cleanup_db():
    print("Cleaning up database for test user...")
    from app import create_app, db
    from app.models import User, StudentProfile, AssessmentSession, Response, AssessmentScore, Flag
    app = create_app('development')
    with app.app_context():
        u = User.query.filter_by(uai_id='himanshu.pathak@universalai.in').first()
        if u:
            sp = u.student_profile
            if sp:
                sessions = AssessmentSession.query.filter_by(student_id=sp.id).all()
                for s in sessions:
                    Response.query.filter_by(session_id=s.id).delete()
                    AssessmentScore.query.filter_by(session_id=s.id).delete()
                    db.session.delete(s)
                Flag.query.filter_by(student_id=u.id).delete()
                db.session.delete(sp)
            db.session.delete(u)
            db.session.commit()
            print("Cleanup complete")
    
    import subprocess
    subprocess.check_call(['python', 'create_user.py'])

def test_portal():
    print("--- STARTING PORTAL VERIFICATION TEST ---")
    cleanup_db()
    s = requests.Session()
    # 0. Test Welcome page
    print("[0] Testing Welcome page...")
    r_welcome = s.get(BASE_URL)
    if r_welcome.status_code != 200:
        print(f"FAIL: Welcome page returned status code {r_welcome.status_code}")
        sys.exit(1)
    if "Safe Space" not in r_welcome.text or "AI-Driven Analysis" not in r_welcome.text:
        print("FAIL: Welcome page content not found")
        sys.exit(1)
    print("SUCCESS: Welcome page verified.")

    # 1. Log in as student
    print("[1] Logging in as student...")
    login_url = f"{BASE_URL}/auth/login"
    csrf_token = get_csrf_token(s, login_url)
    if not csrf_token:
        print("FAIL: Could not retrieve CSRF token for login")
        sys.exit(1)
        
    login_data = {
        'csrf_token': csrf_token,
        'uai_id': 'himanshu.pathak@universalai.in',
        'password': 'Mahazan@486828',
        'role': 'student',
        'submit': 'Log In'
    }
    
    r_login = s.post(login_url, data=login_data, allow_redirects=True)
    if "Informed Consent" not in r_login.text and "Student Dashboard" not in r_login.text and "Student Details" not in r_login.text:
        print(f"FAIL: Login failed. Response text snippet:\n{r_login.text[:500]}")
        sys.exit(1)
    print("SUCCESS: Logged in successfully.")

    # 2. Handle Consent if present
    if "Informed Consent" in r_login.text:
        print("[2] Submitting Informed Consent...")
        csrf_token = get_csrf_token(s, f"{BASE_URL}/student/consent")
        consent_data = {
            'csrf_token': csrf_token,
            'action': 'agree'
        }
        r_consent = s.post(f"{BASE_URL}/student/consent", data=consent_data, allow_redirects=True)
        print("SUCCESS: Consent agreed.")
        
    # 3. Handle Details if present
    # Check if currently on details page
    r_current = s.get(f"{BASE_URL}/student/details")
    if "Student Details" in r_current.text:
        print("[3] Submitting Student Details...")
        csrf_token = get_csrf_token(s, f"{BASE_URL}/student/details")
        details_data = {
            'csrf_token': csrf_token,
            'name': 'Himanshu Pathak',
            'age': '21',
            'gender': 'male',
            'department': 'BSc Psychology',
            'year_of_study': '2',
            'phone': '1234567890',
            'previous_counselling': 'no',
            'mental_health_diagnosis': 'no',
            'submit': 'Save & Continue'
        }
        r_details = s.post(f"{BASE_URL}/student/details", data=details_data, allow_redirects=True)
        print("SUCCESS: Details updated.")

    # 4. Start Assessment
    print("[4] Starting Assessment...")
    r_start = s.get(f"{BASE_URL}/student/assessment/start", allow_redirects=False)
    if r_start.status_code != 302:
        print(f"FAIL: /assessment/start did not redirect (status code: {r_start.status_code})")
        sys.exit(1)
        
    next_url = r_start.headers.get('Location')
    print(f"SUCCESS: Redirected to {next_url}")
    
    # 5. Verify Redirect to instructions page for Section 1
    r_next = s.get(f"{BASE_URL}{next_url}", allow_redirects=False)
    if "instructions" not in r_next.headers.get('Location', ''):
        print(f"FAIL: Q1 did not redirect to Section 1 instructions page (redirected to: {r_next.headers.get('Location')})")
        sys.exit(1)
        
    inst_url = r_next.headers.get('Location')
    print(f"SUCCESS: Correctly redirected to instructions: {inst_url}")
    
    # Retrieve instructions page content
    r_inst_page = s.get(f"{BASE_URL}{inst_url}")
    if "Section 1: Well-being Indicators" not in r_inst_page.text:
        print("FAIL: Section 1 title not found in instructions page")
        sys.exit(1)
    print("SUCCESS: Section 1 instructions verified.")
    
    # 6. Acknowledge Section 1 instructions
    # Extract acknowledge url from instructions page or construct it
    # Format of ack url: /assessment/acknowledge/<int:assessment_id>?next_q_num=X
    # Let's search for "acknowledge/" in instructions page
    ack_match = re.search(r'href="(/student/assessment/acknowledge/[^"]+)"', r_inst_page.text)
    if not ack_match:
        print("FAIL: Could not find acknowledge url in instructions page")
        sys.exit(1)
    ack_url = ack_match.group(1)
    print(f"Acknowledging section via: {ack_url}")
    r_ack = s.get(f"{BASE_URL}{ack_url}", allow_redirects=True)
    
    # 7. Check question 1 page layout (hiding panel and timer)
    print("[7] Verifying Question 1 Page layout...")
    # The redirected page should be Question 1
    soup_q = BeautifulSoup(r_ack.text, 'html.parser')
    
    # Ensure quiz-sidebar is not in DOM
    sidebar = soup_q.find('div', {'class': 'quiz-sidebar'})
    if sidebar:
        print("FAIL: Left sidebar (panel) is still present in DOM")
        sys.exit(1)
    else:
        print("SUCCESS: Left sidebar panel successfully removed.")
        
    # Ensure timer elements are not in DOM
    timer_txt = soup_q.find('div', {'id': 'timer-text'})
    timer_box = soup_q.find('div', {'class': 'timer-box'})
    if timer_txt or timer_box:
        print("FAIL: Timer text/box is still present in DOM")
        sys.exit(1)
    else:
        print("SUCCESS: Timer successfully removed.")
        
    # Ensure category badges are not in DOM
    badge = soup_q.find('div', {'class': 'dept-badge'})
    if badge:
        print("FAIL: Category name badge is still present in DOM")
        sys.exit(1)
    else:
        print("SUCCESS: Category badges successfully removed.")
        
    # Ensure Previous and Skip buttons are not in DOM
    skip_btn = soup_q.find('button', {'id': 'skip-btn'})
    prev_btn = soup_q.find('button', {'id': 'prev-btn'})
    if skip_btn or prev_btn:
        print("FAIL: Skip or Previous button is still present in DOM")
        sys.exit(1)
    else:
        print("SUCCESS: Skip and Previous buttons successfully removed.")

    # 8. Check URL skipping lock (Locking browser navigation)
    print("[8] Testing URL navigation lock (trying to skip to Q5)...")
    r_skip_test = s.get(f"{BASE_URL}/student/assessment/question/5", allow_redirects=False)
    if r_skip_test.status_code != 302:
        print("FAIL: Skip to Q5 did not redirect")
        sys.exit(1)
    if r_skip_test.headers.get('Location') != "/student/assessment/question/1":
        print(f"FAIL: Skip to Q5 redirected to {r_skip_test.headers.get('Location')} instead of Q1")
        sys.exit(1)
    print("SUCCESS: URL navigation lock active. Successfully redirected back to Q1.")

    # 9. Loop and answer all questions sequentially
    print("[9] Simulating answering all questions...")
    q_num = 1
    total_q = None
    
    while True:
        # Get CSRF token for the current question page
        csrf_token = get_csrf_token(s, f"{BASE_URL}/student/assessment/question/{q_num}")
        if not csrf_token:
            print(f"FAIL: Could not retrieve CSRF token for Q{q_num}")
            sys.exit(1)
            
        # Extract question ID from page
        r_q_page = s.get(f"{BASE_URL}/student/assessment/question/{q_num}")
        soup_q = BeautifulSoup(r_q_page.text, 'html.parser')
        q_id_elem = soup_q.find('input', {'id': 'question-id'})
        if not q_id_elem:
            print(f"FAIL: Could not find question-id input on Q{q_num} page")
            sys.exit(1)
        q_id = int(q_id_elem.get('value'))
        
        # Get total questions if not already known
        if total_q is None:
            total_text = soup_q.find('span', style=lambda value: value and 'color:#555' in value).text
            # Format is "Question 1 of 296"
            total_q = int(re.search(r'of (\d+)', total_text).group(1))
            print(f"Detected total questions: {total_q}")
            
        # Select first option value (usually "0" or whatever value the options have)
        option_card = soup_q.find('div', {'class': 'option-card'})
        if not option_card:
            print(f"FAIL: No option card found for Q{q_num}")
            sys.exit(1)
        opt_val = option_card.get('data-value')
        
        # Post answer
        answer_data = {
            'question_id': q_id,
            'selected_option': opt_val,
            'time_taken': 2,
            'auto_submitted': False
        }
        
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json'
        }
        
        r_ans = s.post(f"{BASE_URL}/student/assessment/answer?q_num={q_num}", 
                       json=answer_data, 
                       headers=headers)
                       
        if r_ans.status_code != 200:
            print(f"FAIL: Submit answer for Q{q_num} failed with status {r_ans.status_code}")
            sys.exit(1)
            
        ans_res = r_ans.json()
        if not ans_res.get('success'):
            print(f"FAIL: Submit answer response shows failure: {ans_res}")
            sys.exit(1)
            
        # Advance
        if ans_res.get('is_last') or q_num >= total_q:
            print(f"Answered last question Q{q_num}.")
            break
            
        next_q = ans_res.get('next_question')
        
        # GET next question. Check if it redirects to instructions screen
        r_next_q = s.get(f"{BASE_URL}/student/assessment/question/{next_q}", allow_redirects=False)
        if r_next_q.status_code == 302:
            redirect_loc = r_next_q.headers.get('Location')
            if "instructions" in redirect_loc:
                # Retrieve instructions, acknowledge, then proceed
                print(f"Transitioning section: Redirected to instructions {redirect_loc}")
                r_inst = s.get(f"{BASE_URL}{redirect_loc}")
                ack_match = re.search(r'href="(/student/assessment/acknowledge/[^"]+)"', r_inst.text)
                if not ack_match:
                    print("FAIL: Could not find acknowledge url in instructions")
                    sys.exit(1)
                ack_url = ack_match.group(1)
                s.get(f"{BASE_URL}{ack_url}")
                print("Section acknowledged. Continuing assessment.")
                
        q_num = next_q
        if q_num % 50 == 0:
            print(f"Progress: Answered {q_num} questions...")

    # 10. Complete Assessment
    print("[10] Completing assessment...")
    csrf_token = get_csrf_token(s, f"{BASE_URL}/student/assessment/question/{total_q}")
    headers = {
        'X-CSRFToken': csrf_token,
        'Content-Type': 'application/json'
    }
    r_comp = s.post(f"{BASE_URL}/student/assessment/complete", json={'total_time': 600}, headers=headers)
    if r_comp.status_code != 200 or not r_comp.json().get('success'):
        print(f"FAIL: Assessment complete API call failed: {r_comp.text}")
        sys.exit(1)
        
    complete_redirect = r_comp.json().get('redirect')
    print(f"SUCCESS: Assessment complete redirected to {complete_redirect}")
    
    r_complete_page = s.get(f"{BASE_URL}{complete_redirect}")
    if "Assessment Results Summary" not in r_complete_page.text and "Universal AI University" not in r_complete_page.text:
        print("FAIL: Results summary page not loaded correctly")
        sys.exit(1)
        
    # 11. Verify exported text report total question count
    print("[11] Verifying text report export...")
    r_export = s.get(f"{BASE_URL}/student/export_results")
    if r_export.status_code != 200:
        print("FAIL: /student/export_results returned non-200 status")
        sys.exit(1)
        
    export_text = r_export.text
    if "Total Questions : 296" not in export_text:
        print("FAIL: Exported text results does not display correct Total Questions: 296")
        # Find where it shows Total Questions
        matches = re.findall(r'Total Questions.*', export_text)
        print(f"Found matches: {matches}")
        sys.exit(1)
    print("SUCCESS: Text report export displays correct Total Questions count (296).")

    # 12. Log in as counsellor
    print("[12] Logging in as counsellor...")
    s_coun = requests.Session()
    csrf_token = get_csrf_token(s_coun, login_url)
    
    login_data_coun = {
        'csrf_token': csrf_token,
        'uai_id': 'COUN_ANJALI_PANDEY',
        'password': 'Coun@123',
        'role': 'counsellor',
        'submit': 'Log In'
    }
    
    r_login_coun = s_coun.post(login_url, data=login_data_coun, allow_redirects=True)
    if "Counsellor Insights" not in r_login_coun.text and "COUNSELLOR PORTAL" not in r_login_coun.text:
        print(f"FAIL: Counsellor login failed. Response text snippet:\n{r_login_coun.text[:500]}")
        sys.exit(1)
    print("SUCCESS: Counsellor logged in.")

    # 13. Verify Counsellor Student Report API
    print("[13] Verifying counsellor student report API...")
    # Find student ID for himanshu.pathak@universalai.in
    # We can query `/student/<id>/report`
    # Let's inspect the counsellor dashboard to find Himanshu's student profile ID or query API.
    # We can write a quick query endpoint or search the counsellor dashboard text for "Himanshu Pathak"
    profile_id_match = re.search(r'/counsellor/student/(\d+)/report', r_login_coun.text)
    if not profile_id_match:
        # Search in the full dashboard page
        r_dash = s_coun.get(f"{BASE_URL}/counsellor/dashboard")
        profile_id_match = re.search(r'/counsellor/student/(\d+)/report', r_dash.text)
        
    if not profile_id_match:
        # If not in HTML (since dashboard is React-based, it loads data from a script tag)
        # Let's look for window.__FLASK_FLAGGED_STUDENTS__ inside script tags
        # Let's search script tag contents
        students_match = re.search(r'window\.__FLASK_FLAGGED_STUDENTS__\s*=\s*(.*?);', r_login_coun.text or r_dash.text)
        if students_match:
            students_data = json.loads(students_match.group(1))
            for st in students_data:
                if st.get('name') == 'Himanshu Pathak':
                    profile_id = st.get('profile_id')
                    break
            else:
                profile_id = students_data[0].get('profile_id') if students_data else None
        else:
            profile_id = None
    else:
        profile_id = int(profile_id_match.group(1))
        
    if not profile_id:
        # Hardcode fallback or print warning
        print("WARNING: Could not parse student profile ID from dashboard. Querying database via python instead.")
        # Let's use database directly to get the student profile ID of himanshu.pathak
        import subprocess
        out = subprocess.check_output(['python', '-c', "from app import create_app; from app.models import User; app = create_app('development'); ctx = app.app_context(); ctx.push(); u = User.query.filter_by(uai_id='himanshu.pathak@universalai.in').first(); print(u.student_profile.id)"])
        profile_id = int(out.decode().strip())
        
    print(f"Using student profile ID: {profile_id}")
    
    # Query student report API
    report_api_url = f"{BASE_URL}/counsellor/api/counsellor/student/{profile_id}/report"
    r_api = s_coun.get(report_api_url)
    if r_api.status_code != 200:
        print(f"FAIL: Report API returned {r_api.status_code}: {r_api.text}")
        sys.exit(1)
        
    report_data = r_api.json()
    print("SUCCESS: Retrieved counsellor report API payload.")
    
    # Verify exact question responses are in the API payload
    q_resps = report_data.get('question_responses', [])
    if len(q_resps) != 296:
        print(f"FAIL: API payload did not return all 296 questions (returned: {len(q_resps)})")
        sys.exit(1)
    print("SUCCESS: API payload contains all 296 question responses.")
    
    # 14. Verify student report HTML page and full-report API
    print("[14] Verifying counsellor student full-report API...")
    r_full_api = s_coun.get(f"{BASE_URL}/counsellor/api/counsellor/student/{profile_id}/full-report")
    if r_full_api.status_code != 200:
        print(f"FAIL: full-report API returned status {r_full_api.status_code}")
        sys.exit(1)
        
    full_data = r_full_api.json()
    for key in ["bfi44", "dass21", "eq_sq", "home", "summary"]:
        if key not in full_data:
            print(f"FAIL: full-report API missing key '{key}'")
            sys.exit(1)
    print("SUCCESS: full-report API verified.")

    print("[14.1] Verifying student report HTML page layout...")
    r_report_page = s_coun.get(f"{BASE_URL}/counsellor/student/{profile_id}/report")
    
    required_sections = [
        "Safe Space",
        "Big Five Personality Profile",
        "DASS-21 Severity Scales",
        "EQ-SQ Social-Emotional Quotients",
        "Home & Family Adjustment Environment",
        "Integrated Clinical Summary"
    ]
    
    for section in required_sections:
        if section not in r_report_page.text:
            print(f"FAIL: Section title '{section}' not found in HTML report")
            sys.exit(1)
            
    print("SUCCESS: Redesigned student report HTML structure verified.")
        
    # 15. Verify PDF generation
    print("[15] Testing PDF generation...")
    r_pdf = s_coun.get(f"{BASE_URL}/counsellor/student/{profile_id}/pdf")
    if r_pdf.status_code != 200 or r_pdf.headers.get('Content-Type') != 'application/pdf':
        print(f"FAIL: PDF generation returned status {r_pdf.status_code}, content type {r_pdf.headers.get('Content-Type')}")
        sys.exit(1)
    print("SUCCESS: PDF successfully generated and returned as application/pdf.")

    print("\n--- ALL TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    test_portal()
