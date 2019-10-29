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

document.getElementById("upload_dataset").style.display = "none";

document.getElementById("upload_button").addEventListener("click", showUpload);

function showUpload() {
  document.getElementById("upload_dataset").style.display = "block";
}

//document.getElementById("div_id_max_depth").style.display = "none";
//document.getElementById("div_id_subsample").style.display = "none";
//
//$("#id_id_training_method_0_1").change(function() {
//
//        document.getElementById("div_id_max_depth").style.display = "none";
//        document.getElementById("div_id_subsample").style.display = "none";
//});
//
//$("#id_id_training_method_0_2").change(function() {
//
//        document.getElementById("div_id_max_depth").style.display = "none";
//        document.getElementById("div_id_subsample").style.display = "none";
//});
//
//$("#id_id_training_method_0_3").change(function() {
//
//    if ($(this).prop('checked')) {
//        document.getElementById("div_id_max_depth").style.display = "block";
//        document.getElementById("div_id_subsample").style.display = "block";
//    }
//
//});