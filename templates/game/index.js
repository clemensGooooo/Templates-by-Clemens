var side = document.getElementById("playsection");
var kangaroo = document.getElementById("kangaroo");
var element = document.getElementById("element");
var working = 0;
jump = () => {
    if (working == 0) {
        working = 1;
        var randomColor = Math.floor(Math.random() * 16777215).toString(16);
        side.style.backgroundColor = "#" + randomColor;
        kangaroo.style.animation = "jump 4s";
        setTimeout(() => {
            kangaroo.style.animation = "";
            working = 0;
        }, 1550)
    }
}
setInterval(() => {
    console.log(element.offsetWidth);
}, 50)