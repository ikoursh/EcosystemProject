const {
    ipcRenderer
} = require('electron');
const cmd = require("./cmd.js")
const Store = require('electron-store');
const store = new Store();
const fs = require('fs');

let sims = store.get("sims", []);

const root = require('electron').remote.getGlobal('vars').path;
console.log(root);

if (!fs.existsSync(`${root}/EcoSystemProject(GUI-runs)/`)) {
    fs.mkdirSync(`${root}/EcoSystemProject(GUI-runs)/`)
}

function updateSims() {
    store.set("sims", sims);
}


ipcRenderer.on('registerSim', (event, arg) => {
    let sim = new Sim(arg.payload);
    sim.run();
    sims.push(sim);
    updateSims();
});


class Sim {
    constructor(json) {
        this.command = json.command;
        this.runID = json.runID;
        this.data = json.data;
        this.startData = json.startData;
        this.state_OT = [];
        this.spellID = -1;
        this.path = `${root}\\EcoSystemProject(GUI-runs)\\run_${this.runID}`;
        fs.mkdirSync(this.path);
        this.state = {
            steps: 0,
            food: 0,
            agents: 0
        }

        this.spell = this.startData.platform === "spell";
    }

    run() {
        const dataCallback = (data) => {
            this.data.push(data);
            this.update_statistics();
        };

        let c_a = `cd ${store.get("env_sim_path", "")} && ${this.command}`;
        cmd.run_script(c_a, [], null, dataCallback);
    }

    update_statistics() {
        let d = this.data[this.data.length - 1];
        if (d[1] == -1) {
            return;
        }
        let l = d[0];
        try {
            if (this.spell && this.spellID === -1 && l.includes("Casting spell #")) {
                this.spellID = l.split("#")[1].split(".")[0]; //get the spellRunID
            }

            this.state = JSON.parse(l);
            this.state_OT.push(this.state);

        } catch (e) {
        }

        if (l.startsWith("Simulation complete") && !this.spell) {
            //sim is now complete, move the output files to local storage

            let origin = l.split(": ")[1].trim();
            fs.readdirSync(`${origin}`).forEach((f) => {
                fs.copyFileSync(`${origin}\\${f}`, `${root}\\EcoSystemProject(GUI-runs)\\run_${this.runID}\\${f}`);
            });
        } else if (l.trim() === `Run ${this.spellID} complete`) {
            //sim is complete and spell has finished pushing thee files to the spell file system
            cmd.run_script(`spell cp -f runs/${this.spellID}/proj/graphs-0.3/ ${root}/EcoSystemProject(GUI-runs)/run_${this.runID}`, [], null, (d) => {
            });

        }
        updateSims();

    }
}
