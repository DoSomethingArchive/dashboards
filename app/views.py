from app import app, openDB
from flask import render_template

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  #results = overall.query.all()
  results = 'hi'


  return render_template('about.html',results=results)


@app.route('/content_page_1')
def content_page_1():
  results = 'hi'
  return render_template('content_page_1.html')

@app.route('/morebars')
def morebars():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))
  results = 'hi'
  tmp = [11,33,56,74,23,99,14]
  return render_template('morebars.html',results=results,tmp = tmp )




@app.route('/groupbars')
def groupbars():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))

  cur = openDB()
  cur.execute('select campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "y" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  predata = []
  for i in cur.fetchall():
    x = {}
    for a in i:
      if a == 'campaign':
        x[a]=i[a]
      if a == 'sign_ups':
        x['Sign Ups']=i[a]
      if a == 'new_members':
        x['New Members']=i[a]
      if a == 'report_backs':
        x['Reportbacks']=i[a]

    predata.append(x)
  data = sorted(predata,reverse=True, key=lambda k: k['Sign Ups'])
  """
  for i in cur.fetchall():
    campaign = {}

    for x in i:
      campaign['State']=[0],
      campaign['Sign Ups']=i[1],
      campaign['New members']=i[2],
      campaign['Reportbacks']=i[3]
      data.append(campaign)
      print campaign

  """
  print data
  cur.close()

  return render_template('groupbars.html', data=data )

@app.route('/groupBarsNonStaff')
def groupBarsNonStaff():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))

  cur = openDB()
  cur.execute('select campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "n" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  predata = []
  for i in cur.fetchall():
    x = {}
    for a in i:
      if a == 'campaign':
        x[a]=i[a]
      if a == 'sign_ups':
        x['Sign Ups']=i[a]
      if a == 'new_members':
        x['New Members']=i[a]
      if a == 'report_backs':
        x['Reportbacks']=i[a]

    predata.append(x)
  data = sorted(predata,reverse=True, key=lambda k: k['Sign Ups'])
  """
  for i in cur.fetchall():
    campaign = {}

    for x in i:
      campaign['State']=[0],
      campaign['Sign Ups']=i[1],
      campaign['New members']=i[2],
      campaign['Reportbacks']=i[3]
      data.append(campaign)
      print campaign

  """
  print data
  cur.close()

  return render_template('groupBarsNonStaff.html', data=data )

@app.route('/causes')
def causes():
  return render_template('causes.html')

@app.route('/hpStaff')
def hpStaff():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))

  cur = openDB()
  cur.execute('select campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "y" and cause = "homelessness and poverty" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  predata = []
  for i in cur.fetchall():
    x = {}
    for a in i:
      if a == 'campaign':
        x[a]=i[a]
      if a == 'sign_ups':
        x['Sign Ups']=i[a]
      if a == 'new_members':
        x['New Members']=i[a]
      if a == 'report_backs':
        x['Reportbacks']=i[a]

    predata.append(x)
  data = sorted(predata,reverse=True, key=lambda k: k['Sign Ups'])
  """
  for i in cur.fetchall():
    campaign = {}

    for x in i:
      campaign['State']=[0],
      campaign['Sign Ups']=i[1],
      campaign['New members']=i[2],
      campaign['Reportbacks']=i[3]
      data.append(campaign)
      print campaign

  """
  print data
  cur.close()

  return render_template('groupBarsHPStaff.html', data=data )

@app.route('/hpNonStaff')
def hpNonStaff():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))

  cur = openDB()
  cur.execute('select campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "n" and cause = "homelessness and poverty" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  predata = []
  for i in cur.fetchall():
    x = {}
    for a in i:
      if a == 'campaign':
        x[a]=i[a]
      if a == 'sign_ups':
        x['Sign Ups']=i[a]
      if a == 'new_members':
        x['New Members']=i[a]
      if a == 'report_backs':
        x['Reportbacks']=i[a]

    predata.append(x)
  data = sorted(predata,reverse=True, key=lambda k: k['Sign Ups'])
  """
  for i in cur.fetchall():
    campaign = {}

    for x in i:
      campaign['State']=[0],
      campaign['Sign Ups']=i[1],
      campaign['New members']=i[2],
      campaign['Reportbacks']=i[3]
      data.append(campaign)
      print campaign

  """
  print data
  cur.close()

  return render_template('groupBarsHPNonStaff.html', data=data )


@app.route('/form_query', methods=['GET', 'POST'])
def form_query():






  #cur = openDB()
  #cur.execute('select campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "n" and cause = "homelessness and poverty" and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc')
  #cur.close()
  data =[]
  return render_template('form_query.html', data=data )


@app.route('/members')
def members():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))

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

  """
  for i in cur.fetchall():
    campaign = {}

    for x in i:
      campaign['State']=[0],
      campaign['Sign Ups']=i[1],
      campaign['New members']=i[2],
      campaign['Reportbacks']=i[3]
      data.append(campaign)
      print campaign

  """
  print data
  cur.close()

  return render_template('members.html', data=data )


@app.route('/members_12')
def members_12():
  #results = overall.query.all()
  #tmp = []
  #for i in results:
    #tmp.append(int(i.sign_ups))



  return render_template('members_12.html' )

@app.route('/test_submit')
def form():




  return render_template('test_submit.html' )


@app.route('/test_action', methods=['POST'])
def test_action():

  try:
    c1=request.form['c1']
    print c1
    c2=request.form['c2']
    print c2
    metric = request.form['metric']
    print metric
    c1_query = 'select * from overall.overall where campaign="{0}"'.format(c1)
    cur = openDB()
    cur.execute(c1_query)

    c1_su =  cur.fetchone()[metric]
    cur.close()

    c2_query = 'select * from overall.overall where campaign="{0}"'.format(c2)
    cur = openDB()
    cur.execute(c2_query)

    c2_su =  cur.fetchone()[metric]
    cur.close()

    return render_template('test_action.html', c1=c1,c1_su=c1_su,c2=c2,c2_su=c2_su )
  except:
    return render_template('query_error.html')

@app.route('/test_sort')
def test_sort():




  return render_template('test_sort.html' )

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
