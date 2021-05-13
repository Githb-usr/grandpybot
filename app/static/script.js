const API_URL = "http://127.0.0.1:5000";
const WIKI_URL = "https://fr.wikipedia.org/wiki";
const MAP_URL = "https://geocode.search.hereapi.com/v1/geocode";
const CHAT_AREA = document.getElementById('chat-area');

// Retrieval of the question asked + display of the answer (via AJAX)
let form = document.querySelector("#user-question-form");
form.addEventListener("submit", function (event) {
  event.preventDefault();

  // We send the content of the form to the server
  let question = document.getElementById('user-question').value;
  const questionUrl = `${API_URL}/question?q=${question}`;
  fetch(questionUrl)
  .then(function(response) { 
    if(response.ok) {
      response.json()
      .then(function(data) {
        // We get the data generated by the Python code
        const wikiData = data.wiki
        const mapApiKey = data.apiKey
        let wikiUrl = `${WIKI_URL}/${wikiData["wiki_title"]}`;
        let wikiLink = document.createElement('a');
        wikiLink.textContent = "[Cliquez ici pour en savoir plus]";
        wikiLink.href = wikiUrl;
        let messages = [question, wikiData["wiki_extract"]];

        // We fill the chat window with questions and answers
        let nodes = messages.map(message => {
          let p = document.createElement('p');
          p.textContent = message;
          if (message == wikiData["wiki_extract"]) {
            p.className = "chat-response";
            p.appendChild(wikiLink);
          } else {
            p.className = "chat-question";
          }

          return p;
          });

          CHAT_AREA.append(...nodes);
          scrollToBottom();

        // We change the title of the map and display the map
        const mapTitle = document.getElementById('map-title');
        mapTitle.innerText = 'Situez "' + wikiData["wiki_title"] + '" sur la carte'

        displayMap(mapApiKey, wikiData["wiki_coord"])
      })

    } else {
      console.log('ça marche pas')
    }
  })
  .catch(error => console.log(error))
})

// We scroll automatically at the bottom of the chat
function scrollToBottom() {
  CHAT_AREA.scrollTop = (CHAT_AREA.scrollHeight + 20);
}

/*
 DISPLAY AN INTERACTIVE MAP
 **************************
*/
// console.log("HEEEEEEEEEEEEE", coordinates)

function initializeMap(apiKey) {
  //Step 1: initialize communication with the platform
  const platform = new H.service.Platform({
    apikey: apiKey
  });

  const defaultLayers = platform.createDefaultLayers();
  let defaultCoordinates = {
    lat: 54.525961,
    lng: 15.255119
  }

  //Step 2: initialize a map - this map is centered over Paris
  const map = new H.Map(document.getElementById('map-area'),
    defaultLayers.raster.normal.map,{
    center: defaultCoordinates,
    zoom: 13,
    pixelRatio: window.devicePixelRatio || 1
  });

  // add a resize listener to make sure that the map occupies the whole container
  window.addEventListener('resize', () => map.getViewPort().resize());

  //Step 3: make the map interactive
  const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
    // Create the default UI components
  const ui = H.ui.UI.createDefault(map, defaultLayers);

  return map;
}

function displayMap(mapApiKey, mapData) {
  let coordinates = {
    lat: mapData[0],
    lng: mapData[1]
   }
  
  const mapContainer = document.getElementById('map-area');
  mapContainer.innerText = ''

  map = initializeMap(mapApiKey)
  // Create a marker icon from an image URL:
  const icon = new H.map.Icon('./static/img/map-marker.png');
  // Create a marker using the previously instantiated icon:
  let marker = new H.map.Marker(coordinates, { icon: icon });
  
  map.clearContent()
  map.setCenter(coordinates);
  map.setZoom(13);
  // Add the marker to the map:
  map.addObject(marker);
 }

// Loading spinner
