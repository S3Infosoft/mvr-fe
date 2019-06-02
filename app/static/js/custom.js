document.querySelectorAll("#messages").forEach(function(message) {
    setTimeout(function() {
        $(message).fadeOut("slow");
    }, 3000)
});
