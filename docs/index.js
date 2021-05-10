// const urlRoot = "http://localhost:8000/";
const urlRoot = "https://lts-fastapi-c8pjh.ondigitalocean.app/";

const colors = {
  blue: "0, 128, 255",
  red: "175, 9, 159",
  black: "0, 0, 0",
};

const chart_ctx = document.getElementById("myChart");
const data = {
  labels: [],
  datasets: [
    {
      label: "Inbound Trips",
      backgroundColor: "rgba(" + colors.blue + ", 0.5)",
      borderColor: "rgb(" + colors.blue + ")",
      data: [],
    },
    {
      label: "Outbound Trips",
      backgroundColor: "rgba(" + colors.red + ", 0.5)",
      borderColor: "rgb(" + colors.red + ")",
      data: [],
    },
  ],
};
const config = {
  type: "bar",
  data,
  options: {
    indexAxis: "y",
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Custom Chart Title",
      },
    },
  },
};
var myChart = new Chart(chart_ctx, config);

function update_graph_with_api_data(url) {
  fetch(url).then(function (response) {
    response.text().then(function (text) {
      let timeSeriesData = JSON.parse(text);

      myChart.data.labels = [];
      myChart.data.datasets[0].data = [];
      myChart.data.datasets[1].data = [];

      timeSeriesData.Inbound.labels.forEach((label) => {
        myChart.data.labels.push(label);
      });

      console.log(myChart.data.labels);

      timeSeriesData.Inbound.data_values.forEach((val) => {
        myChart.data.datasets[0].data.push(val);
      });
      timeSeriesData.Outbound.data_values.forEach((val) => {
        myChart.data.datasets[1].data.push(val);
      });

      myChart.update();
    });
  });
}

// function get_data_from_api(url) {
//   fetch(url)
//     .then((response) => response.text())
//     .then((text) => JSON.parse(text))
//     .then((j) => {
//       return j;
//     });
// }

let time_url = urlRoot + "indego/timeseries/?q=3004";

// const data = {
//   labels: timeSeriesData.Inbound.labels,
//   datasets: [
//     {
//       label: "Inbound Trips",
//       backgroundColor: "rgb(255, 99, 132)",
//       borderColor: "rgb(255, 99, 132)",
//       data: timeSeriesData.Inbound.data_values,
//     },
//     {
//       label: "Outbound Trips",
//       backgroundColor: "rgb(255, 255, 20)",
//       borderColor: "rgb(255, 99, 132)",
//       data: timeSeriesData.Outbound.data_values,
//     },
//   ],
// };
// const config = {
//   type: "bar",
//   data,
//   options: {},
// };
// var myChart = new Chart(chart_ctx, config);

// function update_graph(url) {
//   fetch(url).then(function (response) {
//     response.text().then(function (text) {
//       let response_data = JSON.parse(text);

//       chart_ctx.destroy();

//       const data = {
//         labels: response_data.Inbound.labels,
//         datasets: [
//           {
//             label: "Inbound Trips",
//             backgroundColor: "rgb(255, 99, 132)",
//             borderColor: "rgb(255, 99, 132)",
//             data: response_data.Inbound.data_values,
//           },
//           {
//             label: "Outbound Trips",
//             backgroundColor: "rgb(255, 255, 20)",
//             borderColor: "rgb(255, 99, 132)",
//             data: response_data.Outbound.data_values,
//           },
//         ],
//       };
//       const config = {
//         type: "bar",
//         data,
//         options: {},
//       };
//       var myChart = new Chart(chart_ctx, config);
//     });
//   });
// }

mapboxgl.accessToken =
  "pk.eyJ1IjoiYWFyb25kdnJwYyIsImEiOiJja2NvN2s5dnAwaWR2MnptbzFwYmd2czVvIn0.Fcc34gzGME_zHR5q4RnSOg";
var map = new mapboxgl.Map({
  container: "map", // container ID
  style: "mapbox://styles/mapbox/streets-v10", // style URL
  center: [-75.16362, 39.95238],
  zoom: 12, // starting zoom
});

