
// Graph line stroke size
const STROKE_SIZE = 2

// Is the input a valid option of the given list
function is_valid_datalist_value(idDataList, inputValue) {
    let selector = "#" + idDataList + " option[value='" + inputValue + "']"
    let option = document.querySelector(selector);
    if (option != null) return option.value.length > 0;
    return false;
}

// delete everything inside of a given chart
function emptyChart(chart) {
    while (chart.series.length) {
        chart.series.pop()
    }
    while (chart.xAxes.length) {
        chart.xAxes.pop()
    }
    while (chart.yAxes.length) {
        chart.yAxes.pop()
    }
    currentDate.emptyCallBack()
}

// Graph 1 line series class
class Line {

    constructor(input, color) {
        this.input = input
        this.color = color
        this.country = undefined
        this.series = undefined
        input.oninput = () => {
            this.refreshSeries()
        }
        color.oninput = () => {
            if (this.series !== undefined)
                this.series.stroke = color.value
        }
    }

    refreshSeries() {
        if (!is_valid_datalist_value(this.input.list.id, this.input.value)) {
            if (this.series !== undefined) chart.series.removeValue(this.series)
            this.series = undefined
            return
        }
        fetchData('var/dynamic', {
            country: this.country,
            variable: this.input.value
        })
        .then(data => {
            if (this.series !== undefined) chart.series.removeValue(this.series)
            let seriesData = []
            for (let key of Object.keys(data)) {
                seriesData.push({
                    date: new Date(key),
                    value: data[key]
                })
            }
            let newSeries = new am4charts.LineSeries()
            newSeries.dataFields.dateX = 'date'
            newSeries.dataFields.valueY = 'value'
            newSeries.strokeWidth = STROKE_SIZE
            newSeries.stroke = this.color.value
            newSeries.data = seriesData

            newSeries.tooltip.pointerOrientation = "horizontal";
            newSeries.tooltip.getStrokeFromObject = true;
            newSeries.tooltip.getFillFromObject = false;
            newSeries.tooltip.background.fill = am4core.color("#000000");
            newSeries.tooltip.fontSize = "0.8em";
            newSeries.tooltipText = `${this.input.value}: {valueY}`;

            this.series = newSeries
            chart.series.push(newSeries)
        })
    }
}

// Graph 2 line series class. different from the first class in that its
// variables can be static.
class Line2 {

    constructor(input, color) {
        this.input = input
        this.color = color
        this.variable = undefined
        this.series = undefined
        input.oninput = () => {
            this.refreshSeries()
        }
        color.oninput = () => {
            if (this.series !== undefined)
                this.series.stroke = color.value
        }
    }

    refreshSeries() {
        if (!is_valid_datalist_value(this.input.list.id, this.input.value)) {
            if (this.series !== undefined) chart.series.removeValue(this.series)
            this.series = undefined
            return
        }
        let route = 'var/static'
        if (is_valid_datalist_value('dynamic-variables', this.variable)) route = 'var/dynamic'
        fetchData(route, {
            country: this.input.value,
            variable: this.variable
        })
        .then(data => {
            if (this.series !== undefined) chart.series.removeValue(this.series)
            let seriesData = []
            for (let key of Object.keys(data)) {
                seriesData.push({
                    date: new Date(key),
                    value: data[key]
                })
            }
            let newSeries = new am4charts.LineSeries()
            newSeries.dataFields.dateX = 'date'
            newSeries.dataFields.valueY = 'value'
            newSeries.strokeWidth = STROKE_SIZE
            newSeries.stroke = this.color.value
            newSeries.data = seriesData

            newSeries.tooltip.pointerOrientation = "horizontal";
            newSeries.tooltip.getStrokeFromObject = true;
            newSeries.tooltip.getFillFromObject = false;
            newSeries.tooltip.background.fill = am4core.color("#000000");
            newSeries.tooltip.fontSize = "0.8em";
            newSeries.tooltipText = "{valueY}";

            this.series = newSeries
            chart.series.push(newSeries)
        })
    }
}

