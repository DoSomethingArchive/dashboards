String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
}

//all values set to 0 get reassigned values in further functions
//master_array is in the following format - [{key: key_name, values: [], color: color}];
//extra parameters are just a new object in master_array,
//example - [{key:'SMS', values:verified_all_s, color: '#151B54'},{key:'Web', values:verified_all_w, color: '#00CCFF'}]
//need to also give a metric, this name is based on the id for kpi_pgae.html, because using this name to find elements on
//the page.
//chart_svg is the id of the chart
function kpiChart(metric, master_array, chart_svg) {
  this.metric = metric;
  this.master_array = master_array;
  this.compare_all = 0;
  this.compare_last_month = 0;
  this.chart_svg = chart_svg;
}
//making sure int
kpiChart.prototype.coerceToInt = function () {
  for (var x=0; x<this.master_array.length; x++) {
    for (var i = 0; i<this.master_array[x].values.length; i++) {
      this.master_array[x].values[i].y=+this.master_array[x].values[i].y*this.master_array[x].values[i].days_in_month;
    }
  }
}
//compresses master array to on array, then reconverts each month to average per day, and then compares it
//to last month and the past 12
kpiChart.prototype.getAverages = function () {
  //compress array
  var master_length = this.master_array.length;
  var values_length = this.master_array[0].values.length;
  this.totals_array = new Array;
  for (var i=0; i<values_length; i++){
    var total = 0;
    for (var x = 0; x<master_length; x++) {
      total += (this.master_array[x].values[i].y/this.master_array[x].values[i].days_in_month);
    }
    this.totals_array.push(total);
  }
  //get last 13
  this.totals_array = this.totals_array.slice(-13,values_length);
  //calc this month to last month
  this.compare_last_month = Math.round((this.totals_array[12]/this.totals_array[11]-1)*100);
  //get average of last 12
  var total_last_12 = 0;
  for (var q = 0; q<12; q++) {
    total_last_12 += this.totals_array[q];
  }
  //calc this month to average of last 12
  this.compare_all = Math.round((this.totals_array[12]/(total_last_12/12)-1)*100);
}
//build chart
kpiChart.prototype.buildChart = ds.makeBarChart;
//find stat box on page and add updated averages
kpiChart.prototype.addStatsToPage= function () {
  var last_month = this.metric + '_last_month';
  console.log(last_month);
  var all = this.metric + '_all';
	document.getElementById(last_month)
		.innerHTML = 'Percent change, last month average: ' + this.compare_last_month.toString() + '%';
	document.getElementById(all)
		.innerHTML = 'Percent change, year average: ' + this.compare_all.toString() + '%';
}
//color the current month yellow
kpiChart.prototype.colorBar = function(c) {
  var chart_string = c.slice(0, -4);
  var chart_rect = chart_string +' rect';
  var checkExist = setInterval( function () {
    //checks if the rect element exists yet
    if ($(chart_rect).length) {
      $chart = $(chart_string);
 		  $lastRect = $chart.find('rect:last-child');
 		  $lastRect.css({'fill':'#FFCC33'});
      clearInterval(checkExist);
    }
  }, 10);
}

//stats for active
active = new kpiChart('average_active', [{key:'Active', values:active_data, color:'#368BC1'}], '#chart svg');
active.coerceToInt();
active.getAverages();
active.buildChart(active.chart_svg,active.master_array);
active.addStatsToPage();
active.colorBar(active.chart_svg);

//stats for verified
verified_all = new kpiChart('average_verified', [{key:'SMS', values:verified_all_s, color: '#151B54'},{key:'Web', values:verified_all_w, color: '#00CCFF'}], '#chart2 svg');
verified_all.coerceToInt();
verified_all.getAverages();
verified_all.buildChart(verified_all.chart_svg,verified_all.master_array);
verified_all.addStatsToPage();
verified_all.colorBar(verified_all.chart_svg);

//stats for new
new_m = new kpiChart('average_new', [{key:'New', values:new_data, color:'#368BC1'}], '#chart3 svg');
new_m.coerceToInt();
new_m.getAverages();
new_m.buildChart(new_m.chart_svg,new_m.master_array);
new_m.addStatsToPage();
new_m.colorBar(new_m.chart_svg);

//recolor last month on resize
window.onresize = function() {
  active.colorBar(active.chart_svg);
  verified_all.colorBar(verified_all.chart_svg);
  new_m.colorBar(new_m.chart_svg);
}

