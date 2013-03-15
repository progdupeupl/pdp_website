$(document).ready(function() {
    $(".move-btn").popover({html: "true"});

    $("textarea").before("<p style=\"text-align: right;\"><a href=\"/pages/aide-markdown\" class=\"mdhelper\">Aide-mémoire markdown</a></p>");

    $(".mdhelper").click(function(event) {
        event.preventDefault();
        var toggle = ($(this).data('toggle') == undefined) ? true : $(this).data('toggle');

        if(toggle) {
            $.ajax({
                url: "/pages/aide-markdown.ajax",
                context: this
            }).done(function(msg){
                $(this).before(msg);
                $(this).text("Masquer");
            });
        } else {
            $(this).prev("table").remove();
            $(this).text("Aide-mémoire markdown");
        }

        $(this).data("toggle", !toggle);

        });
});
