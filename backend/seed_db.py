from flaskr import create_app
from models import db, Question, Category

app = create_app()

categories = [
    (1, "Science"), (2, "Art"), (3, "Geography"),
    (4, "History"), (5, "Entertainment"), (6, "Sports"),
]

questions = [
    (5, "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "Maya Angelou", 2, "4"),
    (9, "What boxer's original name is Cassius Clay?", "Muhammad Ali", 1, "4"),
    (2, "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", "Apollo 13", 4, "5"),
    (4, "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?", "Tom Cruise", 4, "5"),
    (6, "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", "Edward Scissorhands", 3, "5"),
    (10, "Which is the only team to play in every soccer World Cup tournament?", "Brazil", 3, "6"),
    (11, "Which country won the first ever soccer World Cup in 1930?", "Uruguay", 4, "6"),
    (12, "Who invented Peanut Butter?", "George Washington Carver", 2, "4"),
    (13, "What is the largest lake in Africa?", "Lake Victoria", 2, "3"),
    (14, "In which royal palace would you find the Hall of Mirrors?", "The Palace of Versailles", 3, "3"),
    (15, "The Taj Mahal is located in which Indian city?", "Agra", 2, "3"),
    (16, "Which Dutch graphic artist, initials M C, was a creator of optical illusions?", "Escher", 1, "2"),
    (17, "La Giaconda is better known as what?", "Mona Lisa", 3, "2"),
    (18, "How many paintings did Van Gogh sell in his lifetime?", "One", 4, "2"),
    (19, "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?", "Jackson Pollock", 2, "2"),
    (20, "What is the heaviest organ in the human body?", "The Liver", 4, "1"),
    (21, "Who discovered penicillin?", "Alexander Fleming", 3, "1"),
    (22, "Hematology is a branch of medicine involving the study of what?", "Blood", 4, "1"),
    (23, "Which dung beetle was worshipped by the ancient Egyptians?", "Scarab", 4, "4"),
]

with app.app_context():
    db.create_all()

    if Category.query.count() == 0:
        for _id, type_ in categories:
            db.session.add(Category(type=type_))
        db.session.commit()
        print(f"Seeded {len(categories)} categories.")
    else:
        print("Categories already seeded, skipping.")

    if Question.query.count() == 0:
        for _id, q, a, diff, cat in questions:
            db.session.add(Question(question=q, answer=a, category=cat, difficulty=diff))
        db.session.commit()
        print(f"Seeded {len(questions)} questions.")
    else:
        print("Questions already seeded, skipping.")

    print("Categories:", Category.query.count(), "Questions:", Question.query.count())
