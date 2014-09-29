//in css, clor last bar different, and make stats horizontal to eachother, color box by positive, negative

function kpiChart(data,metric,color,chart_svg){
	this.input_data=data;
	this.metric=metric;
	this.master_array=[{key:'Active Members',values:[],color:color}];
	this.averages={total:0,average_last_month:0,this_month_average:0};
	this.compare_all = 0;
	this.compare_last_month=0;
	this.chart_svg=chart_svg;
}

kpiChart.prototype.getShape= function () {
	//set obj for all average stats
	for (var i=0; i<this.input_data.length;i++)  {
	temp_obj={};
	temp_obj.x=this.input_data[i].date;
	temp_obj.y=this.input_data[i][this.metric]*this.input_data[i].days_in_month;
	//console.log(temp_obj);
	this.master_array[0].values.push(temp_obj);
	}
}

kpiChart.prototype.getAverages = function () {
	//set obj for all average stats
	for (var i=0; i<this.input_data.length;i++)  {

	if (i<this.input_data.length-1) {
		this.averages.total+=this.input_data[i][this.metric];

		if (i===this.input_data.length-2){
		this.averages.average_last_month=this.input_data[i][this.metric];
		}
	}

	else {
		this.averages.this_month_average=this.input_data[i][this.metric];
		}
	}
		this.compare_all = Math.round(
			(this.averages.this_month_average/(this.averages.total/(this.input_data.length-1))-1)
			*100);
		this.compare_last_month = Math.round(
			((this.averages.this_month_average/this.averages.average_last_month)-1)
			*100);
}

kpiChart.prototype.buildChart=ds.makeMyChart;

kpiChart.prototype.addStatsToPage= function () {
	var last_month=this.metric+'_last_month';
	var all =this.metric+'_all';
	document.getElementById(last_month)
		.innerHTML = 'Pecent change, last month: '+this.compare_last_month.toString()+'%';
	document.getElementById(all)
		.innerHTML = 'Pecent change, year average: '+this.compare_all.toString()+'%';
}

//stats for active
active = new kpiChart(active_data,'average_active','#99FF66','#chart svg');
active.getShape();
active.getAverages();
active.buildChart(active.chart_svg,active.master_array);
active.addStatsToPage();

//stats for verified
verified = new kpiChart(verified_data,'average_verified','#99FF66','#chart2 svg');
verified.getShape();
verified.getAverages();
verified.buildChart(verified.chart_svg,verified.master_array);
verified.addStatsToPage();

//stats for new
new_m = new kpiChart(new_data,'average_new','#99FF66','#chart3 svg');
new_m.getShape();
new_m.getAverages();
new_m.buildChart(new_m.chart_svg,new_m.master_array);
new_m.addStatsToPage();

//only colors first set
$(window).load(
	function(){
		var i = 0;
		$("div#chart rect").each(function()
			{
				var x=$(this).attr('transform');
				if (x!=undefined) {
				y = parseFloat(x.slice(10,18));
				if (y > i) {
					i=y;
					}
				}
		});

		$("div#chart rect").each(function(d)
			{
				var x=$(this).attr('transform');
				if (x!=undefined) {
				y = parseFloat(x.slice(10,18));

				if (y === i) {
					console.log(y);
					$(this).css("fill","#5F9EA0");

					}
				}
		});
	}
);
