d3.json("/get-causes.json", function(error, json) {
  if (error) { return console.warn(error); }
  var data = json;

  var div = d3.select("#content")
              .append("div")
              .attr("class", "main")

  var causeSpace = div.selectAll("div")
                      .data(data)
                      .enter()
                      .append("div")
                      .attr("class", "cause-space");

  causeSpace.html(formatCampaignName);

  causeSpace.append("p").html(formatCampaigninfo);

  causeSpace.on("click", getCauseCampaigns);

});

function formatCampaignName(d) {
  return "<h3>" + d.cause + "</h3>";
}

function formatCampaigninfo(d) {
  var format = d3.format("0,000");
  return "Sign Ups : " + format(d.sign_ups) + "</br>"
        + "New Members : " + format(d.new_members) + "</br>"
        + "Reportbacks : "+ format(d.report_backs) + "</br>"
        + "Traffic : "+ format(d.traffic) + "</br>"
        + "Gate Conversion : " + format(d.conv) + '%' + "</br>"
        + "Campaigns : " + format(d.campaigns);
}

function getCauseCampaigns(d) {
  var cause_name = d.cause.toLowerCase();
  window.location = "/cause/campaigns/" + cause_name;
}
