


let chart = am4core.create("chart", am4charts.XYChart);
chart.paddingRight = 20;
chart.height = am4core.percent(100)
chart.width = am4core.percent(100)

let data = [];
let visits = 10;
for (let i = 1; i < 50000; i++) {
    visits += Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10);
    data.push({ date: new Date(2018, 0, i), value: visits });
}

chart.data = data;

let white = am4core.color("#fff")

let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.grid.template.location = 0;
dateAxis.minZoomCount = 5;
dateAxis.renderer.labels.template.fill = white

// this makes the data to be grouped
dateAxis.groupData = true;
dateAxis.groupCount = 500;

let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.labels.template.fill = white


let series = chart.series.push(new am4charts.LineSeries());
series.dataFields.dateX = "date";
series.dataFields.valueY = "value";
series.tooltipText = "{valueY}";
series.tooltip.pointerOrientation = "vertical";
series.tooltip.background.fillOpacity = 0.5;

chart.cursor = new am4charts.XYCursor();
chart.cursor.xAxis.fill = white
chart.cursor.xAxis = dateAxis;


