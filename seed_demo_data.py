import os
import sys
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Ensure root directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, StudentProfile, AssessmentSession, Response, Question, Assessment, Flag, AssessmentScore
from utils.scoring import calculate_scores, determine_overall_risk

app = create_app('development')

def get_real_faculty():
    html_path = r"C:\Users\Himanshu Pathak\.gemini\antigravity\brain\12a1de88-2bb3-4e0c-b62c-d45046770d99\.system_generated\steps\222\content.md"
    faculty_list = []
    
    if not os.path.exists(html_path):
        print("Scraped HTML file not found, using fallback prominent faculty list.")
        return [
            {"name": "Ms. Anjali Pandey", "designation": "Counselling Psychologist(Safe Space)", "department": "School of Social, Liberal Arts & Behavioural Sciences"},
            {"name": "Ms. Tamanna Sharma", "designation": "Counselling Psychologist(Safe Space)", "department": "School of Social, Liberal Arts & Behavioural Sciences"},
            {"name": "Dr. Harshita Kumar", "designation": "Dean - School of Management (PG)", "department": "School of Management"},
            {"name": "Dr. Waheeda S Thomas", "designation": "Dean - School of Management (UG)", "department": "School of Management"},
            {"name": "Dr. Shilpa Shailesh Joshi", "designation": "Professor, Dean - Academics", "department": "School of AI & Future Technologies"},
            {"name": "Mr. Pranav More", "designation": "Assistant Professor", "department": "School of AI & Future Technologies"},
            {"name": "Mr. Rajesh Bhise", "designation": "Assistant Professor", "department": "School of AI & Future Technologies"}
        ]
        
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        html_start = html_content.find("<!doctype html>")
        if html_start != -1:
            html_content = html_content[html_start:]

        soup = BeautifulSoup(html_content, 'html.parser')

        for tag in ['h3', 'h4']:
            for el in soup.find_all(tag):
                name = el.get_text(strip=True)
                # Filter out standard non-name headings
                if any(w in name.lower() for w in ['link', 'admission', 'about', 'social', 'welcome', 'management', 'analytics', 'finance', 'operations', 'resource', 'quick', 'login']):
                    continue
                    
                designation = ""
                parent = el.parent
                if parent:
                    pos_el = parent.find(class_=lambda x: x and ('position' in x.lower() or 'designation' in x.lower() or 'role' in x.lower()))
                    if pos_el:
                        designation = pos_el.get_text(strip=True)
                    else:
                        sibling = el.find_next_sibling()
                        if sibling:
                            designation = sibling.get_text(strip=True)
                            
                department = "School of Management"
                curr = el
                while curr:
                    prev_h2 = curr.find_previous('h2')
                    if prev_h2:
                        h2_text = prev_h2.get_text(strip=True)
                        if any(k in h2_text.lower() for k in ["school", "faculty", "department", "pgdm", "analytics"]):
                            department = h2_text
                            break
                    curr = curr.parent
                    
                # Clean up name titles
                clean_name = name.replace("MR. ", "").replace("MR ", "").replace("MS. ", "").replace("MS ", "").replace("DR. ", "").replace("DR ", "").replace("Ms. ", "").replace("Dr. ", "").replace("Prof. ", "").replace("PROF. ", "")
                clean_name = clean_name.strip()
                
                faculty_list.append({
                    "name": clean_name,
                    "designation": designation or "Faculty",
                    "department": department
                })
    except Exception as e:
        print(f"Error reading scraped HTML: {e}")
        
    # Remove duplicates
    unique_fac = []
    seen = set()
    for f in faculty_list:
        norm_name = f["name"].lower().strip()
        if norm_name not in seen and len(norm_name) > 3:
            seen.add(norm_name)
            unique_fac.append(f)
            
    return unique_fac

