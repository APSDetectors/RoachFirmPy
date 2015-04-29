
# PlanAhead Launch Script for Pre-Synthesis Floorplanning, created by Project Navigator

create_project -name mkidadc -dir "/home/oxygen26/TMADDEN/xilinxProjects/mkidadc/planAhead_run_2" -part xc6vsx475tff1759-1
set_param project.pinAheadLayout yes
set srcset [get_property srcset [current_run -impl]]
set_property target_constrs_file "adc_mkid_4x_interface.ucf" [current_fileset -constrset]
set hdlfile [add_files [list {adc_mkid_4x_interface.v}]]
set_property file_type Verilog $hdlfile
set_property library work $hdlfile
set_property top adc_mkid_4x_interface $srcset
add_files [list {adc_mkid_4x_interface.ucf}] -fileset [get_property constrset [current_run]]
open_rtl_design -part xc6vsx475tff1759-1
