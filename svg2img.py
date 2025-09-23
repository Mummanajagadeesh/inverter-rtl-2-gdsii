import cairosvg

cairosvg.svg2png(
    url="yosys-reports/inverter_synth.svg",
    write_to="inverter_synth.png",
    background_color="white",
    dpi=300  
)
