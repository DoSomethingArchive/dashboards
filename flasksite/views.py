from flasksite import app, openDB, json, queryToData, forms, db, lm, oid, models
from flask import render_template, request, url_for, jsonify, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from cache import cache
import locale
import queries
import requests
from datetime import datetime as dt

locale.setlocale(locale.LC_ALL, 'en_US')

#load user
@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

#login in page.
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('home'))

  form = forms.LoginForm()

  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

  return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

#Handles login. If no email of null, deny access. If user in system and gmail login successful, allow.
#If user email ends in 'dosomething', and gmail login successful, create account with basic role and allow
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    #get user data from db
    user = models.User.query.filter_by(email=resp.email).first()

    if user is None and resp.email.split('@')[1] == 'dosomething.org':
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = models.User(nickname=nickname, email=resp.email, role='basic')
        db.session.add(user)
        db.session.commit()

    if user is not None:
      remember_me = False
      if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    else:
      flash('User does not exist. Go away.')
      return redirect(url_for('login'))
    #perform login
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('home'))

#store user data
@app.before_request
def before_request():
    g.user = current_user

#handle logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#returns homepage
@app.route('/')
@login_required
@cache.cached(timeout=1000)
def home():
  cur = openDB()

  data = int(queryToData(cur,queries.home_total_members,0,'total'))
  formatted_data = formatThousandNumber(data)

  data2_f = queryToData(cur,queries.home_net_members_daily)

  data3_f = queryToData(cur,queries.home_gross_mobile_new_members)

  data4_f = queryToData(cur,queries.home_gross_mail_new_members)

  data5_f = queryToData(cur,queries.home_gross_mobile_optedout_members)

  data6_f = queryToData(cur,queries.home_gross_mail_optedout_members)

  cur.close()

  fbook = get_facebook_data()
  likes = formatThousandNumber(fbook["likes"])
  talking_about = formatThousandNumber(fbook["talking_about_count"])

  return render_template('home.html',formatted_data=formatted_data, data2 = data2_f, data3 = data3_f, data4 = data4_f, data5 = data5_f, data6 = data6_f, talking_about = talking_about, likes = likes)

#returns cause-level json
@app.route('/get-causes.json')
@login_required
def getCausesdata():
  cur = openDB()
  #all_casues needed for chart
  data = queryToData(cur,queries.getCausesdata_causes)
  return data

#returns cause-level page
@app.route('/causes')
@login_required
def causes():
  return render_template('causes.html')

#returns cause selection template
@app.route('/cause/campaigns/<cause>')
@login_required
def causeStaffPicks(cause):
  title = cause.capitalize()
  causes_list = cause.split("+")
  if request.args.get('staff') is None:
   staff = "y"
  else:
    staff = request.args.get('staff')

  quoted_causes = ['"'+str(cause)+'"' for cause in causes_list]
  formatted_causes = ','.join(quoted_causes)

  if cause != 'all':
    q = queries.causeStaffPicks_formatted_causes % (staff,formatted_causes)
  else:
    q = queries.causeStaffPicks_causes % (staff)

  cur = openDB()
  j = queryToData(cur,q)
  cur.close()

  if len(j) > 2:
    return render_template('cause-campaigns.html', title=title,causes=cause, j=j)
  else:
    return render_template('cause-campaigns-nodata.html', title=title,causes=cause)

#returns monthly kpi data
@app.route('/monthly-stats')
@login_required
def monthly():

  cur = openDB()
  data = queryToData(cur,queries.monthly_stats)
  cur.close()

  return render_template('monthly-stats.html', data=data )

@app.route('/cause/campaigns/<cause>/<campaign>')
@login_required
def getSpecificCampaign(cause,campaign):
  # campaign=str(request.form['vals']).replace(" ","_").lower()
  name=str(campaign).replace("+","_").lower()
  cur = openDB()
  data = queryToData(cur,queries.getSpecificCampaign_campaign_info.format(name),need_json=0)
  is_sms = data[0]['is_sms']
  is_staff_pick = data[0]['staff_pick']

  data = {}

  def query(name,query):
    info = queryToData(cur,query)
    data[name]=info

  if is_sms=='n' and is_staff_pick=='y':
    query('signups',queries.getSpecificCampaign_staff_sign_up.format(name))
    query('newmembers',queries.getSpecificCampaign_staff_new_members.format(name))
    query('sources',queries.getSpecificCampaign_staff_sources.format(name))
    query('traffic',queries.getSpecificCampaign_traffic_regular.format(name))
    query('overall', queries.getSpecificCampaign_overall.format(name))

  if is_sms=='n' and is_staff_pick=='n':
    query('signups',queries.getSpecificCampaign_nonstaff_sign_up.format(name))
    query('newmembers',queries.getSpecificCampaign_nonstaff_new_members.format(name))
    query('sources',queries.getSpecificCampaign_nonstaff_sources.format(name))
    query('traffic',queries.getSpecificCampaign_traffic_regular.format(name))
    query('overall', queries.getSpecificCampaign_overall.format(name))

  if is_sms=='y' and is_staff_pick=='y':
    query('signups',queries.getSpecificCampaign_staff_sign_up.format(name))
    query('newmembers',queries.getSpecificCampaign_staff_new_members.format(name))
    query('sources',queries.getSpecificCampaign_staff_sources.format(name))
    query('traffic',queries.getSpecificCampaign_traffic_sms.format(name))
    query('overall', queries.getSpecificCampaign_overall.format(name))

  cur.close()
  return render_template('campaign-specific.html',campaign=campaign.replace("+"," ").upper(),signups=data['signups'],newmembers=data['newmembers'],sources=data['sources'],traffic=data['traffic'],overall=data['overall'])

@app.route('/kpis')
@login_required
def kpis():

  q_active = queries.kpisActive
  cur = openDB()
  active = queryToData(cur,q_active)

  q_verified_all_s = queries.kpisVerifiedAll_S
  cur = openDB()
  verified_all_s = queryToData(cur,q_verified_all_s)

  q_verified_all_w = queries.kpisVerifiedAll_W
  cur = openDB()
  verified_all_w = queryToData(cur,q_verified_all_w)

  q_new = queries.kpisNew
  cur = openDB()
  new = queryToData(cur,q_new)

  q_text = queries.kpiText
  cur = openDB()
  text = queryToData(cur,q_text)
  cur.close()

  return render_template('kpi_page.html', active=active, verified_all_w=verified_all_w, verified_all_s=verified_all_s,  new_m=new, q_text=text, user_role=g.user.role)

#need to handle quotes
@app.route('/kpisubmit', methods=['POST'])
@login_required
def kpisubmit():
  #get rid of quotes aspostraphes when writing to mysql, and replace them later when called to the page
  text = request.form['text'].replace("'","|").replace('"',"%^&")
  q_insert = queries.kpiTextInsert % (dt.now(), text, request.form['box_id'])
  cur = openDB()
  insert = queryToData(cur,q_insert)
  return q_insert

def formatThousandNumber(num):
  return locale.format("%d", num, grouping=True)

# @cache.cached(timeout=50, key_prefix='facebook_data')
def get_facebook_data():
      r = requests.get("http://graph.facebook.com/7630216751/")
      fbook = (json.loads(r.content))
      return fbook
