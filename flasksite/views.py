from flasksite import app, openDB, json
from flask import render_template, request, url_for, jsonify
import locale


locale.setlocale(locale.LC_ALL, 'en_US')



#returns homepage
@app.route('/')
def home():
  cur = openDB()
  cur.execute("select total from overall.total")
  data = cur.fetchall()[0]['total']
  formatted_data = locale.format("%d", data, grouping=True)
  cur.close()
  return render_template('home.html',formatted_data=formatted_data)

#returns cause-level json
@app.route('/get-causes.json')
def getCausesdata():
  cur = openDB()
  #all_casues needed for chart
  q = """
  select 'Sex+Relationships' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Sex',"Relationships")
  union all
  select 'Homelessness+Poverty' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Homelessness',"Poverty")
  union all
  select 'Bullying+Violence' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Bullying',"Violence")
  union all
  select 'Mental Health+Physical Health' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Mental Health',"Physical Health")
  union all
  select cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause not in ('Bullying',"Violence",'Mental Health',"Physical Health",'Homelessness',"Poverty",'Sex',"Relationships") group by cause
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
    q = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" and cause in (%s) and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc' % (staff,formatted_causes)
  else:
    q = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc' % (staff)

  cur = openDB()
  cur.execute(q)
  data = cur.fetchall()
  cur.close()
  j = json.dumps(data)

  if len(data) > 0:
    return render_template('cause-campaigns.html', title=title,causes=cause, j=j)
  else:
    return render_template('cause-campaigns-nodata.html', title=title,causes=cause)

#returns monthly kpi data
@app.route('/monthly-stats')

def monthly():

  cur = openDB()
  cur.execute('select date_format(date, "%M %Y") as date, new_members_last_12_percent as new, engaged_members_last_12_percent as engaged, active_members_last_12_percent as active, verified_members_last_12_percent as verified from members.bod_2014 order by date_format(date, "%Y-%m-%d")' )
  d = cur.fetchall()
  cur.close()
  data = json.dumps(d)




  return render_template('monthly-stats.html', data=data )

@app.route('/cause/campaigns/<cause>/<campaign>')

def getSpecificCampaign(cause,campaign):
  # campaign=str(request.form['vals']).replace(" ","_").lower()
  name=str(campaign).replace("+","_").lower()
  q_test = 'select is_sms, staff_pick from {0}.campaign_info'.format(name)
  cur = openDB()
  cur.execute(q_test)
  data = cur.fetchall()
  is_sms = data[0]['is_sms']
  is_staff_pick = data[0]['staff_pick']

  #queries

  q_overall = "select sign_ups, new_members, report_backs, all_traffic, average_daily_traffic, concat(round(avg_gate_conversion*100,2),'%') as average_gate_conversion from overall.overall where campaign = '{0}' ".format(name)

  q_staff_signup = """
  select w.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w left join {0}.mobile_sign_ups m on w.date=m.date
  union
  select m.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w right join {0}.mobile_sign_ups m on w.date=m.date
  order by date
  """.format(name)
  q_staff_newmembers = """
  select w.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w left join {0}.mobile_new_members m on w.date=m.date
  union
  select m.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w right join {0}.mobile_new_members m on w.date=m.date
  order by date
  """.format(name)

  q_nonstaff_signup = """
  select date, web_sign_ups as web from {0}.web_sign_ups
  """.format(name)

  q_nonstaff_newmembers = """
  select date, web_new_members as web from {0}.web_new_members
  """.format(name)

  q_sources_staff = """
  select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 1000  )
  """.format(name)

  q_sources_nonstaff = """
  select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 50  )
  """.format(name)

  q_traffic_regular = """
  select t.date, t.unq_visits, ifnull(s.web_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_sign_ups s on t.date=s.date
  """.format(name)
  q_traffic_sms = """
  select t.date, t.unq_visits, ifnull(a.alpha_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_alphas a on t.date=a.date
  """.format(name)
  data = {}

  def query(name,query):
    cur.execute(query)
    info = json.dumps(cur.fetchall())
    data[name]=info


  if is_sms=='n' and is_staff_pick=='y':
    query('signups',q_staff_signup)
    query('newmembers',q_staff_newmembers)
    query('sources',q_sources_staff)
    query('traffic',q_traffic_regular)
    query('overall', q_overall)

  if is_sms=='n' and is_staff_pick=='n':
    query('signups',q_nonstaff_signup)
    query('newmembers',q_nonstaff_newmembers)
    query('sources',q_sources_nonstaff)
    query('traffic',q_traffic_regular)
    query('overall', q_overall)

  if is_sms=='y' and is_staff_pick=='y':
    query('signups',q_staff_signup)
    query('newmembers',q_staff_newmembers)
    query('sources',q_sources_staff)
    query('traffic',q_traffic_sms)
    query('overall', q_overall)

  cur.close()
  return render_template('campaign-specific.html',campaign=campaign.replace("+"," ").upper(),signups=data['signups'],newmembers=data['newmembers'],sources=data['sources'],traffic=data['traffic'],overall=data['overall'])
