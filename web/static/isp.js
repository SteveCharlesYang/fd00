"use strict";

var nodes = [];

var tier_std = {
  tier1: 0.08,
  tier2: 0.03,
  tier3: 0.005,
  clients: 0,
  invalids: -1
};

$(document).ready(function() {
  jQuery.getJSON("/static/graph.json?t=" + Math.floor(Date.now() / 600000), function(data) {
    nodes = data.nodes;

    var tier1 = [];
    var tier2 = [];
    var tier3 = [];
    var clients = [];
    var invalids = [];

    for (var i = 0; i < nodes.length; ++i) {
      if (nodes[i].centrality >= tier_std["tier1"]) {
        tier1.push(nodes[i]);
      } else if (nodes[i].centrality >= tier_std["tier2"]) {
        tier2.push(nodes[i]);
      } else if (nodes[i].centrality >= tier_std["tier3"]) {
        tier3.push(nodes[i]);
      } else if (nodes[i].centrality >= tier_std["clients"]){
        clients.push(nodes[i]);
      } else {
        invalids.push(nodes[i])
      }
    }

    renderList("tier1", tier1);
    renderList("tier2", tier2);
    renderList("tier3", tier3);
    renderList("clients", clients);
    renderList("invalids", invalids)
  });
});

function renderList(tier, nodes) {
  nodes.sort((a, b) =>
    a.centrality > b.centrality ? -1 : b.centrality > a.centrality ? 1 : 0
  );
  var content =
    "<p>" +
    tier +
    " ISPs have centrality more than " +
    tier_std[tier] +
    ".</p><table style='width: 100%;'>";
  for (var i = 0; i < nodes.length; ++i) {
    content +=
      "<tr class='isp-item'><td><a href='/lookup/AS" +
      nodes[i].name +
      "'>" +
      nodes[i].name +
      "</a></td><td>" +
      nodes[i].label +
      "</td></tr>";
  }
  content += "</table>";

  $("#" + tier).append(content);
}
