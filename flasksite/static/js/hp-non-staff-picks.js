d3.json("/get-hp-non-staff-picks-data.json", function(error, json) {
  if (error) { return console.warn(error); }
  var data = json;
  var padding = 75;
  var format = d3.format("0,000");

  var margin = {top: 10, right: 40, bottom: 140, left: 40},
      width = 1100 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x0 = d3.scale.ordinal()
      .rangeRoundBands([0, width], 0.1);

  var x1 = d3.scale.ordinal();

  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.ordinal()
      .range(["#23b7fb", "#FCD116","#4e2b63"]);

  var xAxis = d3.svg.axis()
      .scale(x0)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(6);

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("id","svgMain");

    /** Return an object array with all ages and state, so '5 and under':100, '16':150, 'state':ca,
    * and each array is a state. This is how d3 converts the csv.
    * The remaining code creates an array of keys, and then foreach array in the data (d3.foreach(data)),
    * it creates a new ages  object array for each state, each satae  has an ages array each element
    * the array being an age:value object.
    * It then creates the x0 domain with d.State from data using maop, passes thr x range to x1,
    * and uses max age for y. The g elements are based on the x0(state) scale.
    * Finally, for each g, rects are built from each states ages array, the name being the x, and height the value.
    * Try this example by recreating it with the data object array data structure (the original).
    * If that works, chnage the data to ds data
    */

    var ageNames = d3.keys(data[0]).filter(function(key) { return key !== "campaign"; });

    data.forEach(function(d) {
      d.ages = ageNames.map(function(name) { return {name: name, value: +d[name]}; });
      d.ages.sort(function(a, b){ return d3.descending(a.value, b.value); });
    });

    x0.domain(data.map(function(d) { return d.campaign; }));
    x1.domain(ageNames).rangeRoundBands([0, x0.rangeBand()]);
    y.domain([0, d3.max(data, function(d) { return d3.max(d.ages, function(d) { return d.value; }); })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate("+padding+"," + height + ")")
      .call(xAxis)
      .selectAll("text")  
      .style("text-anchor", "end")
      .attr("transform", function(d) {
          return "rotate(-65)" 
              });

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate("+padding+",0)")
      .call(yAxis);



  function showTooltip(d) {
    // Get this bar's x/y values, then augment for the tooltip
    var xPosition = parseFloat(d3.select(this).attr("x")) + x0.rangeBand() / 2;
    var yPosition = parseFloat(d3.select(this).attr("y")) / 2 + height / 2;
    x0.domain(data.map(function(d) { return d.campaign; }));

    // Update the tooltip position and value
    d3.select("#tooltip")
      .style("top", (d3.event.pageY-50) + "px")
      .style("left", (d3.event.pageX-100) + "px")
      .select("#value")
      .text(format(d.value)); 

    // Show the tooltip.
    d3.select("#tooltip").classed("hidden", false);
  }

  function hideTooltip() {
    d3.select("#tooltip").classed("hidden", true);
  }

 var campaign = svg.selectAll(".campaign")
      .data(data)
      .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { var g_x = x0(d.campaign)+padding; return "translate(" + g_x + ",0)";});

  campaign.selectAll("rect")
      .data(function(d) {return d.ages;})
      .enter().append("rect")
      .attr("width", x1.rangeBand())
      .attr("x", function(d) { return x1(d.name); })
      .attr("y", function(d) { return height; })
      .attr("height", function(d) { return 0 ; })
      .attr("class","bars")
      .on("mouseover", showTooltip)
      .on("mouseout", hideTooltip);

  campaign.selectAll("rect")
    .transition()
    .ease("linear")
    .duration(1000)
    .attr("width", x1.rangeBand())
    .attr("x", function(d) {return x1(d.name); })
    .attr("y", function(d) { return y(d.value); })
    .attr("height", function(d) { return height - y(d.value); })
    .attr("class","bars")
    .style("fill", function(d) { return color(d.name); });


 var legend = svg.selectAll(".legend")
      .data(ageNames.slice().reverse())
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
      .text(function(d) { return d.replace('_',' ').toUpperCase();});
});
