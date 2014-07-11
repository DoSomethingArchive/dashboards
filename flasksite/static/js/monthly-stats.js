//most of the following data transformations needed for d3 are done in regualr js vs d3 methods so they are easier to follow
//parse the data returned from flask to json
var json = JSON.parse(x);

//initial values(metrics) to parse by. make this dynamic using d3.keys
var metrics = ['engaged_members','active_members','new_members', 'verified_members'];

//raw json orded by date, use this as test data
/*
var json = [{date:'2014-01-01','a':'123','b':'555','c':'2000'},{date:'2014-02-01','b':'446','a':'456','c':'20000'},{date:'2014-03-01','b':'90','a':'230','c':'600'},{date:'2014-04-01','b':'10009','a':'178','c':'20'},{date:'2014-05-01','b':'541','a':'1000','c':'3490'}];
*/
//make sure int

json.forEach(function(d) {                
    for (i in d)
    {
      if (i !=='date')

        {d[i]= +d[i];}

        }                    
  });
//container for formatted json
var new_json = [];
//iterate through the metrics list, then for each metric, iterate throgh the elements in the json. 
//For each element, iterate through the values. If the value matches the metric, add it to the metric object 
//as metric:metricname, values:[{date:date,members,members},...] 
for (var i=0;i<metrics.length;i++) {

  var new_element = {metric:metrics[i],values:[]};
  
  for (var x=0;x<json.length;x++) {

    for (var k in json[x]) {

      if (k===metrics[i]) {
        
        var date = json[x]['date']
        var members = json[x][k]
        //add members by date date:members
        new_element.values.push({'date':date,'members':members});
      }
      
    }

  }
//push completed metric
new_json.push(new_element);
}

//console.log(new_json[0].values);
//set margins
var margin = {top: 10, right: 40, bottom: 140, left: 40},
  width = 1100 - margin.left - margin.right,
  height = 550 - margin.top - margin.bottom;
//set padding
var padding = 75;
//set color scale
var color = d3.scale.ordinal()
  .range(["#23b7fb", "#FCD116","#4e2b63","#66CC33"]);

//great main svg
var svgMain = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .attr("id","svgMain").append("g").attr("transform", "translate(" + padding + "," + padding + ")");;

//need to use original, preprocessed json to get ordinal domain
var xScale = d3.scale.ordinal().domain(json.map(function(d){return d.date;})).rangeBands([0,width-padding]);
//use original json to get domain for y scale too
var yScale = d3.scale.linear().domain([0,d3.max(json, function(d) {
  //iteraters through each object to return the highest value, independant of the metric.
  //some var is 0
  var x = 0;
  // for each object in the array, return the highest value amogst all the metrics
  for (i in d) {
    if (i != 'date') {
      if (d[i] > x) {
        x = d[i]        
      }
    }
  }
  
  return x;
})]).range([height-padding,0]);


var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");
//define line function 
var lineFunc = d3.svg.line()                
  .x(function(d) {return xScale(d.date)+padding+20;})          
  .y(function(d,i) { return yScale(d.members);})
  .interpolate("linear"); 
//append x axis
svgMain.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate("+0+"," + (height-padding) + ")")
  .call(xAxis)
  .selectAll("text")  
  .style("text-anchor", "end")
  .attr("transform", function(d) {
      return "rotate(-65)" 
          });
//append y axis
svgMain.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate("+0+",0)")
      .call(yAxis);
//for each metric in the new_json object array, apply the line function to the values (object array fo dtes and members)
new_json.forEach(function(d) {
svgMain.append("path").attr("d", lineFunc(d.values)).attr("stroke", color(d.metric)).attr("stroke-width","3")
                          
                           .attr("fill", "none");});

// Legend.
var legend = svgMain.selectAll(".legend")
  .data(metrics.slice())
  .enter().append("g")
  .attr("class", "legend")
  .attr("transform", function(d, i) { return "translate(-50," + i * 20 + ")"; });

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
  .text(function(d) { return d.replace('_',' ').toUpperCase(); });

