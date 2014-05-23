d3.json("/get-hp-staff-picks-data.json", function(error, json) {
  if (error) { return console.warn(error); }
  var data = json;

  var margin = {top: 20, right: 20, bottom: 30, left: 40},
      width = 1100 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x0 = d3.scale.ordinal()
      .rangeRoundBands([0, width], 0.1);

  var x1 = d3.scale.ordinal();

  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.ordinal()
      .range(["#663366", "#FFCC00", "#666666"]);

  var xAxis = d3.svg.axis()
      .scale(x0)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format("2s"));

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("id","svgMain");


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
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Active");

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
      .text(d.value);

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
      .attr("transform", function(d) { return "translate(" + x0(d.campaign) + ",0)";});

  campaign.selectAll("rect")
      .data(function(d) {return d.ages;})
      .enter().append("rect")
      .attr("width", x1.rangeBand())
      .attr("x", function(d) { return x1(d.name); })
      .attr("y", function(d) { return height; })
      .attr("height", function(d) { return 0 ; })
      .attr("class","bars")
      .style("opacity",".1")
      .on("mouseover", showTooltip)
      .on("mouseout", hideTooltip);

  campaign.selectAll("rect")
      .transition()
      .ease("linear")
      .duration(1000)
      .attr("width", x1.rangeBand())
      .attr("x", function(d) { return x1(d.name); })
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); })
      .attr("class","bars")
      .style("fill", function(d) { return color(d.name); })
      .style("opacity",".7");

  // Legend.
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
      .text(function(d) { return d; });

});
