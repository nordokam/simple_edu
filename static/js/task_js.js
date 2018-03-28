function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var checkTaskCode = function (taskId, url) {
    $.ajax({
        method: 'POST',
        url: url,
        data: {
            task_id: taskId
        }
    }).done(function (response) {
        showCodeCheckResult(response)
    });
};


var showCodeCheckResult = function (response) {
    if (response.valid) {
        $('#successMsg').show();
        $('.messages').append('<div class="alert alert-success fade show" role="alert">\n' +
            '<button type="button" class="close" data-dismiss="alert"\n' +
            'aria-label="Close">\n' +
            '<span aria-hidden="true">&times;</span>\n' +
            '</button>\n' +
            '<strong>Your code is clean</strong>\n' +
            '</div>')
    } else {
        let new_message = '<div class="alert alert-danger fade show" role="alert">\n' +
            '<button type="button" class="close" data-dismiss="alert"\n' +
            'aria-label="Close">\n' +
            '<span aria-hidden="true">&times;</span>\n' +
            '</button>\n' +
            '<strong>Got errors!</strong>\n';
        response.errors.forEach(function callback(currentValue, index, array) {
            new_message += `<p class="mb-0">${currentValue}</p>`;
        });
        new_message += '</div>';
        $('.messages').append(new_message);
    }
};

$('.js_submit_order').click(function (e) {
    e.preventDefault();
    let taskId = this.getAttribute('data-id');
    let url = this.getAttribute('data-url');
    checkTaskCode(taskId, url);
});