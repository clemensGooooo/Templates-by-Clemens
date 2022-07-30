var field = document.getElementById("button");
var value = document.getElementById("value");
var randomField = document.getElementById("fieldRan");
var difference = document.getElementById("difference");
var counterD = document.getElementById("counter");
var iq = document.getElementById("iq");
var couter = 0;

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

randomField.innerText = "secret";

if (value.value > 0 && value.value <= 20)
    field.className = "disabled enabled"
else
    field.className = "disabled";

numberChange = () => {
    if (value.value > 0 && value.value <= 20) {
        field.className = "disabled enabled"
    }
}
numberClick = () => {
    couter++;
    counterD.innerText = couter;
    if (value.value > 0 && value.value <= 20) {
        field.className = "disabled enabled"
            // alert(`Number is ${value.value}`)
        var ranNum = getRandomNumber(1, 20);
        var dif = "";
        randomField.innerText = ranNum;
        if (value.value > ranNum) {
            dif = value.value - ranNum;
        } else if (value.value < ranNum) {
            dif = ranNum - value.value
        }
        if (value.value != ranNum) {
            iq.innerText = String(140 - (dif * 3)) + String(" IQ");
            dif = String(dif + " - ") + String(dif / 20 * 100) + "%";
        }
        if (value.value == ranNum) {
            dif = "You are very amongus like";
            iq.innerText = "10000000000 IQ"
            couter = 0;
        }
        difference.innerText = dif;
    } else {
        alert("Please change the number 1-20")
    }
}