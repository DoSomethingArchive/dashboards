d3.json("/get-causes.json", function(error, json) {
  if (error) { return console.warn(error); }
  var data = json;
  var format = d3.format("0,000");

  var div = d3.select("body")
              .append("div")
              .attr("class", "main")


  div.selectAll('div')
              .data(data)
              .enter()
              .append('button')
              .attr("class", "front")
              .attr("name","button")
              .attr("type","submit")
              .attr("value",function(d){return d.all_causes + "|" + d.cause + "|" + "y";})
              .append("p")
              .attr("id", "title")
              .text(function(d){return d.cause;})
              .append("p")
              .attr("class", "text")
              .on("click", getCauseCampaigns)
              .html(function(d){return "Sign Ups : " + format(d.sign_ups)+ "</br>" + "New Members : " + format(d.new_members) + "</br>" + "Reportbacks : "+ format(d.report_backs) + "</br>" + "Traffic : "+ format(d.traffic) + "</br>" + "Gate Conversion : " + format(d.conv) + '%' + "</br>" + "Campaigns : " + format(d.campaigns);});


});

function getCauseCampaigns(d) {
  var cause_name = d.cause.split(' ').join('').toLowerCase();
  window.location = "/cause/campaigns/" + cause_name;
}
