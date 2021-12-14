from logging import error
import os

from flask import Flask, request, redirect, render_template, url_for, request, jsonify
from flask.helpers import flash, make_response
from settings import SECRET_KEY
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from mydb import db, cursor
import threading
import psycopg2 
import sqlite3 
from get_streamers_status import trigger

#C:/Users/user1/Documents/anaconda/Scripts/activate C:/Users/user1/Documents/anaconda/Scripts/activate 
#C:/Users/user1/Documents/anaconda/Scripts/activate C:/Users/user1/Documents/anaconda/Scripts/activate

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = SECRET_KEY


@app.route('/iamadminad/add_name', methods=['POST', 'GET'])
def add_name():
  if request.method == 'POST':
    name = request.form['input__name']
    description = request.form['input__name-description']
    if 'https://www.youtube.com/' in name or 'https://www.twitch.tv/' in name and name!='':
      cursor.execute(
          "SELECT streamer_name FROM streamers WHERE streamer_name = (?)", [name.strip()])
      if cursor.fetchone() is None:
        cursor.execute("INSERT INTO streamers(streamer_name, streamer_status, stream_img, stream_title, channel_discription) VALUES ( ?, ?, ?, ?, ?)",
                        (name.strip(), None, None, None, str(description)))
        db.commit()

        return redirect(url_for('main_admin'))
      else:
        error = 'Этот канал уже в добавленных.'
        flash(error)
    else:
      error = 'Invalid value'
      flash(error)
      
  
  return render_template('add_name.html', title='Add name | SC')


@app.route('/iamadminad/update_channel_data_id=<id>', methods=['POST', 'GET'])
def update_name(id):
  try:

    cursor.execute("SELECT streamer_username FROM streamers WHERE id=(?)", [id])
    channel_name = cursor.fetchone()
  except:
    cursor.execute("SELECT streamer_username FROM streamers WHERE id=(?)", [id])
    channel_name = cursor.fetchone()
  #print(*channel_name)
  if request.method == 'POST':
    description = request.form['input__name-description-to-update']
    new_name = request.form['input__name-to-update']
    #print('POST ED\nPOST ED\nPOST ED\nPOST ED\n')
    #print(len(str(description)))
    if  len(str(description)) > 25:
        
        error = 'Описание слишком длинное, покороче, пожалуйста'
        flash(error)
    elif 'https://www.youtube.com/' in new_name or 'https://www.twitch.tv/' in new_name:
      cursor.execute(
          "SELECT streamer_name FROM streamers WHERE streamer_name=(?)", [new_name.strip()])
      if cursor.fetchone():
        error = 'Этот канал уже в добавленных.'
        flash(error)
      elif cursor.fetchone() is None and len(str(description)) < 26:
        cursor.execute("UPDATE streamers SET channel_discription=(?), streamer_name=(?) WHERE id=(?)",
            (description, new_name.strip(), id))
        db.commit()

        return redirect(url_for('main_admin'))
        
    elif new_name=='':
        cursor.execute("UPDATE streamers SET channel_discription=(?) WHERE id=(?)",
            (description, id))
        db.commit()
    
        return redirect(url_for('main_admin'))
    else:
      error = 'Invalid value'
      flash(error)
      
  
  return render_template('update_channel.html', title='Update description | SC', name=channel_name[0])

@app.route('/streamers/None')
def none_streamer():
    error = 'WaitingError'
    return render_template('error.html', title=error)

