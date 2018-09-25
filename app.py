from flask import Flask, render_template
import sqlite3
import os



app = Flask(__name__)

conn = sqlite3.connect('mydb.db')

c = conn.cursor()

recentList = list(c.execute("SELECT * from data ORDER BY id DESC LIMIT 20"))












@app.route("/")

def main():

	

	return render_template('index.html', data=recentList)




if __name__ == "__main__":

	app.run()



