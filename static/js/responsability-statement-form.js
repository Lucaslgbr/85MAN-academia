function addContextVariable(context_variable) {
    context_variable = `{{ ${context_variable} }}`
    const cursorPosition = $('#id_content').prop("selectionStart");
    let content = $('#id_content').val()
    const before = content.substr(0, cursorPosition)
    const after = content.substr(cursorPosition, content.length)
    content = `${before} ${context_variable} ${after}`
    const newCursorPosition = before.length + context_variable.length + 1
    $('#id_content').val(content)
    $('#id_content').focus();
    $('#id_content').prop("selectionStart", newCursorPosition);
    $('#id_content').prop("selectionEnd", newCursorPosition);

}