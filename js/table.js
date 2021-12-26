
// when closing the update panel
function onCloseUpdatePanel() {
    document.getElementById('updatePanel').style.display = 'none'
}

// when submitting the name and password to check if admin
async function onSubmit() {
    let username = document.getElementById('mail').value
    let password = document.getElementById('password').value
    let result = await fetchData('admin', {username: username, password: password})
    if (result.hasOwnProperty('error')) return
    if (result['is_admin']) login()
    else showPopup('incorrect', 'Incorrect Username Or Password')
}

// display popup error text
function showPopup(name, text) {
    let obj = document.getElementById(name)
    obj.innerHTML = text
    obj.style.visibility = 'visible'
    setTimeout(() => obj.style.visibility = 'hidden', 1500)
}

// check if logged in - to avoid asking again
let hasLoggedIn=false
function login() {
    if (hasLoggedIn) return
    onCloseLogin()
    generateTable()
    document.getElementById('updatePanel').style.display = 'flex'
    document.getElementById('login-button').onclick = () => {
        document.getElementById('updatePanel').style.display = 'flex'
        generateTable()
    }
    hasLoggedIn = true
}

// adding a new measurement type as admin
async function addMsr() {
    let input = document.getElementById('msr-input')
    if (input.value !== '' && !(input.value.indexOf(' ') >= 0)) {
        let result = await fetchData('addmsr', {msr: input.value})
        if (result['exist']) {
            showPopup('sent-msr', 'Already Exists')
            return
        }
        datalistOptions('dynamic-variables', [input.value])
        datalistOptions('static-variables', [input.value])
        showPopup('sent-msr', 'Added New Measurement')
    } else {
        showPopup('sent-msr', 'Invalid Name - Contains WhiteSpaces or Empty')
    }
    input.value = ''
}

// generating the table of requests from users
async function generateTable() {
    let table = document.getElementById('table')
    table.innerHTML = ''
    table.appendChild(createColumns(['Country', 'Date', 'Variable', 'New Value', '', '']))
    let requests = await fetchData('updates', {})
    if (requests.hasOwnProperty('error')) return
    if (requests === null) return
    for (let country of Object.keys(requests)) {
        for (let dict of requests[country]) {
            table.appendChild(createRow(
                [country, dict['msr_timestamp'], dict['msr_name'], dict['msr_value']]))
        }
    }
}

// updaing a new value
async function updateValue() {
    let country = document.getElementById('country-input').value
    let date = document.getElementById('date-input').value
    let variable = document.getElementById('variable-input').value
    let value = document.getElementById('value-input').value
    let endDates = await datesData.then(data => data)
    let text = undefined

    if (!is_valid_datalist_value('countries', country)) {
        text = 'Invalid Country'
    } else if (date === '') {
        text = 'Invalid Date'
    } else if (!is_valid_datalist_value('dynamic-variables', variable)) {
        text = 'Invalid Variable'
    } else if (isNaN(parseInt(value))) {
        text = 'Invalid Value'
    }

    if (text === undefined) {
        showPopup('result', 'Sent!')
        fetchData('update', {
            country: country,
            date: date,
            variable: variable,
            value: value
        })
    } else {
        showPopup('result', text)
    }
}

// creating a column for the table
function createColumns(columns) {
    let row = document.createElement('tr')
    for (let c of columns) {
        let t = document.createElement('th')
        t.innerHTML = c
        row.appendChild(t)
    }
    return row
}

// creating a new row for the table
function createRow(values) {
    let row = document.createElement('tr')
    for (let v of values) {
        let t = document.createElement('td')
        t.innerHTML = v
        row.appendChild(t)
    }

    // Approve button
    let t = document.createElement('td')
    let approve = document.createElement('button')
    approve.innerHTML = 'Approve'
    approve.classList.add('approve')
    approve.onclick = () => approveRequest(values)
    t.appendChild(approve)
    row.appendChild(t)

    // Deny button
    t = document.createElement('td')
    let deny = document.createElement('button')
    deny.innerHTML = 'Deny'
    deny.classList.add('deny')
    deny.onclick = () => denyRequest(values)
    t.appendChild(deny)
    row.appendChild(t)

    // return final row product
    return row
}

// approving a request - changing the data in the data base
async function approveRequest(values) {
    let result = await fetchData('approve', {
        country: values[0],
        date: values[1],
        variable: values[2],
        value: values[3],
    })
    if (result.hasOwnProperty('error')) return
    if (result['isFound']) {
        showPopup('updated', 'Action Succeeded')
    } else {
        showPopup('updated', 'Failed. Query has been taken care of.')
    }
    generateTable()
}

// denying a request.
async function denyRequest(values) {
    let result = await fetchData('deny', {
        country: values[0],
        date: values[1],
        variable: values[2],
        value: values[3],
    })
    if (result.hasOwnProperty('error')) return
    if (result['isFound']) {
        showPopup('updated', 'Action Succeeded')
    } else {
        showPopup('updated', 'Failed. Query has been taken care of.')
    }
    generateTable()
}