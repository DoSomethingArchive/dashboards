var ds = {};

ds.convertDate = function(date) {
    var converted = new Date(date);
    converted.setTime(converted.getTime() + converted.getTimezoneOffset() * 60 * 1000);
    return converted;
};


//ensure all data that should be int is int
ds.coerceToInt = function(list) {

for (var i=0;i<list.length;i++) {

	list[i]['y']=+list[i].y;
	}
};

//apply coerceToInt to objects in main array
ds.shapeData = function(main_list) {

  for (var i=0; i<main_list.length;i++) {
    coerceToInt(main_list[i].values);
  }
}

ds.makeMyChart = function(svgname,data) {
nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
        .transitionDuration(350)
        .reduceXTicks(true)   //If 'false', every single x-axis tick label will be rendered.
        .rotateLabels(0)      //Angle to rotate x-axis labels.
        .showControls(false)   //Allow user to switch between 'Grouped' and 'Stacked' mode.
        .groupSpacing(0.1)
        .stacked(true);

      chart.xAxis
        .tickFormat(function(d) {
          d = ds.convertDate(d);
          return d3.time.format('%x')(d)
        });

    chart.yAxis
        .tickFormat(d3.format(',f'));

    d3.select(svgname)
        .datum(data)
        .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
	});
};