from flask import Flask,render_template,request,redirect, flash, url_for,session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta,date
from sqlalchemy import func,case
from rule_basedAi import *
app = Flask(__name__)
app.secret_key = "a_very_secret_key_12345"  # <--- add this line

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"check_same_thread": False}
}

db = SQLAlchemy(app)

class admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# users table (registration + login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self)->str:
        return f"{self.id}{self.username}"
#Interview schedule data 
class interview_data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(150), nullable=False)
    interview_type=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(100),nullable=False)
    date=db.Column(db.Date(),nullable=False)
    time=db.Column(db.Time(),nullable=False)
    score = db.Column(db.Float,nullable=True)
    status=db.Column(db.String(100),nullable=True)

@app.route('/')
def home_without_login():
    return render_template('home_without_login.html')

@app.route('/about-us')
def about(): 
    return render_template('about_us.html')

@app.route('/working')
def how_working():
    return render_template('how_it_works.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #store email and password into database 
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        #it used for email verification 
        if not user:
            flash("Email not registered! Please register first.", "warning")
            return redirect(url_for('register_new_user'))

        if not check_password_hash(user.password, password):
            flash("Incorrect password. Try again.", "danger")
            return redirect(url_for('login'))

        # ✅ Login success
        session['user_id'] = user.id
        session['user_name'] = user.f_name
        session['user_email'] = user.email

        flash("Login successful!", "success")
        return redirect(url_for('schedule_page'))

    return render_template('login.html')


@app.route('/admin_login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        admin_user = admin.query.filter_by(user_mail=email).first()

        if not admin_user:
            flash("Admin email not found!", "warning")
            return redirect(url_for('admin_login'))

        if not check_password_hash(admin_user.password, password):
            flash("Incorrect password!", "danger")
            return redirect(url_for('admin_login'))

        session['admin_id'] = admin_user.id
        session['admin_name'] = admin_user.f_name
        session['admin_email'] = admin_user.user_mail

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_login.html')

@app.route('/admin_register', methods=['GET','POST'])
def admin_register():

    if request.method == 'POST':

        try:
            name = request.form.get('f_name')
            email = request.form.get('email')
            password = request.form.get('password')
            c_password = request.form.get('c_password')

            # Password match check
            if password != c_password:
                flash("Passwords do not match!", "danger")
                return redirect(url_for('admin_register'))

            # Check if admin already exists
            existing_admin = admin.query.filter_by(user_mail=email).first()

            if existing_admin:
                flash("Admin already exists with this email!", "warning")
                return redirect(url_for('admin_register'))

            # Hash password
            hashed_password = generate_password_hash(password)

            # Create new admin
            new_admin = admin(
                f_name=name,
                user_mail=email,
                password=hashed_password
            )

            db.session.add(new_admin)
            db.session.commit()

            return redirect(url_for('admin_login'))

        except Exception as e:
            db.session.rollback()
            print("Registration Error:", e)
            flash("Something went wrong while registering!", "danger")
            return redirect(url_for('admin_register'))

    return render_template('admin_register.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin_all_users')
def admin_all_users():

    users = User.query.all() # database मधून data fetch

    return render_template(
        'admin_all_users.html',
        users=users)

@app.route('/interview_count')
def interview_count():

    data = db.session.query(
        interview_data.email,
        func.count(interview_data.id).label('total_interviews')
    ).group_by(interview_data.email).all()

    return render_template(
        'interview_count.html',
        data=data
    )

@app.route('/role_wise')
def role_wise():

    data = db.session.query(
        interview_data.role,
        func.count(interview_data.id).label('total_interviews')
    ).group_by(interview_data.role).all()

    return render_template(
        'role_wise.html',
        data=data
    )

@app.route('/answer_quality')
def answer_quality():

    quality_data = db.session.query(
        case(
            (interview_data.score >= 80, "Excellent"),
            (interview_data.score >= 60, "Good"),
            (interview_data.score >= 40, "Average"),
            else_="Poor"
        ).label("quality"),
        func.count(interview_data.id)
    ).group_by("quality").all()

    return render_template(
        "answer_quality.html",
        data=quality_data
    )

@app.route('/type_priority')
def type_priority():

    data = db.session.query(
        interview_data.interview_type,
        func.count(interview_data.id).label('total_interviews')
    ).group_by(
        interview_data.interview_type
    ).order_by(
        func.count(interview_data.id).desc()
    ).all()

    return render_template(
        'type_priority.html',
        data=data
    )

@app.route('/role_priority')
def role_priority():

    data = db.session.query(
        interview_data.interview_type,
        func.count(interview_data.id).label("total")
    ).group_by(
        interview_data.interview_type
    ).order_by(
        func.count(interview_data.id).desc()
    ).all()

    return render_template(
        "role_priority.html",
        data=data
    )

@app.route('/daily_report')
def daily_report():

    today = date.today()

    # Total interviews scheduled today
    total_today = interview_data.query.filter_by(date=today).count()

    # Completed interviews
    completed_today = interview_data.query.filter_by(
        date=today,
        status="completed"
    ).count()

    # Not completed interviews
    not_completed = interview_data.query.filter_by(
        date=today,
        status="not completed"
    ).count()

    # Average score
    avg_score = db.session.query(
        func.avg(interview_data.score)
    ).filter(
        interview_data.date == today
    ).scalar()

    if avg_score:
        avg_score = round(avg_score, 2)
    else:
        avg_score = 0

    return render_template(
        "daily_report.html",
        total_today=total_today,
        completed_today=completed_today,
        not_completed=not_completed,
        avg_score=avg_score
    )

@app.route('/monthly_report')
def monthly_report():

    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Total interviews this month
    total_month = interview_data.query.filter(
        func.extract('month', interview_data.date) == current_month,
        func.extract('year', interview_data.date) == current_year
    ).count()

    # Completed interviews
    completed_month = interview_data.query.filter(
        func.extract('month', interview_data.date) == current_month,
        func.extract('year', interview_data.date) == current_year,
        interview_data.status == "completed"
    ).count()

    # Not completed interviews
    not_completed_month = interview_data.query.filter(
        func.extract('month', interview_data.date) == current_month,
        func.extract('year', interview_data.date) == current_year,
        interview_data.status == "not completed"
    ).count()

    # Average score
    avg_score = db.session.query(
        func.avg(interview_data.score)
    ).filter(
        func.extract('month', interview_data.date) == current_month,
        func.extract('year', interview_data.date) == current_year
    ).scalar()

    if avg_score:
        avg_score = round(avg_score, 2)
    else:
        avg_score = 0

    return render_template(
        "monthly_report.html",
        total_month=total_month,
        completed_month=completed_month,
        not_completed_month=not_completed_month,
        avg_score=avg_score
    )

@app.route('/weekly_report')
def weekly_report():

    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)

    # Total interviews this week
    total_week = interview_data.query.filter(
        interview_data.date >= week_start,
        interview_data.date <= week_end
    ).count()

    # Completed interviews
    completed_week = interview_data.query.filter(
        interview_data.date >= week_start,
        interview_data.date <= week_end,
        interview_data.status == "completed"
    ).count()

    # Not completed interviews
    not_completed_week = interview_data.query.filter(
        interview_data.date >= week_start,
        interview_data.date <= week_end,
        interview_data.status == "not completed"
    ).count()

    # Average score
    avg_score = db.session.query(
        func.avg(interview_data.score)
    ).filter(
        interview_data.date >= week_start,
        interview_data.date <= week_end
    ).scalar()

    if avg_score:
        avg_score = round(avg_score, 2)
    else:
        avg_score = 0

    return render_template(
        "weekly_report.html",
        total_week=total_week,
        completed_week=completed_week,
        not_completed_week=not_completed_week,
        avg_score=avg_score
    )

@app.route('/harder_section')
def harder_section():

    data = db.session.query(
        interview_data.role,
        func.avg(interview_data.score).label("avg_score")
    ).group_by(
        interview_data.role
    ).all()

    result = []

    for role, avg_score in data:

        if avg_score < 40:
            level = "Hard"
        elif avg_score < 70:
            level = "Medium"
        else:
            level = "Easy"

        result.append({
            "role": role,
            "avg_score": round(avg_score,2),
            "level": level
        })

    return render_template(
        "harder_section.html",
        data=result
    )

@app.route('/register_new_user', methods=['GET', 'POST'])
def register_new_user():
    if request.method == 'POST':
        f_name = request.form['f_name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        # 1️⃣ Password match check
        if password != c_password:
            flash("Password and Confirm Password do not match!", "danger")
            return redirect(url_for('register_new_user'))

        # 2️⃣ Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for('login'))

        # 3️⃣ Hash password
        hashed_password = generate_password_hash(password)

        # 4️⃣ Save user
        reg_user = User(
            f_name=f_name,
            email=email,
            password=hashed_password
        )
        db.session.add(reg_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register_new_file.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if email exists
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered!", "danger")
            return redirect(url_for('forgot_password'))

        # Check password match
        if new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('forgot_password'))

        # Hash new password
        hashed_password = generate_password_hash(new_password)

        # Update password in database
        user.password = hashed_password
        db.session.commit()

        flash("Password updated successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('forgot.html')

@app.route('/schedule_page', methods=['GET', 'POST'])
def schedule_page():
    if 'user_email' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        interview_type = request.form['interview_type']
        role = request.form['role']
        date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        time = datetime.strptime(request.form['time'], "%H:%M").time()

        email = session['user_email']

        # ✅ CHECK IF SAME INTERVIEW ALREADY EXISTS
        existing_interview = interview_data.query.filter_by(
            email=email,
            date=date,
            time=time
        ).first()

        if existing_interview:
            flash("You have already scheduled an interview at this date and time!", "danger")
            return redirect(url_for('schedule_page'))

        interviewer = interview_data(
        name=name,
        email=email,
        interview_type=interview_type,
        role=role,
        date=date,
        time=time,
        score=0,
        status="scheduled"
        )

        db.session.add(interviewer)
        db.session.commit()

        return redirect(url_for('upcoming_interview'))

    return render_template('home_with_login.html')

@app.route('/upcoming_interview')
def upcoming_interview():

    if 'user_email' not in session:
        return redirect(url_for('login'))

    user_email = session['user_email']

    interviews = interview_data.query.filter_by(
        email=user_email
    ).order_by(
        interview_data.date,
        interview_data.time
    ).all()

    now = datetime.now()

    for interview in interviews:

        interview.datetime_obj = datetime.combine(
            interview.date,
            interview.time
        )

        interview.datetime_str = interview.datetime_obj.strftime(
            "%d %b %Y, %I:%M %p"
        )

        join_start_time = interview.datetime_obj - timedelta(minutes=5)
        join_end_time = interview.datetime_obj + timedelta(minutes=1)

        # ⭐ STATUS STATE MACHINE
        if interview.status == "scheduled":

            if now > join_end_time:
                interview.status = "not completed"

        elif interview.score and interview.score > 0:
            interview.status = "completed"

        # Button Logic
        interview.can_join = (
            interview.status == "scheduled"
            and join_start_time <= now <= join_end_time
        )

        interview.is_missed = (
            interview.status == "scheduled"
            and now > join_end_time
        )

    db.session.commit()

    return render_template(
        "upcoming_interview.html",
        interviews=interviews,
        user_name=session.get('user_name')
    )

@app.route('/interview_conduct/<int:interview_id>')
def interview_conduct(interview_id):
    interview = interview_data.query.get_or_404(interview_id)

    session["current_interview_id"] = interview_id   # ✅ ADD THIS
    session[f"asked_{interview_id}"] = []
    session[f"scores_{interview_id}"] = {}  # also reset scores

    ai_message = get_welcome_message(
        interview.name,
        interview.role,
        interview.interview_type
    )

    return render_template(
        "interview_conduct.html",
        interview=interview,
        ai_message=ai_message
    )

@app.route('/interview_question/<int:interview_id>', methods=['POST'])
def interview_question(interview_id):

    interview = interview_data.query.get_or_404(interview_id)

    role = interview.role.strip().lower()
    interview_type = interview.interview_type.strip().lower()

    asked = session.get(f"asked_{interview_id}", [])
    scores = session.get(f"scores_{interview_id}", {})

    user_answer = request.json.get("user_answer", "") if request.is_json else ""

    # Evaluate previous answer
    if asked and user_answer:

        last_question = asked[-1]

        correct_answer = None

        for q in question_bank.get(role, {}).get(interview_type, []):
            if q["question"] == last_question:
                correct_answer = q["answer"]
                break

        if correct_answer:
            score = check_answer(user_answer, correct_answer)
            scores[last_question] = score

            session[f"scores_{interview_id}"] = scores

    # Next Question
    next_question = get_next_question(role, interview_type, asked)

    if next_question is None:

        # ⭐ End Interview Automatically
        total = sum(scores.values())
        final_score = round((total / max(len(asked),1)) * 100)

        interview.score = final_score

        if final_score >= 40:
            interview.status = "completed"
        else:
            interview.status = "not completed"

        db.session.commit()

        return jsonify({"redirect": url_for('feedback')})

    asked.append(next_question)
    session[f"asked_{interview_id}"] = asked

    return jsonify({"question": next_question})

@app.route('/end_interview_manual/<int:interview_id>', methods=['POST'])
def end_interview_manual(interview_id):
    interview = interview_data.query.get_or_404(interview_id)
    
    asked = session.get(f"asked_{interview_id}", []) or []
    scores = session.get(f"scores_{interview_id}", {}) or {}

    total = sum(scores.values())
    #final_score = round(total / max(len(asked),1), 2)
    final_score = round((total / max(len(asked),1)) * 100)

    interview.score = final_score
    interview.status = "completed" if final_score >= 0 else "not completed"
    db.session.commit()

    return redirect(url_for('feedback'))

@app.route('/feedback')
def feedback():

    interview_id = session.get("current_interview_id")

    if not interview_id:
        flash("No interview found!", "warning")
        return redirect(url_for('dashboard'))

    interview = interview_data.query.get(interview_id)

    return render_template(
        "feedback.html",
        total_score=interview.score if interview else 0,
        interview=interview
    )

@app.route('/dashboard')
def dashboard():

    if 'user_email' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('login'))

    user_email = session['user_email']
    now = datetime.now()

    interviews = interview_data.query.filter_by(
        email=user_email
    ).order_by(
        interview_data.date.desc()
    ).all()
    

    upcoming_interviews = []
    past_interviews = []
    for interview in interviews:

        interview_datetime = datetime.combine(
            interview.date,
            interview.time
        )

        interview.datetime_str = interview_datetime.strftime(
            "%d %b %Y, %I:%M %p"
        )

        join_start_time = interview_datetime - timedelta(minutes=5)
        join_end_time = interview_datetime + timedelta(minutes=10)

        # Default
        interview.can_join = False

        if (
            interview.status.lower() == "scheduled"
            or join_start_time <= now <= join_end_time
        ):
            interview.can_join = True
            upcoming_interviews.append(interview)

        else:
            past_interviews.append(interview)
    return render_template(
        "dashboard.html",
        upcoming_interviews=upcoming_interviews,
        past_interviews=past_interviews,
        user_name=session.get('user_name')
    )

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('home_without_login'))


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

with app.app_context():

    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
