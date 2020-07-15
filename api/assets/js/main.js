$(document).ready(function() {

    if ($('#original_url').attr('href') != "") {
        var stampifying_time_sec = 0;
        var stampify_duration_interval = setInterval(function() {
            stampifying_time_sec += 1;
            $('#stampify-time-taken')[0].innerHTML = 'Stampifying duration: <b>' + stampifying_time_sec + ' seconds </b>';
        }, 1000);
    }

    $('#stamp-iframe').on('load', function() {
        $('.loader').remove();
        var stamp_html_code = $('#stamp-iframe')[0].contentWindow.document.all[0].outerHTML;

        if($($(stamp_html_code)[3]).text() == "Error"){
            $('#stamp-code')[0].innerHTML = 'No stamp generated!'
        }else{
            $('#stamp-code')[0].innerHTML = he.encode(stamp_html_code);
        }
        clearInterval(stampify_duration_interval);
        $('#stampify-time-taken')[0].innerHTML = 'Stampified in <b>' + stampifying_time_sec + ' seconds</b>';
    });

    $("#copy-btn").click(function() {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($('#stamp-code').text()).select();
        document.execCommand("copy");
        $temp.remove();
    });
});
