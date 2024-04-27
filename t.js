const s = `
InteractionTool$$select
KarbonCalligraphyTool$$calligraphy
PathTool$$shape_handling
SvgTextTool$$draw-text
KritaShape/KisToolEllipse$$krita_tool_ellipse
KritaShape/KisToolLine$$krita_tool_line
KritaShape/KisToolRectangle$$krita_tool_rectangle
KritaShape/KisToolMultiBrush$$krita_tool_multihand
KisToolPolyline$$polyline
KritaShape/KisToolDyna$$krita_tool_dyna
KritaShape/KisToolBrush$$krita_tool_freehand
KisToolPolygon$$krita_tool_polygon
KisToolPencil$$krita_tool_freehandvector
KisToolPath$$krita_draw_path
KritaShape/KisToolMeasure$$krita_tool_measure
KisAssistantTool$$krita_tool_assistant
ToolReferenceImages$$krita_tool_reference_images
KisToolSelectSimilar$$tool_similar_selection
KisToolSelectElliptical$$tool_elliptical_selection
KisToolSelectContiguous$$tool_contiguous_selection
KisToolSelectPath$$tool_path_selection
KisToolSelectRectangular$$tool_rect_selection
KisToolSelectPolygonal$$tool_polygonal_selection
KisToolSelectOutline$$tool_outline_selection
KisToolSelectMagnetic$$tool_magnetic_selection
KisToolEncloseAndFill$$NULL
KritaFill/KisToolFill$$krita_tool_color_fill
KritaSelected/KisToolColorSampler$$NULL
KritaShape/KisToolLazyBrush$$krita_tool_lazybrush
KritaShape/KisToolSmartPatch$$krita_tool_smart_patch
KritaFill/KisToolGradient$$krita_tool_gradient
ZoomTool$$tool_zoom
PanTool$$tool_pan
KisToolTransform$$krita_tool_transform
KritaTransform/KisToolMove$$krita_tool_move
KisToolCrop$$tool_crop

`.trim().split(/\r?\n/).map(x=>x.split('$$'))

console.log(s)

const res = {}
for (const [k, v] of s) {
    res[k] = v
}
console.log(JSON.stringify(res, null, 4))