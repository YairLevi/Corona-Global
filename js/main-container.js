
// Main container
let container = am4core.create('chart', am4core.Container)
container.width = am4core.percent(98);
container.height = am4core.percent(100);
container.background = new am4core.RoundedRectangle()
container.valign = "bottom"
container.align = 'center'
container.background.fill = am4core.color("#00000000")
container.background.cornerRadius(20, 20, 0, 0)

// Buttons and Country, Date label container
let buttonsAndLabelContainer = container.createChild(am4core.Container)
buttonsAndLabelContainer.height = am4core.percent(12)
buttonsAndLabelContainer.maxHeight = '40px'
buttonsAndLabelContainer.width = am4core.percent(100)
buttonsAndLabelContainer.valign = 'top'

// country-date label
let label = buttonsAndLabelContainer.createChild(am4core.Label);
label.text = "Hello world!";
label.text.valign = 'middle'
label.height = am4core.percent(50)
label.fontSize = '1.5em';
label.paddingLeft = am4core.percent(1)
label.valign = "middle"
label.text.align = "left"
label.fill = am4core.color("#fff")

// buttons sub-container
let buttonContainer = buttonsAndLabelContainer.createChild(am4core.Container)
buttonContainer.valign = 'center'
buttonContainer.align = 'right'
buttonContainer.layout = 'horizontal'
buttonContainer.contentAlign = 'middle'
buttonContainer.contentValign = 'top'
buttonContainer.minWidth = am4core.percent(40)
buttonContainer.height = am4core.percent(60)
buttonContainer.height = am4core.percent(50)
buttonContainer.marginRight = am4core.percent(0.5)

// Chart managing container
let mainContainer = container.createChild(am4core.Container)
mainContainer.background = new am4core.RoundedRectangle()
mainContainer.background.cornerRadius(20, 20, 0, 0)
mainContainer.align = 'right'
mainContainer.valign = 'bottom'
mainContainer.width = am4core.percent(100)
mainContainer.height = am4core.percent(88)
mainContainer.background.fill = '#00000955'

// Actual Chart
let chart = mainContainer.createChild(am4charts.XYChart)
let chart3D = mainContainer.createChild(am4charts.XYChart3D)
setupChart(chart)
setupChart(chart3D)
function setupChart(chart) {
    chart.height = am4core.percent(88)
    chart.width = am4core.percent(80)
    chart.background.fill = '#ffffff00'
    chart.align = 'right'
    chart.valign = 'bottom'
    chart.tooltipX.text = 'Hello'

    chart.fontSize = '0.8em'
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.lineX.stroke = am4core.color('#fff')
    chart.cursor.lineY.disabled = true
    chart.cursor.behavior = "none";
}

chart.scrollbarX = new am4charts.XYChartScrollbar();
chart.scrollbarX.minHeight = 10
chart.scrollbarX.unselectedOverlay.fill = am4core.color("#fff");
chart.scrollbarX.unselectedOverlay.fillOpacity = 0.2;
chart.scrollbarX.background.fill = am4core.color("#000");
chart.scrollbarX.background.fillOpacity = 0.2;
chart.scrollbarX.startGrip.icon.disabled = true;
chart.scrollbarX.endGrip.icon.disabled = true;
chart.zIndex = 2

let chartLabel = mainContainer.createChild(am4core.Label)
chartLabel.text = "Loading Data...";
chartLabel.height = am4core.percent(50)
chartLabel.fontSize = '2em';
chartLabel.paddingLeft = am4core.percent(1)
chartLabel.valign = "middle"
chartLabel.align = "center"
chartLabel.fill = am4core.color("#fff")
chartLabel.visible = false

// Slider Container
let sliderContainer = mainContainer.createChild(am4core.Container)
sliderContainer.padding(20, 0, 0, 0)
sliderContainer.height = am4core.percent(10)
sliderContainer.minHeight = am4core.percent(10)
sliderContainer.width = am4core.percent(100)
sliderContainer.background.fill = '#00000000'
sliderContainer.valign = 'top'
sliderContainer.align = 'center'

// Slider
let slider = sliderContainer.createChild(am4core.Slider)
slider.width = am4core.percent(95)
slider.background.fill = '#ffffff'
slider.align = 'center'


