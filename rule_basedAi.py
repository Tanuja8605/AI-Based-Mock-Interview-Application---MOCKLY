# rule_basedAi.py
import sqlite3
import re
from flask import Flask,session

app = Flask(__name__)  
# Example: database connection
conn = sqlite3.connect("interview.db")  # Interview table stored in interview.db
cursor = conn.cursor()

def get_welcome_message(user_name, role=None, interview_type=None):
    """
    Return AI welcome message based on user name, optionally role/type
    """
    return f"Hel lo {user_name}, welcome to your mock interview! Please introduce yourself."

def get_next_question(role, interview_type, asked):
    """
    Returns the next question for the user based on role and already asked questions
    """
    # Normalize role/interview_type
    role = role.lower().strip()
    interview_type = interview_type.lower().strip()

    questions = question_bank.get(role, {}).get(interview_type, [])

    for q in questions:
        if q["question"] not in asked:
            return q["question"]
    return None

def check_answer(user_answer, correct_answer):
    user_answer = user_answer.lower()
    correct_answer = correct_answer.lower()

    # Remove special characters
    user_answer = re.sub(r'[^a-z0-9 ]', '', user_answer)
    correct_answer = re.sub(r'[^a-z0-9 ]', '', correct_answer)

    # Remove extra spaces
    user_words = set(user_answer.split())
    correct_words = set(correct_answer.split())

    if not correct_words:
        return 0

    # Better matching (set intersection)
    match_count = len(user_words.intersection(correct_words))

    score = match_count / len(correct_words)

    return round(score, 2)
