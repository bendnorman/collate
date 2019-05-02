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
  
const plutoOneDataset = new carto.source.Dataset(`
  table_1_pluto
`);
const plutoTwoDataset = new carto.source.Dataset(`
  table_2_pluto
`);
const plutoThreeDataset = new carto.source.Dataset(`
  table_3_pluto
`);
const cleanPlutoDataset = new carto.source.Dataset(`
  cleaned_pluto
`);

const zillowNeighborhoodsStyle = new carto.style.CartoCSS(`
    #layer {
    polygon-fill: #1548fb;
      polygon-opacity: 0.5;
      ::outline {
        line-width: 0.3;
        line-color: #000000;
        line-opacity: 0.5;
      }
    }
  `);
const zillowNeighborhoods = new carto.layer.Layer(zillowNeighborhoodsDataset, zillowNeighborhoodsStyle);
const plutoOne = new carto.layer.Layer(plutoOneDataset, zillowNeighborhoodsStyle);
const plutoTwo = new carto.layer.Layer(plutoTwoDataset, zillowNeighborhoodsStyle);
const plutoThree = new carto.layer.Layer(plutoThreeDataset, zillowNeighborhoodsStyle);

const cleanPluto = new carto.layer.Layer(cleanPlutoDataset, zillowNeighborhoodsStyle);



// client.addLayers([zillowNeighborhoods, plutoOne, plutoTwo, plutoThree]);
// client.addLayers([plutoOne, plutoTwo, plutoThree]);
client.addLayers([cleanPluto])

client.getLeafletLayer().addTo(map);



var img = document.getElementById('trends');
img.style.visibility = 'hidden';

function updateOccupantInput(val) {
    var avgPopulation = parseFloat(document.getElementById('avgPopulation').innerHTML)
    document.getElementById('occupantsVal').innerHTML=val; 
    val = parseFloat(val)
    
    // console.log(val)
    // console.log(avgPopulation)
    var change = Number((((val + avgPopulation) / avgPopulation) * 100 - 100).toFixed(2))
    document.getElementById('populationDiff').innerHTML = change + ' %'
    
    document.getElementById('pop_diff').style.background = rgba(10 + change*20, 203 - change * 20, 0, 0.2);
}

function rgba(r, g, b, a){
  return "rgba("+r+","+g+","+b+","+a+")";
}

function updateIncomeInput(val) {
    var avgIncome = document.getElementById('avgIncome').innerHTML
    document.getElementById('incomeVal').innerHTML=val; 
    var change = Number(((val - avgIncome) / avgIncome * 100).toFixed(2))
    document.getElementById('incomeDiff').innerHTML = change  + ' %';
    document.getElementById('income_diff').style.background = rgba(10 + change*10, 203 - change * 10, 0, 0.2);
}

// function buttonClick() {
//     var address = document.getElementById('address').value
// 
// }

//// Project Profile
function getProjectData() {
    var address = document.getElementById('address').value
    console.log(address)
    const Http = new XMLHttpRequest();
    const url = 'http://3.14.181.240:8080/?address=' + address;
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
            map.setView([location['long'], location['lat']], 17);
            
            console.log(data['census_data'])
            document.getElementById('avgIncome').innerHTML = data['census_data']['income'];
            document.getElementById('avgPopulation').innerHTML = data['census_data']['population'];
            
            var img = document.getElementById('trends');
            img.style.visibility = 'visible';
            
            
            
            // DISPLAYING RED DOT
            const spainCitiesSource = new carto.source.SQL(`
                    SELECT *
                      FROM table_1_pluto
                      WHERE address = \'1 EAST LOOP ROAD\'
                  `);
            // TODO: THIS IS HARDCODED AND ONLY LOOKING AT A THIRD OF PLUTO
            console.log(spainCitiesSource)

            const spainCitiesStyle = new carto.style.CartoCSS(`
                  #layer {
                    marker-width: 20;
                    marker-fill: #EE4D5A;
                    marker-line-color: #FFFFFF;
                  }
                `);
            const spainCitiesLayer = new carto.layer.Layer(spainCitiesSource, spainCitiesStyle);
            client.addLayers([spainCitiesLayer])
            
            // console.log(data['polygon'])
            // 
            // var polygon = L.polygon(data['polygon'], {color: 'red'});
            // polygon.addTo(map)

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
