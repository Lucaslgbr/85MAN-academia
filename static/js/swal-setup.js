function SwalSetup(key, title, type, url) {
    swal({
        title: title,
        type: type,
        showCancelButton: true,
        confirmButtonColor: '#1ab394',
        allowEscapeKey: false,
        confirmButtonText: 'Sim',
        cancelButtonText: 'Não',
        closeOnConfirm: false,
        allowOutsideClick: false
    }).then(function (data) {
        if (!data['dismiss']) {
            $.ajax({
                url: url,
                method: "POST",
                data: {
                    id: key,
                    csrfmiddlewaretoken: CONTEXT.CSRF_TOKEN
                },
                success: function (data) {
                    window.location.reload();
                }
            });
        }
    });
}