# role/type dependent questions
question_bank = {
    "python developer": {
        "technical": [
            {"question": "Explain what is Python's.", "answer": "Python is a high-level, interpreted programming language."},
            {"question": "What is list comprehension?", "answer": "A concise way to create lists in a single line."},
            {"question": "Explain decorators in Python.", "answer": "Functions that modify behavior of other functions without changing their code."},
            {"question": "What is Flask?", "answer": "Flask is a lightweight Python web framework."},
            {"question": "Explain dynamically typed language in Python.", "answer": "Python variables can change type during execution without explicit declaration."},
            {"question": "List vs Tuple vs Set differences.", "answer": "List is mutable, Tuple is immutable, Set stores unique unordered items."},
            {"question": "How do you handle exceptions in Python?", "answer": "Using try-except blocks and optionally finally for cleanup."},
            {"question": "Explain class and object in Python.", "answer": "Class is a blueprint; object is an instance of the class."},
            {"question": "How is inheritance implemented in Python?", "answer": "By passing parent class in parentheses when defining a class."},
            {"question": "Explain encapsulation, polymorphism, and abstraction with example.", "answer": "Encapsulation hides data, polymorphism allows multiple forms, abstraction hides implementation."},
            {"question": "How do you check if a key exists in a dictionary?", "answer": "Using 'key in dict' or dict.get() method."},
            {"question": "Explain stack and queue implementation in Python.", "answer": "Stack: LIFO, use list with append/pop; Queue: FIFO, use deque from collections."},
            {"question": "NumPy vs Pandas differences.", "answer": "NumPy is for numerical arrays, Pandas for tabular data with DataFrame and Series."},
            {"question": "How to visualize data using Matplotlib/Seaborn?", "answer": "Use plot(), scatter(), hist() in Matplotlib or sns.lineplot(), sns.barplot() in Seaborn."},
            {"question": "Explain basic workflow of TensorFlow/PyTorch.", "answer": "Define model, prepare data, forward pass, compute loss, backpropagate, update weights."}
        ],
        "managerial": [
            {"question": "Describe a time when you had to lead a team under tight deadlines.", "answer": "Explain a real-life scenario where leadership and time management helped complete tasks."},
            {"question": "How do you handle conflicts within your team?", "answer": "Listen to both sides, mediate, find common ground, resolve professionally."},
            {"question": "Give an example of a difficult decision you made and how you handled it.", "answer": "Describe decision-making process, challenges faced, and outcome."},
            {"question": "How do you prioritize tasks when managing multiple projects?", "answer": "Use urgency and importance matrix, delegate when necessary."},
            {"question": "Explain your approach to mentoring or developing team members.", "answer": "Provide guidance, training, feedback, and growth opportunities."},
            {"question": "How do you ensure effective communication within your team?", "answer": "Regular meetings, clear documentation, open feedback culture."},
            {"question": "Describe a situation where a project failed. How did you handle it?", "answer": "Explain lessons learned and corrective actions taken."},
            {"question": "How do you motivate your team to achieve targets?", "answer": "Recognition, incentives, clear goals, support and guidance."},
            {"question": "How do you handle underperforming team members?", "answer": "Identify root cause, provide training, monitor improvement, and feedback."},
            {"question": "What strategies do you use to manage cross-functional teams?", "answer": "Clear objectives, regular communication, align goals, resolve conflicts."},
            {"question": "How do you allocate resources for a project?", "answer": "Based on priorities, skill set, and project deadlines."},
            {"question": "Explain your experience with project management tools.", "answer": "Tools like Jira, Trello, MS Project to plan, track and manage tasks."},
            {"question": "How do you monitor project progress and ensure timely delivery?", "answer": "Regular updates, milestones, KPIs, and risk management."},
            {"question": "Describe your experience with budgeting and cost management.", "answer": "Tracking costs, resource allocation, and reporting to stakeholders."},
            {"question": "How do you assess risks and create mitigation plans for projects?", "answer": "Identify risks, evaluate impact, develop mitigation strategies."}
        ],
        "hr": [
    {"question": "How do you handle conflicts between team members?", "answer": "Mediating, listening to both sides, and resolving professionally."},
    {"question": "Describe your experience with recruitment or hiring processes.", "answer": "Posting jobs, screening resumes, interviews, onboarding."},
    {"question": "How do you ensure team engagement and motivation?", "answer": "Recognition, team-building activities, feedback, and support."},
    {"question": "Explain a time you implemented a policy change in your team.", "answer": "Describe policy, implementation steps, and outcome."},
    {"question": "How do you handle difficult conversations with employees?", "answer": "Prepare, listen actively, be clear and empathetic."},
    {"question": "What strategies do you use to manage high-performing and low-performing employees?", "answer": "Provide challenges for high performers, guidance for low performers."},
    {"question": "Describe a situation where you had to mediate between employees.", "answer": "Explain conflict, approach, resolution, and lessons learned."},
    {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and professional experience."},
    {"question": "Why do you want to work in this company?", "answer": "Explain your interest in the company and how your skills align with its goals."},
    {"question": "What are your strengths?", "answer": "Highlight strengths such as teamwork, problem solving, or leadership."},
    {"question": "What is your biggest weakness?", "answer": "Mention a weakness and explain how you are working to improve it."},
    {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career goals and growth plans."},
    {"question": "How do you handle stress or pressure at work?", "answer": "By prioritizing tasks, staying organized, and maintaining focus."},
    {"question": "Describe a challenge you faced at work and how you handled it.", "answer": "Explain the situation, actions taken, and results."},
    {"question": "Why should we hire you?", "answer": "Explain how your skills, experience, and attitude make you a good fit for the role."}
]
    },
    "java developer": {
    "technical": [
        {"question": "What is Java?", "answer": "Java is an object-oriented, platform-independent programming language."},
        {"question": "Explain JVM, JRE, and JDK.", "answer": "JVM runs Java bytecode, JRE provides runtime environment, JDK provides tools for development."},
        {"question": "What are OOP principles in Java?", "answer": "Encapsulation, Inheritance, Polymorphism, and Abstraction."},
        {"question": "What is the difference between ArrayList and LinkedList?", "answer": "ArrayList uses dynamic arrays while LinkedList uses nodes."},
        {"question": "Explain method overloading.", "answer": "Method overloading allows multiple methods with same name but different parameters."},
        {"question": "Explain method overriding.", "answer": "Method overriding allows a subclass to provide specific implementation of a parent class method."},
        {"question": "What is exception handling in Java?", "answer": "Handling runtime errors using try, catch, finally, throw, and throws."},
        {"question": "Difference between interface and abstract class.", "answer": "Interface defines contract with methods, abstract class can have both abstract and concrete methods."},
        {"question": "What is multithreading?", "answer": "Executing multiple threads simultaneously to improve performance."},
        {"question": "What is garbage collection?", "answer": "Automatic memory management that removes unused objects."},
        {"question": "Explain the Java Collections Framework.", "answer": "A framework providing classes like List, Set, Map for storing and manipulating data."},
        {"question": "Difference between HashMap and HashTable.", "answer": "HashMap is not synchronized, HashTable is synchronized."},
        {"question": "What is Spring Framework?", "answer": "A Java framework used for building enterprise applications."},
        {"question": "What is Spring Boot?", "answer": "Spring Boot simplifies Spring application setup with auto-configuration."},
        {"question": "Explain REST API in Java.", "answer": "REST APIs allow communication between client and server using HTTP methods."}
    ],

    "managerial": [
        {"question": "Describe a time when you led a development team.", "answer": "Explain leadership approach, responsibilities, and outcome."},
        {"question": "How do you manage multiple development tasks?", "answer": "Prioritize tasks based on urgency and importance."},
        {"question": "How do you ensure code quality in your team?", "answer": "Code reviews, testing, and coding standards."},
        {"question": "How do you handle tight deadlines?", "answer": "Prioritize work, delegate tasks, and maintain communication."},
        {"question": "Explain your experience with Agile methodology.", "answer": "Working in sprints, daily stand-ups, and iterative development."},
        {"question": "How do you mentor junior developers?", "answer": "Provide guidance, code reviews, and learning resources."},
        {"question": "How do you manage cross-functional teams?", "answer": "Clear communication, defined roles, and collaborative tools."},
        {"question": "How do you track project progress?", "answer": "Using project management tools like Jira or Trello."},
        {"question": "How do you deal with project delays?", "answer": "Identify causes, adjust timelines, and improve coordination."},
        {"question": "How do you allocate tasks in a team?", "answer": "Based on skillset and project requirements."},
        {"question": "How do you motivate your team?", "answer": "Recognition, growth opportunities, and supportive environment."},
        {"question": "How do you handle disagreements in technical decisions?", "answer": "Encourage discussion and evaluate solutions objectively."},
        {"question": "Explain your experience managing large software projects.", "answer": "Planning, resource allocation, monitoring, and delivery."},
        {"question": "How do you manage risk in software projects?", "answer": "Identify risks early and create mitigation strategies."},
        {"question": "How do you ensure timely delivery of projects?", "answer": "Milestones, regular monitoring, and proactive communication."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience."},
        {"question": "Why do you want to work as a Java developer?", "answer": "Explain your interest in Java technologies and development."},
        {"question": "What are your strengths?", "answer": "Mention technical and personal strengths relevant to the role."},
        {"question": "What are your weaknesses?", "answer": "Discuss a weakness and how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain your skills, experience, and value you bring."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain career growth goals."},
        {"question": "Describe a challenge you faced at work.", "answer": "Explain the problem, actions taken, and outcome."},
        {"question": "How do you handle stress at work?", "answer": "Prioritize tasks and stay organized."},
        {"question": "Describe a time you worked in a team.", "answer": "Explain teamwork experience and contribution."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and improve performance."},
        {"question": "What motivates you at work?", "answer": "Learning, solving problems, and achieving goals."},
        {"question": "How do you handle conflicts with colleagues?", "answer": "Discuss issues calmly and find mutual solutions."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative, innovative, and growth-oriented."},
        {"question": "How do you stay updated with new technologies?", "answer": "Online courses, documentation, and community learning."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by planning and prioritizing tasks effectively."}
    ]
},
"frontend developer": {
    "technical": [
        {"question": "What is HTML?", "answer": "HTML stands for HyperText Markup Language and is used to structure web pages."},
        {"question": "What is CSS?", "answer": "CSS is used to style and layout web pages including colors, fonts, and spacing."},
        {"question": "What is JavaScript?", "answer": "JavaScript is a scripting language used to add interactivity to web pages."},
        {"question": "Difference between HTML and HTML5.", "answer": "HTML5 includes new elements like video, audio, canvas, and better semantic structure."},
        {"question": "What is responsive web design?", "answer": "Designing websites that adapt to different screen sizes using media queries and flexible layouts."},
        {"question": "Explain Flexbox.", "answer": "Flexbox is a CSS layout module used to create flexible and responsive layouts."},
        {"question": "Explain CSS Grid.", "answer": "CSS Grid is a two-dimensional layout system for designing web page layouts."},
        {"question": "What is DOM?", "answer": "DOM (Document Object Model) represents the structure of a web page that JavaScript can manipulate."},
        {"question": "Difference between let, const, and var.", "answer": "var is function scoped, let and const are block scoped; const cannot be reassigned."},
        {"question": "What is event handling in JavaScript?", "answer": "Responding to user actions like clicks, keyboard input, or mouse events."},
        {"question": "What is AJAX?", "answer": "AJAX allows asynchronous communication between client and server without reloading the page."},
        {"question": "What is REST API?", "answer": "REST API allows communication between frontend and backend using HTTP methods."},
        {"question": "What is React?", "answer": "React is a JavaScript library used to build interactive user interfaces."},
        {"question": "What is state in React?", "answer": "State is an object that stores data that can change and affect component rendering."},
        {"question": "What is version control (Git)?", "answer": "Git is a system used to track changes in code and collaborate with developers."}
    ],

    "managerial": [
        {"question": "How do you manage multiple frontend tasks in a project?", "answer": "Prioritize tasks based on deadlines and importance."},
        {"question": "How do you ensure code quality in frontend development?", "answer": "Code reviews, linting tools, and testing."},
        {"question": "How do you handle tight deadlines in UI development?", "answer": "Break tasks into smaller steps and prioritize critical features."},
        {"question": "How do you coordinate with backend developers?", "answer": "Clear API communication and regular collaboration."},
        {"question": "How do you mentor junior frontend developers?", "answer": "Provide code reviews, guidance, and learning resources."},
        {"question": "How do you manage UI/UX feedback from stakeholders?", "answer": "Evaluate feedback and implement feasible improvements."},
        {"question": "How do you track progress in frontend projects?", "answer": "Using project management tools like Jira or Trello."},
        {"question": "How do you ensure responsive design across devices?", "answer": "Using media queries, testing on multiple screen sizes."},
        {"question": "How do you manage design consistency?", "answer": "Using design systems and reusable components."},
        {"question": "How do you handle conflicts in the development team?", "answer": "Encourage open discussion and resolve issues collaboratively."},
        {"question": "How do you handle client changes in UI requirements?", "answer": "Analyze impact and update tasks accordingly."},
        {"question": "How do you allocate frontend tasks in a team?", "answer": "Based on skillset and project priorities."},
        {"question": "How do you improve team productivity?", "answer": "Clear communication, proper planning, and collaboration."},
        {"question": "How do you ensure accessibility in web design?", "answer": "Following accessibility guidelines like WCAG."},
        {"question": "How do you ensure timely delivery of frontend features?", "answer": "Setting milestones and monitoring progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience."},
        {"question": "Why do you want to work as a frontend developer?", "answer": "Explain your interest in UI development and web technologies."},
        {"question": "What are your strengths?", "answer": "Mention strengths like creativity, problem solving, and coding skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience fit the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career growth goals."},
        {"question": "How do you handle stress at work?", "answer": "By planning tasks and staying organized."},
        {"question": "Describe a challenging project you worked on.", "answer": "Explain the challenge and how you solved it."},
        {"question": "How do you stay updated with new frontend technologies?", "answer": "Online courses, blogs, and developer communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration and teamwork."},
        {"question": "How do you handle criticism on your work?", "answer": "Accept feedback positively and improve."},
        {"question": "What motivates you in your work?", "answer": "Learning new technologies and solving problems."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and innovative environment."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by prioritizing and managing time effectively."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company and its products."}
    ]
},
"backend developer": {
    "technical": [
        {"question": "What is backend development?", "answer": "Backend development focuses on server-side logic, databases, APIs, and application performance."},
        {"question": "What is a REST API?", "answer": "REST API allows communication between client and server using HTTP methods like GET, POST, PUT, DELETE."},
        {"question": "What is the difference between GET and POST requests?", "answer": "GET retrieves data from server while POST sends data to the server."},
        {"question": "What is a database?", "answer": "A database is an organized collection of structured data stored electronically."},
        {"question": "Difference between SQL and NoSQL databases.", "answer": "SQL databases use structured tables while NoSQL databases store unstructured or flexible data."},
        {"question": "What is an ORM?", "answer": "ORM (Object Relational Mapping) allows developers to interact with databases using programming languages instead of SQL."},
        {"question": "Explain MVC architecture.", "answer": "MVC separates application into Model, View, and Controller for better organization."},
        {"question": "What is authentication?", "answer": "Authentication verifies the identity of a user before granting access."},
        {"question": "What is authorization?", "answer": "Authorization determines what actions a user is allowed to perform."},
        {"question": "What is API rate limiting?", "answer": "Rate limiting restricts the number of API requests a client can make within a certain time."},
        {"question": "What is caching?", "answer": "Caching stores frequently accessed data temporarily to improve performance."},
        {"question": "What is middleware?", "answer": "Middleware is software that connects different parts of an application and processes requests."},
        {"question": "What is Docker?", "answer": "Docker is a containerization tool used to package applications and their dependencies."},
        {"question": "What is load balancing?", "answer": "Load balancing distributes incoming network traffic across multiple servers."},
        {"question": "What is microservices architecture?", "answer": "Microservices architecture divides applications into small independent services."}
    ],

    "managerial": [
        {"question": "How do you manage multiple backend services in a project?", "answer": "Prioritize services based on business requirements and system dependencies."},
        {"question": "How do you ensure backend code quality?", "answer": "Through code reviews, automated testing, and coding standards."},
        {"question": "How do you handle tight deadlines in backend development?", "answer": "Prioritize critical tasks and maintain clear communication with the team."},
        {"question": "How do you coordinate with frontend developers?", "answer": "By clearly defining API contracts and maintaining communication."},
        {"question": "How do you mentor junior backend developers?", "answer": "Provide guidance, code reviews, and share best practices."},
        {"question": "How do you handle production issues?", "answer": "Analyze logs, identify root cause, and deploy fixes quickly."},
        {"question": "How do you track backend project progress?", "answer": "Using project management tools and regular team updates."},
        {"question": "How do you ensure system scalability?", "answer": "Using scalable architecture, load balancing, and database optimization."},
        {"question": "How do you handle database performance issues?", "answer": "By optimizing queries, indexing, and caching."},
        {"question": "How do you handle team disagreements about system design?", "answer": "Encourage discussion and choose the most efficient technical solution."},
        {"question": "How do you allocate backend tasks in a team?", "answer": "Based on developer skills and project priorities."},
        {"question": "How do you manage risks in backend systems?", "answer": "Identify potential issues early and prepare mitigation plans."},
        {"question": "How do you improve team productivity?", "answer": "By improving workflows, automation, and communication."},
        {"question": "How do you ensure system security?", "answer": "Implement authentication, authorization, and secure coding practices."},
        {"question": "How do you ensure timely delivery of backend features?", "answer": "Set milestones and continuously monitor progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience."},
        {"question": "Why do you want to work as a backend developer?", "answer": "Explain your interest in server-side development and system design."},
        {"question": "What are your strengths?", "answer": "Mention strengths like problem-solving, logical thinking, and coding skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience fit the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your long-term career goals."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and staying organized."},
        {"question": "Describe a challenging backend problem you solved.", "answer": "Explain the problem, approach, and outcome."},
        {"question": "How do you stay updated with backend technologies?", "answer": "Through documentation, courses, and developer communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration and communication in development projects."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and use it to improve."},
        {"question": "What motivates you in backend development?", "answer": "Solving complex problems and building scalable systems."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and growth-oriented workplace."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing tasks effectively."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company and its services."}
    ]
},
"full stack developer": {
    "technical": [
        {"question": "What is a Full Stack Developer?", "answer": "A Full Stack Developer works on both frontend and backend development of web applications."},
        {"question": "What technologies are used in frontend development?", "answer": "HTML, CSS, JavaScript, and frameworks like React, Angular, or Vue."},
        {"question": "What technologies are used in backend development?", "answer": "Languages like Python, Java, Node.js and frameworks like Flask, Django, or Spring."},
        {"question": "What is REST API?", "answer": "REST API enables communication between frontend and backend using HTTP methods."},
        {"question": "What is a database?", "answer": "A database stores and manages application data efficiently."},
        {"question": "Difference between SQL and NoSQL databases.", "answer": "SQL databases use structured tables while NoSQL databases store flexible or unstructured data."},
        {"question": "What is version control?", "answer": "Version control like Git helps track changes and collaborate in code development."},
        {"question": "What is authentication?", "answer": "Authentication verifies the identity of a user before granting access."},
        {"question": "What is authorization?", "answer": "Authorization determines the permissions a user has in the system."},
        {"question": "What is responsive web design?", "answer": "Designing websites that adapt to different screen sizes and devices."},
        {"question": "Explain MVC architecture.", "answer": "MVC separates application logic into Model, View, and Controller."},
        {"question": "What is API integration?", "answer": "API integration allows different systems or services to communicate with each other."},
        {"question": "What is Docker?", "answer": "Docker is a containerization platform used to deploy applications consistently."},
        {"question": "What is CI/CD?", "answer": "CI/CD automates testing and deployment of applications."},
        {"question": "What is microservices architecture?", "answer": "An architecture where applications are divided into small independent services."}
    ],

    "managerial": [
        {"question": "How do you manage both frontend and backend tasks?", "answer": "Prioritize tasks and allocate time efficiently between frontend and backend work."},
        {"question": "How do you ensure code quality in full stack projects?", "answer": "Through code reviews, testing, and coding standards."},
        {"question": "How do you handle tight deadlines in development projects?", "answer": "Prioritize important features and maintain communication with the team."},
        {"question": "How do you coordinate between frontend and backend teams?", "answer": "By defining clear APIs and maintaining communication."},
        {"question": "How do you mentor junior developers?", "answer": "Provide guidance, code reviews, and learning support."},
        {"question": "How do you manage project requirements changes?", "answer": "Analyze impact and update development plans accordingly."},
        {"question": "How do you track development progress?", "answer": "Using project management tools like Jira or Trello."},
        {"question": "How do you ensure scalability of applications?", "answer": "By using scalable architecture and efficient system design."},
        {"question": "How do you handle production bugs?", "answer": "Identify the issue quickly and deploy fixes after testing."},
        {"question": "How do you manage collaboration in development teams?", "answer": "Encourage communication and teamwork."},
        {"question": "How do you allocate development tasks?", "answer": "Based on skill sets and project priorities."},
        {"question": "How do you manage risks in software projects?", "answer": "Identify potential risks and prepare mitigation plans."},
        {"question": "How do you improve team productivity?", "answer": "By optimizing workflows and encouraging collaboration."},
        {"question": "How do you ensure application security?", "answer": "Implement secure coding practices and authentication mechanisms."},
        {"question": "How do you ensure timely delivery of features?", "answer": "By setting milestones and monitoring project progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and development experience."},
        {"question": "Why do you want to work as a full stack developer?", "answer": "Explain your interest in working on both frontend and backend systems."},
        {"question": "What are your strengths?", "answer": "Mention strengths such as problem solving, adaptability, and coding skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience match the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career growth goals."},
        {"question": "How do you handle stress at work?", "answer": "By planning tasks and staying organized."},
        {"question": "Describe a challenging project you worked on.", "answer": "Explain the challenge and how you solved it."},
        {"question": "How do you stay updated with new technologies?", "answer": "Online learning, documentation, and developer communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain teamwork and collaboration in development projects."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and improve your work."},
        {"question": "What motivates you as a developer?", "answer": "Learning new technologies and solving complex problems."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and innovative environment."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing tasks effectively."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company and its products/services."}
    ]
},
"data analyst": {
    "technical": [
        {"question": "What is data analysis?", "answer": "Data analysis is the process of inspecting, cleaning, transforming, and modeling data to discover useful insights."},
        {"question": "What tools are commonly used by data analysts?", "answer": "Common tools include Excel, SQL, Python, R, Power BI, and Tableau."},
        {"question": "What is SQL?", "answer": "SQL is a language used to manage and query relational databases."},
        {"question": "What is the difference between INNER JOIN and LEFT JOIN?", "answer": "INNER JOIN returns matching records from both tables, while LEFT JOIN returns all records from the left table and matching records from the right table."},
        {"question": "What is data cleaning?", "answer": "Data cleaning is the process of removing errors, duplicates, and inconsistencies from data."},
        {"question": "What is data visualization?", "answer": "Data visualization is presenting data in graphical formats like charts and dashboards."},
        {"question": "What is a dashboard?", "answer": "A dashboard is a visual interface that displays key metrics and insights."},
        {"question": "What is the difference between structured and unstructured data?", "answer": "Structured data is organized in tables, while unstructured data includes text, images, or videos."},
        {"question": "What is descriptive analytics?", "answer": "Descriptive analytics summarizes past data to understand what happened."},
        {"question": "What is a KPI?", "answer": "KPI (Key Performance Indicator) is a measurable value used to evaluate performance."},
        {"question": "What is the difference between mean, median, and mode?", "answer": "Mean is average value, median is middle value, and mode is most frequent value."},
        {"question": "What is data normalization?", "answer": "Data normalization organizes data to reduce redundancy and improve integrity."},
        {"question": "What is Pandas in Python?", "answer": "Pandas is a Python library used for data manipulation and analysis."},
        {"question": "What is NumPy?", "answer": "NumPy is a Python library used for numerical computing and array operations."},
        {"question": "What is ETL?", "answer": "ETL stands for Extract, Transform, Load and is used for data integration."}
    ],

    "managerial": [
        {"question": "How do you manage multiple data analysis projects?", "answer": "Prioritize tasks based on deadlines and business importance."},
        {"question": "How do you ensure data accuracy in reports?", "answer": "By validating data sources and performing data cleaning."},
        {"question": "How do you communicate insights to non-technical stakeholders?", "answer": "Using simple explanations and visualizations."},
        {"question": "How do you prioritize business requirements for analysis?", "answer": "Focus on high-impact problems and stakeholder needs."},
        {"question": "How do you handle tight deadlines in data projects?", "answer": "Break tasks into smaller steps and prioritize critical analysis."},
        {"question": "How do you collaborate with other departments?", "answer": "Through meetings, clear communication, and shared goals."},
        {"question": "How do you ensure your analysis supports business decisions?", "answer": "By aligning analysis with business objectives and KPIs."},
        {"question": "How do you manage large datasets?", "answer": "Using optimized queries, data pipelines, and efficient tools."},
        {"question": "How do you ensure consistency in reports?", "answer": "Using standardized data sources and templates."},
        {"question": "How do you handle conflicting data from multiple sources?", "answer": "Verify sources and validate data accuracy."},
        {"question": "How do you track project progress?", "answer": "Using project management tools and regular updates."},
        {"question": "How do you mentor junior analysts?", "answer": "Provide guidance, training, and feedback."},
        {"question": "How do you identify business problems through data?", "answer": "By analyzing trends and patterns in data."},
        {"question": "How do you improve team productivity?", "answer": "By automating repetitive tasks and improving workflows."},
        {"question": "How do you ensure timely delivery of reports?", "answer": "By setting milestones and monitoring progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and data analysis experience."},
        {"question": "Why do you want to become a data analyst?", "answer": "Explain your interest in working with data and extracting insights."},
        {"question": "What are your strengths?", "answer": "Mention strengths like analytical thinking and problem-solving."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience fit the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career goals in data analytics."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and staying organized."},
        {"question": "Describe a challenging data problem you solved.", "answer": "Explain the problem, approach, and outcome."},
        {"question": "How do you stay updated with new data technologies?", "answer": "Online courses, blogs, and analytics communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration in data projects."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and use it to improve."},
        {"question": "What motivates you in data analytics?", "answer": "Finding insights that help businesses make better decisions."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and data-driven workplace."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing tasks."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company's business and data needs."}
    ]
},
"data scientist": {
    "technical": [
        {"question": "What is Data Science?", "answer": "Data Science is the field of extracting insights and knowledge from data using statistics, machine learning, and programming."},
        {"question": "What is the difference between Data Science and Data Analytics?", "answer": "Data Analytics focuses on analyzing past data, while Data Science uses machine learning to predict future outcomes."},
        {"question": "What is Machine Learning?", "answer": "Machine Learning is a method where computers learn patterns from data without being explicitly programmed."},
        {"question": "Explain supervised learning.", "answer": "Supervised learning is a machine learning technique where models are trained using labeled data."},
        {"question": "Explain unsupervised learning.", "answer": "Unsupervised learning finds hidden patterns in unlabeled data."},
        {"question": "What is a regression model?", "answer": "Regression is used to predict continuous values such as price or sales."},
        {"question": "What is classification in machine learning?", "answer": "Classification predicts categorical outcomes such as spam or not spam."},
        {"question": "What is overfitting?", "answer": "Overfitting occurs when a model learns training data too well and performs poorly on new data."},
        {"question": "What is underfitting?", "answer": "Underfitting happens when a model is too simple to capture patterns in the data."},
        {"question": "What is feature engineering?", "answer": "Feature engineering is the process of selecting and transforming variables to improve model performance."},
        {"question": "What is cross validation?", "answer": "Cross validation is a technique to evaluate model performance by splitting data into multiple training and testing sets."},
        {"question": "What is the difference between precision and recall?", "answer": "Precision measures correctness of positive predictions, while recall measures how many actual positives were identified."},
        {"question": "What is Pandas in Python?", "answer": "Pandas is a Python library used for data manipulation and analysis."},
        {"question": "What is NumPy?", "answer": "NumPy is a Python library used for numerical operations and array processing."},
        {"question": "What is TensorFlow or PyTorch?", "answer": "They are machine learning frameworks used for building and training deep learning models."}
    ],

    "managerial": [
        {"question": "How do you manage multiple data science projects?", "answer": "Prioritize projects based on business impact and deadlines."},
        {"question": "How do you communicate complex models to non-technical stakeholders?", "answer": "Using visualizations and simple explanations."},
        {"question": "How do you ensure model accuracy?", "answer": "By proper data preprocessing, validation, and performance evaluation."},
        {"question": "How do you handle missing or incomplete data?", "answer": "Using techniques like imputation or removing invalid records."},
        {"question": "How do you prioritize business problems for analysis?", "answer": "Focus on problems with highest business value."},
        {"question": "How do you collaborate with engineering teams?", "answer": "Through clear documentation and communication of model requirements."},
        {"question": "How do you track project progress?", "answer": "Using project management tools and regular updates."},
        {"question": "How do you ensure scalability of machine learning models?", "answer": "By optimizing algorithms and deploying scalable infrastructure."},
        {"question": "How do you handle conflicting results from different models?", "answer": "Compare metrics and choose the most reliable model."},
        {"question": "How do you manage large datasets?", "answer": "Using distributed computing tools and optimized queries."},
        {"question": "How do you mentor junior data scientists?", "answer": "Provide guidance, code reviews, and learning resources."},
        {"question": "How do you ensure ethical use of data?", "answer": "By following privacy regulations and ethical guidelines."},
        {"question": "How do you improve team productivity?", "answer": "Automate repetitive tasks and encourage collaboration."},
        {"question": "How do you validate business impact of a model?", "answer": "Measure improvements in key business metrics."},
        {"question": "How do you ensure timely project delivery?", "answer": "By setting milestones and monitoring progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience in data science."},
        {"question": "Why do you want to become a data scientist?", "answer": "Explain your interest in solving problems using data and machine learning."},
        {"question": "What are your strengths?", "answer": "Mention strengths such as analytical thinking and problem solving."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience fit the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career growth goals."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and staying organized."},
        {"question": "Describe a challenging data science project you worked on.", "answer": "Explain the problem, approach, and outcome."},
        {"question": "How do you stay updated with new technologies?", "answer": "Online courses, research papers, and developer communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration in data science projects."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and use it to improve."},
        {"question": "What motivates you in data science?", "answer": "Solving complex problems and discovering insights from data."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and data-driven workplace."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing tasks effectively."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company's business and data needs."}
    ]
},
"AI/ML Engineer": {
    "technical": [
        {"question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence is the simulation of human intelligence in machines that can learn and make decisions."},
        {"question": "What is Machine Learning?", "answer": "Machine Learning is a subset of AI where machines learn patterns from data without being explicitly programmed."},
        {"question": "What is Deep Learning?", "answer": "Deep Learning is a subset of machine learning that uses neural networks with multiple layers."},
        {"question": "What is the difference between supervised and unsupervised learning?", "answer": "Supervised learning uses labeled data while unsupervised learning uses unlabeled data."},
        {"question": "What is reinforcement learning?", "answer": "Reinforcement learning is a technique where an agent learns by interacting with an environment and receiving rewards or penalties."},
        {"question": "What is a neural network?", "answer": "A neural network is a computational model inspired by the human brain used to recognize patterns."},
        {"question": "What is overfitting?", "answer": "Overfitting occurs when a model performs well on training data but poorly on new data."},
        {"question": "What is underfitting?", "answer": "Underfitting occurs when a model is too simple to capture patterns in the data."},
        {"question": "What is feature engineering?", "answer": "Feature engineering is the process of selecting and transforming input variables to improve model performance."},
        {"question": "What is model evaluation?", "answer": "Model evaluation measures the performance of a machine learning model using metrics like accuracy or F1-score."},
        {"question": "What is the difference between TensorFlow and PyTorch?", "answer": "Both are deep learning frameworks, TensorFlow is widely used in production while PyTorch is popular for research."},
        {"question": "What is Natural Language Processing (NLP)?", "answer": "NLP is a field of AI that enables machines to understand and process human language."},
        {"question": "What is Computer Vision?", "answer": "Computer Vision enables machines to interpret and understand visual information from images or videos."},
        {"question": "What is transfer learning?", "answer": "Transfer learning uses a pre-trained model and adapts it for a new task."},
        {"question": "What is model deployment?", "answer": "Model deployment is the process of integrating a trained model into a production environment."}
    ],

    "managerial": [
        {"question": "How do you manage multiple AI/ML projects?", "answer": "Prioritize projects based on business value and deadlines."},
        {"question": "How do you ensure model accuracy?", "answer": "Through proper data preprocessing, validation, and hyperparameter tuning."},
        {"question": "How do you communicate AI insights to non-technical stakeholders?", "answer": "Using visualizations and simplified explanations."},
        {"question": "How do you handle large datasets?", "answer": "Using distributed computing and optimized data pipelines."},
        {"question": "How do you ensure scalability of AI models?", "answer": "By optimizing models and deploying them on scalable infrastructure."},
        {"question": "How do you collaborate with software engineers?", "answer": "By defining APIs and integrating models with applications."},
        {"question": "How do you track AI project progress?", "answer": "Using project management tools and regular team updates."},
        {"question": "How do you ensure ethical use of AI?", "answer": "By following responsible AI guidelines and avoiding biased datasets."},
        {"question": "How do you mentor junior AI engineers?", "answer": "Provide guidance, code reviews, and learning resources."},
        {"question": "How do you handle model failures in production?", "answer": "Monitor performance, analyze logs, and retrain models if necessary."},
        {"question": "How do you evaluate different machine learning models?", "answer": "By comparing metrics like accuracy, precision, recall, and F1-score."},
        {"question": "How do you improve team productivity?", "answer": "By automating workflows and encouraging collaboration."},
        {"question": "How do you manage risks in AI systems?", "answer": "Identify potential risks early and create mitigation plans."},
        {"question": "How do you ensure data quality for AI models?", "answer": "Through proper data validation and preprocessing."},
        {"question": "How do you ensure timely delivery of AI solutions?", "answer": "By setting milestones and monitoring project progress."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience in AI/ML."},
        {"question": "Why do you want to become an AI/ML engineer?", "answer": "Explain your interest in artificial intelligence and machine learning."},
        {"question": "What are your strengths?", "answer": "Mention strengths such as analytical thinking and problem solving."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience fit the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career growth goals."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and staying organized."},
        {"question": "Describe a challenging AI project you worked on.", "answer": "Explain the problem, approach, and results."},
        {"question": "How do you stay updated with new AI technologies?", "answer": "Through research papers, courses, and developer communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration in AI development projects."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and improve."},
        {"question": "What motivates you in AI development?", "answer": "Solving complex problems and building intelligent systems."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and innovation-driven environment."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing tasks."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company's work in AI or technology."}
    ]
},
"devOps engineer": {
    "technical": [
        {"question": "What is DevOps?", "answer": "DevOps is a set of practices that combines software development and IT operations to improve collaboration and automate workflows."},
        {"question": "What is CI/CD?", "answer": "CI/CD stands for Continuous Integration and Continuous Deployment, used to automate testing and deployment of applications."},
        {"question": "What is Docker?", "answer": "Docker is a containerization platform that packages applications and their dependencies into containers."},
        {"question": "What is Kubernetes?", "answer": "Kubernetes is a container orchestration platform used to manage and scale containerized applications."},
        {"question": "What is Infrastructure as Code (IaC)?", "answer": "IaC is the process of managing infrastructure using code instead of manual configuration."},
        {"question": "What is Jenkins?", "answer": "Jenkins is an open-source automation server used for building, testing, and deploying applications."},
        {"question": "What is version control?", "answer": "Version control systems like Git help track changes in code and enable collaboration among developers."},
        {"question": "What is configuration management?", "answer": "Configuration management tools like Ansible or Puppet automate system configuration."},
        {"question": "What is monitoring in DevOps?", "answer": "Monitoring tracks system performance, availability, and errors using tools like Prometheus or Grafana."},
        {"question": "What is load balancing?", "answer": "Load balancing distributes incoming traffic across multiple servers to improve performance and reliability."},
        {"question": "What is cloud computing?", "answer": "Cloud computing provides on-demand access to computing resources such as servers and storage over the internet."},
        {"question": "What is AWS?", "answer": "AWS is a cloud platform that provides services like computing, storage, and networking."},
        {"question": "What is container orchestration?", "answer": "Container orchestration manages container deployment, scaling, and networking."},
        {"question": "What is blue-green deployment?", "answer": "Blue-green deployment is a strategy that reduces downtime by running two environments simultaneously."},
        {"question": "What is microservices architecture?", "answer": "Microservices architecture divides applications into small independent services."}
    ],

    "managerial": [
        {"question": "How do you manage multiple DevOps pipelines?", "answer": "Prioritize pipelines based on project needs and automate workflows."},
        {"question": "How do you ensure system reliability?", "answer": "By implementing monitoring, alerting, and failover strategies."},
        {"question": "How do you handle production outages?", "answer": "Identify root cause quickly and restore services using backup or rollback."},
        {"question": "How do you collaborate with development teams?", "answer": "By improving communication and integrating DevOps tools into workflows."},
        {"question": "How do you ensure security in DevOps pipelines?", "answer": "By implementing secure coding practices and automated security checks."},
        {"question": "How do you manage infrastructure costs?", "answer": "By optimizing resource usage and using cloud monitoring tools."},
        {"question": "How do you ensure scalability of systems?", "answer": "By using load balancing, auto-scaling, and container orchestration."},
        {"question": "How do you track DevOps project progress?", "answer": "Using project management tools and monitoring dashboards."},
        {"question": "How do you mentor junior DevOps engineers?", "answer": "Provide guidance, training, and code reviews."},
        {"question": "How do you improve deployment speed?", "answer": "By automating CI/CD pipelines and reducing manual steps."},
        {"question": "How do you handle configuration drift?", "answer": "Using infrastructure as code and configuration management tools."},
        {"question": "How do you manage risks in production systems?", "answer": "By implementing backup systems and disaster recovery plans."},
        {"question": "How do you improve team productivity?", "answer": "Automate repetitive tasks and streamline workflows."},
        {"question": "How do you evaluate DevOps tools?", "answer": "Based on scalability, integration capability, and reliability."},
        {"question": "How do you ensure timely delivery of deployments?", "answer": "By setting milestones and monitoring pipeline performance."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and DevOps experience."},
        {"question": "Why do you want to work as a DevOps engineer?", "answer": "Explain your interest in automation and infrastructure management."},
        {"question": "What are your strengths?", "answer": "Mention strengths like problem solving and automation skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience match the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career goals in DevOps and cloud technologies."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and maintaining system monitoring."},
        {"question": "Describe a challenging DevOps problem you solved.", "answer": "Explain the problem, approach, and outcome."},
        {"question": "How do you stay updated with new DevOps tools?", "answer": "Through documentation, online courses, and communities."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration between development and operations teams."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and improve."},
        {"question": "What motivates you in DevOps?", "answer": "Improving system efficiency and automation."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and technology-driven environment."},
        {"question": "Are you comfortable working under pressure?", "answer": "Yes, especially during deployments or incident resolution."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company's products and infrastructure."}
    ]
},
"automation tester": {
    "technical": [
        {"question": "What is automation testing?", "answer": "Automation testing uses software tools to execute test cases automatically, reducing manual effort."},
        {"question": "What are the benefits of automation testing?", "answer": "Faster execution, reusability of test scripts, higher accuracy, and consistent results."},
        {"question": "What is Selenium?", "answer": "Selenium is an open-source automation tool used for web application testing."},
        {"question": "What is the difference between Selenium WebDriver and Selenium RC?", "answer": "WebDriver interacts directly with browsers while RC requires a server for communication."},
        {"question": "What is TestNG?", "answer": "TestNG is a testing framework used with Selenium to manage test execution and reporting."},
        {"question": "What is the difference between functional and non-functional testing?", "answer": "Functional testing verifies features work correctly, non-functional testing checks performance, security, etc."},
        {"question": "What are locators in Selenium?", "answer": "Locators identify elements on a web page, like ID, Name, XPath, CSS Selector."},
        {"question": "What is the difference between assert and verify in Selenium?", "answer": "Assert stops execution on failure, verify continues execution after failure."},
        {"question": "What is a test script?", "answer": "A test script is a set of instructions written to test a particular functionality of an application."},
        {"question": "What is continuous integration (CI) in testing?", "answer": "CI automates build and testing processes whenever code changes are committed."},
        {"question": "What is the difference between manual and automation testing?", "answer": "Manual testing is done by humans executing test cases; automation uses tools/scripts."},
        {"question": "What is data-driven testing?", "answer": "Data-driven testing runs the same test with multiple data sets to check different scenarios."},
        {"question": "What is keyword-driven testing?", "answer": "Keyword-driven testing uses keywords to represent actions, making scripts reusable and readable."},
        {"question": "What is the Page Object Model (POM)?", "answer": "POM is a design pattern that separates UI locators and test scripts for maintainability."},
        {"question": "What is the difference between smoke testing and regression testing?", "answer": "Smoke testing checks basic functionality; regression testing checks that new changes did not break existing features."}
    ],

    "managerial": [
        {"question": "How do you plan and prioritize automation testing tasks?", "answer": "By evaluating test coverage, business impact, and deadlines."},
        {"question": "How do you ensure test coverage is sufficient?", "answer": "By analyzing requirements, use cases, and previous defects."},
        {"question": "How do you manage multiple automation projects?", "answer": "Prioritize tasks, assign resources, and monitor progress using tracking tools."},
        {"question": "How do you integrate automated tests into CI/CD pipelines?", "answer": "By configuring tools like Jenkins to run automated tests on each build."},
        {"question": "How do you ensure test scripts are maintainable?", "answer": "By following coding standards, using POM, and modularizing scripts."},
        {"question": "How do you handle failing test scripts?", "answer": "Analyze the root cause, fix scripts or report issues to the development team."},
        {"question": "How do you communicate automation results to stakeholders?", "answer": "Through dashboards, reports, and summaries with actionable insights."},
        {"question": "How do you measure the ROI of automation testing?", "answer": "By comparing time and effort saved versus manual testing costs."},
        {"question": "How do you manage test environments?", "answer": "By using versioned environments, configuration management, and automation."},
        {"question": "How do you mentor junior automation testers?", "answer": "Provide guidance, review scripts, and share best practices."},
        {"question": "How do you ensure quality in automated testing?", "answer": "By implementing review processes, regression suites, and robust test design."},
        {"question": "How do you handle last-minute requirement changes?", "answer": "Update test cases/scripts and prioritize high-impact changes."},
        {"question": "How do you improve team productivity?", "answer": "By automating repetitive tasks and optimizing test workflows."},
        {"question": "How do you assess risk in testing?", "answer": "By identifying critical modules and allocating more testing resources."},
        {"question": "How do you ensure timely delivery of testing?", "answer": "By tracking progress, managing dependencies, and optimizing test execution."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your background, skills, and experience in automation testing."},
        {"question": "Why do you want to work as an automation tester?", "answer": "Explain your interest in test automation and ensuring software quality."},
        {"question": "What are your strengths?", "answer": "Mention strengths like attention to detail, problem-solving, and scripting skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your skills and experience match the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career growth goals in QA and automation."},
        {"question": "How do you handle stress at work?", "answer": "By prioritizing tasks and staying organized during tight deadlines."},
        {"question": "Describe a challenging automation problem you solved.", "answer": "Explain the problem, approach, and results achieved."},
        {"question": "How do you stay updated with new automation tools?", "answer": "Through online courses, communities, and documentation."},
        {"question": "Describe your experience working in a team.", "answer": "Explain collaboration with developers, QA, and stakeholders."},
        {"question": "How do you handle criticism?", "answer": "Accept feedback positively and improve scripts or processes."},
        {"question": "What motivates you in automation testing?", "answer": "Ensuring high-quality software and reducing manual testing effort."},
        {"question": "Describe your ideal work environment.", "answer": "Collaborative and process-oriented QA team."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing time and prioritizing testing tasks effectively."},
        {"question": "What do you know about our company?", "answer": "Explain your understanding of the company's products, QA practices, and team."}
    ]
},
"UI/UX designer": {
    "technical": [
        {"question": "What is UI design?", "answer": "UI design focuses on the visual appearance and interactive elements of a product."},
        {"question": "What is UX design?", "answer": "UX design focuses on user experience, usability, and product functionality."},
        {"question": "What is the difference between UI and UX?", "answer": "UI focuses on visuals, UX focuses on user experience and usability."},
        {"question": "What is wireframing?", "answer": "Wireframing is creating a basic layout of a design before adding visual details."},
        {"question": "What is prototyping?", "answer": "Prototyping is creating interactive models of designs for testing."},
        {"question": "What tools do UI/UX designers use?", "answer": "Tools like Figma, Adobe XD, Sketch, and InVision."},
        {"question": "What is responsive design?", "answer": "Responsive design ensures designs adapt to different screen sizes."},
        {"question": "What is usability testing?", "answer": "Usability testing evaluates how easy a product is to use."},
        {"question": "What is user research?", "answer": "User research involves studying user behavior and needs."},
        {"question": "What are design systems?", "answer": "Design systems are reusable components and design guidelines."},
        {"question": "What is color theory in design?", "answer": "Color theory is the study of color combinations and visual harmony."},
        {"question": "What is typography?", "answer": "Typography is the art of arranging text to improve readability and appearance."},
        {"question": "What is information architecture?", "answer": "Information architecture organizes content in a structured way."},
        {"question": "What is user flow?", "answer": "User flow is the path a user takes to complete a task in a product."},
        {"question": "What is accessibility in design?", "answer": "Accessibility ensures products can be used by people with disabilities."}
    ],

    "managerial": [
        {"question": "How do you manage design projects?", "answer": "By prioritizing tasks, following design sprints, and communicating with teams."},
        {"question": "How do you collaborate with developers?", "answer": "By providing design specifications and reviewing implementations."},
        {"question": "How do you handle design feedback?", "answer": "By analyzing feedback and improving designs accordingly."},
        {"question": "How do you ensure design consistency?", "answer": "By using design systems and style guides."},
        {"question": "How do you manage multiple design tasks?", "answer": "By prioritizing based on business value and deadlines."},
        {"question": "How do you improve team productivity?", "answer": "By using design tools and reusable components."},
        {"question": "How do you handle client design changes?", "answer": "By evaluating impact and updating designs accordingly."},
        {"question": "How do you track design progress?", "answer": "Using project management tools and sprint reviews."},
        {"question": "How do you ensure user-centered design?", "answer": "By conducting user research and usability testing."},
        {"question": "How do you work with product managers?", "answer": "By aligning design with business goals and requirements."},
        {"question": "How do you handle tight design deadlines?", "answer": "By prioritizing core features and iterating quickly."},
        {"question": "How do you mentor junior designers?", "answer": "Provide feedback, guidance, and design best practices."},
        {"question": "How do you evaluate design quality?", "answer": "By usability, accessibility, and visual consistency."},
        {"question": "How do you measure design success?", "answer": "Using user engagement metrics and feedback."},
        {"question": "How do you manage design risks?", "answer": "By validating designs early through prototypes."}
    ],

    "hr": [
        {"question": "Tell me about yourself.", "answer": "Briefly explain your design background and experience."},
        {"question": "Why do you want to become a UI/UX designer?", "answer": "Explain your passion for design and user experience."},
        {"question": "What are your strengths?", "answer": "Mention creativity, attention to detail, and design skills."},
        {"question": "What are your weaknesses?", "answer": "Mention a weakness and explain how you are improving it."},
        {"question": "Why should we hire you?", "answer": "Explain how your design skills match the role."},
        {"question": "Where do you see yourself in 5 years?", "answer": "Explain your career goals in design."},
        {"question": "How do you handle stress?", "answer": "By organizing tasks and maintaining focus."},
        {"question": "Describe a challenging design project you worked on.", "answer": "Explain the challenge and solution."},
        {"question": "How do you stay updated with design trends?", "answer": "Through design communities, blogs, and courses."},
        {"question": "Describe your teamwork experience.", "answer": "Explain collaboration with developers and product teams."},
        {"question": "How do you handle design criticism?", "answer": "Accept feedback and improve designs."},
        {"question": "What motivates you in design?", "answer": "Creating user-friendly and visually appealing products."},
        {"question": "Describe your ideal work environment.", "answer": "Creative and collaborative environment."},
        {"question": "Are you comfortable working under deadlines?", "answer": "Yes, by managing design tasks efficiently."},
        {"question": "What do you know about our company?", "answer": "Explain your knowledge of the company products and design philosophy."}
    ]
}

}

if __name__ == "__main__":
    app.run(debug=True)

