function setHeroGradient(baseColor, lighten) {
    var topColor = tinycolor(baseColor).lighten(lighten).toString()
    var grad = _.template("linear-gradient(to top, <%= start %>, <%= end %>)")
    $(".main").css({background: grad({start: baseColor, end: topColor})})

}

$(document).ready(function() {
    setHeroGradient("#00A1FF", 20);
})