# Inverter RTL-to-GDSII Flow using OpenLane and SkyWater 130nm PDK


<p align="center">
  <img src="yosys-reports/inverter_rtl.png" alt="Yosys RTL Diagram" width="600"/><br/>
  <em>Figure 1: RTL schematic generated from Yosys (inverter)</em>
</p>

<p align="center">
  <img src="kalyout_floorplan_inverter.png" alt="Floorplan Layout" width="600"/><br/>
  <em>Figure 2: Floorplan of inverter after OpenLane flow</em>
</p>

<p align="center">
  <img src="kalyout_placement_inverter.png" alt="Placement Layout" width="400"/>
  <img src="kalyout_routing_inverter.png" alt="Routing Layout" width="400"/><br/>
  <em>Figure 3: Placement (left) and Routing (right) stages of physical design</em>
</p>

<p align="center">
  <img src="kalyout_signoff_inverter_z.png" alt="Signoff Zoomed View" width="400"/>
  <img src="kalyout_signoff_inverter.png" alt="Final Signoff Layout" width="400"/><br/>
  <em>Figure 4: Final signoff view of inverter layout (zoomed detail on left)</em>
</p>

This repository demonstrates the complete ASIC design flow for a simple **inverter** — from **RTL (Verilog)** to **GDSII** — using the **OpenLane** toolchain and the **SkyWater 130nm PDK (sky130)**.

The flow covers:

* RTL simulation and verification
* Logic synthesis with Yosys
* Floorplanning, placement, CTS, and routing with OpenLane/OpenROAD
* Sign-off checks (DRC/LVS) using Magic/KLayout
* Waveform analysis with GTKWave

---

## Repository Structure

```bash
jagadeesh97@LAPTOP-BJUEJNDK:~/OpenLane/designs/inverter$ tree -L 3
.
├── config.json
├── config.tcl
├── kalyout_floorplan_inverter.png
├── kalyout_placement_inverter.png
├── kalyout_routing_inverter.png
├── kalyout_signoff_inverter.png
├── kalyout_signoff_inverter_z.png
├── runs
│   └── myrun
│       ├── OPENLANE_COMMIT
│       ├── PDK_SOURCES
│       ├── cmds.log
│       ├── config.tcl
│       ├── logs
│       ├── openlane.log
│       ├── reports
│       ├── results
│       ├── runtime.yaml
│       ├── tmp
│       └── warnings.log
├── sim
│   ├── inverter_sim
│   └── inverter_tb.v
├── src
│   └── inverter.v
├── synth.ys
└── yosys-reports
    ├── inverter_flat_netlist.dot
    ├── inverter_flat_netlist.png
    ├── inverter_hierarchy.dot
    ├── inverter_hierarchy.png
    ├── inverter_mapped.json
    ├── inverter_mapped.v
    ├── inverter_rtl.dot
    ├── inverter_rtl.png
    ├── inverter_synth.blif
    ├── inverter_synth.edf
    ├── inverter_synth.json
    ├── inverter_synth.v
    ├── inverter_synth_clean.json
    ├── inverter_synth_clean.v
    └── module_inverter.dot

9 directories, 33 files
```

---

## 1. RTL Simulation

RTL functionality is validated before synthesis.

Compile and simulate:

```bash
iverilog -o sim/inverter_sim sim/inverter_tb.v src/inverter.v
vvp sim/inverter_sim
```

Output from testbench:

```
Time    in      out
0       0       1
10000   1       0
20000   0       1
30000   1       0
Testbench finished
```

View waveform:

```bash
gtkwave sim/inverter.vcd
```

---

## 2. Logic Synthesis (Yosys)

Run Yosys with the provided script:

```bash
yosys synth.ys
```

### synth.ys

<details>
<summary>Click to expand</summary>

