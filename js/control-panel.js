
// creating a slot in the control panel area
function makeSeriesSelector() {
    let seriesSelector = document.createElement('div')
    seriesSelector.classList.add('series-selector')
    return seriesSelector
}

// make input drop-down list
function inputList(listName, placeHolder='', value='') {
    let input = document.createElement('input')
    input.setAttribute('list', listName)
    input.setAttribute('spellcheck', 'false')
    input.placeholder = placeHolder
    input.oninput = () => console.log(input.value)
    return input
}

// make input color picker
function colorList(value='#ffffff') {
    let color = document.createElement('input')
    color.type = 'color'
    color.value = value
    return color
}

// emptying panel
function returnEmptyPanel() {
    let panel = document.getElementById('panel')
    panel.innerHTML = ''
    return panel
}

function setSpecialChart() {
    let panel = returnEmptyPanel()
    for (let i = 0; i < 3; i++) {
        let b = document.createElement('button')
        b.innerHTML = 'Stringency'
        panel.appendChild(b)
    }
}