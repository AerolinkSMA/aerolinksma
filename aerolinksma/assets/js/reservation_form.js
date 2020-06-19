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
var costCashSpan = $("#cost-cash");
var costPaypalSpan = $("#cost-paypal");
var placeSelect = $("#id_place");
var fareTypeSelect = $("#id_fare_type");

function hideCostCard() {
  $(totalCostCard).addClass('d-none');
}

function showCostCard() {
  $(totalCostCard).removeClass('d-none');
}

function calculate() {
  var cost = {
    cash: 0,
    paypal: 0
  };
  var fareType = $(fareTypeSelect).val();
  var placeID = $(placeSelect).val();
  var placePrice = parseFloat(placesPrices[placeID]);

  cost.cash = placePrice;

  // Double cost if fare type is round trip.
  if (fareType === "RT") {
    var newCost = cost.cash * 2;
    newCost = Math.ceil(newCost - (newCost * 0.10)); // 10% less.
    cost.cash = newCost;
  }

  // Calculate PayPal cost, which is 20.5% more.
  cost.paypal = Math.ceil(cost.cash + (cost.cash * 0.205));

  $(costCashSpan).text(cost.cash);
  $(costPaypalSpan).text(cost.paypal);
}

// Initialize, in case of page refresh or form errors, which sets
// initial values for the form.
if ($(placeSelect).val() !== "" && $(fareTypeSelect).val() !== "") {
  calculate();
  showCostCard();
}

$(placeSelect).on("change", function(ev) {
  if ($(this).val() !== "") {
    calculate();
    showCostCard();
  } else {
    hideCostCard();
  }
});

$(fareTypeSelect).on("change", function(ev) {
  calculate();
});
