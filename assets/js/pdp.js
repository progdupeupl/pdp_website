$(document).ready(function() {
    $(".move-btn").popover({html: "true"});

    $("textarea").before("<a href=\"/pages/aide-markdown\" class=\"btn btn-link mdhelper\">Aide-mémoire markdown</a>");

    $(".mdhelper").click(
        function(event) {
            event.preventDefault();
            $.ajax({
                url: "/pages/aide-markdown.ajax",
                context: this
            }).done(function(msg){
                $(this).before(msg);
                $(this).remove();
            });
        });
});