// first Line chart.
class LineChart {

    constructor() {
        this.country = inputList('countries', 'Select country')
        this.hasBeenDisplayed = false
        this.variables = []
        for (let i = 0; i < 3; i++) {
            let json = {}
            json.value = inputList('dynamic-variables', 'Select variable')
            json.color = colorList('#ffffff')
            json.series = new Line(json.value, json.color)
            this.variables.push(json)
        }
    }

    displayPanel() {
        emptyChart(chart)

        while (chart3D.series.length) {
            chart3D.series.pop()
        }
        chart3D.visible = false
        chartLabel.visible = false
        chart.visible = true

        let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
        dateAxis.renderer.labels.template.fill = '#fff'
        dateAxis.renderer.grid.template.stroke = '#fff'
        dateAxis.renderer.minGridDistance = 50;
        dateAxis.dataFields.dateX = 'date'
        dateAxis.cursorTooltipEnabled = false

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis())
        valueAxis.renderer.labels.template.fill = '#fff'
        valueAxis.renderer.grid.template.stroke = '#fff'
        valueAxis.renderer.minGridDistance = 30;
        valueAxis.dataFields.valueY = 'value'
        valueAxis.cursorTooltipEnabled = false

        let panel = returnEmptyPanel()
        let ss = makeSeriesSelector()
        this.country.oninput = () => this.displayChart()
        ss.appendChild(this.country)
        panel.appendChild(ss)
        for (let i = 0; i < this.variables.length; i++) {
            let ss = makeSeriesSelector()
            ss.appendChild(this.variables[i].value)
            ss.appendChild(this.variables[i].color)
            panel.appendChild(ss)
        }
        if (this.hasBeenDisplayed) this.displayChart()
        this.hasBeenDisplayed = true
    }

    displayChart() {
        if (is_valid_datalist_value(this.country.list.id, this.country.value)) {
            for (let i = 0; i < this.variables.length; i++) {
                this.variables[i].series.country = this.country.value
                this.variables[i].series.refreshSeries()
            }
        }
    }
}

// Second line chart - used to compare between countries
class ColumnChart {
    constructor() {
        this.variable = inputList('static-variables', 'Select variable')
        this.hasBeenDisplayed = false
        this.countries = []
        for (let i = 0; i < 3; i++) {
            let json = {}
            json.value = inputList('countries', 'Select country')
            json.color = colorList('#ffffff')
            json.series = new Line2(json.value, json.color)
            this.countries.push(json)
        }
    }

    displayPanel() {
        while (chart3D.series.length) {
            chart3D.series.pop()
        }
        emptyChart(chart)
        // mainContainer.children.removeValue(chart3D)
        chart3D.visible = false
        chartLabel.visible = false
        chart.visible = true

        let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
        dateAxis.renderer.labels.template.fill = '#fff'
        dateAxis.renderer.grid.template.stroke = '#fff'
        dateAxis.renderer.minGridDistance = 50;
        dateAxis.dataFields.dateX = 'date'
        dateAxis.cursorTooltipEnabled = false

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis())
        valueAxis.renderer.labels.template.fill = '#fff'
        valueAxis.renderer.grid.template.stroke = '#fff'
        valueAxis.renderer.minGridDistance = 30;
        valueAxis.dataFields.valueY = 'value'
        valueAxis.cursorTooltipEnabled = false

        let panel = returnEmptyPanel()
        let ss = makeSeriesSelector()
        this.variable.oninput = () => this.displayChart()
        ss.appendChild(this.variable)
        panel.appendChild(ss)
        for (let i = 0; i < this.countries.length; i++) {
            let ss = makeSeriesSelector()
            ss.appendChild(this.countries[i].value)
            ss.appendChild(this.countries[i].color)
            panel.appendChild(ss)
        }
        if (this.hasBeenDisplayed) this.displayChart()
        this.hasBeenDisplayed = true
    }

    displayChart() {
        if (is_valid_datalist_value(this.variable.list.id, this.variable.value)) {
            for (let i = 0; i < this.countries.length; i++) {
                this.countries[i].series.variable = this.variable.value
                this.countries[i].series.refreshSeries()
            }
        }
    }
}

