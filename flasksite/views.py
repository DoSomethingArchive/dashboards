from flasksite import app, openDB, json
from flask import render_template


#returns homepage
@app.route('/')
def home():
  return render_template('home.html')

#returns all staff picks, cause agnostic
@app.route('/campaigns/staff-picks')
def staffPicks():
  return render_template('staff-picks.html')

#returns json object array of all staff picks, cause agnostic
@app.route('/get-staff-picks-data.json')
def getStaffPicksData():
  cur = openDB()
  cur.execute('select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "y" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  data = cur.fetchall()
  cur.close()
  return json.dumps(data)

#returns all non-staff picks, cause agnostic
@app.route('/campaigns/non-staff-picks')
def nonStaffPicks():
  return render_template('non-staff-picks.html')

#returns json object array of all non-staff picks, cause agnostic
@app.route('/get-non-staff-picks-data.json')
def getNonStaffPicksData():
  cur = openDB()
  cur.execute('select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "n" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  data = cur.fetchall()
  cur.close()
  return json.dumps(data)

#returns cause-level json
@app.route('/get-causes.json')
def getCausesdata():
  cur = openDB()
  q = """
  select 'Sex + Relationships' as cause, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Sex',"Relationships") 
  union all
  select 'Homelessness + Poverty' as cause, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Homelessness',"Poverty") 
  union all
  select 'Bullying + Violence' as cause, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Bullying',"Violence") 
  union all
  select 'Health' as cause, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Mental Health',"Physical Health") 
  union all
  select cause, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause not in ('Bullying',"Violence",'Mental Health',"Physical Health",'Homelessness',"Poverty",'Sex',"Relationships") group by cause
  """
  cur.execute(q)
  data = cur.fetchall()
  cur.close()
  json.dumps(data)
  
  return json.dumps(data)

#returns cause-level page
@app.route('/causes')
def causes():
  return render_template('causes.html')


#returns homelessness and poverty staff picks campaigns
@app.route('/causes/homelessness-and-poverty/staff-picks')
def hpStaffPicks():
  return render_template('hp-staff-picks.html')

#returns json object array of hp staff picks
@app.route('/get-hp-staff-picks-data.json')
def getHpStaffPicksData():
  cur = openDB()
  cur.execute('select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "y" and cause in ("Homelessness","Poverty") and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  data = cur.fetchall()
  cur.close()
  return json.dumps(data)

#returns homelessness and poverty non-staff picks campaigns
@app.route('/causes/homelessness-and-poverty/non-staff-picks')
def hpNonStaffPicks():
  return render_template('hp-non-staff-picks.html')

#returns json object array of hp non-staff picks
@app.route('/get-hp-non-staff-picks-data.json')
def getHpNonStaffPicksData():
  cur = openDB()
  cur.execute('select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "n" and cause in ("Homelessness","Poverty") and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  data = cur.fetchall()
  cur.close()
  return json.dumps(data)

#returns campaign selection template
@app.route('/form_query', methods=['GET', 'POST'])
def form_query():

  data =[]
  return render_template('form_query.html', data=data )

#returns graphed result of input from form_query
@app.route('/sortbars', methods=['POST'])
def sortbars():
  try:

    tmp = []
    tmp2 = []

    c1 = request.form['c1']
    c2 = request.form['c2']
    metric = request.form['metric']

    if metric != 'all_traffic':
      c1_query = 'select {1} from {0}.{1}'.format(c1, metric)
      cur = openDB()
      print c1_query
      cur.execute(c1_query)

      for i in cur.fetchall():
        tmp.append(i[metric])
      cur.close()

    else:
      c1_query = 'select unq_visits from {0}.{1}'.format(c1, metric)
      cur = openDB()
      print c1_query
      cur.execute(c1_query)

      for i in cur.fetchall():
        tmp.append(i['unq_visits'])
      cur.close()


    if metric != 'all_traffic':
      c2_query = 'select {1} from {0}.{1}'.format(c2, metric)
      cur = openDB()
      print c2_query
      cur.execute(c2_query)

      for i in cur.fetchall():
        tmp2.append(i[metric])
      cur.close()

    else:
      c2_query = 'select unq_visits from {0}.{1}'.format(c2, metric)
      cur = openDB()
      print c2_query
      cur.execute(c2_query)

      for i in cur.fetchall():
        tmp2.append(i['unq_visits'])
      cur.close()


    return render_template('sortbars.html', tmp=tmp, tmp2=tmp2, c1=c1,c2=c2, metric=metric )
  except:
    return render_template('query_error.html')

#returns monthly kpi data
@app.route('/members')
def members():

  cur = openDB()
  cur.execute('select date, total_members_abs, new_membrs_abs, engaged_members_abs, verified_members_abs, campaigns_verified_abs, sms_game_verified_abs from members.bod_2014')
  predata = []
  for i in cur.fetchall():
    x = {}
    for a in i:
      if a == 'date':
        x[a]=i[a]

      if a == 'new_membrs_abs':
        x['New Members']=i[a]
      if a == 'engaged_members_abs':
        x['Engaged Members']=i[a]
      if a == 'verified_members_abs':
        x['Verified Members']=i[a]
      if a == 'campaigns_verified_abs':
        x['Reportbacks']=i[a]
      if a == 'sms_game_verified_abs':
        x['Web Alphas']=i[a]




    predata.append(x)
    data = sorted(predata,reverse=True, key=lambda k: k['Engaged Members'])

  print data
  cur.close()

  return render_template('members.html', data=data )



