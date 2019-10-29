function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//XGBoost
document.getElementById("div_id_gamma").style.display = "none";
document.getElementById("div_id_min_child_weight").style.display = "none";
document.getElementById("div_id_max_delta_step").style.display = "none";
document.getElementById("div_id_max_depth").style.display = "none";
document.getElementById("div_id_subsample").style.display = "none";
document.getElementById("div_id_colsample_bytree").style.display = "none";
document.getElementById("div_id_eta").style.display = "none";


$("#id_id_model_0_1").change(function() {

    //XGBoost
    document.getElementById("div_id_gamma").style.display = "none";
    document.getElementById("div_id_min_child_weight").style.display = "none";
    document.getElementById("div_id_max_delta_step").style.display = "none";
    document.getElementById("div_id_max_depth").style.display = "none";
    document.getElementById("div_id_subsample").style.display = "none";
    document.getElementById("div_id_colsample_bytree").style.display = "none";
    document.getElementById("div_id_eta").style.display = "none";

    document.getElementById("id_id_training_method_0_1").click();
});

$("#id_id_model_0_2").change(function() {

    //XGBoost
    document.getElementById("div_id_gamma").style.display = "none";
    document.getElementById("div_id_min_child_weight").style.display = "none";
    document.getElementById("div_id_max_delta_step").style.display = "none";
    document.getElementById("div_id_max_depth").style.display = "none";
    document.getElementById("div_id_subsample").style.display = "none";
    document.getElementById("div_id_colsample_bytree").style.display = "none";
    document.getElementById("div_id_eta").style.display = "none";

    document.getElementById("id_id_training_method_0_1").click();
});


$("#id_id_training_method_0_1").change(function() {

    //XGBoost
    document.getElementById("div_id_gamma").style.display = "none";
    document.getElementById("div_id_min_child_weight").style.display = "none";
    document.getElementById("div_id_max_delta_step").style.display = "none";
    document.getElementById("div_id_max_depth").style.display = "none";
    document.getElementById("div_id_subsample").style.display = "none";
    document.getElementById("div_id_colsample_bytree").style.display = "none";
    document.getElementById("div_id_eta").style.display = "none";

});


$("#id_id_training_method_0_2").change(function() {

    //XGBoost
    document.getElementById("div_id_gamma").style.display = "none";
    document.getElementById("div_id_min_child_weight").style.display = "none";
    document.getElementById("div_id_max_delta_step").style.display = "none";
    document.getElementById("div_id_max_depth").style.display = "none";
    document.getElementById("div_id_subsample").style.display = "none";
    document.getElementById("div_id_colsample_bytree").style.display = "none";
    document.getElementById("div_id_eta").style.display = "none";
});


$("#id_id_training_method_0_3").change(function() {

    if ($(this).prop('checked')) {

        if (document.getElementById('id_id_model_0_1').checked) {
            //XGBoost
            document.getElementById("div_id_gamma").style.display = "block";
            document.getElementById("div_id_min_child_weight").style.display = "block";
            document.getElementById("div_id_max_delta_step").style.display = "block";
            document.getElementById("div_id_max_depth").style.display = "block";
            document.getElementById("div_id_subsample").style.display = "block";
            document.getElementById("div_id_colsample_bytree").style.display = "block";
            document.getElementById("div_id_eta").style.display = "block";

        }
        else {
            alert("You didn't check it! Let me check it for you.");
        }

    }

});