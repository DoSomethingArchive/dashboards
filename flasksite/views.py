from flasksite import app, openDB, openDB2, json, lm, queryToData, models
from flask import Flask, render_template, request, url_for, jsonify, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import db
from cache import cache
import locale
import queries
import requests
from datetime import datetime as dt

locale.setlocale(locale.LC_ALL, 'en_US')

#needed to get global user object before request
@app.before_request
def before_request():
    g.user = current_user

#loads user
@lm.user_loader
def load_user(id):
  return models.User.query.get(int(id))

#login in page.
@app.route('/login', methods=['GET', 'POST'])
def login():
  #Takes post data. If existing user, login,
  #if user doesn't exist, but  dosomething user, create basic account and login
  #else, return user to login page
  if request.method == 'POST':

    try:
      email = request.form['email']
      source = email.split('@')[1]
      name = email.split('@')[0]
      user = models.User.query.filter_by(email=email).first()

      if user is not None and user.is_authenticated():
        login_user(user)
        return redirect(url_for('home'))

      if user is None and source == 'dosomething.org' or user is None and source == 'tmiagency.org':
        u = models.User(nickname=name, email=email, role='basic')
        db.session.add(u)
        db.session.commit()
        user = models.User.query.filter_by(email=email).first()
        login_user(user)
        return redirect(url_for('home'))

      else:
        error =  flash("I don't know you. Go away.")
        return render_template('login.html', error=error)

    except Exception as e:
      print e
      return render_template('login.html')

  elif request.method == 'GET':
    return render_template('login.html')

#logout
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
  cur2 = openDB2()

  data = queryToData(cur2,queries.home_total_members,0,'total')
  data = int(json.loads(data))
  formatted_data = formatThousandNumber(data)

  data2_f = queryToData(cur2,queries.home_net_members_daily)

  data3_f = queryToData(cur2,queries.home_gross_mobile_new_members)

  data4_f = queryToData(cur2,queries.home_gross_mail_new_members)

  data5_f = queryToData(cur2,queries.home_gross_mobile_optedout_members)

  data6_f = queryToData(cur2,queries.home_gross_mail_optedout_members)

  cur.close()
  cur2.close()

  fbook = get_facebook_data()
  likes = formatThousandNumber(fbook["likes"])
  talking_about = formatThousandNumber(fbook["talking_about_count"])

  return render_template('home.html',formatted_data=formatted_data, data2 = data2_f, data3 = data3_f, data4 = data4_f, data5 = data5_f, data6 = data6_f, talking_about = talking_about, likes = likes)

#returns cause-level json
@app.route('/get-causes.json')
@login_required
def getCausesdata():
  cur = openDB()
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

#gets list of campaigns
@app.route('/list-campaigns')
@login_required
def listCampaigns():

  cur2 = openDB2()
  data = queryToData(cur2,queries.list_all_campaigns)
  cur2.close()

  return render_template('list-campaigns.html', data=data )


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
  #when redoing this function, don't need to break it down so far. because there are no longer tables for each campaign
  #if there si no data it will just be blank. the decsionibg happens for conversion rate, report backs, and impact.
  # campaign=str(request.form['vals']).replace(" ","_").lower()
  print campaign
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

#kpis page
@app.route('/kpis')
@login_required
def kpis():
  q_active = queries.kpisActive
  cur = openDB2()
  active = queryToData(cur,q_active)

  q_verified_all_s = queries.kpisVerifiedAll_S
  cur = openDB2()
  verified_all_s = queryToData(cur,q_verified_all_s)

  q_verified_all_w = queries.kpisVerifiedAll_W
  cur = openDB2()
  verified_all_w = queryToData(cur,q_verified_all_w)

  q_new = queries.kpisNew
  cur = openDB2()
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

@app.route('/campaign_signups/<nid>')
def campaignDataEnpoint(nid):
  try:
    nid = int(nid)
    q_metadata = queries.campaignDataEnpoint_basic_campaign_metadata % (nid)
    cur = openDB()
    text = queryToData(cur,q_metadata)
    return text
  except:
    return json.dumps({'error':500})

@app.route('/<campaign>')
@login_required
def getSpecificCampaignNew(campaign):
  campaign = campaign.replace('^&^', '#')

  cur2 = openDB2()
  data = queryToData(cur2,queries.list_one_campaign.format(campaign),need_json=0)
  print data
  #ned to differentiate out sms games because of web alphas, even for sign ups
  #some new members issues?
  #sorces by campaign run?
  #sources different for non staff as lower threshold
  if data[0]['mobile_ids'] is not None and data[0]['mobile_ids'] != '0':
    c_id = ",".join(['"'+i+'"' for i in data[0]['mobile_ids'].split(',') if i != 0])
  else:
    c_id = "'999'"


  su = queryToData(cur2,queries.new_sign_ups_new.format(c_id, data[0]['nid']))
  nm = queryToData(cur2,queries.new_members_new.format(c_id, data[0]['nid']))
  srcs = queryToData(cur2,queries.sources_new.format(data[0]['nid']))
  print queries.new_members_new.format(c_id, data[0]['nid'])
  print srcs



  return render_template('campaign-new.html', campaign=campaign, su=su, nm=nm, srcs=srcs)





