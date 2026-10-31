from app import create_app, db
from app.models import Assessment, Question

app = create_app('development')

def update_questions():
    with app.app_context():
        # Update EQ questions
        eq = Assessment.query.filter_by(name='EQ').first()
        if eq:
            eq_qs = Question.query.filter_by(assessment_id=eq.id).order_by(Question.order_number).all()
            for i, q in enumerate(eq_qs):
                q.question_text = f"EQ Question {i+1}: I can easily tell if someone else wants to enter a conversation."
        
        # Update SQ questions
        sq = Assessment.query.filter_by(name='SQ').first()
        if sq:
            sq_qs = Question.query.filter_by(assessment_id=sq.id).order_by(Question.order_number).all()
            for i, q in enumerate(sq_qs):
                q.question_text = f"SQ Question {i+1}: I am fascinated by how machines work."
        
        db.session.commit()
        print("Questions updated successfully!")

if __name__ == '__main__':
    update_questions()