map.on("load", function () {
  // Add a data source containing GeoJSON data.

  update_graph_with_api_data(urlRoot + "indego/timeseries/?q=3004");

  // TODO: show bike lanes with vector source
  map.addSource("LTS", {
    type: "vector",
    data: " https://www.tiles.dvrpc.org/data/lts.json",
  });

  map.addSource("indego", {
    type: "geojson",
    data: urlRoot + "indego/all",
  });
  map.addSource("indego-query", {
    type: "geojson",
    data: urlRoot + "indego/trip-points/?q=3004",
  });
  map.addSource("indego-query-spider", {
    type: "geojson",
    data: urlRoot + "indego/trip-spider/?q=3004",
  });

  // This layers shows the spider lines based upon the API output for a selected station
  map.addLayer({
    id: "spider",
    type: "line",
    source: "indego-query-spider", // reference the data source
    layout: {},
    paint: {
      "line-width": ["get", "destinations"],
      "line-opacity": 0.3,
      "line-color": "rgb(" + colors.blue + ")",
    },
  });
  // This layer has every station point and text attribute data
  map.addLayer({
    id: "indego-all",
    type: "circle",
    source: "indego", // reference the data source
    layout: {},
    paint: {
      "circle-opacity": 0.2,
      "circle-stroke-width": 1,
      "circle-stroke-color": "#000000",
      "circle-stroke-opacity": 0.5,
      "circle-radius": 2,
    },
  });

  // This layers shows the scaled dots based upon the API output for a selected station
  map.addLayer({
    id: "indego-query",
    type: "circle",
    source: "indego-query", // reference the data source
    paint: {
      "circle-color": "rgb(" + colors.blue + ")", // blue color fill
      "circle-opacity": 0.3,
      "circle-stroke-width": 2,
      "circle-stroke-color": "rgb(" + colors.blue + ")",
      "circle-radius": ["get", "destinations"],
    },
  });
  // map.addLayer({
  //     'id': 'indego-query-labels',
  //     'type': 'symbol',
  //     'source': 'indego-query', // reference the data source
  //     'layout': {
  //         'text-field': ["format", ['get', 'origins'], { 'round': 0 }],
  //         'text-variable-anchor': ['top'],
  //         'text-radial-offset': 0,
  //         'text-justify': 'auto',
  //     },
  //     'filter': [">", "origins", 5]
  // });

  // This layer exists to show the station that the user clicked on in YELLOW
  map.addLayer({
    id: "indego-selected",
    type: "circle",
    source: "indego-query", // reference the data source
    paint: {
      "circle-opacity": 0.5,
      "circle-color": "#fff123",
      "circle-stroke-width": 5,
      "circle-stroke-color": "#fff123",
      "circle-radius": ["get", "destinations"],
    },
    filter: ["in", "station_id", 3004],
  });

  // hovering over the "all" layer makes the dots grow and show that they're clickable
  map.on("mouseenter", "indego-all", () => {
    map.getCanvas().style.cursor = "pointer";
    map.setPaintProperty("indego-all", "circle-radius", 15);
  });

  // moving mouse away from "all" layer makes them small again
  map.on("mouseleave", "indego-all", () => {
    map.getCanvas().style.cursor = "";
    map.setPaintProperty("indego-all", "circle-radius", 2);
  });

  map.on("click", "indego-all", function (e) {
    var props = e.features[0].properties;

    // Update the title in the header block and address
    const stationTextDiv = document.querySelector("#station-name");
    const stationAddressTextDiv = document.querySelector("#station-address");

    stationTextDiv.innerHTML = props.name;
    stationAddressTextDiv.innerHTML = props.addressstreet;

    // filter selected layer to this id
    var id_filter = ["in", "station_id", props.station_id];
    map.setFilter("indego-selected", id_filter);

    // hit the API for station points
    let point_url =
      urlRoot + "indego/trip-points/?q=" + props.station_id.toString();
    fetch(point_url).then(function (response) {
      response.text().then(function (text) {
        let data = JSON.parse(text);

        // update mapbox layer data with API result
        map.getSource("indego-query").setData(data);

        // Get a bounding box of high-volume stations
        var bounds = new mapboxgl.LngLatBounds();

        data.features.forEach(function (feature) {
          // TODO: tie this to the selected direction instead of origins
          if (feature.properties.origins >= 2) {
            bounds.extend(feature.geometry.coordinates);
          }
        });

        // zoom map to fit bounding box that was just defined
        map.fitBounds(bounds);

        // force the full station layer back to small dots (user may not have mouseexited yet)
        map.setPaintProperty("indego-all", "circle-radius", 2);
      });
    });

    // hit the API for spider lines and update mapbox data source afterwards
    let spider_url =
      urlRoot + "indego/trip-spider/?q=" + props.station_id.toString();
    fetch(spider_url).then(function (response) {
      response.text().then(function (text) {
        let data = JSON.parse(text);

        map.getSource("indego-query-spider").setData(data);
      });
    });

    let time_url =
      urlRoot + "indego/timeseries/?q=" + props.station_id.toString();
    update_graph_with_api_data(time_url);
  });
});

const selectElement = document.querySelector("#directionality");

selectElement.addEventListener("change", (event) => {
  var v = event.target.value;
  if (v == "origins") {
    var color = "rgb(" + colors.red + ")";
  }
  if (v == "destinations") {
    var color = "rgb(" + colors.blue + ")";
  }
  if (v == "totalTrips") {
    var color = "rgb(" + colors.black + ")";
  }

  map.setPaintProperty("spider", "line-color", color);
  map.setPaintProperty("indego-query", "circle-color", color);
  map.setPaintProperty("indego-query", "circle-stroke-color", color);

  map.setPaintProperty("indego-selected", "circle-radius", [
    "get",
    event.target.value,
  ]);
  map.setPaintProperty("indego-query", "circle-radius", [
    "get",
    event.target.value,
  ]);
  map.setPaintProperty("spider", "line-width", ["get", event.target.value]);
});

// let time_url = urlRoot + "indego/timeseries/?q=3004";
// make_initial_graph(time_url);