def run_scoring_saver(session_id):
    """Calculates and saves scores using the new utils.scoring module."""
    sess_obj = AssessmentSession.query.get(session_id)
    if not sess_obj: return
    
    dass_score = calculate_scores(sess_obj, "DASS21")
    bfi_score = calculate_scores(sess_obj, "BFI44")
    eq_score = calculate_scores(sess_obj, "EQ")
    sq_score = calculate_scores(sess_obj, "SQ")
    home_score = calculate_scores(sess_obj, "HOME")
    
    all_scores = {
        "DASS21": dass_score,
        "BFI44": bfi_score,
        "EQ": eq_score,
        "SQ": sq_score,
        "HOME": home_score
    }
    
    risk_data = determine_overall_risk(all_scores)
    risk_level = risk_data["risk_level"]
    
    assessments = Assessment.query.all()
    for ass in assessments:
        score_data = None
        total_score = 0.0
        severity = ""
        
        if ass.name == "DASS-21":
            score_data = dass_score
            total_score = float(dass_score["total_score"])
            severity = risk_level.capitalize()
        elif ass.name == "BFI-44":
            score_data = bfi_score
            total_score = float(bfi_score["total_score"])
            severity = bfi_score["severity_labels"].get("Neuroticism", "")
        elif ass.name == "EQ":
            score_data = eq_score
            total_score = float(eq_score["total_score"])
            severity = eq_score["severity_labels"]["Emotional Awareness"]
        elif ass.name == "SQ":
            score_data = sq_score
            total_score = float(sq_score["total_score"])
            severity = sq_score["severity_labels"]["Social Awareness"]
        elif ass.name == "Home Adjustment Questionnaire":
            score_data = home_score
            total_score = float(home_score["total_score"])
            severity = home_score["severity_labels"]["Home Adjustment"]
            
        if score_data:
            score_rec = AssessmentScore(
                session_id=sess_obj.id,
                assessment_id=ass.id,
                category_scores=score_data,
                total_score=total_score,
                severity_label=severity
            )
            db.session.add(score_rec)
            
    profile = StudentProfile.query.get(sess_obj.student_id)
    if profile:
        profile.risk_level = risk_level.capitalize()
        if risk_level in ["high", "severe"]:
            flag = Flag(
                student_id=profile.user_id,
                counsellor_id=profile.assigned_counsellor_id,
                reason=f"Automated risk flag: {risk_level.upper()} severity detected in DASS-21 assessment session {sess_obj.id}.",
                created_at=datetime.utcnow()
            )
            db.session.add(flag)
    db.session.commit()

