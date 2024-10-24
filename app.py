from flask import Flask, request, render_template
import datetime
import psycopg2

# Функция подключения к базе данных PostgreSQL
def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="loan_system",    # Имя базы данных
        user="postgres",           # Имя пользователя PostgreSQL
        password="mypassword"       # Пароль для этого пользователя
    )
    return conn

# Функция для сохранения данных клиента в базе данных
def save_client(name, dob, email, phone, work, salary, debts, loan_amount, repayment_amount):
    conn = connect_db()
    c = conn.cursor()

    # SQL-запрос для вставки данных в таблицу
    c.execute('''
        INSERT INTO clients (name, dob, email, phone, work, salary, debts, loan_amount, repayment_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (name, dob, email, phone, work, salary, debts, loan_amount, repayment_amount))

    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    dob = request.form['dob']
    email = request.form['email']
    phone = request.form['phone']
    work = request.form['work']
    salary = float(request.form['salary'])
    debts = float(request.form['debts']) if request.form['debts'] else 0
    
    # Валидация возраста
    age = datetime.date.today().year - datetime.datetime.strptime(dob, '%Y-%m-%d').year
    if age < 18 or age > 90:
        return "Простите, мы не можем вам помочь."

    # Валидация зарплаты и занятости
    if salary < 50000 or work == 'Безработный':
        return "Простите, мы не можем вам помочь."
    
    # Расчет займа и суммы возврата
    loan_amount = (salary - debts) * 10
    repayment_amount = loan_amount + loan_amount * 0.03 * 12

    # Сохранение данных клиента в базе данных
    save_client(name, dob, email, phone, work, salary, debts, loan_amount, repayment_amount)

    return f"Ваш займ готов, мы готовы выдать вам {loan_amount} тенге на 1 год. Вернуть нужно будет {repayment_amount} тенге!"

if __name__ == '__main__':
    app.run(debug=True)
