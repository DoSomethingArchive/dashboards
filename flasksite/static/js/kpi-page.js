String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
}

//all values set to 0 get reassigned values in further functions
function kpiChart(data, metric, color, chart_svg) {
  this.input_data = data;
  this.metric = metric;
  this.key_name = this.metric.slice(8).capitalize() + ' Members';
  this.master_array = [{key: this.key_name, values: [], color: color}];
  this.averages = {total: 0, average_last_month: 0, this_month_average: 0};
  this.compare_all = 0;
  this.compare_last_month = 0;
  this.chart_svg = chart_svg;
}

kpiChart.prototype.getShape = function () {
  for (var i = 0; i<this.input_data.length; i++) {
  temp_obj = {};
  temp_obj.x = this.input_data[i].date;
  temp_obj.y = this.input_data[i][this.metric] * this.input_data[i].days_in_month;
  this.master_array[0].values.push(temp_obj);
	}
}

kpiChart.prototype.getAverages = function () {
	for (var i=0; i<this.input_data.length;i++) {
    //first if statement gets averages for all months except the current
    if (i<this.input_data.length-1) {
		  this.averages.total+=this.input_data[i][this.metric];
      //second if statement gets the average for the last month
		  if (i === this.input_data.length-2) {
		    this.averages.average_last_month = this.input_data[i][this.metric];
      }
	  }
    //gets the average for the current month
    else {
      this.averages.this_month_average = this.input_data[i][this.metric];
		}
	}
  //compares the current month average to the average of all previous months
  this.compare_all = Math.round(
	  (this.averages.this_month_average/(this.averages.total/(this.input_data.length-1))-1) *100);
	//compares the current month average to the last month average
  this.compare_last_month = Math.round(((this.averages.this_month_average/this.averages.average_last_month)-1) *100);
}

kpiChart.prototype.buildChart = ds.makeMyChart;

kpiChart.prototype.addStatsToPage= function () {
  var last_month = this.metric + '_last_month';
  var all = this.metric + '_all';
	document.getElementById(last_month)
		.innerHTML = 'Percent change, last month average: ' + this.compare_last_month.toString() + '%';
	document.getElementById(all)
		.innerHTML = 'Percent change, year average: ' + this.compare_all.toString() + '%';
}

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
active = new kpiChart(active_data,'average_active','#368BC1','#chart svg');
active.getShape();
active.getAverages();
active.buildChart(active.chart_svg,active.master_array);
active.addStatsToPage();
active.colorBar(active.chart_svg);

//stats for verified
verified = new kpiChart(verified_data,'average_verified','#151B54','#chart2 svg');
verified.getShape();
verified.getAverages();
verified.buildChart(verified.chart_svg,verified.master_array);
verified.addStatsToPage();
verified.colorBar(verified.chart_svg);

//stats for new
new_m = new kpiChart(new_data,'average_new','#368BC1','#chart3 svg');
new_m.getShape();
new_m.getAverages();
new_m.buildChart(new_m.chart_svg,new_m.master_array);
new_m.addStatsToPage();
new_m.colorBar(new_m.chart_svg);
