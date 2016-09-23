// simulate data
var data = Array.apply(0, Array(31)).map(function(item, i) {
    i++;
    return {date: i , pv: parseInt(Math.random() * 100)}
});

var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// x Scale
var xScale = d3.scale.linear()
               .domain(d3.extent(data, function(d){
                   return d.date;
               }))
               .range([0, width]);
// y Scale
var yScale = d3.scale.linear()
               .domain(d3.extent(data, function(d){
                   return d.pv;
               }))
               .range([height, 0]);
// x axis
var xAxis = d3.svg.axis()
              .scale(xScale)
              .orient("bottom");
// y axis
var yAxis = d3.svg.axis()
              .scale(yScale)
              .orient("left");

var line = d3.svg.line()
             .x(function(d) {
                 console.log('Plotting X value for data point: ' + d.date + ' to be at: ' + xScale(d.date) + ' using our xScale.');
                 return xScale(d.date);
                })
            .y(function(d) {
                console.log('Plotting Y value for data point: ' + d.pv + ' to be at: ' + yScale(d.pv) + " using our yScale.");
                return yScale(d.pv);
            });

var svg = d3.select("body").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
// add axis
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
   .text("PV value");

svg.append("path")
   .datum(data)
   .attr("class", "line")
   .attr("d", function(d){
       return line(d);
