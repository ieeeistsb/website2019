$.fn.turnVisible = function () {
    var rect = this[0].getBoundingClientRect();
    var adjustY = (0 - rect.top > 0 ? 0 - rect.top : (window.innerHeight - rect.bottom < 0 ? window.innerHeight - rect.bottom : 0));
    var adjustX = (0 - rect.left > 0 ? 0 - rect.left + 20 : (window.innerWidth - rect.right < 0 ? window.innerWidth - rect.right - 30 : 0));
    $(this[0].parentNode).addClass("smooth-move");
    $(this[0].parentNode).css("margin-left", "+=" + adjustX);
    //$(this[0].parentNode).css("margin-top", "+=" + adjustY);  /*Do not need this*/
};

$.fn.isFullyVisible = function () {
    var rect = this[0].getBoundingClientRect();
    return (
        (rect.height > 0 || rect.width > 0) &&
        rect.bottom >= 0 &&
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.right >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) &&
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

(function () {
    var cont, margin, number_events = $(".ieee-ist-event").length, event_width = $(".ieee-ist-event").outerWidth();
    var content_width = number_events * event_width + number_events * 10 + 30; // width + padding
    $(".ieee-ist-content").css("min-width", content_width);
    var rect = $(".ieee-ist-content")[0].getBoundingClientRect();
    var maxMove = (0 - rect.left > 0 ? 0 - rect.left + 20 : (window.innerWidth - rect.right < 0 ? window.innerWidth - rect.right - 30 : 0));

    console.log(maxMove);

    new Hammer(document.getElementById("timeline-ieee-ist"), {
        domEvents: true
    });
    $(".ieee-ist-content-container").on("panstart", function (e) {

        cont = $(".ieee-ist-content");
        cont.removeClass("smooth-move");
        margin = parseInt(cont.css("margin-left"));
    });
    $(".ieee-ist-content-container").on("pan", function (e) {
        var delta = margin + e.originalEvent.gesture.deltaX;
        if (delta >= maxMove && delta <= 0) {
            cont.css({
                "margin-left": margin + e.originalEvent.gesture.deltaX
            });
        }
    });
})();


$(".ieee-ist-timeline li").hover(
    function () {
        $(this).find(".timeline-date").css("visibility", "visible").css("opacity", "1");
        id = $(this).find("div").attr("href");
        $(id).addClass("highlight");
        if (!$(id).isFullyVisible()) {
            $(id).turnVisible();
        }
    },
    function () {
        $(this).find(".timeline-date").css("visibility", "hidden").css("opacity", "0");
        id = $(this).find("div").attr("href");
        $(id).removeClass("highlight");

    }
)
;

$(".ieee-ist-event").hover(
    function () {
        id = $(this).attr("id");
        $("[href='#" + id + "']").find(".timeline-date").css("visibility", "visible").css("opacity", "1");
    }, function () {
        id = $(this).attr("id");
        $("[href='#" + id + "']").find(".timeline-date").css("visibility", "hidden").css("opacity", "0");
    });

