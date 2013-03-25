$(document).ready(function() {
    /* Popover on move buttons */
    $(".move-btn").popover({html: "true"});

    /* Tooltips */
    $(".forum-stats span").tooltip();

    /* Markdown helpers */
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
