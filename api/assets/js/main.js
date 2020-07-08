$(document).ready(function() {

    if ($('#original_url').text() != " ") {
        var stampifying_time_sec = 0;
        var stampify_duration_interval = setInterval(function() {
            stampifying_time_sec += 1;
            $('#stampify-time-taken')[0].innerHTML = 'Stampifying duration: <b>' + stampifying_time_sec + ' seconds </b>';
        }, 1000);
    }

    $('#stamp-iframe').on('load', function() {
        $('#stamp-code')[0].innerHTML = he.encode($('#stamp-iframe')[0].contentWindow.document.all[0].outerHTML);
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
