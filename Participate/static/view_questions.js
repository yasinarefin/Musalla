$(document).ready(function () {

    // add custom styles to raw html from db

    $("[data-type='question-container']").each(
        function(idx, element){
            $(element).find("img").addClass("img-fluid");
            $(element).find("table").addClass("table table-bordered");
        }
    );

    if(time_remaining != 0){
        $('#countdown-timer').timeTo(
            time_remaining,
            function () {
                location.reload(true);
            }
        );
    }

    
    
    $("#question-list-container").on("click", "button[data-btn-type='submit']", function () {
        var clickedBtn = $(this);
        //var questionCont = clickedBtn.parent().parent().parent();
        var questionCont = clickedBtn.closest("[data-question-id]");
        var questionId = questionCont.attr("data-question-id");
        var answer = []
        var options = clickedBtn.parent().parent().parent().children().eq(2);
        if (questionCont.attr("data-question-type") === "single_choice") {
            
            var checkedIdx = -1;

            options.children().each(function (idx, element) {
                if ($(element).children().eq(0).is(":checked")) {
                    checkedIdx = idx;
                }
            });

            answer.push(checkedIdx);

        }else if(questionCont.attr("data-question-type") === "multiple_choice"){

            options.children().each(function (idx, element) {
                if ($(element).children().eq(0).is(":checked")) {
                    answer.push(idx);
                }
            });
        }

        $.ajax({
            url: `/participate/submit/${questionId}/`,
            type: 'POST',
            dataType: "json",
            data: {
                answer: JSON.stringify(answer),
                csrfmiddlewaretoken: csrf_token
            },
            success: function (data, textStatus, jQxhr) {
                if (jQxhr.status == 200) {
                    alert("submiited");
                    clickedBtn.prop("disabled", true);
                }
            },
            error: function (jqXhr, textStatus, errorThrown) {
                alert(jqXhr.responseText);
            }
        });

        //var options = clickedBtn.closest("ul[data-list-name='option-list']");



    });
});