var countDownDate = new Date().getTime() + 12 * 60 * 60 * 1000; // 12 hours from now

var countdown = setInterval(function () {
    var now = new Date().getTime();
    var distance = countDownDate - now;

    // Time calculations for hours, minutes and seconds
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var days = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.querySelector(".hourbox").innerText = hours;
    document.querySelector(".daybox").innerText = days;
    document.querySelector(".minutebox").innerText = minutes;
    document.querySelector(".secondbox").innerText = seconds;

    // If the countdown is finished, write some text
    if (distance < 0) {
        clearInterval(countdown);
        document.querySelector(".ctd").innerHTML = "EXPIRED";
    }
}, 1000);
