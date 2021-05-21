const API_URL = "http://127.0.0.1:33507";
const WIKI_URL = "https://fr.wikipedia.org/wiki";
const MAP_URL = "https://geocode.search.hereapi.com/v1/geocode";
const CHAT_AREA = document.getElementById('chat-area');

// Retrieval of the question asked + display of the answer (via AJAX)
let form = document.querySelector("#user-question-form");
form.addEventListener("submit", function (event) {
  event.preventDefault();

  // We send the content of the form to the server
  let question = document.getElementById('user-question').value;
  if(question.length > 0) {
    const questionUrl = new URL(`${API_URL}/question`)
    questionUrl.searchParams.append('q', question)

    fetch(questionUrl)
    .then(function(response) {
      if(response.ok) {
        response.json()
        .then(function(data) {
          // We get the data generated by the Python code
          const wikiData = data.wiki;
          const mapApiKey = data.apiKey;
          const defaultTitle = data.default_title;
          const defaultExtract = data.default_extract;
          const positiveMessages = data.positive_messages;
          const negativeMessages = data.negative_messages;

          // We fill the chat window with questions and answers
          let p1 = displayQuestion(question);
          let p2Negative = selectReplica(negativeMessages);
          let p2Positive = selectReplica(positiveMessages);
          let p3 = displayResponse(wikiData);

          if (wikiData["wiki_extract"] == defaultExtract) {
            let nodes = [createNegativeBloc(p1, p2Negative)]
            CHAT_AREA.append(...nodes);
          } else {
            let nodes = [createPositiveBloc(p1, p2Positive, p3)]
            CHAT_AREA.append(...nodes);
          }

          scrollToBottom();

          // We change the title of the map and display the map
          const mapTitle = document.getElementById('map-title');
          if(wikiData["wiki_page_title"] != defaultTitle) {
            mapTitle.innerText = 'Situez "' + wikiData["wiki_page_title"] + '" sur la carte'
          } else {
            mapTitle.innerText = 'Pas de carte à afficher, désolé...'
          }

          displayMap(mapApiKey, wikiData["wiki_coordinates"])
        })
      } else {
        console.log('ça marche pas')
      }
    })
    .catch(error => console.log('La fonction fetch ne fonctionne pas correctement', error))
  } else {
    let p = document.createElement('p');
    p.className = "empty-form";
    p.textContent = 'Attention : vous devez posez une question avant de cliquer sur "OK"';
    CHAT_AREA.append(p);
  }
})


// We scroll automatically at the bottom of the chat
function scrollToBottom() {
  CHAT_AREA.scrollTop = (CHAT_AREA.scrollHeight + 20);
}

// We select a Grandpy replica at random
function displayQuestion(question) {
  let p = document.createElement('p');
  p.className = "chat-question";
  p.textContent = question;

  return p
}

// We select a Grandpy replica at random
function selectReplica(messagesList) {
  let p = document.createElement('p');
  p.className = "chat-response";
  let randomReplica = messagesList[Math.floor(Math.random() * messagesList.length)];
  p.textContent = randomReplica;

  return p
}

// We select a Grandpy replica at random
function displayResponse(wikiData) {
  let p = document.createElement('p');
  p.className = "chat-response";
  p.style.marginBottom = "25px";
  p.textContent = wikiData["wiki_extract"];
  let wikiUrl = `${WIKI_URL}/${wikiData["wiki_page_title"]}`;
  let wikiLink = document.createElement('a');
  wikiLink.textContent = "[Cliquez ici pour en savoir plus]";
  wikiLink.href = wikiUrl;
  p.appendChild(wikiLink);

  return p
}

// We create a bloc of chat (a question with its positive response)
function createPositiveBloc(p1, p2Positive, p3) {
  let div = document.createElement('div');
  div.className = "positive-bloc";
  div.appendChild(p1);
  div.appendChild(p2Positive);
  div.appendChild(p3);

  return div
}

// We create a bloc of chat (a question with its negative response)
function createNegativeBloc(p1, p2Negative) {
  let div = document.createElement('div');
  div.className = "negative-bloc";
  div.appendChild(p1);
  div.appendChild(p2Negative);

  return div
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

  // Add a resize listener to make sure that the map occupies the whole container
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