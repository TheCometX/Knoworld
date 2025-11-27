class API:
    import html
    import json
    from random import choice, shuffle

    def get_questions():
        questionList = []
        numNames = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

        with open('trivia_api.json', 'r') as file:
            questions = API.json.load(file)
            while len(questionList) != 10:
                question = API.choice(questions["results"])
                if question["question"] not in [question[1] for question in questionList]:
                    questionNum = numNames[len(questionList)]
                    questionText = question["question"]
                    questionText = API.html.unescape(questionText)
                    questionOptions = [question["correct_answer"]] + question["incorrect_answers"]
                    API.shuffle(questionOptions)
                    correctAnswer = question["correct_answer"]
                    questionList.append([questionNum, questionText, questionOptions, correctAnswer])
        return questionList
        

class Database:
    import sqlite3

    def get_highestScore(username):
        conn = Database.sqlite3.connect('database.db')
        cursor = conn.cursor()
        object = cursor.execute('SELECT highestScore FROM results WHERE username = ?', (username,))
        list = object.fetchall()
        score = list[0][0]
        conn.close()
        return score
    
    def get_ranking():
        conn = Database.sqlite3.connect('database.db')
        cursor = conn.cursor()
        object = cursor.execute('SELECT username, highestScore FROM results ORDER BY highestScore DESC LIMIT 10')
        list = object.fetchall()
        ranking = [[x + 1, list[x][0], list[x][1]] for x in range(len(list))]
        return ranking
    
    def login(username, password):
        conn = System.sqlite3.connect('database.db')
        cursor = conn.cursor()
        object = cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        list = object.fetchall()
        conn.close()
        if list != []:
            correctPassword = list[0][0]
            hash = System.hashing(password)
            if hash == correctPassword:
                return True
        return False
    
    def register(username, password):
        conn = Database.sqlite3.connect('database.db')
        cursor = conn.cursor()
        object = cursor.execute('SELECT username FROM users')
        registredUsernames = [row[0] for row in object.fetchall()]
        if username not in registredUsernames:
            password = System.hashing(password)
            cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
            cursor.execute("INSERT INTO results(username, highestScore) VALUES(?, ?)", (username, 0))
            conn.commit()
            conn.close()
            return True
        else:
            return False
        
    def set_score(score, username):
        conn = Database.sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE results SET highestScore = ? WHERE username = ?', (score, username))
        conn.commit()
        conn.close()
        

class System(Database, API):
    def hashing(password):
        import hashlib

        return hashlib.sha256(password.encode()).hexdigest()