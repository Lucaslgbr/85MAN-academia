function reduceListToHtml(list, htmlTemplate, initialContent = '') {
    return list.reduce((content, object, idx) => {
        return content += htmlTemplate(object, idx)
    }, initialContent)
}

function buildSelectDropdownFromList({
                                         list,
                                         labelKey,
                                         valueKey = 'id',
                                         hasEmptyOption = true,
                                         className = '',
                                         id = '',
                                         disabled = false,
                                         //the onchange method name nees to be an string with the method name because it will be rendered in the DOM later
                                         onchange = () => {
                                         },
                                         checkSelectedCallback = () => false
                                     }) {
    return `
            <select ${disabled ? 'disabled' : ''} id="${id}" onchange='${onchange}' class="form-control ${className}">
                                        ${reduceListToHtml(list, (item) => `<option ${checkSelectedCallback(item) ? 'selected' : ''} value="${item[valueKey]}">${item[labelKey]}</option>`, hasEmptyOption ? '<option value="">--------------</option>' : '')}                                                        
                                    </select>
`
}