```tcl
# ===============================
# Yosys Synthesis Script - Inverter
# ===============================

# Create report directory
# mkdir -p yosys-reports

# 1. Read Design
read_verilog src/*.v
hierarchy -check
synth -top inverter

# 2. Optimization and Checks
proc; opt; fsm; opt; memory; opt
check > yosys-reports/inverter_check.txt
stat > yosys-reports/inverter_stat.txt

# 3. Save Netlists
write_verilog yosys-reports/inverter_synth.v
write_json yosys-reports/inverter_synth.json
write_edif yosys-reports/inverter_synth.edf
write_blif yosys-reports/inverter_synth.blif
write_verilog yosys-reports/inverter_synth_clean.v
write_json yosys-reports/inverter_synth_clean.json

# 4. RTL Diagram
show -format dot -prefix yosys-reports/inverter_rtl

# 5. Hierarchy Diagram
hierarchy -top inverter
show -format dot -prefix yosys-reports/inverter_hierarchy

# 6. Flat Netlist
flatten
show -format dot -prefix yosys-reports/inverter_flat_netlist

# 7. Technology Mapping
techmap; opt
stat -tech xilinx > yosys-reports/inverter_techmap_stat.txt
write_verilog yosys-reports/inverter_mapped.v
write_json yosys-reports/inverter_mapped.json

# 8. Module Graph
show -format dot -prefix yosys-reports/module_inverter

# 9. Rough Timing Analysis (using Sky130 Liberty)
abc -liberty /usr/share/yosys/techlibs/sky130_fd_sc_hd/sky130_fd_sc_hd__tt_025C_1v80.lib
stat > yosys-reports/inverter_abc_stat.txt

# Done
echo "All Yosys reports saved in yosys-reports/"
```

</details>

This generates netlists, reports, and `.dot` diagrams which can be converted into `.png` using Graphviz.

---

## 3. Physical Design with OpenLane

Initialize:

```bash
./flow.tcl -design inverter -init_design_config -add_to_designs
```

Run:

```bash
./flow.tcl -design inverter -tag myrun -overwrite
```

### config.tcl

<details>
<summary>Click to expand</summary>

```tcl
# Design setup
set ::env(DESIGN_NAME) "inverter"
set ::env(VERILOG_FILES) "$::env(DESIGN_DIR)/src/inverter.v"

# Clock settings (required for STA, even for combinational logic)
set ::env(CLOCK_PORT) "clk"
set ::env(CLOCK_PERIOD) 10.0

# Floorplan sizing
set ::env(FP_SIZING) "absolute"
set ::env(DIE_AREA) "0 0 200 200"

# Power distribution network
set ::env(FP_PDN_CORE_RING) 0
set ::env(FP_PDN_AUTO_ADJUST) 1
```

</details>

Results (logs, reports, GDS) are stored in `runs/myrun/`.

---

## 4. Layout and Signoff

View final GDS:

```bash
klayout runs/myrun/results/final/gds/inverter.gds
```

Check DRC and LVS with Magic and Netgen.

Representative layout images are included:

* Floorplan: `kalyout_floorplan_inverter.png`
* Placement: `kalyout_placement_inverter.png`
* Routing: `kalyout_routing_inverter.png`
* Final signoff: `kalyout_signoff_inverter.png`

---

## 5. Tools Used

* SkyWater 130nm PDK (sky130)
* OpenLane (flow orchestration)
* Yosys (synthesis)
* OpenROAD (PnR)
* Magic / KLayout (layout, DRC)
* Netgen (LVS)
* Icarus Verilog / GTKWave (simulation)

---

## Usage Notes

* `PDK_ROOT` must point to the SkyWater PDK installation.
* `OPENLANE_ROOT` must be set before invoking OpenLane.
* Use Dockerized OpenLane for consistency.
* Convert `.dot` files from Yosys to `.png` with Graphviz.

---

## Final Output

* RTL simulation results (`sim/`)
* Gate-level netlists and diagrams (`yosys-reports/`)
* Physical design results, reports, and GDSII (`runs/myrun/`)
* Verified inverter layout snapshots
