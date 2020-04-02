"use strict";

var nodes = [];

$(document).ready(function() {
  jQuery.getJSON("/static/graph.json", function(data) {
    nodes = data.nodes;

    var tier1 = []
    var tier2 = []
    var tier3 = []
    var clients = []

    for (var i = 0; i < nodes.length; ++i) {
      if(nodes[i].centrality > 0.1){
        tier1.push(nodes[i])
      }
      else if(nodes[i].centrality > 0.05){
        tier2.push(nodes[i])
      }
      else if(nodes[i].centrality > 0.01){
        tier3.push(nodes[i])
      }
      else{
        clients.push(nodes[i])
      }
    }

    renderList("#tier1", tier1)
    renderList("#tier2", tier2)
    renderList("#tier3", tier3)
    renderList("#clients", clients)

  });

});

function renderList(tier, nodes){
  var content = "<table style='width: 100%;'>"
  for(var i=0; i<nodes.length; ++i){
      content += '<tr><td>' + nodes[i].name + '</td><td>' + nodes[i].label + '</td></tr>';
  }
  content += "</table>"
  
  $(tier).append(content);
}