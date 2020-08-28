const require = parent.require;
const Chart = require("chart.js");
const Store = require("electron-store");
const store = new Store();

let sims = store.get("sims", []);
if (sims.length === 0) {
  document.getElementById('latest_sim').style.display = "none";
  document.getElementById("title").innerText = "No simulation to display";
}


const max_s = 1;
const colors = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"];

const max_x = 10000;

let l_actual = Math.min(max_s, sims.length);
let datasets = [];

for (let i = 0; i < l_actual; i++) {
  let sim = sims[sims.length - i - 1];
  let data = []
  for (let j = 0; j < Math.min(max_x/sim.startData.data_points, sim.state_OT.length); j++) {
    data.push({
      x: sim.state_OT[j].steps,
      y: sim.state_OT[j].agents
    });
  }

  console.log(data);

  datasets.push({
    data: data,
    label: sim.runID
  });
}


console.log(datasets);
new Chart(document.getElementById("latest_sim").getContext('2d'), {
  type: 'line',
  data: {
    datasets: datasets
  },
  options: {
    title: {
      display: true,
      text: 'World population per region (in millions)'
    }
  }
});
