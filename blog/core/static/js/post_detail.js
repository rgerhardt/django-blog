var approveComment = function () {
    var btn = $(this);
    var approvalUrl = btn.data('approve-url');
    
    $.ajax({
        type: 'GET',
        url: approvalUrl,
        dataType: 'json',
        success: function (response) {
            window.location.reload();
        },
        error: function (xhr,errmsg,err) {
            alert('Internal error');
        }
    });
};

var disapproveComment = function () {
    var btn = $(this);
    var disapproveUrl = btn.data('disapprove-url');

    $.ajax({
        type: 'GET',
        url: disapproveUrl,
        success: function (result) {
            window.location.reload();
        },
        error: function (xhr, errmsg, err) {
           console.log(xhr);
        }
    });
};

var main = function() {
    $('.approve-btn').click(approveComment);
    $('.disapprove-btn').click(disapproveComment);
};

$(main);