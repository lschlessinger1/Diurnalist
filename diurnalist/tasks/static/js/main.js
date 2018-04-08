$(function(){
    $(".done-btn").click(function(event){
        event.preventDefault();
        var url = $(this).attr("href");
        var $listItem = $(this).closest(".list-group-item");

        $listItem.animate({'left': '100px'}, "slow")
            .fadeOut("slow", function () {
                window.location.href = url;
        });

    });

    $(".delete-btn").click(function(event){
        event.preventDefault();
        var url = $(this).attr("href");
        var $listItem = $(this).closest(".list-group-item");
        $listItem.fadeOut("slow", function () {
            window.location.href = url;
        });
    });
});