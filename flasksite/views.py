from flasksite import app, openDB, json, queryToData
from flask import render_template, request, url_for, jsonify
from cache import cache
import locale
import queries
import requests



locale.setlocale(locale.LC_ALL, 'en_US')

#returns homepage
@app.route('/')
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
def getCausesdata():
  cur = openDB()
  #all_casues needed for chart
  data = queryToData(cur,queries.getCausesdata_causes)
  return data

#returns cause-level page
@app.route('/causes')
def causes():
  return render_template('causes.html')

#returns cause selection template
@app.route('/cause/campaigns/<cause>')
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

def monthly():

  cur = openDB()
  data = queryToData(cur,queries.monthly_stats)
  cur.close()

  return render_template('monthly-stats.html', data=data )

@app.route('/cause/campaigns/<cause>/<campaign>')

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
def kpis():
  q_active = queries.kpisActive
  cur = openDB()
  active = queryToData(cur,q_active)

  q_verified = queries.kpisVerified
  cur = openDB()
  verified = queryToData(cur,q_verified)

  q_new = queries.kpisNew
  cur = openDB()
  new = queryToData(cur,q_new)

  cur.close()
  return render_template('kpi_page.html', active=active, verified=verified, new_m=new)



def formatThousandNumber(num):
  return locale.format("%d", num, grouping=True)

# @cache.cached(timeout=50, key_prefix='facebook_data')
def get_facebook_data():
      r = requests.get("http://graph.facebook.com/7630216751/")
      fbook = (json.loads(r.content))
      return fbook
