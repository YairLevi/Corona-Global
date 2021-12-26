
const port = 8000
const host = 'localhost'
const url = `http://${host}:${port}/`
const countryData = fetchData('countries', {})
const variables = fetchData('variables', {})
const datesData = fetchData('dates', {})

async function fetchData(route, queryParams) {
    let params = ''
    for (let key of Object.keys(queryParams)) {
        let value = queryParams[key]
        let param = `${key}=`
        if (Array.isArray(value)) {
            let string = `${value[0]}`
            for (let i = 1; i < value.length; i++) {
                string += `,${value[i]}`
            }
            param += `${string}`
        }
        else
            param += `${value}`
        params += `${param}&`}
    let request = `${url}${route}?${params}`
    let result = await fetch(request)
        .then(response => response.json())
        .then(data => data)
        .catch(err => console.log(`Error: ${err}\nPlease Contact The Admins.`))
    try {
        if (result['connection_error']) {
            alert('Connection to MySQL server closed. Please restart application.')
        }
    } catch (e) {}
    try {
        if (result.hasOwnProperty('error')) {
            alert(`Error occured:\n${result['error']}`)
        }
    } catch (e) {}
    return result
}
