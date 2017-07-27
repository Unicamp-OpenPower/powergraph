const DATA_FOLDER = "data/";
document.getElementsByTagName("body")[0].style.height = "600px";
document.getElementById('table').style.height = "450px";

// Set the dimensions of the canvas / graph
var	margin = {top: 30, right: 20, bottom: 30, left: 50},
	width = 810 - margin.left - margin.right,
	height = 270 - margin.top - margin.bottom;

// Parse the date / time
var	parseDate = function(d){return moment.utc(d,"YYYY-MM-DD, utcZZ, HH:mm:ss").toDate();}

// Set the ranges
var	x = d3.scaleTime().range([0, width]);
var	y = d3.scaleLinear().range([height, 0]);

// Define the axes
var	xAxis = d3.axisBottom(x).ticks(5);

var	yAxis = d3.axisLeft(y).ticks(5);

// Define the line
var	valueline = d3.line()
	.x(function(d) { return x(d[0]); })
	.y(function(d) { return y(d[1]); });

// Adds the svg canvas
var	svg = d3.select("#scatter")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		// Add the X Axis
  	svg.append("g")
  		.attr("class", "x axis")
  		.attr("transform", "translate(0," + height + ")")
  		.call(xAxis);

  	// Add the Y Axis
  	svg.append("g")
  		.attr("class", "y axis")
  		.call(yAxis);
// Get the data
function getData(form) {
	var TestVar = form.consumptionDate.value;
  // alert ("You typed: " + TestVar);
  var loading = document.createElement('div');
	loading.className = 'loader';
	// document.getElementById('scatter').appendChild(loading);
	d3.text(DATA_FOLDER+TestVar+".csv", function(text) {
	  var data = d3.csvParseRows(text).map(function(row) {
	    return row.map(function(value) {
	      return value;
	    });
	  });
	  console.log(data);
	// });

  // d3.csv(DATA_FOLDER+TestVar+".csv", function(error, data) {
  	data.forEach(function(d) {
  		d[0] = parseDate(TestVar + ", utc-03:00, " + d[0]);
  		d[1] = +d[1];
  	});

  	// Scale the range of the data
  	x.domain(d3.extent(data, function(d) { return d[0]; }));
  	y.domain([0, d3.max(data, function(d) { return d[1]; })]);

		svg.selectAll(".line").remove();

  	// Add the valueline path.
  	svg.append("path")
  		.attr("class", "line")
  		.attr("d", valueline(data));

		svg.selectAll(".axis").remove();


		// Add the X Axis
  	svg.append("g")
  		.attr("class", "x axis")
  		.attr("transform", "translate(0," + height + ")")
  		.call(xAxis);

  	// Add the Y Axis
  	svg.append("g")
  		.attr("class", "y axis")
  		.call(yAxis);

  });
}

var yesterday = new Date();
var dd = yesterday.getDate()-1;
var mm = yesterday.getMonth()+1; //January is 0!
var yyyy = yesterday.getFullYear();
 if(dd<10){
        dd='0'+dd
    }
    if(mm<10){
        mm='0'+mm
    }

yesterday = yyyy+'-'+mm+'-'+dd;
document.getElementById("consumptionDate").setAttribute("max", yesterday);
document.getElementById("consumptionDate").setAttribute("value", yesterday);
