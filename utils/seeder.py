import os
import sys

# Ensure the root directory is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Assessment, Question

def seed_assessments():
    """
    Seeds all 5 assessments (DASS-21, BFI-44, EQ, SQ, Home Adjustment Questionnaire)
    and their exact questions with categories, order numbers, JSON options, and reverse scored flags.
    Updates existing questions in place if they already exist.
    """
    # 1. BFI-44
    bfi_options = [
        {"value": 1, "label": "Disagree Strongly"},
        {"value": 2, "label": "Disagree a Little"},
        {"value": 3, "label": "Neither Agree nor Disagree"},
        {"value": 4, "label": "Agree a Little"},
        {"value": 5, "label": "Agree Strongly"}
    ]
    
    bfi_questions = [
        ("is talkative", "Extraversion", False),
        ("tends to find fault with others", "Agreeableness", True),
        ("does a thorough job", "Conscientiousness", False),
        ("is depressed, blue", "Neuroticism", False),
        ("is original, comes up with new ideas", "Openness", False),
        ("is reserved", "Extraversion", True),
        ("is helpful and unselfish", "Agreeableness", False),
        ("can be somewhat careless", "Conscientiousness", True),
        ("is relaxed and handles stress well", "Neuroticism", True),
        ("is curious about many different things", "Openness", False),
        ("is full of energy", "Extraversion", False),
        ("starts quarrels with others", "Agreeableness", True),
        ("is a reliable worker", "Conscientiousness", False),
        ("can be tense", "Neuroticism", False),
        ("is ingenious and a deep thinker", "Openness", False),
        ("generates a lot of enthusiasm", "Extraversion", False),
        ("has a forgiving nature", "Agreeableness", False),
        ("tends to be disorganized", "Conscientiousness", True),
        ("worries a lot", "Neuroticism", False),
        ("has an active imagination", "Openness", False),
        ("tends to be quiet", "Extraversion", True),
        ("is generally trusting", "Agreeableness", False),
        ("tends to be lazy", "Conscientiousness", True),
        ("is emotionally stable, not easily upset", "Neuroticism", True),
        ("is inventive", "Openness", False),
        ("has an assertive personality", "Extraversion", False),
        ("can be cold and aloof", "Agreeableness", True),
        ("perseveres until the task is finished", "Conscientiousness", False),
        ("can be moody", "Neuroticism", False),
        ("values artistic and aesthetic experiences", "Openness", False),
        ("is sometimes shy and inhibited", "Extraversion", True),
        ("is considerate and kind to almost everyone", "Agreeableness", False),
        ("does things efficiently", "Conscientiousness", False),
        ("remains calm in tense situations", "Neuroticism", True),
        ("prefers work that is routine", "Openness", True),
        ("is outgoing and sociable", "Extraversion", False),
        ("is sometimes rude to others", "Agreeableness", True),
        ("makes plans and follows through", "Conscientiousness", False),
        ("gets nervous easily", "Neuroticism", False),
        ("likes to reflect and play with ideas", "Openness", False),
        ("has few artistic interests", "Openness", True),
        ("likes to cooperate with others", "Agreeableness", False),
        ("is easily distracted", "Conscientiousness", True),
        ("is sophisticated in art/music/literature", "Openness", False),
    ]

    # 2. DASS-21
    dass_options = [
        {"value": 0, "label": "Did not apply to me at all"},
        {"value": 1, "label": "Applied to me to some degree or some of the time"},
        {"value": 2, "label": "Applied to me to a considerable degree or a good part of the time"},
        {"value": 3, "label": "Applied to me very much or most of the time"}
    ]
    
    dass_questions = [
        ("I found it hard to wind down.", "Stress", False),
        ("I was aware of dryness of my mouth.", "Anxiety", False),
        ("I couldn't seem to experience any positive feelings at all.", "Depression", False),
        ("I experienced breathing difficulty (excessively rapid breathing or breathlessness).", "Anxiety", False),
        ("I found it difficult to work up the initiative to do things.", "Depression", False),
        ("I tended to over-react to situations.", "Stress", False),
        ("I experienced trembling (e.g. in the hands).", "Anxiety", False),
        ("I felt that I was using a lot of nervous energy.", "Stress", False),
        ("I was worried about situations in which I might panic and make a fool of myself.", "Anxiety", False),
        ("I felt that I had nothing to look forward to.", "Depression", False),
        ("I found myself getting agitated.", "Stress", False),
        ("I found it difficult to relax.", "Stress", False),
        ("I felt down-hearted and blue.", "Depression", False),
        ("I was intolerant of anything that kept me from getting on with what I was doing.", "Stress", False),
        ("I felt I was close to panic.", "Anxiety", False),
        ("I was unable to become enthusiastic about anything.", "Depression", False),
        ("I felt I wasn't worth much as a person.", "Depression", False),
        ("I felt that I was rather touchy.", "Stress", False),
        ("I was aware of the action of my heart in the absence of physical exertion.", "Anxiety", False),
        ("I felt scared without any good reason.", "Anxiety", False),
        ("I felt that life was meaningless.", "Depression", False)
    ]

    # 3. EQ
    eq_options = [
        {"value": 1, "label": "Strongly Disagree"},
        {"value": 2, "label": "Disagree"},
        {"value": 3, "label": "Neutral"},
        {"value": 4, "label": "Agree"},
        {"value": 5, "label": "Strongly Agree"}
    ]
    
    eq_questions = [
        ("I can clearly identify what I am feeling.", "Emotional Awareness", False),
        ("I remain calm during stressful situations.", "Emotional Awareness", False),
        ("I think before reacting emotionally.", "Emotional Awareness", False),
        ("I understand why certain situations upset me.", "Emotional Awareness", False),
        ("I recover quickly after emotional setbacks.", "Emotional Awareness", False),
        ("I can control my anger appropriately.", "Emotional Awareness", False),
        ("I stay motivated even when things become difficult.", "Emotional Awareness", False),
        ("I can express my emotions in a healthy manner.", "Emotional Awareness", False)
    ]

    # 4. SQ
    sq_options = eq_options  # Same 1-5 scale
    
    sq_questions = [
        ("I can easily understand other people's feelings.", "Social Awareness", False),
        ("I communicate comfortably with new people.", "Social Awareness", False),
        ("I adjust well in different social environments.", "Social Awareness", False),
        ("I work effectively in group activities.", "Social Awareness", False),
        ("I resolve conflicts calmly and respectfully.", "Social Awareness", False),
        ("People usually find me approachable.", "Social Awareness", False),
        ("I understand social cues and body language well.", "Social Awareness", False),
        ("I maintain healthy interpersonal relationships.", "Social Awareness", False)
    ]

    # 5. HOME ADJUSTMENT
    home_options = [
        {"value": 0, "label": "Not True"},
        {"value": 1, "label": "True"}
    ]
    
    home_questions = [
        ("I often feel that at least one of my parents does not understand me.", "Home Adjustment", False),
        ("My parents always force me to obey them even if what they are saying is not right.", "Home Adjustment", False),
        ("I have frequently had to keep quiet or leave the house in order to have peace at home.", "Home Adjustment", False),
        ("I feel that my friends have a happier home life than me.", "Home Adjustment", False),
        ("I do not like the type of work my father does.", "Home Adjustment", False),
        ("I often doubt if my parents love me.", "Home Adjustment", False),
        ("My parents often beat me.", "Home Adjustment", False),
        ("My parents criticize me without any reason.", "Home Adjustment", False),
        ("I feel that my parents teach me one thing but do the other thing.", "Home Adjustment", False),
        ("My parents love my brother or sister more than me.", "Home Adjustment", False),
        ("I sometimes feel that my parents are disappointed in me.", "Home Adjustment", False),
        ("My parents often find fault with my conduct.", "Home Adjustment", False),
        ("I feel that my parents are very strict with me.", "Home Adjustment", False),
        ("My parents have certain habits which irritate me.", "Home Adjustment", False),
        ("I sometimes love and sometimes hate my family members.", "Home Adjustment", False)
    ]

    assessments_data = [
        {
            "name": "BFI-44",
            "description": "Big Five Inventory (BFI-44)",
            "questions": bfi_questions,
            "options": bfi_options,
            "bfi_prefix": "I see myself as someone who... "
        },
        {
            "name": "DASS-21",
            "description": "Depression Anxiety Stress Scale (DASS-21)",
            "questions": dass_questions,
            "options": dass_options,
            "bfi_prefix": None
        },
        {
            "name": "EQ",
            "description": "Emotional Quotient (EQ)",
            "questions": eq_questions,
            "options": eq_options,
            "bfi_prefix": None
        },
        {
            "name": "SQ",
            "description": "Social Quotient (SQ)",
            "questions": sq_questions,
            "options": sq_options,
            "bfi_prefix": None
        },
        {
            "name": "Home Adjustment Questionnaire",
            "description": "Home Adjustment Questionnaire",
            "questions": home_questions,
            "options": home_options,
            "bfi_prefix": None
        }
    ]

    for data in assessments_data:
        # Check if assessment exists
        assessment = Assessment.query.filter_by(name=data["name"]).first()
        if not assessment:
            assessment = Assessment(name=data["name"], description=data["description"])
            db.session.add(assessment)
            db.session.commit()
            assessment = Assessment.query.filter_by(name=data["name"]).first()
            
        # Check if questions already exist
        existing_qs = Question.query.filter_by(assessment_id=assessment.id).order_by(Question.order_number).all()
        
        if len(existing_qs) == len(data["questions"]):
            # Update existing questions in place
            for idx, q in enumerate(existing_qs):
                text, category, reverse = data["questions"][idx]
                full_text = text
                if data["bfi_prefix"]:
                    full_text = f"{data['bfi_prefix']}{text}"
                
                q.question_text = full_text
                q.category = category
                q.options = data["options"]
                q.reverse_scored = reverse
                q.order_number = idx + 1
            db.session.commit()
            print(f"Seeded {data['name']}: {len(data['questions'])} questions")
        else:
            # Delete and re-insert if count differs
            if len(existing_qs) > 0:
                Question.query.filter_by(assessment_id=assessment.id).delete()
                db.session.commit()
                
            # Insert all questions
            for idx, (text, category, reverse) in enumerate(data["questions"]):
                full_text = text
                if data["bfi_prefix"]:
                    full_text = f"{data['bfi_prefix']}{text}"
                    
                q = Question(
                    assessment_id=assessment.id,
                    question_text=full_text,
                    category=category,
                    options=data["options"],
                    order_number=idx + 1,
                    reverse_scored=reverse,
                    time_limit=10
                )
                db.session.add(q)
                
            db.session.commit()
            print(f"Seeded {data['name']}: {len(data['questions'])} questions")

if __name__ == "__main__":
    app = create_app('development')
    with app.app_context():
        seed_assessments()
