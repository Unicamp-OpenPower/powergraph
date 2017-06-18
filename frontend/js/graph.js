const DATA_FOLDER = "data/last.csv";

// Set the dimensions of the canvas / graph
var margin = {top: 20, right: 20, bottom: 120, left: 70},
margin2 = {top: 430, right: 20, bottom: 20, left: 70},
width = 960 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom,
height2 = 500 - margin2.top - margin2.bottom;

// Store actual csv data
var origdata;

// Parse the date / time
var parseDate = function(d){return moment.utc(d,"HH:mm:ss").toDate();}
// Format the date / time
var formatDate = d3.timeFormat("%H:%M:%S");
var longFormatDate = d3.timeFormat("%H:%M:%S UTC%Z");

// Set the ranges
var xScale = d3.scaleTime().range([0, width]);
var xScale2 = d3.scaleTime().range([0, width]);
var yScale = d3.scaleLinear().range([height, 0]);
var yScale2 = d3.scaleLinear().range([height2, 0]);

// Define the axes
var xAxis = d3.axisBottom(xScale).tickFormat(formatDate);
var xAxis2 = d3.axisBottom(xScale2).tickFormat(formatDate);
var yAxis =  d3.axisLeft(yScale);

// Define the brush
var brush = d3.brushX()
.extent([[0, -10], [width, height2]])
.on("brush", brushed);

// Define the line
var valueline = d3.line()
.x(function(d) { return xScale(d.date); })
.y(function(d) { return yScale(d.consumption); });

// Dots information
var tip = d3.tip()
.attr("class", "d3-tip")
.offset([-10, 0])
.html(function(d) {
  return "<span style='color:#5F9EA0'><strong>Time:</strong></span> "+longFormatDate(d.date) + "<br>"+
  "<span style='color:#5F9EA0'><strong>Consumption: </strong></span>"+d.consumption+" W";
});

// Adds the svg canvas
var svg = d3.select("#scatter").append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom);

svg.append("defs").append("clipPath")
.attr("id", "clip")
.append("rect")
.attr("width", width)
.attr("height", height);

svg.call(tip);

var focus = svg.append("g")
.attr("class", "focus")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var context = svg.append("g")
.attr("class", "context")
.attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

//timer declaration (not used when init)
var inter = 0;

//checkbox activate function RealTime
d3.select("#checkChange").on("change",realTime);

// Get the data
d3.csv(DATA_FOLDER, function(error, data) {
  data.forEach(function(d) {
    // TODO: remove gambiarra
    d.date = moment(parseDate(d.date)).add(10, 'hours').toDate();
    d.consumption = +d.consumption;
  });

  origdata = data;

  // Scale the range of the data
  xScale.domain([moment(d3.min(data, function(d) { return d.date; })).subtract(2, 'seconds').toDate(),moment(d3.max(data, function(d) { return d.date; })).add(2, 'seconds').toDate()]);
  // .nice(d3.timeSecond, 20);
  // console.log(d3.extent(data, function(d) { return d.date; }));
  console.log([moment(d3.min(data, function(d) { return d.date; })).subtract(1, 'minutes').toDate(),moment(d3.max(data, function(d) { return d.date; })).add(1, 'minutes').toDate()]);
  // console.log(moment(d3.min(data, function(d) { return d.date; })).isValid());
  yScale.domain([d3.min(data, function(d) { return d.consumption; }) - 400, d3.max(data, function(d) { return d.consumption; }) + 50]);
  xScale2.domain(xScale.domain());
  yScale2.domain(yScale.domain()).nice(1);

  // Add the valueline path.
  var path = focus.append("path")
  .attr("clip-path", "url(#clip)")
  .attr("class", "line")
  .attr("d", valueline(data))
  .style("opacity", .5);

  // Add the scatterplot
  var dots = focus.append("g").attr('class', 'dotA');
  dots.attr("clip-path", "url(#clip)");
  dots.selectAll("dot")
  .data(data)
  .enter().append("circle")
  .attr('class', 'dot')
  .attr("r", 3.5)
  .attr("cx", function(d) { return xScale(d.date); })
  .attr("cy", function(d) { return yScale(d.consumption); })
  .style("fill", "#006699")
  .on("mouseover", tip.show)
  .on("mouseout", tip.hide);

  // Add the X Axis
  var eixoX = focus.append("g")
  .attr("class", "axis--x")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);

  focus.append("text")
        .attr("text-anchor", "right")
        .attr("transform", "translate("+ (width - 40) +","+(height+30)+")")
        .text("Time");

  // Add the Y Axis
  var eixoY = focus.append("g")
  .attr("class", "axis--y")
  .call(yAxis);

  focus.append("text")
      .attr("text-anchor", "right")  // this makes it easy to centre the text as the transform is applied to the anchor
      .attr("transform", "translate("+ (-45) +","+(height - 230)+")rotate(-90)")  // text is drawn off the screen top left, move down and out and rotate
      .text("Consumption (W)");

  // Append scatter plot to brush chart area
  var dots = context.append("g").attr('class', 'dotB');
  dots.attr("clip-path", "url(#clip)");
  dots.selectAll("dot")
  .data(data)
  .enter().append("circle")
  .attr('class', 'dotContext')
  .attr("r", 1.8)
  .attr("cx", function(d) { return xScale2(d.date); })
  .attr("cy", function(d) { return yScale2(d.consumption); })
  .style("fill", "#006699").style("opacity", 1);

  context.append("g")
  .attr("class", "axis--x")
  .attr("transform", "translate(0," + height2 + ")")
  .call(xAxis2);

  context.append("g")
  .attr("class", "brush")
  .call(brush)
  .call(brush.move, xScale.range());

});

