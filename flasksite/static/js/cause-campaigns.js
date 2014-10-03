//randomly return array of colors. Outside of chart function so color stays the same when resized
var randColor = function() {
  var color_array = [["#368BC1","#FBB917","#659EC7"],["#BCC6CC","#C11B17","#848482"],["#4E387E","#B2C248","#5E5A80"]];
  var colors = color_array[Math.floor(Math.random() * color_array.length)];
  return colors;
}

var color = randColor();

//h&w based on window size
h = window.innerHeight;
w = window.innerWidth;

//make the chart, input height, width, color
var makeChart = function (h,w,c) {

  //need to reparse raw datat when remake chart or gets borked
  var data=JSON.parse(x);
  var padding = 75;
  var format = d3.format("0,000");
  var margin = {top: 10, right: 70, bottom: 300, left: 70};
  var width = (w-(w/4)) - margin.left - margin.right;
  var height = (h-(h/3)) - margin.top - margin.bottom;

  //set scale for entire chart
  var x0 = d3.scale.ordinal()
    .rangeRoundBands([0, width], 0.1);

  //set scale for campaign level bar group
  var x1 = d3.scale.ordinal();

  //set scale for y value
  var y = d3.scale.linear()
    .range([height, 10]);


  //range of colors
  var color = d3.scale.ordinal()
    .range(c);

  //scale for x axis
  var xAxis = d3.svg.axis()
    .scale(x0)
    .orient("bottom");

  //scale for y axis
  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(6);

  //append svg to the form, not the input element
  var svg = d3.select("div.main")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class","svgMain");

  //sort keys (currently object) by value
  var objSort = function () {
    var temp_array =[];
    var final_array=[];
    var a = data[0];

    for (var i in a) {
      if (i != 'campaign') {
        var temper_array = [];
        temper_array.push(i);
        temper_array.push(a[i]);
        temp_array.push(temper_array);
      }
    }
    temp_array.sort(function(a,b){return b[1]-a[1]})

    for (var z = 0; z < temp_array.length; z++) {
      final_array.push(temp_array[z][0]);
    }
    return final_array;
  }

  var metrics = objSort();

  //shape campaign-specific data
  data.forEach(function(d) {
    d.campaign_info = metrics.map(function(name) { return {name: name, value: +d[name]}; });
  });

  //set domians
  x0.domain(data.map(function(d) { return d.campaign; }));
  x1.domain(metrics).rangeRoundBands([0, x0.rangeBand()]);
  y.domain([0, d3.max(data, function(d) { return d3.max(d.campaign_info, function(d) { return d.value; }); })]);

  //call xAxis
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate("+padding+"," + height + ")")
    .call(xAxis)
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("transform", function(d) {
      return "rotate(-65)";
    });

  //call y axis
  svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate("+padding+",0)")
    .call(yAxis);

  //tooltip function
  function showTooltip(d) {
  // Get this bar's x/y values, then augment for the tooltip
    var xPosition = parseFloat(d3.select(this).attr("x")) + x0.rangeBand() / 2;
    var yPosition = parseFloat(d3.select(this).attr("y")) / 2 + height / 2;
    x0.domain(data.map(function(d) { return d.campaign; }));

  // Update the tooltip position and value
    d3.select("#tooltip")
      .style("top", (height) + "px")
      .style("left", (d3.event.pageX-(width/4)) + "px")
      .select("#value")
      .text(d.name.replace('_',' ').toUpperCase()+': '+format(d.value));

  // Show the tooltip.
    d3.select("#tooltip").classed("hidden", false);
  }

  function hideTooltip() {
    d3.select("#tooltip").classed("hidden", true);
  }

  //make campaign-specifc g for grouped bars
  var campaign = svg.selectAll(".campaign")
    .data(data)
    .enter().append("g")
    .attr("class", "g")
    .on("click",getCampaignSpecificData)
    .attr("transform", function(d) { var g_x = x0(d.campaign)+padding; return "translate(" + g_x + ",0)";});

  //add specifc bars to campaign group
  campaign.selectAll("rect")
    .data(function(d){ return d.campaign_info;})
    .enter().append("rect")
    .attr("width", x1.rangeBand())
    .attr("x", function(d) {  return x1(d.name); })
    .attr("y", function(d) { return y(d.value); })
    .attr("height", function(d) { return height - y(d.value); })
    .attr("class","bars")
    .style("fill", function(d) { return color(d.name); })
    .on("mouseover", showTooltip)
    .on("mouseout", hideTooltip);

  // legend
  var legend = svg.selectAll(".legend")
    .data(metrics)
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
    .attr("x", width + 40)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

  legend.append("text")
    .attr("x", width + 30)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "end")
    .text(function(d) {  return d.replace('_',' ').toUpperCase(); });

    //end of makeChart function
}

//call makeChart
makeChart(h,w,color);

//function to resize chart.
var resizeChart = function() {
  var h = window.innerHeight;
  var w = window.innerWidth;
  //remove old svg
  d3.select('svg').remove();
  makeChart(h,w,color)
}

//call resizeChart on window resize
window.onresize=resizeChart;

//function to make bars submit bar data on click
function getCampaignSpecificData(d) {
  var campaign_name = d.campaign.split(' ').join('+');
  window.location = window.location.pathname + '/' + campaign_name.toLowerCase();
}
