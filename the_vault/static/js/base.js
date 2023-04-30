$(document).ready(function () {

    // Get the current timezone from the client side
    // $('#timezone').text(Intl.DateTimeFormat().resolvedOptions().timeZone);

    $.ajax({
        url: '/api/app_settings',
        type: 'GET',
        dataType: 'json',
        success: function (data) {

            if (data.UI_TIMEZONE) {
                $('#timezone').text(data.UI_TIMEZONE);
            } else {
                $('#timezone').text('NOT CONFIGURED');
            }
        },
        error: function (data) {
            $('#timezone').text('ERROR GETTING TIMEZONE');
        }
    });
});
