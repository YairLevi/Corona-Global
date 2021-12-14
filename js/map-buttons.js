
function addButton(name) {
    let button = buttonContainer.createChild(am4core.Button)
    button.label.valign = "middle"
    button.label.text = name
    button.valign = 'top'
    button.label.fill = am4core.color("#ffffff");
    button.label.fontSize = "0.9rem";
    button.background.cornerRadius(30, 30, 30, 30);
    button.background.fillOpacity = 0;
    button.background.stroke = '#999';
    button.background.padding(2, 3, 2, 3);
    button.dummyData = 'off'

    let hover = button.background.states.create('hover')
    hover.properties.fillOpacity = 0

    let down = button.background.states.create('down')
    down.properties.fillOpacity = 0

    let circle = new am4core.Circle();
    circle.radius = 8;
    circle.fill = '#999';
    circle.valign = "middle";
    circle.marginRight = 5;
    button.icon = circle;

    return button
}

function updateButtons(json) {
    for (let k of Object.keys(json)) {
        if (json[k] == null) json[k] = 0
    }
    total_cases_btn.label.text = 'Total Cases: ' + json['total_cases']
    new_cases_btn.label.text = 'New Cases: ' + json['new_cases']
    total_deaths_btn.label.text = 'Total Deaths: ' + json['total_deaths']
    new_deaths_btn.label.text = 'New Deaths: ' + json['new_deaths']
}

let total_cases_btn = addButton('Total Cases: Loading...')
let new_cases_btn = addButton('New Cases: Loading...')
let total_deaths_btn = addButton('Total Deaths: Loading...')
let new_deaths_btn = addButton('New Deaths: Loading...')

