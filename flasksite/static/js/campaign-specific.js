// Slightly modified code from multiBar example at
// http://nvd3.org/livecode/#codemirrorNav
// to demonstrate defaulting to stacked bar
var format = d3.format("0,000");
//div for overall metrics
var div = d3.select("#campaign-overall-stats")
            .attr("class","grid2");

//add p for each metric
for (i in ovrll[0]) {
  var p = d3.select("div.grid2")
            .append("p")
            .attr("class","overall")
            .append("p")
            .attr("class","words")
            .html(function(d){
              if (i==='average_gate_conversion') {
                  return i.replace("_", " ").toUpperCase().replace("_"," ")+" "+":"+" "+ovrll[0][i];
              }
              else {
                return i.replace("_", " ").toUpperCase().replace("_"," ")+" "+":"+" "+format(ovrll[0][i]);
              }
            });
}



//make this more general so can use on other 2 data formats. this data shping func is used for first 2 data sets

var dataFormat = function(data,metric) {
  var m = {key:'Mobile', values:[]};
  var w = {key:'Web', values:[]};

  for (var i = 0; i<data.length; i++) {
    if (data[i].mobile) {
      var element = {x:data[i].date,y:data[i].mobile};
      m.values.push(element);
    }

    if (data[i].web) {
      var element = {x:data[i].date,y:data[i].web};
      w.values.push(element);
    }
  }

  if (m.values.length<1) {
    metric.push(w);
  }
  else {
    metric.push(m);
    metric.push(w);

  }
  return metric;
}

var sign_ups=[];

dataFormat(su,sign_ups);

var new_members=[];

dataFormat(nm,new_members);

var makeMultiBarChart = function(selector, data) {
    var chart = nv.models.multiBarChart();
    // need to set date ticks as date object
    chart.xAxis
        .tickFormat(function(d) {
            d = convertDate(d);
            return d3.time.format('%x')(new Date(d))
        });

    chart.yAxis
        .tickFormat(d3.format(',1f'));

    chart.multibar.stacked(true); // default to stacked
    chart.showControls(false); // don't show controls

    d3.select(selector + ' svg')
        .datum(data)
        .transition().duration(300).call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
};

//chart 1 - sign ups
makeMultiBarChart('#chart', sign_ups);

//chart 2 - new members
makeMultiBarChart('#chart2', new_members);

//data shping for chart 3

var sources = [];
var dates = [];
var formatted_sources = [];

//get list of distinct sources
for (var i=0; i<srcs.length; i++) {

  var s = srcs[i].source;
  var is_in = sources.indexOf(s);

  if (is_in===-1) {
    sources.push(s);
  }

}

//get distinct dates - needed because not all sources ran all dates, and nvd3 breaks if individual graph elements do
// not have identical format
for (var i=0; i<srcs.length; i++) {

  var d = srcs[i].date;
  var is_in = dates.indexOf(d);
  if (is_in===-1) {
    dates.push(d);
  }

}

//for each source, find all other sources and dates, format and add to source.values array
for (var i=0; i<sources.length; i++) {
  element = {key:sources[i],values:[]}

  for (var x=0; x<srcs.length; x++) {
    var s = srcs[x].source;
    if (s===sources[i]) {
      var z = [];
      var date = srcs[x].date;
      var visits = +srcs[x].unq_visits;
      z.push(date,visits);
      element.values.push(z);
    }
  }

  formatted_sources.push(element);

}

//sort by most frequently occuring source
formatted_sources.sort(function(a,b){ return b.values.length-a.values.length});
//take top 10
var f_source = formatted_sources.slice(0,11);

//add dates with 0 traffic if not exist
for (var i=0; i<f_source.length; i++) {
  var v = f_source[i].values;
  var current_dates = [];
  //get cexisting dates
  for (var x=0; x<v.length; x++) {
    var d = v[x][0];
    current_dates.push(d);
    //var is_in = dates.indexOf(d);
    //if (is_in===-1) {
    //var new_date =
    //v.push(new_date);
  }

  //check for missing dates against master dates array, add missing dates
  for (var z=0; z<dates.length; z++) {
    var d2 = dates[z];
    var is_in = current_dates.indexOf(d2);
    if (is_in===-1) {
      blank_array = [d2,0];
      v.push(blank_array);}
  }
  //sort dates ascending
  v.sort(function(a,b){return new Date(a[0])-new Date(b[0])})

}


//build chart 3
nv.addGraph(function() {
  var chart3 = nv.models.stackedAreaChart()
                .margin({right: 100})
                //need to tell nvd3 that it's a date
                .x(function(d) { return new Date(d[0]); })   //We can modify the data accessor functions...
                .y(function(d) { return d[1]; })   //...in case your data is formatted differently.
                .useInteractiveGuideline(true)    //Tooltips which show all data points. Very nice!
                 //Let's move the y-axis to the right side.
                .transitionDuration(300)
                .showControls(true)       //Allow user to choose 'Stacked', 'Stream', 'Expanded' mode.
                .clipEdge(false);

  //Format x-axis labels with custom function.
  //override tick functions by giving array of tick values - need to make this dynamic
  /*
  chart3.xAxis.tickValues([new Date(data3[0].values[0][0]), new Date(data3[0].values[1][0]), new Date(data3[0].values[2][0]),new Date(data3[0].values[3][0])]);
  */
  chart3.xAxis.showMaxMin(false)
        .tickFormat(function(d) {
            d = convertDate(d);
            return d3.time.format("%x")(new Date(d))
        });

  chart3.yAxis
        .tickFormat(d3.format(',1f'));

  d3.select('#chart3 svg')
        .datum(f_source)
        .call(chart3);

  nv.utils.windowResize(chart3.update);

  return chart3;
});

//shape data for chart 4
var traffic_f = [];
var t = {key:'Traffic', bar: true, color:'gray', values:[]};
var c = {key:'Conversion Rate', values:[]};

//create the objects for each metric
//some conversion rates are over 100% becasue of low traffic (or internal traffic from ds) and internal sign ups
for (var i=0; i<trfc.length;i++) {

    if (trfc[i].conversion_rate<=1) {
    var a = [trfc[i].date, trfc[i].conversion_rate];
    var b = [trfc[i].date, trfc[i].unq_visits];
    t.values.push(b);
    c.values.push(a);
    }

    else {
    var a = [trfc[i].date, 1];
    var b = [trfc[i].date, trfc[i].unq_visits];
    t.values.push(b);
    c.values.push(a);
    }

  }
traffic_f.push(t);
traffic_f.push(c);

//build chart 4
nv.addGraph(function() {
      var chart4 = nv.models.linePlusBarChart()
                    .margin({top: 30, right: 60, bottom: 50, left: 70})
                    //We can set x data accessor to use index. Reason? So the bars all appear evenly spaced.
                    .x(function(d,i) {  return i; })
                    .y(function(d,i) {return d[1] })
                    ;
            //need to only display non-zero elements
      chart4.xAxis.tickFormat(function(d) {
          var dx = traffic_f[0].values[d] && traffic_f[0].values[d][0] || 0;
          dx = convertDate(dx);
              return d3.time.format('%x')(new Date(dx))
      });



      chart4.y1Axis
            .tickFormat(d3.format(',f'));

      chart4.y2Axis
            .tickFormat(function(d) { return d3.format('%f')(d) });

      chart4.bars.forceY([0]);

      d3.select('#chart4 svg')
        .datum(traffic_f)
        .transition()
        .duration(100)
        .call(chart4);

      nv.utils.windowResize(chart4.update);

      return chart4;
  });
