const map = L.map('map').setView([40.75, -73.95], 11);
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png', {
    maxZoom: 18
}).addTo(map);

// Adding Voyager Labels
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}.png', {
    maxZoom: 18,
    zIndex: 10
}).addTo(map);

var client = new carto.Client({
    apiKey: '9d8dfbe609f8a21a07aada09014da359eeccefd9',
    username: 'bendnorman'
});

const zillowNeighborhoodsDataset = new carto.source.Dataset(`
    zillowneighborhoods_ny
  `);

const zillowNeighborhoodsStyle = new carto.style.CartoCSS(`
    #layer {
    polygon-fill: #162945;
      polygon-opacity: 0.5;
      ::outline {
        line-width: 1;
        line-color: #FFFFFF;
        line-opacity: 0.5;
      }
    }
  `);
const zillowNeighborhoods = new carto.layer.Layer(zillowNeighborhoodsDataset, zillowNeighborhoodsStyle);

client.addLayers([zillowNeighborhoods]);
client.getLeafletLayer().addTo(map);

//// Project Profile
function getProjectData(form) {
    var address = form.inputbox.value;
    console.log(address)
    const Http = new XMLHttpRequest();
    const url = 'http://localhost:8080/?address=' + address;
    Http.open("GET", url, true);
    Http.send();

    Http.onerror = function() {
        console.log('There was an error!');
    };

    // Get data back
    Http.onload = function() {
        if (Http.readyState == XMLHttpRequest.DONE) {
            var data = JSON.parse(Http.responseText)
            var location = data['location']
            map.setView([location['long'], location['lat']], 15);

            // get real estate trends
            var trend = data['real_estate']

            // set the dataview
            real_estate_trend.set(trend)

        }
    }
}

// const real_estate_trend = new carto.dataview.>?!?!>!

// Add a dataview to the client
client.addDataview(real_estate_trend)
 .then(() => {
   console.log('Dataview added');
 })
 .catch(cartoError => {
   console.error(cartoError.message);
 });


real_estate_trend.on('dataChanged', data => {
  refreshRealEstateTrendWidget(data.result);
});

function refreshRealEstateTrendWidget(real_estate_trend) {
  const widgetDom = document.querySelector('#real_estate_trends');
  const averagePopulationDom = widgetDom.querySelector('.js-price-trend');
  averagePopulationDom.innerText = Math.round(real_estate_trend);
}
