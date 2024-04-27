from PyQt5.QtWidgets import QToolButton

from krita import *

qdock = next((w for w in Krita.instance().dockers() if w.objectName() == 'ToolBox'), None)
wobj: QToolButton = qdock.findChild(QToolButton,'KritaShape/KisToolBrush')
print(wobj.shortcut().isEmpty())

for action in Krita.instance().actions():
  if not action.shortcut().isEmpty():
    print(action.objectName(), action.shortcut().toString())


__DATA__

True
save_incremental_version Ctrl+Alt+S
save_incremental_backup F4
tablet_debugger Ctrl+Shift+T
rotate_canvas_right Ctrl+]
rotate_canvas_left Ctrl+[
wrap_around_mode Shift+W
level_of_detail_mode Shift+L
softProof Ctrl+Y
gamutCheck Ctrl+Shift+Y
view_show_canvas_only Tab
zoom_to_100pct Ctrl+0
view_zoom_in Ctrl++
view_zoom_out Ctrl+-
toggle_fg_bg X
reset_fg_bg D
filter_apply_again Ctrl+F
krita_filter_colorbalance Ctrl+B
krita_filter_desaturate Ctrl+Shift+U
krita_filter_hsvadjustment Ctrl+U
krita_filter_invert Ctrl+I
krita_filter_levels Ctrl+L
krita_filter_perchannel Ctrl+M
edit_cut Ctrl+X
edit_copy Ctrl+C
edit_paste Ctrl+V
paste_new Ctrl+Shift+N
paste_at Ctrl+Alt+V
paste_as_reference Ctrl+Shift+R
copy_merged Ctrl+Shift+C
select_all Ctrl+A
deselect Ctrl+Shift+A
clear Del
reselect Ctrl+Shift+D
invert_selection Ctrl+Shift+I
copy_selection_to_new_layer Ctrl+Alt+J
cut_selection_to_new_layer Ctrl+Shift+J
fill_selection_foreground_color Shift+Backspace
fill_selection_background_color Backspace
fill_selection_foreground_color_opacity Ctrl+Shift+Backspace
fill_selection_background_color_opacity Ctrl+Backspace
toggle_display_selection Ctrl+H
show_snap_options_popup Shift+S
flatten_image Ctrl+Shift+E
merge_layer Ctrl+E
activateNextLayer PgUp
activatePreviousLayer PgDown
switchToPreviouslyActiveNode ;
duplicatelayer Ctrl+J
create_quick_group Ctrl+G
create_quick_clipping_group Ctrl+Shift+G
quick_ungroup Ctrl+Alt+G
add_new_paint_layer Ins
add_new_shape_layer Shift+Ins
view_grid Ctrl+Shift+'
view_snap_to_grid Ctrl+Shift+;
make_brush_color_lighter L
make_brush_color_darker K
increase_opacity O
decrease_opacity I
mirror_canvas M
mirror_canvas_around_cursor Alt+M
erase_action E
Next Blending Mode Alt+Shift++
Previous Blending Mode Alt+Shift+-
Select Normal Blending Mode Alt+Shift+N
Select Dissolve Blending Mode Alt+Shift+I
Select Behind Blending Mode Alt+Shift+Q
Select Clear Blending Mode Alt+Shift+R
Select Darken Blending Mode Alt+Shift+K
Select Multiply Blending Mode Alt+Shift+M
Select Color Burn Blending Mode Alt+Shift+B
Select Linear Burn Blending Mode Alt+Shift+A
Select Lighten Blending Mode Alt+Shift+G
Select Screen Blending Mode Alt+Shift+S
Select Color Dodge Blending Mode Alt+Shift+D
Select Linear Dodge Blending Mode Alt+Shift+W
Select Overlay Blending Mode Alt+Shift+O
Select Hard Overlay Blending Mode Alt+Shift+P
Select Soft Light Blending Mode Alt+Shift+F
Select Hard Light Blending Mode Alt+Shift+H
Select Vivid Light Blending Mode Alt+Shift+V
Select Linear Light Blending Mode Alt+Shift+J
Select Pin Light Blending Mode Alt+Shift+Z
Select Hard Mix Blending Mode Alt+Shift+L
Select Difference Blending Mode Alt+Shift+E
Select Exclusion Blending Mode Alt+Shift+X
Select Hue Blending Mode Alt+Shift+U
Select Saturation Blending Mode Alt+Shift+T
Select Color Blending Mode Alt+Shift+C
Select Luminosity Blending Mode Alt+Shift+Y
next_favorite_preset ,
previous_favorite_preset .
previous_preset /
show_brush_presets F6
show_brush_editor F5
imagesize Ctrl+Alt+I
canvassize Ctrl+Alt+C
featherselection Shift+F6
increase_brush_size ]
decrease_brush_size [
undo_polygon_selection Shift+Z
KritaSelected/KisToolColorSampler P
KisToolTransform Ctrl+T
movetool-move-up Up
movetool-move-down Down
movetool-move-left Left
movetool-move-right Right
movetool-move-up-more Shift+Up
movetool-move-down-more Shift+Down
movetool-move-left-more Shift+Left
movetool-move-right-more Shift+Right
KisToolSelectRectangular Ctrl+R
pathsegment-line F
pathsegment-curve Shift+C
pathpoint-insert Ins
pathpoint-remove Backspace
pathpoint-join J
convert-to-path P
KritaShape/KisToolRectangle Shift+R
object_order_front Ctrl+Shift+]
object_order_raise Ctrl+Alt+]
object_order_lower Ctrl+Alt+[
object_order_back Ctrl+Shift+[
KritaFill/KisToolGradient G
KritaShape/KisToolEllipse Shift+J
KritaTransform/KisToolMove T
movetool-show-coordinates Ctrl+Alt+Shift+C
KisToolCrop C
KritaFill/KisToolFill F
KisToolSelectElliptical J
KritaShape/KisToolMultiBrush Q
toggle_assistant Ctrl+Shift+L
KritaShape/KisToolBrush B
RenameCurrentLayer F2
layer_properties F3
remove_layer Shift+Del
move_layer_up Ctrl+PgUp
move_layer_down Ctrl+PgDown
show_wg_color_selector Shift+O
file_new Ctrl+N
file_open Ctrl+O
file_quit Ctrl+Q
fullscreen Ctrl+Shift+F
file_save Ctrl+S
file_save_as Ctrl+Shift+S
edit_undo Ctrl+Z
edit_redo Ctrl+Shift+Z
file_close_all Ctrl+Shift+W
file_close Ctrl+W
command_bar_open Ctrl+Return
pykrita_yuuki_krita_helper_trigger_floating_docker `
activate_preset_1 Ctrl+Alt+1
activate_preset_2 Ctrl+Alt+2
activate_preset_3 Ctrl+Alt+3
activate_preset_4 Ctrl+Alt+4
activate_preset_5 Ctrl+Alt+5
activate_preset_6 Ctrl+Alt+6
activate_preset_7 Ctrl+Alt+7
activate_preset_8 Ctrl+Alt+8
activate_preset_9 Ctrl+Alt+9
activate_preset_0 Ctrl+Alt+0
execute_script_1 Ctrl+Shift+1
execute_script_2 Ctrl+Shift+2
execute_script_3 Ctrl+Shift+3
execute_script_4 Ctrl+Shift+4
execute_script_5 Ctrl+Shift+5
execute_script_6 Ctrl+Shift+6
execute_script_7 Ctrl+Shift+7
execute_script_8 Ctrl+Shift+8
execute_script_9 Ctrl+Shift+9
execute_script_10 Ctrl+Shift+0
PluginDevToolsToggleOnOff F12
show_color_selector Shift+I
show_mypaint_shade_selector Shift+M
show_minimal_shade_selector Shift+N
show_color_history H
show_common_colors U
