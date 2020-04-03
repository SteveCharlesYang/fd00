"use strict";

$(document).ready(function() {
  jQuery.get("/static/roa.txt", function(data) {
    data = data.split(/\r?\n/);
    var data_obj4 = [];
    var data_obj6 = [];
    data.forEach(el => {
      if (el != "") {
        var tmp = el.split(" ASN ");
        if (
          tmp[0].match(
            /^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$/
          )
        )
          data_obj4.push({
            CIDR: tmp[0],
            ASN: tmp[1]
          });
        else
          data_obj6.push({
            CIDR: tmp[0],
            ASN: tmp[1]
          });
      }
    });
    renderList("rao_ipv4", data_obj4);
    renderList("rao_ipv6", data_obj6);
  });
});

function renderList(label, data) {
  var content = "<table style='width: 100%;'>";
  for (var i = 0; i < data.length; ++i) {
    content +=
      "<tr><td>" + data[i].CIDR + "</td><td>" + data[i].ASN + "</td></tr>";
  }
  content += "</table>";

  $("#" + label).append(content);
}