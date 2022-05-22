
from flask import Flask, render_template, url_for,request,redirect
app = Flask(__name__)
import sqlite3

connection = sqlite3.connect('students.db',check_same_thread=False)



table = """CREATE TABLE users(
           name VARCHAR(15),
           lastname VARCHAR(15),
           Math VARCHAR(3),
           History VARCHAR(3),
           Python VARCHAR(3),
           Average VARCHAR(4)
         );"""
cursor = connection.cursor()
# თუ table users არ გაქვთ შექმნილი მოხსენით კომენტარი 20-21 linebs,გაუშვით კოდი და ისევ დაკომენტარეთ.
# cursor.execute(table)
# connection.commit()
# ვქმნი ზოგად ფუნქციას რომელსაც ევალება შეინახოს ინფორმაცია ბაზაში, ქულები სახელიდა გვარი
def insertInformationIndb(name,lastname,math,history,python):
    math1 = int(math)
    history1 = int(history)
    python1 = int(python)
    average = int((math1+history1+python1)/3)
    average = str(average)
    # ვამოწმებ რომ ქულები იყოს 0-100 ამდე, მხოლოდ ამ შემთხვევაში შემაქვს ბაზაში
    if python1>=0 and python1<=100 and math1>=0 and math1<=100 and history1>=0 and history1<=100 :
        if float(average) > 50:
            code = f'INSERT INTO users VALUES("{name}","{lastname}","{math1}","{history1}","{python1}","{average}","green")'
            cursor.execute(code)
            connection.commit() 
        else:  
            code = f'INSERT INTO users VALUES("{name}","{lastname}","{math1}","{history1}","{python1}","{average}","red")'
            cursor.execute(code)
            connection.commit() 
    else:
        return 'fill the form with the correct points, from 0 to 100.'

# ფუნქცია რომელიც უბრალოდ მაძლევს ყველა სტუდენტის მონაცემებს რადგან გამოვიტანო ცხრილში
def showAll():
    code = 'SELECT * FROM users'
    cursor.execute(code)
    sourse = cursor.fetchall()
    return sourse
#ფუნქცია რომელიც მაძლევს კონკრეტულ სტუდენტებს დასერჩილი სახელისა და გვარის მიხედვით 
def showconcret(source):
    newlist = []
    word =''
    for i in source:
        if i!=" ":
            word += i
        else :
            newlist.append(word)
            word = '' 
    newlist.append(word)        
    try:
        code = f'SELECT * FROM users WHERE name LIKE "%{newlist[0]}%" AND lastname LIKE "%{newlist[1]}%"'
        print(code)
        cursor.execute(code)
        sourse = cursor.fetchall()
        print(source)
        return sourse    
        
    except:
        try:
             code = f'SELECT * FROM users WHERE name LIKE "%{newlist[0]}%"'
             print(code)
             cursor.execute(code)
             sourse = cursor.fetchall()
             print(sourse)
             print('kk')
             if sourse!=[]:
               return sourse  
             else:
                 code = f'SELECT * FROM users WHERE lastname LIKE "%{newlist[0]}%"'
                 print(code)
                 cursor.execute(code)
                 sourse = cursor.fetchall()
                 print(source)
                 return sourse    
           
        except:
            try:
             code = f'SELECT * FROM users WHERE lastname="{newlist[0]}"'
             print(code)
             cursor.execute(code)
             sourse = cursor.fetchall()
             print(source)
             return sourse    
            except:
                print('idk')
#ვრუთავ :/ ჰოსტს    
@app.route('/',methods=['POST','GET'])
def mainPage():
    if request.method == 'GET':
        student = showAll() 
        return render_template('main.html',students = student)

    elif request.method == 'POST':
        info = request.form
        hm = insertInformationIndb(info['name'],info['lastname'],info['math'],info['history'],info['python'])

        if hm !='fill the form with the correct points, from 0 to 100.':
            student = showAll()
            return render_template('main.html',students = student)

        else:
            student = showAll()
            return render_template('main.html',students = student,sms = hm) 

# ვრუთავ წაშლის ჰოსტს
@app.route('/deleted',methods=['POST'])
def deleted():
    info = request.form
    info = list(info)
    newlist = []
    word =''

    for i in info[0]:
        
        if i!=" ":
            word += i
        else :
            newlist.append(word)
            word = '' 

    newlist.append(word) 
    code =   f'DELETE FROM users WHERE name="{newlist[0]}" AND lastname="{newlist[1]}"'
    cursor.execute(code)
    connection.commit() 
    print(newlist)
    return redirect('/')     
# ვრუთავ სტუდენტის წაშლის ჰოსტს
@app.route('/result',methods = ['POST','GET'])
def result():
    if request.method=='POST':
         source = request.form
         result1 = showconcret(source['info'])
         print(result1)
         return render_template('result.html',students = result1)

if __name__ == '__main__':
   app.run(debug=True)
