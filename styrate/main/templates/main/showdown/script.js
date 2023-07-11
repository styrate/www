// Get the start date
var startDate = new Date("2023-07-10").getTime();

// Calculate the end date as 20 days from the start date
var endDate = startDate + (20 * 24 * 60 * 60 * 1000);

// Check if the countdown data exists in local storage
var countDownDate = localStorage.getItem("countDownDate");

// If the countdown data doesn't exist or the countdown has ended, set the new countdown
if (!countDownDate || countDownDate < startDate || countDownDate > endDate) {
  countDownDate = startDate;
  localStorage.setItem("countDownDate", countDownDate);
}

var countdown = setInterval(function () {
  var now = new Date().getTime();
  var distance = endDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  document.querySelector(".daybox").innerText = days;
  document.querySelector(".hourbox").innerText = hours;
  document.querySelector(".minutebox").innerText = minutes;
  document.querySelector(".secondbox").innerText = seconds;

  // If the countdown is finished, write some text
  if (distance < 0) {
    clearInterval(countdown);
    document.querySelector(".ctd").innerHTML = "EXPIRED";
  }
}, 1000);
