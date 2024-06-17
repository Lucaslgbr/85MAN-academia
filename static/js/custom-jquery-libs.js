$.fn.ajaxSelect2 = function (opts = {}) {
    const select_data = {
        ...opts,
        width: opts.width ?? '100%',
        minimumInputLength: 3,
        ajax: {
            url: opts.url,
            data: function (params) {
                return {...params, ...opts.data ?? {}}
            },
            datatype: 'json',
        }
    }
    if (opts.processResults) {
        select_data.ajax.processResults = opts.processResults
    }
    delete opts.url
    delete opts.processResults
    $(this).select2(select_data);
    return this
}
