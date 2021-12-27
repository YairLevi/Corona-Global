const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
];

// all the dates
let dates;

// current date class.
class CurrentDate {
    constructor() {
        this.date = undefined
        this.callbacks = []
    }

    addCallBack(call) {this.callbacks.push(call)}

    emptyCallBack() {this.callbacks=[]}

    setDate(date) {
        if (date === this.date) return
        this.date = date
        for (let i = 0; i < this.callbacks.length; i++) {
            this.callbacks[i]()
        }
    }

    getDate() {return this.date}
}

const currentDate = new CurrentDate()

// init slider dates when ready
datesData.then(data => {
    dates = getDates(new Date(data['first_date']), new Date(data['last_date']))
    let date = dates[0]
    currentDate.setDate(date)
    let month = monthNames[date.getMonth()]
    let day = date.getDate().toString()
    let year = date.getFullYear()
    label.text = `Date: ${month} ${day}, ${year}`
    let y = year
    let m, d
    if (date.getMonth() + 1 < 10) m = `0${date.getMonth()+1}`
    else m = `${date.getMonth()+1}`
    if (date.getDate() < 10) d = `0${date.getDate()}`
    else d = `${date.getDate()}`
    let toSend = `${y}-${m}-${d}`
    fetchData('map', {date:toSend}).then(data => updateButtons(data))
})

function updateRange(data) {
    dates = getDates(new Date(data['first_date']), new Date(data['last_date']))
    onMouseUp()
}

// when mouse up on scrolling
function onMouseUp(event) {
    if (dates !== undefined) {
        let date = currentDate.getDate()
        let month = monthNames[date.getMonth()]
        let day = date.getDate().toString()
        let year = date.getFullYear()
        label.text = `Date: ${month} ${day}, ${year}`
        let y = year
        let m, d
        if (date.getMonth() + 1 < 10) m = `0${date.getMonth()+1}`
        else m = `${date.getMonth()+1}`
        if (date.getDate() < 10) d = `0${date.getDate()}`
        else d = `${date.getDate()}`
        let toSend = `${y}-${m}-${d}`
        fetchData('map', {date: toSend}).then(data => updateButtons(data))
    }
}

// when scrolling
function onRangeChanged(event) {
    if (dates !== undefined) {
        let date = dates[Math.floor((dates.length - 1) * event.target.start)]
        if (date === currentDate.date) return
        currentDate.setDate(date)
        let month = monthNames[date.getMonth()]
        let day = date.getDate().toString()
        let year = date.getFullYear()
        label.text = `Date: ${month} ${day}, ${year}`
    }
}

slider.events.on('rangechanged', onRangeChanged)
slider.events.on('up', onMouseUp)
