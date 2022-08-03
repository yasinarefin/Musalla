$(document).ready(function(){
    var q_count = 0;
    var $single_choice_option = $(".d-none[data-option-type='single-choice-option']").clone().removeClass("d-none");
    var $single_choice_question = $(".d-none[data-question-type='single_choice']").clone().removeClass("d-none");
    var $multiple_choice_option = $(".d-none[data-option-type='multiple-choice-option']").clone().removeClass("d-none");
    var $multiple_choice_question = $(".d-none[data-question-type='multiple_choice']").clone().removeClass("d-none");
  //  $single_choice_question.children().eq(1).append($single_choice_option);

    function parse_single_choice(element){ // given question container, returns the parsed question
        
        cur_ques = {};
        cur_ques["id"] = parseInt( element.attr("data-question-id"));
                
        cur_ques["question_type"] = element.attr("data-question-type");
        var mce_id = element.find("[data-type='editor']").children().eq(0).attr("id");
        
        
        cur_ques["question_text"] = tinyMCE.get(mce_id).getContent();
                
        cur_ques["points"] = parseInt(element.find("[data-input-name='points']").val());
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
        return cur_ques;
    }

    function parse_multiple_choice(element){
        cur_ques = {};
        cur_ques["id"] = parseInt( element.attr("data-question-id"));
                cur_ques["question_type"] = element.attr("data-question-type");

                var mce_id = element.find("[data-type='editor']").children().eq(0).attr("id");
                cur_ques["question_text"] = tinyMCE.get(mce_id).getContent();
                cur_ques["points"] = parseInt(element.find("[data-input-name='points']").val());
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
        return cur_ques;
    }
    $("#btn-save").click(function(){
        question_arr = [];
        //alert($("#questions").children().length);

        for(let i = 0; i < $("#questions").children().length; i++){
            
            var element = $("#questions").children().eq(i);
            cur_ques = {};
            if(element.attr("data-question-type")==='single_choice'){
                question_arr.push(parse_single_choice(element));
            }else if(element.attr("data-question-type")==='multiple_choice'){
                question_arr.push(parse_multiple_choice(element));

                
            }

            
        }
        update_questions(question_arr);

    });

    function update_questions(question_arr){ // given question  array, sends request to update questions
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
    }


    $("#btn-add-single-choice").click(function(){

        $.ajax({
            url: `/create/${quiz_id}/add-question/`,
            type: 'POST',
            dataType:"json",
            data: {question_type:"single_choice", csrfmiddlewaretoken: csrf_token},
            success: function( data, textStatus, jQxhr ){
                var q_el = $single_choice_question.clone();
                q_el.attr("data-question-id", data["id"]);
                $("#questions").append(q_el);
                q_count++;
                location.reload();
                

            },
            error: function( jqXhr, textStatus, errorThrown ){
                alert("error occured");
            }
        });
        
    });

    $("#btn-add-multiple-choice").click(function(){

        $.ajax({
            url: `/create/${quiz_id}/add-question/`,
            type: 'POST',
            dataType: "json",
            data: {
                question_type: "multiple_choice",
                csrfmiddlewaretoken: csrf_token
            },
            success: function (data, textStatus, jQxhr) {
                if (jQxhr.status == 200) {
                    //success
                    var q_el = $multiple_choice_question.clone();
                    q_el.attr("data-question-id", data["id"]);
                    
                    $("#questions").append(q_el);
                    
                    q_count++;
                    location.reload();
                    
                }
            },
            error: function (jqXhr, textStatus, errorThrown) {
                alert(jqXhr.responseText);
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

        if(parentContainer.attr("data-question-type") == "single_choice"){
            var option = $single_choice_option.clone();

            question_idx =clickedBtn.parent().parent().index(); 
            option.children().eq(0).attr("name", `question-${question_idx}-radio`)
            parentContainer.children().eq(1).append(option);
        }else if(parentContainer.attr("data-question-type") == "multiple_choice"){
            var option = $multiple_choice_option.clone();

            question_idx =clickedBtn.parent().parent().index(); 
            option.children().eq(0).attr("name", `question-${question_idx}-checkbox`)
            parentContainer.children().eq(1).append(option);
        }
        
        
    });

    $("#questions").on("click", "button[data-btype='delete-option']", function(){
        var clickedBtn = $(this);
        clickedBtn.parent().parent().remove();
    });



    $("#questions").on("click", "button[data-btype='update-question']", function(){
        if(confirm("Updating question will delete all submissions to this questions. Proceed?") == false){
            return;
        }
        var clickedBtn = $(this);
        var question_container = clickedBtn.closest("[data-question-id]");
        var question_arr = [];

        if(question_container.attr("data-question-type")==='single_choice'){
            question_arr.push(parse_single_choice(question_container));
        }else if(question_container.attr("data-question-type")==='multiple_choice'){
            question_arr.push(parse_multiple_choice(question_container));
        }

        update_questions(question_arr);
        
    });
    
});