/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

// Apply chart themes
am4core.useTheme(am4themes_animated);
am4core.useTheme(am4themes_kelly);

// Create chart instance
var chart = am4core.create("chartdiv", am4charts.XYChart);

chart.marginRight = 400;

// Add data
chart.data = [{
    "country": "Lithuania",
    "research": 501.9,
    "marketing": 250,
    "sales": 199
}, {
    "country": "Czech Republic",
    "research": 301.9,
    "marketing": 222,
    "sales": 251
}, {
    "country": "Ireland",
    "research": 201.1,
    "marketing": 170,
    "sales": 199
}, {
    "country": "Germany",
    "research": 165.8,
    "marketing": 122,
    "sales": 90
}, {
    "country": "Australia",
    "research": 139.9,
    "marketing": 99,
    "sales": 252
}, {
    "country": "Austria",
    "research": 128.3,
    "marketing": 85,
    "sales": 84
}, {
    "country": "UK",
    "research": 99,
    "marketing": 93,
    "sales": 142
}, {
    "country": "Belgium",
    "research": 60,
    "marketing": 50,
    "sales": 55
}, {
    "country": "The Netherlands",
    "research": 50,
    "marketing": 42,
    "sales": 25
}];

//console.log('chart', chart);

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "country";
categoryAxis.title.text = "Local country offices";
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.minGridDistance = 20;


var  valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.title.text = "Expenditure (M)";

// Create series
var series = chart.series.push(new am4charts.ColumnSeries());
series.dataFields.valueY = "research";
series.dataFields.categoryX = "country";
series.name = "Research";
series.tooltipText = "{name}: [bold]{valueY}[/]";
series.stacked = true;

var series2 = chart.series.push(new am4charts.ColumnSeries());
series2.dataFields.valueY = "marketing";
series2.dataFields.categoryX = "country";
series2.name = "Marketing";
series2.tooltipText = "{name}: [bold]{valueY}[/]";
series2.stacked = true;

var series3 = chart.series.push(new am4charts.ColumnSeries());
series3.dataFields.valueY = "sales";
series3.dataFields.categoryX = "country";
series3.name = "Sales";
series3.tooltipText = "{name}: [bold]{valueY}[/]";
series3.stacked = true;

// Add cursor
chart.cursor = new am4charts.XYCursor();




///////////////////////////// BACK UP FGOR SERIES>JHS ///////////////////////


function ColumnSeries() {

    while (chart.series.length) {
        chart.series.pop()
    }
    while (chart.xAxes.length) {
        chart.xAxes.pop()
    }
    while (chart.yAxes.length) {
        chart.yAxes.pop()
    }

    // let data =  [
    //     {
    //         country:'Israel',
    //         value:10000
    //     },
    //     {
    //         country:'rael',
    //         value:10000
    //     },{
    //         country:'srael',
    //         value:-1000
    //     },
    // ]

    let data = []
    for (let i = 0; i < 200; i++) {
        data.push({
            country: `${i}AA`,
            value: Math.random(),
        })
    }
    chart.data = data


    let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis())
    categoryAxis.renderer.labels.template.fill = '#fff'
    categoryAxis.renderer.grid.template.stroke = '#fff'
    categoryAxis.renderer.minGridDistance = 50;
    categoryAxis.dataFields.category = 'country'

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis())
    valueAxis.renderer.labels.template.fill = '#fff'
    valueAxis.renderer.grid.template.stroke = '#fff'
    valueAxis.renderer.minGridDistance = 30;
    valueAxis.dataFields.value = 'value'

//
//
// // Create series
//     let series = chart.series.push(new am4charts.ColumnSeries());
//     series.dataFields.valueY = "value";
//     series.dataFields.categoryX = "country";
//     series.tooltipText = "{name}: [bold]{valueY}[/]";
//     series.stacked = true;
//
    chart.fontSize = '0.8em'
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.lineX.stroke = am4core.color('#fff')
    chart.cursor.lineY.stroke = am4core.color('#fff')

    // Add scrollbar
    // let scrollbar = new am4charts.XYChartScrollbar();
    // scrollbar.minHeight = 10
    //
    // chart.scrollbarX = scrollbar;
    // chart.scrollbarX.unselectedOverlay.fill = am4core.color("#fff");
    // chart.scrollbarX.unselectedOverlay.fillOpacity = 0.2;
    // chart.scrollbarX.background.fill = am4core.color("#000");
    // chart.scrollbarX.background.fillOpacity = 0.2;
    //
    // chart.scrollbarX.startGrip.icon.disabled = true;
    // chart.scrollbarX.endGrip.icon.disabled = true;
    // var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    // categoryAxis.dataFields.category = "country";
    // categoryAxis.title.text = "Local country offices";
    // categoryAxis.renderer.grid.template.location = 0;
    // categoryAxis.renderer.minGridDistance = 20;
    //
    //
    // var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    // valueAxis.title.text = "Expenditure (M)";
    // valueAxis.dataFields.value = 'value'


    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.valueY = "value";
    series2.dataFields.categoryX = "country";
    series2.name = "Marketing";
    series2.fill = '#fff'
    series2.stroke = '#000'
    series2.tooltipText = "{name}: [bold]{valueY}[/]";
    series2.stacked = true;

// Add cursor
//     chart.cursor = new am4charts.XYCursor();
}

function test() {
    // Add data
    chart.data = [{
        "country": "Lithuania",
        "marketing": 250,
    }, {
        "country": "Czech Republic",
        "marketing": 222,
    }, {
        "country": "Ireland",
        "marketing": 170,
    }, {
        "country": "Germany",
        "marketing": 122,
    }, {
        "country": "Australia",
        "marketing": 99,
    }, {
        "country": "Austria",
        "marketing": 85,
    }, {
        "country": "UK",
        "marketing": 93,
    }, {
        "country": "Belgium",
        "marketing": 50,
    }, {
        "country": "The Netherlands",
        "marketing": 42,
    }];

//console.log('chart', chart);

    chart.series.pop()
    chart.xAxes.pop()
    chart.yAxes.pop()
// Create axes
    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "country";
    categoryAxis.title.text = "Local country offices";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 20;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Expenditure (M)";


    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.valueY = "marketing";
    series2.dataFields.categoryX = "country";
    series2.name = "Marketing";
    series2.tooltipText = "{name}: [bold]{valueY}[/]";
    series2.stacked = true;

// Add cursor
    chart.cursor = new am4charts.XYCursor();
}

function addLineSeries(props) {
    let newSeries = chart.series.push(new am4charts.LineSeries())
    newSeries.dataFields.dateX = 'date'
    newSeries.dataFields.valueY = 'value'
    newSeries.strokeWidth = STROKE_SIZE
    newSeries.stroke = props.color
    newSeries.data = props.data
}

function addColumnSeries(props) {
    let newSeries = chart.series.push(new am4charts.ColumnSeries())
    newSeries.dataFields.categoryX = 'country'
    newSeries.dataFields.valueY = 'value'
    newSeries.strokeWidth = STROKE_SIZE
    newSeries.stroke = props.color
    newSeries.data = props.data
}

function getDummyData() {
    let data = []
    let visits = 10000;
    let dates = getDates(new Date('2021-1-5'), new Date('2021-8-25'))
    for (let i = 0; i < dates.length; i++) {
        visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
        data.push({date: dates[i], value: visits});
    }
    return data
}
