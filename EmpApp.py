from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion


output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    db_conn = connections.Connection(
        host="sm1ajhg6j0477i5.cmuq4uiatswr.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="admin1234",
        db="myapp"
    )
    cursor = db_conn.cursor()
    cursor.execute("select * from employee")
    data = cursor.fetchall()  # data from database
    return render_template('ViewSummary.html', value=data)

@app.route("/showaddemp", methods=['GET', 'POST'])
def showaddemp():
    db_conn = connections.Connection(
        host="sm1ajhg6j0477i5.cmuq4uiatswr.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="admin1234",
        db="myapp"
    )
    return render_template('AddEmp.html')

@app.route("/showsummary", methods=['GET', 'POST'])
def showsummary():
    db_conn = connections.Connection(
        host="sm1ajhg6j0477i5.cmuq4uiatswr.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="admin1234",
        db="myapp"
    )
    cursor = db_conn.cursor()
    cursor.execute("select * from employee")
    data = cursor.fetchall()  # data from database
    return render_template('ViewSummary.html', value=data)
    # return render_template('ViewSummary.html')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    db_conn = connections.Connection(
        host="sm1ajhg6j0477i5.cmuq4uiatswr.ap-southeast-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="admin1234",
        db="myapp"
    )
    fmno = request.form['fmno']
    name = request.form['name']
    team = request.form['team']
    location = request.form['location']
    certification = request.form['certification']
    # emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    # if emp_image_file.filename == "":
    #     return "Please select a file"

    try:

        cursor.execute(insert_sql, (fmno, name, team, location, certification))
        db_conn.commit()

        # # Uplaod image file in S3 #
        # emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        # s3 = boto3.resource('s3')

        # try:
        #     print("Data inserted in MySQL RDS... uploading image to S3...")
        #     s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
        #     bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
        #     s3_location = (bucket_location['LocationConstraint'])
        #
        #     if s3_location is None:
        #         s3_location = ''
        #     else:
        #         s3_location = '-' + s3_location
        #
        #     object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
        #         s3_location,
        #         custombucket,
        #         emp_image_file_name_in_s3)
        #
        # except Exception as e:
        #     return str(e)

    except Exception as e:
        print(e)

    finally:
        print("Entry Done")

    cursor.execute("select * from employee")
    data = cursor.fetchall()  # data from database
    return render_template('ViewSummary.html', value=data)



if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