// Special charts dispalyed
class SpecialChart {
    constructor() {
        this.charts = [
            'Infected to Population Ratio Per Continent',
            'Infected to Global Population Ratio',
            'The Most Aged Countries And Their Death Ratio',
        ]
        this.lastShown = undefined
        this.buttons = []
        for (let i = 0; i < 3; i++) {
            let btn = document.createElement('button')
            btn.innerHTML = this.charts[i]
            btn.setAttribute('data-tooltip', this.charts[i])
            this.buttons.push(btn)
        }
    }

    displayPanel() {
        emptyChart(chart)
        chart.visible = false
        chart3D.visible = true

        let panel = returnEmptyPanel()
        this.buttons[0].onclick = () => this.displayFirstChart()
        this.buttons[1].onclick = () => this.displaySecondChart()
        this.buttons[2].onclick = () => this.displayThirdChart()
        for (let btn of this.buttons) {
            let ss = makeSeriesSelector()
            ss.appendChild(btn)
            panel.appendChild(ss)
        }
        if (this.lastShown !== undefined)
            this.buttons[this.lastShown].onclick()
    }

    prepareChart(Class) {
        mainContainer.children.removeValue(chart3D)
        while (chart3D.series.length > 0) chart3D.series.pop()
        chart3D = mainContainer.createChild(Class)
        setupChart(chart3D)
    }

    async displayFirstChart() {
        this.lastShown = 0
        this.prepareChart(am4charts.XYChart3D)

        var categoryAxis = chart3D.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "continent";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.minGridDistance = 30;
        categoryAxis.renderer.labels.template.fill = '#fff'
        categoryAxis.renderer.grid.template.stroke = '#fff'
        categoryAxis.cursorTooltipEnabled = false

        var valueAxis = chart3D.yAxes.push(new am4charts.ValueAxis());
        valueAxis.renderer.minGridDistance = 50
        valueAxis.renderer.labels.template.fill = '#fff'
        valueAxis.renderer.grid.template.stroke = '#fff'
        valueAxis.cursorTooltipEnabled = false

        chart3D.cursor = new am4charts.XYCursor();
        chart3D.cursor.lineX.stroke = am4core.color('#fff')
        chart3D.cursor.lineY.stroke = am4core.color('#fff')

        chartLabel.visible = true
        await fetchData('case_percentage_population', {})
            .then(data => {

                let d = []
                for (let cont of Object.keys(data)) {
                    d.push({
                        continent: cont,
                        population: data[cont]['total_population'] / 500000000,
                        cases_percentage: data[cont]['cases_percentage']
                    })
                }
                chart3D.data = d
            })
        chartLabel.visible = false

        // Create series
        var case_percent = chart3D.series.push(new am4charts.ColumnSeries3D());
        case_percent.dataFields.valueY = "cases_percentage";
        case_percent.dataFields.categoryX = "continent";
        case_percent.name = "Case Percentage";
        case_percent.clustered = true;
        case_percent.columns.template.tooltipText = "{name}: {valueY}";
        case_percent.columns.template.fillOpacity = 0.9;
        case_percent.fill = '#5cb287'
        case_percent.columns.template.tooltipX = am4core.percent(50);
        case_percent.columns.template.tooltipY = am4core.percent(75);
        case_percent.tooltip.pointerOrientation = 'down'

        var population = chart3D.series.push(new am4charts.ColumnSeries3D());
        population.dataFields.valueY = "population";
        population.dataFields.categoryX = "continent";
        population.name = "Population";
        population.clustered = false;
        population.columns.template.tooltipText = "{name} (Factor of 500m)\n{valueY}";
        population.fill = '#78c'
        population.columns.template.tooltipX = am4core.percent(50);
        population.columns.template.tooltipY = am4core.percent(25);
        population.tooltip.pointerOrientation = 'up'
    }

