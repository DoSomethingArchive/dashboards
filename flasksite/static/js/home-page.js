console.log(master2);
//ensure all data that should be int is int
var coerceToInt = function(list) {

for (var i=0;i<list.length;i++) {

	list[i]['y']=+list[i].y;
	}
};

//apply coerceToInt to objects in main array
var shapeData = function(main_list) {

  for (var i=0; i<main_list.length;i++) {
    coerceToInt(main_list[i].values);
  }
}

//net members
var master = [{key:'Net New Members', values:x, color: '#37006E'}];

shapeData(master);

//gross members
var master2 = [{key:'Mobile', values:x2, color: '#1A661A'},{key:'Email', values:x3, color: '#00FF00'}];
console.log(master2);
shapeData(master2);

console.log(master2);
//gross opt-outs
var master3 = [{key:'Mobile', values:x4, color: '#800000'},{key:'Email', values:x5, color: '#FF3333'}];
shapeData(master3);

//function to call nvd3 multibar function, fix dates, and calll chat
var makeMyChart = function(svgname,data) {
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

makeMyChart('#chart svg',master);
makeMyChart('#chart2 svg',master2);
makeMyChart('#chart3 svg',master3);