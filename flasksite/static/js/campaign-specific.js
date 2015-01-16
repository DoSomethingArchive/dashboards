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
    .html(function (d) {
      if (i === 'average_gate_conversion') {
        return i.replace("_", " ").toUpperCase().replace("_"," ")+" "+":"+" "+ovrll[0][i];
      }
      else {
        return i.replace("_", " ").toUpperCase().replace("_"," ")+" "+":"+" "+format(ovrll[0][i]);
      }
    });
}
//chart 1 - sign ups
ds.makeMultiBarChart('#chart', ds.multiBarDataFormat(su));

//chart 2 - new members
ds.makeMultiBarChart('#chart2', ds.multiBarDataFormat(nm));

//chart 3 - traffic sources
ds.makeStackedAreaChart('#chart3 svg',ds.stackedAreaDataFormat(srcs));

//chart 4 - traffic and conversion by day
ds.makeBarWithLines('#chart4 svg', ds.barWithLineDataFormat(srcs))
