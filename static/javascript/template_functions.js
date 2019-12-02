// When the user scrolls the page, execute myFunction
window.onscroll = function() {stickyOffset()};

$("textarea, select, input").change(autoSave);
// Get the header
var header = document.getElementById("stuckDiv");
// notch.

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

function autoSave() {
    alert("Change Detected");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: $("#post_form").serialize(),
        type: "POST",
        url: $(this).attr('action'),
    })
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

