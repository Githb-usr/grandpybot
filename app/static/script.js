// Récupération de la question posée + affichage de la réponse (via AJAX)
  let form = document.querySelector("#user-question-form")
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    // Envoyer le contenu du formulaire au serveur
    let question = document.getElementById('userQuestion').value;
    let url = `http://127.0.0.1:5000/question?q=${question}`
    fetch(url)
    .then(function(response) { 
      if(response.ok) {
        response.json()
        .then(function(data) {
          const chat = document.getElementById('chat');
          chat.innerHTML = data[1]
        })

      } else {
        console.log('ça marche pas')
      }
    })
    .catch(error => console.log(error))
})

/** AFFICHAGE D'UNE CARTE INTERACTIVE 
*   *********************************
*/

// /**
//  * @param  {H.Map} map      A HERE Map instance within the application
//  */
 function showMap(map){
    map.setCenter({lat:appConfig.lat, lng:appConfig.lon});
    map.setZoom(12);
  }
  
  /**
   * Boilerplate map initialization code starts below:
   */
  
  //Step 1: initialize communication with the platform
  // In your own code, replace variable window.apikey with your own apikey
  var platform = new H.service.Platform({
    // apikey: appConfig.apikey
    apikey: 'mNn4YZYN9Sh5OpIkdtHyxKprDSSFJjZAe376DxDnUl8'
  });
  var defaultLayers = platform.createDefaultLayers();

  //Step 2: initialize a map - this map is centered over Europe
  var map = new H.Map(document.getElementById('mapContainer'),
    defaultLayers.raster.normal.map,{
    center: {lat:50, lng:5},
    zoom: 15,
    pixelRatio: window.devicePixelRatio || 1
  });

  // Create a marker icon from an image URL:
  var icon = new H.map.Icon('./static/map-marker.png');

  // Create a marker using the previously instantiated icon:
  // var marker = new H.map.Marker({ lat: appConfig.lat, lng: appConfig.lon }, { icon: icon });

  // Add the marker to the map:
  // map.addObject(marker);

  // add a resize listener to make sure that the map occupies the whole container
  window.addEventListener('resize', () => map.getViewPort().resize());
  
  //Step 3: make the map interactive
  // MapEvents enables the event system
  // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
  var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
  
  // Create the default UI components
  var ui = H.ui.UI.createDefault(map, defaultLayers);
  
  // Now use the map as required...
  // window.onload = function () {
  //   showMap(map);
  //   map.addObject(marker);
  // }

/** RECHERCHE PAR ADRESSE 
*   *********************
*/

// Instantiate a map and platform object:
// var platform = new H.service.Platform({
//   'apikey': appConfig.apikey
// });

// Get an instance of the geocoding service:
// var service = platform.getSearchService();

// Call the geocode method with the geocoding parameters,
// the callback and an error callback function (called if a
// communication error occurs):
// service.geocode({
//   q: '200 S Mathilda Ave, Sunnyvale, CA'
// }, (result) => {
  // Add a marker for each location found
//   result.items.forEach((item) => {
//     map.addObject(new H.map.Marker(item.position));
//   });
// }, alert);
