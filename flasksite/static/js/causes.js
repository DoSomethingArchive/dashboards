d3.json("/get-causes.json", function(error, json) {
  if (error) { return console.warn(error); }
  var data = json;
  var format = d3.format("0,000");

  var div = 
  d3.select("body").append("div")
  .attr("class", "grid");
  //d3 gives me issues when declaring this var in y or x functions
  
  div.selectAll('div')
  .data(data)
  .enter()
  .append('a')
  .attr("href", "/causes/homelessness-and-poverty/staff-picks")
  .append("div")
  .attr("id", "front")
  .append("p")
  .attr("id", "title")
  .text(function(d){return d.cause;})
  .append("p")
  .attr("class", "text")
  .html(function(d){return "Sign Ups : " + format(d.sign_ups)+ "</br>" + "New Members : " + format(d.new_members) + "</br>" + "Reportbacks : "+ format(d.report_backs) + "</br>" + "Traffic : "+ format(d.traffic) + "</br>" + "Gate Conversion : " + format(d.conv) + '%' + "</br>" + "Campaigns : " + format(d.campaigns);})
  ;
  
  
});