//create brush function redraw scatterplot with selection
function brushed() {
  var selection = d3.event.selection;
  xScale.domain(selection.map(xScale2.invert, xScale2));

  focus.selectAll(".dot")
  .attr("cx", function(d) { return xScale(d.date); })
  .attr("cy", function(d) { return yScale(d.consumption); });
  focus.selectAll(".line").attr("d", valueline(origdata));
  focus.select(".axis--x").call(xAxis);
}


// Update data section
function updateData() {
  // Get the data again
  d3.csv(DATA_FOLDER, function(error, data) {
    data.forEach(function(d) {
      d.date = moment(parseDate(d.date)).add(10, 'hours').toDate();
      d.consumption = +d.consumption;
    });

    // Scale the range of the data (slice to show the most recent 10000 dots)
    // xScale.domain(d3.extent(data.slice(-10000), function(d) { return d.date; }));
    // yScale.domain([400, d3.max(data.slice(-10000), function(d) { return d.consumption; })]).nice(1);
    // xScale2.domain(d3.extent(data, function(d) { return d.date; }));
    // yScale2.domain([400, d3.max(data, function(d) { return d.consumption; })]).nice(1);
    // Scale the range of the data
    // console.log(d3.extent(data, function(d) { return d.date; }));
    // console.log([d3.min(data, function(d) { return parseInt(d.consumption); }) - 400, d3.max(data, function(d) { return parseInt(d.consumption); })]);
    // console.log(moment(d3.min(data, function(d) { return d.date; })).isValid());
    xScale.domain([moment(d3.min(data, function(d) { return d.date; })).subtract(2, 'seconds').toDate(),moment(d3.max(data, function(d) { return d.date; })).add(2, 'seconds').toDate()]);
    yScale.domain([d3.min(data, function(d) { return d.consumption; }) - 400, d3.max(data, function(d) { return d.consumption; }) + 50]);
    xScale2.domain(xScale.domain());
    yScale2.domain(yScale.domain()).nice(1);

    // Select the section we want to apply our changes to
    var focus = d3.select(".focus");
    var circleFocus = focus.select(".dotA").selectAll("dot").data(data);
    var context = d3.select(".context");
    var circleContext = context.select(".dotB").selectAll("dot").data(data);

    // Make the changes
    // remove old circles
    focus.selectAll(".dot").remove();
    context.selectAll(".dotContext").remove();

    // enter new circles
    circleFocus.enter().append("circle")
    .attr('class', 'enter')
    .attr('class', 'dot')
    .attr("r", 3.5)
    .attr("cx", function(d) { return xScale(d.date); })
    .attr("cy", function(d) { return yScale(d.consumption); })
    .style("fill", "#006699")
    .on("mouseover", tip.show)
    .on("mouseout", tip.hide);

    // change the line
    focus.select(".line")
    .attr("d", valueline(data));
    // change axis
    focus.select(".axis--x")
    .call(xAxis);
    focus.select(".axis--y")
    .call(yAxis);


    context.select(".axis--x")
    .call(xAxis2);

    circleContext.enter()
    .append("circle")
    .attr('class', 'dotContext')
    .attr("r", 1.8)
    .attr("cx", function(d) { return xScale2(d.date); })
    .attr("cy", function(d) { return yScale2(d.consumption); })
    .style("fill", "#006699");

    origdata = data;
    console.log("update");
  });
}


function realTime(){
    if(d3.select("#checkChange").property("checked")){
      context.selectAll(".brush").remove();
      context.style("opacity", .2);

      document.getElementById("Button").disabled = true;
      d3.select(".updateButton").style("opacity", .2);

      inter = setInterval(updateData, 500);

    } else {
      window.clearInterval(inter);

      context.append("g")
      .attr("class", "brush")
      .call(brush)
      .call(brush.move, xScale.range());
      context.style("opacity", 1);

      d3.select(".updateButton").style("opacity", 1);
      document.getElementById("Button").disabled = false;
    }
}
