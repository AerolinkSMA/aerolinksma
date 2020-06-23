import $ from "jquery";

import "jquery-datetimepicker";


$("#id_pickup_date").datetimepicker({
  format: "Y-m-d H:i",
});
$("#id_return_date").datetimepicker({
  format: "Y-m-d H:i",
});

var placesPrices = JSON.parse(document.getElementById("places-prices").textContent);
var totalCostCard = $("#total-cost");
var totalCostSmall = $("#total-cost-sm"); // Total cost shown in xs-sm devices.
var costCashSpan = $(".cost-cash");
var costPaypalSpan = $(".cost-paypal");
var placeSelect = $("#id_place");
var fareTypeSelect = $("#id_fare_type");

function hideCostCard() {
  $(totalCostCard).addClass('d-none');
  $(totalCostSmall).addClass('d-none');
}

function showCostCard() {
  $(totalCostCard).removeClass('d-none');
  $(totalCostSmall).removeClass('d-none');
}

function getPrices() {
  /*
   * Prices JSON object is in form:
   *   { [fareType]: { cash: <price>, paypal: <price> } }
   */
  var fareType = $(fareTypeSelect).val();
  var placeID = $(placeSelect).val();
  var cashPrice = placesPrices[placeID][fareType].cash;
  var paypalPrice = placesPrices[placeID][fareType].paypal;

  $(costCashSpan).text(cashPrice);
  $(costPaypalSpan).text(paypalPrice);
}

// Initialize, in case of page refresh or form errors, which sets
// initial values for the form.
if ($(placeSelect).val() !== "" && $(fareTypeSelect).val() !== "") {
  getPrices();
  showCostCard();
}

$(placeSelect).on("change", function(ev) {
  if ($(this).val() !== "") {
    getPrices();
    showCostCard();
  } else {
    hideCostCard();
  }
});

$(fareTypeSelect).on("change", function(ev) {
  getPrices();
});
