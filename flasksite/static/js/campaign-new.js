var format = d3.format("0,000");
//div for overall metrics
var div = d3.select("#campaign-overall-stats")
            .attr("class","grid2");
//add p for each metric

for (i in overall) {
  var p = d3.select("div.grid2")
    .append("p")
    .attr("class","overall")
    .append("p")
    .attr("class","words")
    .html(function (d) {
      if (i === 'Conversion Rate') {
        return i + " " + ":" + " " + overall[i] + '%';
      }
      else {
        return i + " " + ":" + " " + format(overall[i]);
      }
    });
}
//chart 1 - sign ups
ds.makeMultiBarChart('#chart', ds.multiBarDataFormat(su, ['web', 'mobile']));
//chart 2 - new members
ds.makeMultiBarChart('#chart2', ds.multiBarDataFormat(nm, ['web', 'mobile']));

if (is_sms === 0) {
  //chart 5 - reportback
  ds.makeMultiBarChart('#chart5', ds.multiBarDataFormat(rb, ['reportbacks']));
  //chart 6 - impact
  ds.makeMultiBarChart('#chart6', ds.multiBarDataFormat(impact, ['impact']));
}
else {
  //chart 5 - reportback
  ds.makeMultiBarChart('#chart5', ds.multiBarDataFormat(rb, ['alphas']));
  var elem = document.getElementById("chart6");
  elem.remove();

}
//chart 3 - traffic sources
ds.makeStackedAreaChart('#chart3 svg',ds.stackedAreaDataFormat(srcs));
//chart 4 - traffic
ds.makeMultiBarChart('#chart4', ds.multiBarDataFormat(traffic, ['visitors']));