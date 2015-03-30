var main = function() {
    $('.results').hide();

    jQuery.getJSON($SCRIPT_ROOT + '/_search_data').done(function (data) {
        $('#loc').autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(data.keys, request.term);
                response(results.slice(0, 10));
            },
            minLength: 3,
        });
    })
}

var search = function(value) {
    if (value.length > 3) {
        $.getJSON($SCRIPT_ROOT + '/_lookup', {loc: value}, function(data) {
            $('.results').hide();
            if (data.success) {
                $('#locname').text(data.results.location);
                $('#day').text(data.results.day);
                $('#ical').attr('href', $SCRIPT_ROOT + '/static/icals/' + data.results.filename + '.ical');
                $('#pdf').attr('href', data.results.pdf);
                $('#blue').text(data.results.blue_msg);
                $('#red').text(data.results.red_msg);
                $('.results').show();
            }
        });
    }
}

$(document).ready(main)
$(document).on('propertychange change keyup input paste', '#loc', function() {search($('#loc').val())});
$(document).on('autocompleteselect', '#loc', function(event, ui) {search(ui.item.value);});
