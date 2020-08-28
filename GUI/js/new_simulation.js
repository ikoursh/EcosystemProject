const require = parent.require;
const Store = require('electron-store');
const store = new Store();

const electron = require('electron');
const ipcRenderer = electron.ipcRenderer;

const registerSim = (sim) => {
  ipcRenderer.send('registerSim', {
    payload: sim
  });
};

const command = document.getElementById('command');
const runtime = document.getElementById('runtime');
const population = document.getElementById('population');
const dp = document.getElementById('datapoints');
const steps = document.getElementById('steps');
const excel = document.getElementById('excel');
const spss = document.getElementById('spss');
const plt = document.getElementById('plt');
const dp_v = document.getElementById('datapoints_value');

function int(n) {
  return Number(n.replace(/\D/g, ''));
}

function getSteps() {
  return int(steps.value);
}

function getPopulation() {
  return int(population.value);
}


let add_commas = [steps, population];

for (var i = 0; i < add_commas.length; i++) {
  add_commas[i].addEventListener("keyup", function() {
    let v = int(this.value);
    let tr = Number(v).toLocaleString();
    this.value = tr === "0" ? "" : tr;

    if (dp.value>v){
      dp.value = Math.floor(v/100)*100;
      dp_v.value = dp.value;
      update_command();
    }
  });
}


let update_steps = function() {
  dp.max = int(steps.value);
}
steps.addEventListener("keyup", update_steps);
dp.addEventListener("input", function() {
  if (int(this.value) > 1048576) {
    excel.disabled = true;
    excel.checked = false;
  } else {
    excel.disabled = false;
  }
})


function update_range() {
  dp_v.value = dp.value;
  update_command();
}

function update_value() {
  dp.value = dp_v.value;
  update_command();
}


function update_command() {
  let commands = "python auto.py --gui -s " + getSteps() + " -dp " + dp.value + " -p " + getPopulation();
  if (!excel.checked) {
    commands += " --no-excel "
  }

  if (!plt.checked) {
    commands += " --no-plt "
  }

  if (spss.checked) {
    commands += " --spss "
  }
  if (spell()) {
    commands = "spell run -f --pip-req requirements.txt \"" + commands.replace("python", "python3") + "\""
  } else {
    commands = "pip install -r requirements.txt && " + commands
  }
  command.innerHTML = commands;
}

function spell() {
  return runtime.options[runtime.selectedIndex].value === "spell";
}

function getCommand() {
  return command.innerText;
}


let sims = store.get("sims", []);

function new_simulation() {
  registerSim(new Sim(getCommand(), getRunId(), {
    steps: getSteps(),
    platform: spell() ? "spell" : "local",
    version: "0.1", //TODO: get verssion from package.json
    data_points: dp.value,
    steps: getSteps(),
  }));

  console.log("Sending sim off to worker");

}

function getRunId() {
  let runId = store.get("run_id", 0) + 1;
  store.set("run_id", runId);
  console.log(runId);
  return runId;
}


class Sim {
  constructor(command, runID, startData) {
    this.command = command;
    this.runID = runID;
    this.data = [];
    this.startData = startData;
  }

}

update_steps();
update_command();