def seed_demo_data():
    # 200 Hindu Names (100 Boys + 100 Girls)
    boy_names = [
        "Aarav", "Vivaan", "Aditya", "Arjun", "Rohan", "Kartik", "Nikhil", "Sameer", "Harshit", "Shubham",
        "Aniket", "Siddharth", "Pranav", "Ishaan", "Manish", "Rajesh", "Saurabh", "Deepak", "Sanjay", "Anirudh",
        "Varun", "Abhishek", "Ajay", "Ashwin", "Bhavesh", "Chirag", "Devansh", "Gaurav", "Hemant", "Jayesh",
        "Kunal", "Lokesh", "Mohan", "Naveen", "Omkar", "Parth", "Rahul", "Sandeep", "Tejas", "Uday",
        "Vijay", "Yash", "Amar", "Balaji", "Chaitanya", "Damodar", "Eklavya", "Govind", "Harsh", "Indrajit",
        "Jatin", "Krish", "Lalit", "Madhav", "Neeraj", "Ojas", "Prakash", "Ramesh", "Shyam", "Tanmay",
        "Umesh", "Vikas", "Anshul", "Bhaskar", "Chetan", "Darshan", "Ekansh", "Gopal", "Hrithik", "Ishwar",
        "Jayanth", "Keshav", "Laxman", "Manav", "Nishant", "Om", "Pradeep", "Raghav", "Shlok", "Tushar",
        "Vasant", "Yogesh", "Arvind", "Basant", "Chandresh", "Devendra", "Girish", "Hemesh", "Jagdish", "Kailash",
        "Lakshya", "Mukesh", "Nitin", "Prithvi", "Ranjit", "Suraj", "Trivikram", "Venu", "Vishal", "Yuvraj"
    ]

    girl_names = [
        "Ananya", "Kavya", "Radhika", "Sakshi", "Prachi", "Tanvi", "Isha", "Meera", "Suhani", "Vaishnavi",
        "Aditi", "Bhavana", "Charu", "Divya", "Ekta", "Gauri", "Harini", "Ishita", "Jyoti", "Kajal",
        "Lata", "Manisha", "Neha", "Oviya", "Pooja", "Rekha", "Shreya", "Trisha", "Urvashi", "Vidya",
        "Yamini", "Amrita", "Bhavika", "Chhavi", "Damini", "Esha", "Gayatri", "Hema", "Indira", "Jaya",
        "Kalpana", "Lavanya", "Madhuri", "Nandini", "Ojasvi", "Parvati", "Rupa", "Sneha", "Tara", "Uma",
        "Vandana", "Aishwarya", "Bhumika", "Chitra", "Deepa", "Geeta", "Hemlata", "Ishani", "Juhi", "Kusum",
        "Leela", "Mala", "Namrata", "Padma", "Radha", "Savita", "Triveni", "Usha", "Varsha", "Yami",
        "Aarohi", "Bhagyashree", "Chandni", "Devika", "Gopika", "Hiral", "Janhvi", "Kiran", "Laxmi", "Manjari",
        "Navya", "Pallavi", "Ranjana", "Shalini", "Tulsi", "Vani", "Anusha", "Brinda", "Chanchal", "Darshana",
        "Eshwari", "Gargi", "Hema Malini", "Jhanvi", "Komal", "Lalima", "Mohini", "Nisha", "Padmini", "Ritu"
    ]

    with app.app_context():
        print("Cleaning up old database records...")
        # Clear data in dependency order
        Response.query.delete()
        AssessmentScore.query.delete()
        AssessmentSession.query.delete()
        Flag.query.delete()
        StudentProfile.query.delete()
        
        # Delete counsellors, students, faculty
        User.query.filter(User.role.in_(['student', 'counsellor', 'faculty'])).delete()
        db.session.commit()
        print("Cleanup completed.")

        print("Seeding real faculty members from scraped data...")
        real_faculty = get_real_faculty()
        
        counsellor_users = []
        faculty_users = []
        
        # We need to register at least 3 counsellors
        counsellor_candidates = [
            ("Anjali Pandey", "anjali.pandey@universalai.in"),
            ("Tamanna Sharma", "tamanna.sharma@universalai.in"),
            ("Rajesh Bhise", "rajesh.bhise@universalai.in")
        ]
        
        for name, email in counsellor_candidates:
            uai = f"COUN_{name.replace(' ', '_').upper()}"
            c = User(uai_id=uai, name=name, role='counsellor', email=email)
            c.set_password("Coun@123")
            db.session.add(c)
            db.session.flush()
            counsellor_users.append(c)
            
        # Register the remaining unique scraped faculty
        counsellor_names = [cand[0].lower() for cand in counsellor_candidates]
        for f in real_faculty:
            # Skip if already added as counsellor
            if f["name"].lower() in counsellor_names:
                continue
                
            email_prefix = f["name"].replace(" ", ".").lower()
            email = f"{email_prefix}@universalai.in"
            uai = f"FAC_{f['name'].replace(' ', '_').upper()}"
            
            # Create Faculty
            fac = User(
                uai_id=uai,
                name=f["name"],
                role='faculty',
                email=email,
                department=f["department"],
                designation=f["designation"]
            )
            fac.set_password("Fac@123")
            db.session.add(fac)
            db.session.flush()
            faculty_users.append(fac)
            
        print(f"Seeded {len(counsellor_users)} counsellors and {len(faculty_users)} faculty members.")

        # Create 200 Students (100 Male, 100 Female)
        depts = [
            'BTech AI & ML', 'BTech Data Science', 'BTech Sound Engineering',
            'BSc Psychology', 'BSc AI', 'BBA General', 'BBA Marketing',
            'MBA General', 'MBA AI & Business', 'BDes', 'BA Liberal Arts', 'BA Music'
        ]
        
        student_profiles = []
        
        # Male Students
        for i, name in enumerate(boy_names):
            uai = f"STU_M{i+1:03d}"
            s = User(uai_id=uai, name=name, role='student', email=f"{name.lower()}{i+1}@test.com")
            s.set_password("Stu@123")
            db.session.add(s)
            db.session.flush()
            
            profile = StudentProfile(
                user_id=s.id,
                age=random.randint(18, 25),
                gender='Male',
                course='Bachelor of ' + random.choice(depts),
                year_of_study=random.randint(1, 4),
                department=random.choice(depts),
                consent_given=True,
                consent_timestamp=datetime.utcnow() - timedelta(days=2),
                assigned_counsellor_id=random.choice(counsellor_users).id
            )
            db.session.add(profile)
            db.session.flush()
            student_profiles.append(profile)
            
        # Female Students
        for i, name in enumerate(girl_names):
            uai = f"STU_F{i+1:03d}"
            s = User(uai_id=uai, name=name, role='student', email=f"{name.lower()}{i+1}@test.com")
            s.set_password("Stu@123")
            db.session.add(s)
            db.session.flush()
            
            profile = StudentProfile(
                user_id=s.id,
                age=random.randint(18, 25),
                gender='Female',
                course='Bachelor of ' + random.choice(depts),
                year_of_study=random.randint(1, 4),
                department=random.choice(depts),
                consent_given=True,
                consent_timestamp=datetime.utcnow() - timedelta(days=2),
                assigned_counsellor_id=random.choice(counsellor_users).id
            )
            db.session.add(profile)
            db.session.flush()
            student_profiles.append(profile)
            
        print("200 Hindu Student profiles created and assigned to counsellors.")

        # Simulate Completed Sessions for 30 students to provide data for charts
        questions = Question.query.all()
        if not questions:
            print("No questions found in database. Please run seeder.py first!")
            return
            
        for i in range(30):
            profile = student_profiles[i]
            
            session = AssessmentSession(
                student_id=profile.id,
                started_at=datetime.utcnow() - timedelta(days=1),
                completed_at=datetime.utcnow() - timedelta(days=1, minutes=random.randint(10, 20)),
                total_time_seconds=random.randint(400, 900),
                status='completed'
            )
            db.session.add(session)
            db.session.flush()
            
            # Simulate responses
            for q in questions:
                # Select option values based on the assessment type
                if q.assessment.name == 'DASS-21':
                    # Biasing first 6 students to severe/high risk profiles
                    if i < 6:
                        opt_val = random.choice([2, 3]) # Often, Almost Always
                    else:
                        opt_val = random.choice([0, 1, 2])
                elif q.assessment.name == 'BFI-44':
                    # Neuroticism items (scale 1-5)
                    if i < 8 and q.category == 'Neuroticism':
                        opt_val = 2 if q.reverse_scored else 4
                    elif i < 8 and q.category == 'Conscientiousness':
                        opt_val = 4 if q.reverse_scored else 2
                    else:
                        opt_val = random.choice([2, 3, 4])
                elif q.assessment.name == 'EQ':
                    if i < 10:
                        opt_val = random.choice([1, 2]) # Low EQ bias
                    else:
                        opt_val = random.choice([3, 4, 5])
                elif q.assessment.name == 'SQ':
                    opt_val = random.choice([2, 3, 4, 5])
                elif q.assessment.name == 'Home Adjustment Questionnaire':
                    if i < 6:
                        opt_val = 1 # True (High conflict)
                    else:
                        opt_val = random.choice([0, 1])
                else:
                    opt_val = 3
                    
                resp = Response(
                    session_id=session.id,
                    question_id=q.id,
                    selected_option=str(opt_val),
                    time_taken_seconds=random.randint(1, 10), # includes some impulsivity/skipped bounds
                    auto_submitted=(random.random() < 0.05)  # 5% chance of auto-skipped
                )
                db.session.add(resp)
                
            db.session.commit()
            
            # Run the scoring helper
            run_scoring_saver(session.id)
            print(f"Simulated session & ran scores for student: {profile.user.name}")
            
        print("Demo data seeding completed successfully!")

if __name__ == "__main__":
    seed_demo_data()
