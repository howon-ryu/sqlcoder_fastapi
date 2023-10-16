function question_submit(event){
    event.preventDefault();

    console.log("q:",document.getElementsByName("question")[0].value)
    data={
        "question":document.getElementsByName("question")[0].value
    }
    $.ajax({
        url: 'http://127.0.0.1:8001/apitest',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(result) {
            console.log("Response:", result);
            show_query(result)
        },
        error: function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    });


}

function show_query(prop){
    const element = document.getElementById('conversation_body');
    element.innerHTML += '<div>'+prop.result+'</div>';

}