@app.route('/streamers/<streamer_name>')
def view_streamer_data(streamer_name):

  user_status = request.args.get('ad_status')
  main_redirect = '/iamadminad' if user_status=='supaeadminq' else '/'
  print('this user is: ', user_status)
  try:
    
    cursor.execute("SELECT streamer_name, streamer_status, stream_img, streamer_username, id FROM streamers WHERE streamer_username=(?)", [streamer_name.strip()])
    data = cursor.fetchone()
  except psycopg2.ProgrammingError:
    error = 'ProgrammingError'
    return render_template('error.html', title=error)
  except TypeError:
    cursor.execute("SELECT streamer_name, streamer_status, stream_img, streamer_username, id FROM streamers WHERE streamer_username=(?)", [streamer_name.strip()])
    data = cursor.fetchone()
  #cursor.execute("SELECT id FROM streamers WHERE streamer_username=(?)", [streamer_name.strip()])
  #id_ = cursor.fetchone()
  print('data:', data, data[0])
  
  try:
    fullpathhere = 'C:/Users/user1/Documents/MyScripts/freelance_projects/streamers_checker/templates/streamers/' + f'{data[-1]}.html'
  except TypeError:
    pass

  if_file_empty = None
  try:
    print('this file if empy',fullpathhere, os.path.getsize(fullpathhere))
    #print(0==False)
    if os.path.getsize(fullpathhere) == 0:
      if_file_empty = True
    else:
      is_file_empty = False
  except:
    is_file_empty = True

  print(is_file_empty)
  if is_file_empty:
    with open(f'templates\streamers\{data[-1]}.html', 'w', encoding='utf-8') as file:
      # try:
        # stream_status = 'Online' if data[1] else 'Offline'


          file.write("""
            <!DOCTYPE html>
              <html lang="en">
              <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ data[3] }} | SC</title>
                <link rel="shortcut icon" href="../static/images/favicon.ico">
                <link rel="stylesheet" type="text/css" href="../static/css/style.css">
                <link rel="stylesheet" type="text/css" href="../static/css/normalize.css">
              </head>
              <body>
              <div id="top" class="reg__wrapper"><a href="{{ admin_status }}" class="reg__link">К списку стримеров</a></div>
              <div class="main-data">
                <div class="strem_view-name">{{ data[3] }}</div>
                {% if data[1] %}
                <div class="strem_view-status online">Online</div>
                <div class="img_wrapper">
                  <div>
                    <a href="{{data[0]}}"><img class="stream_imageq" src="../static/images/{{ data[-1] }}.jpeg" alt=""></a>
                  </div>
                </div>
                {% else %}
                  <div class="strem_view-status offline">Offline</div>
                {% endif %}
                <div class="strem_view-some-text">{{ streamer_text }}</div>
                <div class="strem_view-some-img">
                <img class="stream_imageq" src="../static/images/{{ streamer__image }}" alt="">
                </div>
                <div class="strem_view-some-text">{{ streamer_text2 }}</div>
                <div class="bottom_btns">
                  <a href="{{ admin_status }}" class="reg__link">На главную</a>
                  <a href="#top">               <div class="header__main-arrow__border">
                    <div class="header__main-center__arrow">Наверх
                      <img class="header__main-center__arrow2" src="../static/images/arrow-up.png" alt=""></a>
                    </div>
                  </div></a>
                </div>
              </div>
              <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js"></script>
              <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>            </body>
              <script src="../static/js/script.js"></script>
              </body>
              </html>
            """)
      
  try:
    #print(data)
    return render_template(f'streamers/{data[-1]}.html', data=data, admin_status=main_redirect,streamer_text='qwrwqwqrwqrqwr', streamer__image='myimg.jpg',streamer_text2='wqzzzzzzz')
  except TypeError:
    cursor.execute("SELECT streamer_name, streamer_status, stream_img, streamer_username, id FROM streamers WHERE streamer_username=(?)", [streamer_name.strip()])
    data = cursor.fetchone()
    #print('data111')
    return render_template(f'streamers/{data[-1]}.html', data=data, admin_status=main_redirect,streamer_text='qwrwqwqrwqrqwr', streamer_text2='wqzzzzzzz',streamer__image='myimg.jpg')


@app.route('/iamadminad/remove_channel_name_id=<id>', methods=['POST', 'GET'])
def remove_name(id):

    cursor.execute(
        "SELECT streamer_name FROM streamers WHERE id=(?)", [id])
    if cursor.fetchone():
      cursor.execute(
          "DELETE FROM streamers WHERE id=(?)", [id])
      db.commit()

      return redirect(url_for('main_admin'))


# @app.route('/admin_validation', methods=['POST', 'GET'])
# def admin_validation():
#   ADMIN_PASSWORD = 'qwrasdfy98q51212asqww'

#   #print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr), admin_status)
#   if request.method == 'POST':
#     password = request.form['input__pass']
#     if password == ADMIN_PASSWORD:
      
      
#       return redirect(url_for('main_admin'))
#     #print(password.remote_addr)
    
  
#   return render_template('admin_validation.html', title="I'm admin | SC")


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/', methods=['POST', 'GET'])
def main():
  try:
    
    cursor.execute("SELECT * FROM streamers")
    rows = cursor.fetchall()

  except psycopg2.ProgrammingError:
    error = 'ProgrammingError'
    return render_template('error.html', title=error)

  except psycopg2.OperationalError:
    cursor.execute("SELECT * FROM streamers")
    rows = cursor.fetchall()
  
  #print(rows[0][5])
  return render_template('main.html', data=rows, title='Main | SC')
  
@app.route('/iamadminad', methods=['POST', 'GET'])
def main_admin():
  try:
    
    cursor.execute("SELECT * FROM streamers")
    rows = cursor.fetchall()


  except psycopg2.ProgrammingError:
    error = 'ProgrammingError'
    return render_template('error.html', title=error)

  except psycopg2.OperationalError:
    cursor.execute("SELECT * FROM streamers")
    rows = cursor.fetchall()
    

  return render_template('admin_main.html', data=rows, title='Main | SC')


if __name__=="__main__":


  # session.init_app(app)
  # db.create_all()

  db.commit()
#   my_demon = threading.Thread(parse_streamers, daemon=True)
  # my_demon.start()
  app.run()
  #app.run(debug=True)
