// When the user scrolls the page, execute myFunction
window.onscroll = function() {stickyOffset()};

$(".readyToStart").change(autoSave);
//$("textarea, select, input").change(autoSave);
//$(document).on("change", ".form-control", function () {
//  autoGet();
//});
// Get the header
var header = document.getElementById("stuckDiv");
// notch.

$(document).ready(function(){ // document ready

    $("a").filter(function () {
        return this.hostname && this.hostname !== location.hostname;
    }).each(function () {
        $(this).attr({
            target: "_blank",
            title: "Visit " + this.href + " (click to open in a new window)"
        });
    });

});

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyOffset() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}

function autoGet() {

        $.get(window.location.href, function(data){
            // Display the returned data in browser
            $("#result").html(data);


    });


}

function autoSave() {
    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: $("form").serialize(),
        type: "POST",
        url: $(this).attr('action'),

    });


}

function bannerDisplay() {
    $('#content').before(($('<div class="savedBanner"> Saved </div>')));
    $(self).delay(0.1).remove();
}

function bannerRemove() {
    $(self).delay(1).remove();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

