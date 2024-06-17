// $('.vDateField ').inputmask('99/99/9999')

function setDateMasks(el = null) {
    if (el) {
        el.inputmask('99/99/9999')
        return
    }
    $('.vDateField ').inputmask('99/99/9999')
}