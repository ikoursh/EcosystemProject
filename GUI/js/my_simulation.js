const require = parent.require;
const Store = require('electron-store');
const store = new Store();
const {
  shell
} = require('electron') // deconstructing assignment

const grid = document.getElementById('grid');
let sims = store.get("sims", []);

const width = 230;
const min_margin = 40;
const height = 340;

let firstGridUpdate = require('electron').remote.getGlobal('vars').firstGridUpdate;
let pbs = [];
let sims_steps = [];
const initial_pb_time = 4;
const update_pb_time = 0.2;


const fps = 60;
const pbg_dt = 1 / fps;


function updateGrid() {
  pbs = [];
  sims_steps = [];
  let columns = Math.floor(grid.clientWidth / (width + min_margin));
  columns += columns == 0 ? 1 : 0;
  let rows = Math.ceil(sims.length / columns);

  let cwidth = grid.clientWidth / columns;
  let margin = (cwidth - width);

  grid.style.padding = "50px " + 2 * margin + "px";
  grid.innerHTML = "";
  grid.style.gridTemplateColumns = (width + "px ").repeat(columns);
  grid.style.gridTemplateRows = (height + "px ").repeat(rows);

  grid.style.rowGap = "50px";
  grid.style.columnGap = Math.floor(margin) + "px";


  for (var i = 0; i < sims.length; i++) {
    try {
      let state = sims[i].state;
      let sim = document.createElement("DIV");
      sim.className = "sim_entity";

      let startData = sims[i].startData;

      let run = document.createElement("H3");
      run.innerHTML = "Run " + (i + 1);
      sim.appendChild(run);


      //progress bar
      // <div class="pb">
      //   <h3 class = "perc_txt">100%</h3>
      //   <svg class="svg" width="200" height="200" viewPort="0 0 100 100" version="1.1" xmlns="http://www.w3.org/2000/svg">
      //     <circle class="bg" r="75" cx="100" cy="100" fill="transparent"></circle>
      //     <!-- stroke-dasharray="565.48" -->
      //     <circle class="bar" r="75" cx="100" cy="100" fill="transparent" ></circle>
      //     </svg>
      // </div>



      let pb = document.createElement("DIV");
      pb.className = "pb";

      let pt = document.createElement("H2");
      pt.className = "perc_txt";
      pb.append(pt);

      let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.className = "svg";
      svg.setAttribute("viewPort", "0 0 100 100");
      svg.setAttribute("width", "200");
      svg.setAttribute("height", "200");
      svg.setAttribute("version", "1.1");
      svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");

      bg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      bg.setAttribute("class", "bg");
      bg.setAttribute("r", "75");
      bg.setAttribute("cx", "100");
      bg.setAttribute("cy", "100");
      bg.setAttribute("fill", "transparent");
      svg.append(bg);

      bar = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      bar.setAttribute("class", "bar");
      bar.setAttribute("r", "75");
      bar.setAttribute("cx", "100");
      bar.setAttribute("cy", "100");
      bar.setAttribute("fill", "transparent");
      bar.setAttribute("stroke-dasharray", c(bar));
      svg.append(bar);

      pb.append(svg);

      wrapper = document.createElement("DIV");
      wrapper.style.textAlign = "center";
      wrapper.append(pb);
      sim.append(wrapper);
      pbs.push(pb);

      let progress = document.createElement("div");

      sim.appendChild(progress);

      let div = document.createElement("div");
      div.className = "info";

      let steps = document.createElement("P");
      steps.innerHTML = `Steps: ${state.steps}/${startData.steps}`;
      div.appendChild(steps);
      sims_steps.push(steps);

      let platform = document.createElement("P");
      platform.innerHTML = "Platform: " + startData.platform;
      div.appendChild(platform);

      let version = document.createElement("P");
      version.innerHTML = "Version: " + startData.version;
      div.appendChild(version);

      sim.appendChild(div);

      grid.appendChild(sim);

      let sim_actual = sims[i];
      sim.onclick = function() {
        console.log(sim_actual);
        shell.openPath(sim_actual.path);
      };
    } catch (e) {
      console.log(`Error showing sim ${i} log: ${e}`);
    }
  }
  updateData(true);

  firstGridUpdate = false;
  require('electron').remote.getGlobal('vars').firstGridUpdate = false;
}

let gradualUpdateInProgress = 0;

function updateData(force) {
  if (gradualUpdateInProgress !== 0 && !force) {
    return;
  }
  sims = store.get("sims", []);
  for (var i = 0; i < pbs.length; i++) {
    try {
      let pb = pbs[i];
      let sim = sims[i];
      let state = sim.state;
      let startData = sim.startData;
      // console.log("Start Data ",startData.steps, state.steps);
      let p = Math.round((state.steps / startData.steps) * 100);
      if (firstGridUpdate) {
        updatePb(pb, 0);
        updatePbGradual(pb, p, firstGridUpdate ? initial_pb_time : update_pb_time);
      } else {
        // console.log(`update data helper is transitioning pbar ${i} from ${strokeDashoffsetToPercent(getChildByClass(pb, "bar"))} to ${p}`);
        sims_steps[i].innerHTML = `Steps: ${state.steps}/${startData.steps}`;
        updatePb(pb, p);
      }
    } catch (e) {
      // console.log(e);
    }

  }

}
window.setInterval(updateData, 1000);
updateGrid();
window.addEventListener("resize", updateGrid);


function updatePbGradual(pb, val, time) {
  gradualUpdateInProgress++;
  let repetitions = time * fps;
  let delay = pbg_dt;
  let bar_actual = getChildByClass(pb, "bar");
  let startValue = strokeDashoffsetToPercent(bar_actual);
  //(0 ; startValue) (time*fps ; val)

  let m = (startValue - val) / (-time * fps);

  var i = 0;
  var intervalID = window.setInterval(() => {
    updatePb(pb, m * i);

    if (++i === repetitions) {
      window.clearInterval(intervalID);
      gradualUpdateInProgress--;
    }
  }, delay);
}

function c(b) {
  return Math.PI * (b.getAttribute('r') * 2);
}

function percentToStrokeDashoffset(p, bar_actual) {
  return c(bar_actual) * ((100 - p) / 100);
}

function strokeDashoffsetToPercent(bar_actual) {
  var r = bar_actual.getAttribute('r');
  var c = Math.PI * (r * 2);
  return 100 - ((100 * bar_actual.getAttribute("stroke-dashoffset")) / c);
}


function getChildByClass(parrent, className) {
  let children = parrent.getElementsByTagName("*");
  for (var i = 0; i < children.length; i++) {
    if (children[i].getAttribute("class") === className) {
      return children[i];
    }
  }
}

function updatePb(pb, val) {
  if (val < 0) {
    val = 0;
  }
  if (val > 100) {
    val = 100;
  }

  //find & update text and pb_actual:

  getChildByClass(pb, "perc_txt").innerHTML = Math.round(val) + "%";
  let pb_actual = getChildByClass(pb, "bar");
  pb_actual.setAttribute("stroke-dashoffset", percentToStrokeDashoffset(val, pb_actual));

}
