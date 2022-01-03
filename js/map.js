am4core.useTheme(am4themes_animated);

countryData.then(data => {

    let mapContainer = am4core.create('map', am4core.Container)
    mapContainer.width = am4core.percent(100)
    mapContainer.height = am4core.percent(100)

    let map = mapContainer.createChild(am4maps.MapChart);
    map.geodata = am4geodata_worldLow;
    map.projection = new am4maps.projections.Miller();
    map.deltaLongitude = -10;
    map.height = am4core.percent(80)
    map.seriesContainer.events.disableType("doublehit");
    map.chartContainer.background.events.disableType("doublehit");

    let title = mapContainer.createChild(am4core.Label)
    title.valign = 'top'
    title.align = 'left'
    title.margin(10, 0, 0, 20)
    title.fontSize = 25
    title.text = 'COVID-19 Spread Data'
    title.fill = '#fff'

    let worldSeries = map.series.push(new am4maps.MapPolygonSeries());
    worldSeries.exclude = ["AQ"];
    worldSeries.useGeodata = true;
    worldSeries.dataFields.zoomLevel = "zoomLevel";
    worldSeries.dataFields.zoomGeoPoint = "zoomGeoPoint";

    let polygonTemplate = worldSeries.mapPolygons.template;
    polygonTemplate.tooltipText = '{name}\n\nContinent: {continent}\nPopulation: {population}'
    polygonTemplate.fill = am4core.color('#555555')
    polygonTemplate.stroke = am4core.color('#000000')
    polygonTemplate.strokeWidth = 0.2
    polygonTemplate.propertyFields.fill = "fill";

    let hs = polygonTemplate.states.create("hover");
    hs.transitionDuration = 500;
    hs.properties.fill = am4core.color("#cccccc");

    polygonTemplate.events.on('hit', (ev) => {
        let country = ev.target.dataItem.dataContext.name
        lineChart.country.value = country
        lineChart.displayPanel()
        // lineChart.displayChart()
        ev.target.series.chart.zoomToMapObject(ev.target, 3)
    })

    for (let country of Object.keys(data)) {
        let iso = ISObyCountry(country)
        if (iso === undefined) continue
        let object = {
            id: iso,
            name: country,
            continent: data[country]['continent'],
            population: data[country]['population']
        }
        if (iso === 'US') {
            object['zoomLevel'] = 2
            object['zoomGeoPoint'] = {
                latitude: 40,
                longitude: -100
            }
        }
        worldSeries.data.push(object)
    }

    document.getElementById('zoom-in').onclick = (e) => {
        map.zoomIn()
    }
    document.getElementById('zoom-out').onclick = (e) => {
        map.goHome()
    }
})

function ISObyCountry(country) {
    if (country === 'Congo') return 'CD'
    for (let key of Object.keys(am4geodata_data_countries2))
        if (am4geodata_data_countries2[key]['country'] === country)
            return key
    c = {
        'Brunei': 'BN',
        'Iran': 'IR',
        'Laos': 'LA',
        'South Korea': 'KR',
        'Palestine': 'PS',
        'Syria': 'SY',
        'Timor': 'TL',
        'Vietnam': 'VN',
        'Czechia': 'CZ',
        'Faeroe Islands': 'FO',
        'Moldova':'MD',
        'Russia':'RU',
        'Vatican':'VA',
        'Democratic Republic of Congo':'CG',
        'Eswatini':undefined,
        'Saint Helena':'SH',
        'Tanzania':'TZ',
        'Bonaire Sint Eustatius and Saba':'BQ',
        'British Virgin Islands':'VG',
        'Sint Maarten':'SX',
        'Bolivia': 'BO',
        'Falkland Islands':'FK',
        'Venezuela':'VE',
        'Micronesia':'FM',
    }
    for (let key of Object.keys(c)) {
        if (key === country) return c[key]
    }
    return undefined
}
