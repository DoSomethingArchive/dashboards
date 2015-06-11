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
}

//capitalize first letter
ds.capitalizeFirst = function(string) {
  var string_aray = string.split(" ");
  var final_array = new Array;
  for (var i = 0; i < string_aray.length; i++) {
    var new_str = string_aray[i].charAt(0).toUpperCase() + string_aray[i].substr(1).toLowerCase();
    final_array.push(new_str);
  }
  var final_str = final_array.join(" ")
  return final_str;
}

//apply coerceToInt to objects in main array
ds.shapeData = function(main_list) {
  for (var i=0; i<main_list.length;i++) {
    coerceToInt(main_list[i].values);
  }
}

//make regular bar
ds.makeBarChart = function(svgname,data) {
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
}

//make NVD3 multibar
ds.makeMultiBarChart = function(selector, data) {
  var chart = nv.models.multiBarChart();
  // need to set date ticks as date object
  chart.xAxis
  .tickFormat(function(d) {
    d = ds.convertDate(d);
    return d3.time.format('%x')(d);
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

//data formatting for multibar - array of objects (one per bar) that values is an array of objects
ds.multiBarDataFormat = function(data, array_of_metrics) {
  var final_metric = [];
  for (var met = 0; met < array_of_metrics.length; met++) {
    var formatted = {key:ds.capitalizeFirst(array_of_metrics[met]), values:[]};

    for (var i = 0; i < data.length; i++) {
      if (data[i][array_of_metrics[met]]) {
        var element = {x:data[i].date,y:+data[i][array_of_metrics[met]]};
        formatted.values.push(element);
      }
    }

    if (formatted.values.length > 1 ) {
      final_metric.push(formatted);
    }
  }
  return final_metric;
};

//get distinct item from an array of objects, return array
ds.getDistinct = function(some_array,some_key) {
  var final_array = [];
  for (var i = 0; i < some_array.length; i++) {
    var s = some_array[i][some_key];
    var is_in = final_array.indexOf(s);
    if (is_in === -1) {
      final_array.push(s);
    }
  }
  return final_array;
}

/*
data shaping for traffic source data or any data that has dates, may have missing values, and many sources.
Takes array of objects with values that are array
*/

ds.stackedAreaDataFormat = function(data) {
  var sources = ds.getDistinct(data,'source');
  var dates = ds.getDistinct(data,'date');
  //final array we will return
  var formatted_sources = [];

  //for each source, find all other sources and dates, format and add to source.values array
  for (var i = 0; i < sources.length; i++) {
    //values are array of array[date,visits]
    element = {key:sources[i],values:[]}
    for (var x = 0; x < data.length; x++) {
      var s = data[x].source;
      if (s === sources[i]) {
        var z = [];
        var date = data[x].date;
        var visits = +data[x].unq_visits;
        z.push(date,visits);
        element.values.push(z);
      }
    }
    formatted_sources.push(element);
  }
  //sort by most frequently occuring source and take top 10
  formatted_sources.sort(function(a,b){ return b.values.length-a.values.length}).slice(0,11);

  //add dates with 0 traffic if not exist
  for (var i = 0; i < formatted_sources.length; i++) {
    var v = formatted_sources[i].values;
    var current_dates = [];
    //get existing dates
    for (var x = 0; x < v.length; x++) {
      var d = v[x][0];
      current_dates.push(d);
    }
    //check for missing dates against master dates array, add missing dates
    for (var z = 0; z < dates.length; z++) {
      var d2 = dates[z];
      var is_in = current_dates.indexOf(d2);
      if (is_in === -1) {
        blank_array = [d2,0];
        v.push(blank_array);
      }
    }
    //sort dates ascending
    v.sort(function(a,b){return new Date(a[0])-new Date(b[0])})
  }
  return formatted_sources
}

//make stacked area chart
ds.makeStackedAreaChart = function(svgname, data) {
  nv.addGraph(function() {
    var chart3 = nv.models.stackedAreaChart()
      .margin({right: 100})
      //need to tell nvd3 that it's a date
      .x(function(d) { return new Date(d[0]); })
      .y(function(d) { return d[1]; })
      .useInteractiveGuideline(true)
      .transitionDuration(300)
      .showControls(true)
      .clipEdge(false);

    chart3.xAxis.showMaxMin(false)
      .tickFormat(function(d) {
        d = ds.convertDate(d);
        return d3.time.format("%x")(d);
      });

    chart3.yAxis.tickFormat(d3.format(',1f'));

    d3.select(svgname)
      .datum(data)
      .call(chart3);

    nv.utils.windowResize(chart3.update);

    return chart3;
  });
}

//data formatting for bar and line
ds.barWithLineDataFormat = function(data) {
  var traffic_f = [];
  var traffic_object = {key:'Traffic', bar: true, color:'gray', values:[]};
  var conv_object = {key:'Conversion Rate', values:[]};

  //create the objects for each metric
  //some conversion rates are over 100% becasue of low traffic (or internal traffic from ds) and internal sign ups
  for (var i = 0; i < trfc.length; i++) {
    if (trfc[i].conversion_rate <= 1) {
      var a = [trfc[i].date, trfc[i].conversion_rate];
      var b = [trfc[i].date, trfc[i].unq_visits];
      traffic_object.values.push(b);
      conv_object.values.push(a);
    }
    else {
      var a = [trfc[i].date, 1];
      var b = [trfc[i].date, trfc[i].unq_visits];
      traffic_object.values.push(b);
      conv_object.values.push(a);
    }
  }
  traffic_f.push(traffic_object);
  traffic_f.push(conv_object);

  return traffic_f
}

//call bar and line
ds.makeBarWithLines = function(svgname,data) {
  nv.addGraph(function() {
    var chart4 = nv.models.linePlusBarChart()
      .margin({top: 30, right: 60, bottom: 50, left: 70})
      .x(function(d,i) {  return i; })
      .y(function(d,i) {return d[1] });

    //need to only display non-zero elements
    chart4.xAxis.tickFormat(function(d) {
      var dx = data[0].values[d] && data[0].values[d][0] || 0;
      dx = ds.convertDate(dx);
      return d3.time.format('%x')(dx);
    });

    chart4.y1Axis
      .tickFormat(d3.format(',f'));

    chart4.y2Axis
      .tickFormat(function(d) { return d3.format('%f')(d) });

  chart4.bars.forceY([0]);

  d3.select(svgname)
    .datum(data)
    .transition()
    .duration(100)
    .call(chart4);

  nv.utils.windowResize(chart4.update);

  return chart4;
  });
}

//remove children
ds.removeChildren = function (id) {
  var elem_overall = document.getElementById(id);
  while (elem_overall.firstChild) {
    elem_overall.removeChild(elem_overall.firstChild);
  }
}
