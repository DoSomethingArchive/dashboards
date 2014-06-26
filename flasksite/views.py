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
  print formatted_data
  cur.close()
  return render_template('home.html',formatted_data=formatted_data)

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
  #all_casues needed for chart
  q = """
  select 'Sex + Relationships' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Sex',"Relationships") 
  union all
  select 'Homelessness + Poverty' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Homelessness',"Poverty") 
  union all
  select 'Bullying + Violence' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Bullying',"Violence") 
  union all
  select 'Health' as cause, group_concat(distinct cause) as all_causes, sum(sign_ups) as sign_ups, sum(new_members) as new_members, sum(report_backs) as report_backs, sum(all_traffic) as traffic, round(avg(avg_gate_conversion)*100,2) as conv, count(*) as campaigns from overall.overall where date_add(end_date, interval 14 day) >= curdate() and cause in ('Mental Health',"Physical Health") 
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
@app.route('/cause/campaigns', methods=['post'])
def causeStaffPicks():
  data=request.form['button']
  values = data.split('|')
  print "these are the values", values

  causes_list = values[0].split(",")

  staff = values[2]

  quoted_causes = ['"'+str(cause)+'"' for cause in causes_list]
  formatted_causes =  ','.join(quoted_causes)
  cur = openDB()
  q = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" and cause in (%s) and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc' % (staff,formatted_causes)
  
  cur.execute(q)
  data = cur.fetchall()
  cur.close()
  title = values[1]
  j = json.dumps(data) 
  return render_template('cause-campaigns.html', title=title,causes=values[0], j=j )


#returns monthly kpi data
@app.route('/monthly-stats')

def monthly():

  cur = openDB()
  cur.execute('select date_format(date, "%M %Y") as date, new_membrs_abs as new_members, engaged_members_abs as engaged_members, active_members_abs as active_members, verified_members_abs as verified_members from members.bod_2014 order by date_format(date, "%Y-%m-%d")' )
  d = cur.fetchall()
  cur.close()
  data = json.dumps(d)
    



  return render_template('monthly-stats.html', data=data )


@app.route('/test_form', methods=['post'])

def test_form():
  #needed becasue better the formatted campaign name. should add a parameter to the campaign json that is db name so no need to format.
  name=str(request.form['vals']).replace(" ","_").lower()
  print name
  q='select sum(web_sign_ups) as su from %s.web_sign_ups' %(name)
  
  

  cur = openDB()
  cur.execute(q)
  data = cur.fetchall()[0]['su']
  print data

  cur.close()
  
  
  return render_template('test_form.html',name=name, data=data)




