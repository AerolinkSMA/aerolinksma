import $ from "jquery";

import "jquery-datetimepicker";
import "jquery-datetimepicker/build/jquery.datetimepicker.min.css";

$(document).ready(function() {
  $("#id_pickup_date").datetimepicker();
  $("#id_return_date").datetimepicker();
});
