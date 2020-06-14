import $ from "jquery";

import "jquery-datetimepicker";
import "jquery-datetimepicker/build/jquery.datetimepicker.min.css";

$(document).ready(function() {
  $("#id_pickup_date").datetimepicker({
    format: "Y-m-d H:i",
  });
  $("#id_return_date").datetimepicker({
    format: "Y-m-d H:i",
  });
});
