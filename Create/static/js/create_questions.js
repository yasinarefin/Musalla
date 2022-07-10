$(document).ready(function(){
    var q_count = 0;
    var $option_element = $(".d-none[data-option-type='single-choice-option']").clone().removeClass("d-none");
    var $question_element = $(".d-none[data-question-type='single_choice']").clone().removeClass("d-none");
    
  //  $question_element.children().eq(1).append($option_element);


    $("#btn-save").click(function(){
        question_arr = [];
        //alert($("#questions").children().length);

        try{

        for(let i = 0; i < $("#questions").children().length; i+=2){
            
            var element = $("#questions").children().eq(i);

            cur_ques = {};
            cur_ques["id"] = parseInt( element.attr("data-question-id"));
            cur_ques["question_type"] = element.attr("data-question-type");
            cur_ques["question_text"] = element.children().eq(0).children().eq(1).val();
            cur_ques["points"] = parseInt(element.children().eq(0).children().eq(0).children().eq(1).children().eq(1).val());
            cur_ques["options"] = [];
            cur_ques["answer"] = [];
            
            element.children().eq(1).children().each(
                function(idx, element2){
                    // remember to wrap element2 with $(), otherwise it is interpreted as DOM element
                    // when iterating childrens
                    var tem = $(element2).children().eq(1).children().eq(1).val();
                    cur_ques["options"].push(tem);
                    if($(element2).children().eq(0).is(":checked")){
                        cur_ques["answer"].push(idx);
                    }
                }
            );
            // alert(cur_ques["question_type"]);
           // alert(cur_ques["question_text"]);

            // cur_ques["options"].forEach(function (item, index) {
            //     alert(item);
            // });

            question_arr.push(cur_ques);

            
            
        }
    }catch(err){
            alert(err);
        }
       // alert(JSON.stringify(question_arr));
        $.ajax({
                url: window.location.pathname,
                type: 'POST',
                dataType:"json",
                data: {questions: JSON.stringify(question_arr), csrfmiddlewaretoken: csrf_token},
                success: function( data, textStatus, jQxhr ){
                    alert("ok");
                },
                error: function( jqXhr, textStatus, errorThrown ){
                    alert("error occured");
                }
        });
    });


    $("#q-add").click(function(){

        $.ajax({
            url: `/create/${quiz_id}/add-question/`,
            type: 'POST',
            dataType:"json",
            data: {question_type:"single_choice", csrfmiddlewaretoken: csrf_token},
            success: function( data, textStatus, jQxhr ){
                var q_el = $question_element.clone();
                q_el.attr("data-question-id", data["id"]);
                q_el.children().first().children().first().children().first().html(`Question`);
                if($("#questions").children().length > 0){
                    $("#questions").append(`<div class="border-top my-3"></div>`);
                }
                
                $("#questions").append(q_el);
                q_count++;
            },
            error: function( jqXhr, textStatus, errorThrown ){
                alert("error occured");
            }
        });
        
    });

    $("#questions").on("click", "button[data-btype='delete-question']", function(){
        var clickedBtn = $(this);
        var q_id = clickedBtn.parent().parent().attr("data-question-id");
        alert(q_id);
        $.ajax({
            url: `/create/${quiz_id}/delete-question/`,
            type: 'POST',
            dataType:"json",
            data: {
                id:parseInt(q_id), 
                csrfmiddlewaretoken: csrf_token
            },
            success: function( data, textStatus, jQxhr ){
                clickedBtn.parent().parent().remove();
            },
            error: function( jqXhr, textStatus, errorThrown ){
                alert("error occured");
            }
        });
        
    });


    $("#questions").on("click", "button[data-btype='add-option']", function(){

        var clickedBtn = $(this);
        var parentContainer = clickedBtn.parent().parent();
        var option = $option_element.clone();
        
        option.children().eq(1).children().first().html( `Option`);
        option.children().eq(0).attr("name", `question-${q_count}-radio`)
        parentContainer.children().eq(1).append(option);
        
    });

    $("#questions").on("click", "button[data-btype='delete-option']", function(){
        var clickedBtn = $(this);
        clickedBtn.parent().parent().remove();
    });
    
});