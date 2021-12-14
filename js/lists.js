
function datalistOptions(listName, options) {
    let list = document.getElementById(listName)
    for (let option of options) {
        let op = document.createElement('option')
        op.value = option
        list.appendChild(op)
    }
}

countryData.then(data => {
    datalistOptions('countries', Object.keys(data))
})
variables.then(data => datalistOptions('dynamic-variables', data['dynamic_variables']))
variables.then(data => {
    datalistOptions('static-variables', data['static_variables'])
    datalistOptions('static-variables', data['dynamic_variables'])
})
