
var w = 1200,
    h = 1200,
    fill = d3.scale.category20();
	


var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("links.json", function(json) {
  var force = d3.layout.force()
      .charge(-160)
      .linkDistance(50)
      .nodes(json.nodes)
      .links(json.links)
      .size([w, h])
      .start();
	  
  var link = vis.selectAll("path.link")
      .data(json.links)
    .enter().append("svg:line")
      .attr("class", function(d) { return "link " + d.type ; })
      .style("stroke-width", function(d) { return Math.sqrt(d.value); })
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  var node = vis.selectAll("circle.node")
      .data(json.nodes)
    .enter().append("svg:circle")
      .attr("class", function(d) { return "node " + d.type ; })
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("r", 8)
	  //.on("click", function(d,i) { alert("Hello world"); })
      .style("fill", function(d) { return fill(d.group); })
      .call(force.drag);
	  
 
  node.append("svg:title")
      .text(function(d) { return d.id + "\nSteps : " +d.dist; });
	  
  node.append("svg:text")
    .attr("x", 12)
    .attr("dy", ".35em")
    .text(function(d) { return d.id; });
	

  vis.style("opacity", 1e-6)
    .transition()
      .duration(100)
      .style("opacity", 1);

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
  
  
	 d3.json("dij_path.json", function(json) {
          
    var table = document.getElementById("table");
	var header = table.createTHead();
 
    header.innerHTML="<th>Path starting at <b>"+  json[0]  + "     </b>(" + (json.length - 1) + " steps) </th>";
  
    for (var i = 1, len = json.length; i < len; ++i) {
     //var v = json[i];
   
    var rowCount = table.rows.length;
    var row = table.insertRow(rowCount);
    row.insertCell(0).innerHTML= i + " - " + json[len-i]
  	}
	 });
 

});
