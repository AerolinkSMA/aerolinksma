import $ from "jquery";

import "jquery-datetimepicker";

$(document).ready(function() {
  $("#id_pickup_date").datetimepicker({
    format: "Y-m-d H:i",
  });
  $("#id_return_date").datetimepicker({
    format: "Y-m-d H:i",
  });
});
