//show/hide daterange div
function showDiv() {
   if (document.getElementById("daterange").style.display === "none") {
    document.getElementById("daterange").style.display = "block";
   }
   else {
    document.getElementById("daterange").style.display = "none";
   }
}
//format
var format = d3.format("0,000");
//div for overall metrics
var div = d3.select("#campaign-overall-stats")
            .attr("class","grid2");
//add p for each metric
var buildOverall = function (input_obj) {
  for (i in input_obj) {
    var p = d3.select("div.grid2")
              .append("p")
              .attr("class","overall")
              .append("p")
              .attr("class","words")
              .html(function (d) {
                if (i === 'Conversion Rate') {
                  return i + " " + ":" + " " + input_obj[i] + '%';
                }
                else {
                  return i + " " + ":" + " " + format(input_obj[i]);
                }
              });
  }
}

//build initial overall stats
buildOverall(overall);
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

//handles ajax data and regeneration of data
function dateRangeSubmit(my_id) {
  //gets start date
  var month_start = document.getElementById("month_start");
  var month_start_val = month_start.options[month_start.selectedIndex].value;

  var day_start = document.getElementById("day_start");
  var day_start_val = day_start.options[day_start.selectedIndex].value;

  var year_start = document.getElementById("year_start");
  var year_start_val = year_start.options[year_start.selectedIndex].value;

  var date_start = String(year_start_val) + "-" + String(month_start_val) + "-" + String(day_start_val);
  //gets end date
  var month_end = document.getElementById("month_end");
  var month_end_val = month_end.options[month_end.selectedIndex].value;

  var day_end = document.getElementById("day_end");
  var day_end_val = day_end.options[day_end.selectedIndex].value;

  var year_end = document.getElementById("year_end");
  var year_end_val = year_end.options[year_end.selectedIndex].value;

  var date_end = String(year_end_val) + "-" + String(month_end_val) + "-" + String(day_end_val);
  //ajax post and chart regenrartion
  $.post('/daterange', {start : date_start, end: date_end, campaign: campaign},
    function (result) {
      //not sure if need to remove for nvd3 charts. often it's fine without removing, but it's not a performance
      //hit and ensures it chart regeneration works
      ds.removeChildren("campaign-overall-stats");
      buildOverall(JSON.parse(result['overall']));

      ds.removeChildren("chart_svg");
      ds.makeMultiBarChart('#chart', ds.multiBarDataFormat(JSON.parse(result['su']), ['web', 'mobile']));

      ds.removeChildren("chart2_svg");
      ds.makeMultiBarChart('#chart2', ds.multiBarDataFormat(JSON.parse(result['nm']), ['web', 'mobile']));

      if (JSON.parse(result['is_sms']) === 0) {
        //chart 5 - reportback
        ds.removeChildren("chart5_svg");
        ds.makeMultiBarChart('#chart5', ds.multiBarDataFormat(JSON.parse(result['rb']), ['reportbacks']));
        //chart 6 - impact
        ds.removeChildren("chart6_svg");
        ds.makeMultiBarChart('#chart6', ds.multiBarDataFormat(JSON.parse(result['impact']), ['impact']));
      }
      else {
        //chart 5 - reportback
        ds.removeChildren("chart5_svg");
        ds.makeMultiBarChart('#chart5', ds.multiBarDataFormat(JSON.parse(result['rb']), ['alphas']));
      }
      //chart 3 - traffic sources
      ds.removeChildren("chart3_svg");
      ds.makeStackedAreaChart('#chart3 svg',ds.stackedAreaDataFormat(JSON.parse(result['srcs'])));
      //chart 4 - traffic
      ds.removeChildren("chart4_svg");
      ds.makeMultiBarChart('#chart4', ds.multiBarDataFormat(JSON.parse(result['traffic']), ['visitors']));

  })
  .done(
    function (x){
      //set button to flash 'Success!'
      document.getElementById(my_id).innerHTML='Success!';
      setTimeout(function(){document.getElementById(my_id).innerHTML='Submit';}, 200);
    }
  )
  .fail(
    function (x){
      //set button to warn on failure
      document.getElementById(my_id).innerHTML='Server Error, Not Submitted!';
    }
  );
}