    async displaySecondChart() {
        this.lastShown = 1
        this.prepareChart(am4charts.PieChart3D)

        let series = chart3D.series.push(new am4charts.PieSeries3D());
        chart3D.hiddenState.properties.opacity = 0; // this creates initial fade-in
        chart3D.hiddenState.properties.fill = '#fff'
        chart3D.legend = new am4charts.Legend();
        chart3D.legend.labels.template.fill = '#fff'
        chart3D.legend.valueLabels.template.fill = '#fff'
        series.labels.template.fill = '#fff'
        series.labels.template.fontSize = 17
        series.slices.template.stroke = '#fff'

        chartLabel.visible = true
        await fetchData('case_percentage_global', {})
            .then(data => {
                let d = []
                for (let cont of Object.keys(data)) {
                    d.push({
                        continent: cont,
                        percentage: data[cont]
                    })
                }
                chart3D.data = d
            })
        chartLabel.visible = false

        series.dataFields.value = "percentage";
        series.dataFields.category = "continent";
    }

    async displayThirdChart() {
        this.lastShown = 2
        this.prepareChart(am4charts.XYChart3D)

        var categoryAxis = chart3D.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "country";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.minGridDistance = 30;
        categoryAxis.renderer.labels.template.fill = '#fff'
        categoryAxis.renderer.grid.template.stroke = '#fff'
        categoryAxis.cursorTooltipEnabled = false

        var valueAxis = chart3D.yAxes.push(new am4charts.ValueAxis());
        valueAxis.renderer.minGridDistance = 50
        valueAxis.renderer.labels.template.fill = '#fff'
        valueAxis.renderer.grid.template.stroke = '#fff'
        valueAxis.cursorTooltipEnabled = false

        chart3D.cursor = new am4charts.XYCursor();
        chart3D.cursor.lineX.stroke = am4core.color('#fff')
        chart3D.cursor.lineY.stroke = am4core.color('#fff')

        chartLabel.visible = true
        await fetchData('death_percentage', {})
            .then(data => {
                let d = []
                for (let cont of Object.keys(data)) {
                    d.push({
                        country: cont,
                        deaths: data[cont]['deaths_percentage'],
                        population: data[cont]['total_population'] / 500000000,
                        aged70orAbove: data[cont]['aged_70_older'],
                        total_cases: data[cont]['total_cases'],
                        total_deaths: data[cont]['total_deaths']
                    })
                }
                chart3D.data = d
            })
        chartLabel.visible = false

        // Create series
        var deaths_percent = chart3D.series.push(new am4charts.ColumnSeries3D());
        deaths_percent.dataFields.valueY = "deaths";
        deaths_percent.dataFields.categoryX = "country";
        deaths_percent.name = "Deaths Percentage";
        deaths_percent.clustered = false;
        deaths_percent.columns.template.tooltipText = "{name}: {valueY}%\n(total: {total_deaths})";
        deaths_percent.columns.template.fillOpacity = 0.9;
        deaths_percent.fill = '#1187aa'
        deaths_percent.columns.template.tooltipX = am4core.percent(50);
        deaths_percent.columns.template.tooltipY = am4core.percent(75);
        deaths_percent.tooltip.pointerOrientation = 'down'

        var aged70 = chart3D.series.push(new am4charts.ColumnSeries3D());
        aged70.dataFields.valueY = "aged70orAbove";
        aged70.dataFields.categoryX = "country";
        aged70.name = "Population over 70";
        aged70.clustered = false;
        aged70.columns.template.tooltipText = "{name}: {valueY}%";
        aged70.fill = '#11d2dd'
        aged70.columns.template.tooltipX = am4core.percent(50);
        aged70.columns.template.tooltipY = am4core.percent(25);
        aged70.tooltip.pointerOrientation = 'up'

    }
}

// Init all charts and display the first one as default.
const lineChart = new LineChart()
const columnChart = new ColumnChart()
const specialChart = new SpecialChart()
lineChart.displayPanel()