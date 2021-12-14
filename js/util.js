
Date.prototype.addDays = function(days) {
    let date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function getDates (startDate, stopDate) {
    let dateArray = []
    let currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push(currentDate);
        currentDate = currentDate.addDays(1);
    }
    return dateArray;
}

function getDateString(date=currentDate.getDate()) {
    // let date = currentDate.getDate()
    let month = date.getMonth() + 1
    if (month < 10) month = `0${month}`
    let day = date.getDate()
    if (day < 10) day = `0${day}`
    let year = date.getFullYear()
    return `${year}-${month}-${day}`
}

function onLogin() {
    document.getElementById('login').style.display = 'flex'
}

function onCloseLogin() {
    document.getElementById('login').style.display = 'none'
}

function onSend() {
    document.getElementById('send-request').style.display = 'flex'
}

function onCloseSend() {
    document.getElementById('send-request').style.display = 'none'
}

const size = {
    current: '55vh',
    maxUp: '30vh',
    maxDown: '88vh',
}

function resize(direction) {
    let chart = document.getElementById('chart')
    let newTop = '55vh'
    mainContainer.height = am4core.percent(direction === 'up' ? 90 : 88)
    if (size.current === '55vh') {
        newTop = (direction === 'up' ? 30 : 88) + 'vh'
    }
    chart.style.setProperty('--top', newTop)
    size.current = newTop

    // Reposition control panel
    let cp = document.getElementById('control-panel')
    switch (size.current) {
        case '55vh':
            cp.style.display = 'flex'
            cp.style.top = '68vh'
            break
        case '30vh':
            cp.style.top = '50vh'
            break
        case '88vh':
            cp.style.display = 'none'
            break
    }
}

function sizeUp() {
    if (size.current === size.maxUp) return
    resize('up')
}

function sizeDown() {
    if (size.current === size.maxDown) return
    resize('down')
}