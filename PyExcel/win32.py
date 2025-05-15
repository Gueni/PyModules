import xlsxwriter
from openpyxl import load_workbook
from PIL import Image
import xlsxwriter
from PIL import Image

# Open the workbook
workbook = xlsxwriter.Workbook('')
# Loop through each sheet
for sheet in workbook.worksheets():
    # Loop through each chart object in the sheet
    for chart_obj in sheet.chart_objects():
        # Check if the chart object is a bar chart
        if chart_obj.type == 'bar':
            # Get the chart area coordinates
            chart_left = chart_obj.left
            chart_top = chart_obj.top
            chart_width = chart_obj.width
            chart_height = chart_obj.height
            # Get the chart as a PIL image
            chart_image = chart_obj.chart.render_image()
            # Get the filename
            filename = f"  /py_pptx/{sheet.name}_{chart_obj.name}.png"
            # Save the chart image as a PNG file
            chart_image.save(filename)
# Close the workbook
workbook.close()