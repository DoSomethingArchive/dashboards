#query naming convention is function name underscore descriptive name, e.g. q_home_total_members


#queries for home
home_total_members = "select total from overall.total"

home_net_members_daily = "select date as x, net as y from data.list_tracking"

home_gross_mobile_new_members = "select date as x, mobile_created as y from data.list_tracking"

home_gross_mail_new_members = "select date as x, mail_created as y from data.list_tracking"

home_gross_mobile_optedout_members = "select date as x, mobile_opt_out as y from data.list_tracking"

home_gross_mail_optedout_members = "select date as x, mail_opt_out as y from data.list_tracking"


#getCausesdata

getCausesdata_causes = """
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
#causeStaffPicks

causeStaffPicks_formatted_causes = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" and cause in (%s) and date_add(end_date, interval 7 day) >= curdate() order by sign_ups desc'

causeStaffPicks_causes = 'select concat(upper(substring(replace(campaign,"_"," "),1,1)),substring(replace(campaign,"_"," "),2)) as campaign, sign_ups, new_members, report_backs from overall.overall where staff_pick = "%s" order by sign_ups desc'

#monthly

monthly_stats = 'select date_format(date, "%M %Y") as date, new_members_last_12_percent as new, engaged_members_last_12_percent as engaged, active_members_last_12_percent as active, verified_members_last_12_percent as verified from members.bod_2014 order by date_format(date, "%Y-%m-%d")'

#getSpecificCampaign

getSpecificCampaign_campaign_info = 'select is_sms, staff_pick from {0}.campaign_info'

getSpecificCampaign_overall = "select sign_ups, new_members, report_backs, all_traffic, average_daily_traffic, concat(round(avg_gate_conversion*100,2),'%') as average_gate_conversion from overall.overall where campaign = '{0}' "

getSpecificCampaign_staff_sign_up = """
  select w.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w left join {0}.mobile_sign_ups m on w.date=m.date
  union
  select m.date, ifnull(web_sign_ups,0) as web, ifnull(mobile_sign_ups,0) as mobile from {0}.web_sign_ups w right join {0}.mobile_sign_ups m on w.date=m.date
  order by date
  """

getSpecificCampaign_staff_new_members = """
  select w.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w left join {0}.mobile_new_members m on w.date=m.date
  union
  select m.date, ifnull(web_new_members,0) as web, ifnull(mobile_new_members,0) as mobile from {0}.web_new_members w right join {0}.mobile_new_members m on w.date=m.date
  order by date
  """

getSpecificCampaign_nonstaff_sign_up = "select date, web_sign_ups as web from {0}.web_sign_ups"

getSpecificCampaign_nonstaff_new_members = "select date, web_new_members as web from {0}.web_new_members"

getSpecificCampaign_staff_sources = "select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 500  )"

getSpecificCampaign_nonstaff_sources = "select * from {0}.sources where source in (select source from {0}.sources  group by source having sum(unq_visits) >= 50  )"

getSpecificCampaign_traffic_regular = "select t.date, t.unq_visits, ifnull(s.web_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_sign_ups s on t.date=s.date"

getSpecificCampaign_traffic_sms = "select t.date, t.unq_visits, ifnull(a.alpha_sign_ups/t.unq_visits,0) as conversion_rate from {0}.all_traffic t  left join {0}.web_alphas a on t.date=a.date"

kpisActive = "select * from data.active_by_month order by date"

kpisVerified = "select * from data.verified_by_month order by date"

kpisNew = "select * from data.new_by_month order by date"


