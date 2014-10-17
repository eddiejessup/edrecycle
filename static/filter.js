var main = function() {
    $('.results').hide();

    jQuery.getJSON($SCRIPT_ROOT + '/_search_data').done(function (data) {
        $('#loc').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(data.keys, request.term);
                response(results.slice(0, 10));
            },
            // source: data.keys,
            minLength: 3,
        });
    })

    $('#loc').keyup(function() {
        if ($('#loc').val().length > 3) {
            $.getJSON($SCRIPT_ROOT + '/_lookup', {loc: $('#loc').val()}, function(data) {
                $('.results').hide();
                if (data.success) {
                    $('#locname').text(data.results.location);
                    $('#day').text(data.results.day);
                    $('#ical').attr('href', $SCRIPT_ROOT + '/static/icals/' + data.results.filename + '.ical');
                    $('#pdf').attr('href', data.results.pdf);
                    if (data.results.blue) {
                        $('#yesblue').show()
                        $('#noblue').hide()
                        $('#blue-date').text(data.results.next_blue_date);
                    } else {
                        $('#yesblue').hide()
                        $('#noblue').show()
                    }
                    if (data.results.red) {
                        $('#yesred').show()
                        $('#nored').hide()
                        $('#red-date').text(data.results.next_red_date);
                    } else {
                        $('#yesred').hide()
                        $('#nored').show()
                    }
                    $('.results').show();
                }
            });
        }
    });
}

$(document).ready(main)
