from flask import Flask, jsonify, request
import psycopg2
import time
  
# creating a Flask app
app = Flask(__name__)
  

@app.route('/', methods = ['GET'])
def test():
    if(request.method == 'GET'):
        return "<p>Hi from test API</p>",200
 
@app.route('/calculate/<int:number1>/<int:number2>/', methods = ['GET'])
def insert(number1,number2):
    conn = psycopg2.connect(database='db_name',user='db_user',password='db_password',host='db_host',port='db_port')
    cur = conn.cursor()
    cur.execute("SELECT uuid_generate_v4()")
    rows=cur.fetchall()
    cur.execute("Insert into public.calculation (number1, number2,unique_identifier) Values ('" + number1 + "' , '" + number2 +  "' , '" +rows[0][0] +"' )'" )
    return jsonify({'unique_identifier': rows[0][0]})


@app.route('get_answer/<identifier>', methods = ['GET'])
def calculate(identifier):
    conn = psycopg2.connect(database='db_name',user='db_user',password='db_password',host='db_host',port='db_port')
    cur = conn.cursor()
    cur.execute("SELECT number1,number2 from public.calculation where unique_identifier='"+ identifier +"'")
    rows=cur.fetchall()
    sum=rows[0][0]+rows[0][1]
    if len(rows) == 0:
        return "<p>Identifier not found</p>",404
    else:
        cur.execute("SELECT answer from public.calculation where unique_identifier='"+ identifier +"'")
        ans=cur.fetchall()
        if len(ans) == 0 or ans[0][0] is None:
            time.sleep(10)
            cur.execute("UPDATE public.calculation set answer='"+sum+"' where unique_identifier='"+ identifier +"'")
            return "<p>Please Wait</p>",200
        else:
            return jsonify({'data': ans[0][0]}),200
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)
