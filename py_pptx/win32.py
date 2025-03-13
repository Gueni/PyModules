import xlsxwriter



from openpyxl import load_workbook
from PIL import Image

import xlsxwriter
from PIL import Image

# Open the workbook
workbook = xlsxwriter.Workbook('/home/hunter/Documents/Workspace/Python_code/py_pptx/step_chart.xlsx')

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
            filename = f"/home/hunter/Documents/Workspace/Python_code/py_pptx/{sheet.name}_{chart_obj.name}.png"

            # Create a new worksheet to insert the chart image
            # image_ws = workbook.add_worksheet(sheet.name)

            # # Insert the chart image in the worksheet
            # image_ws.insert_image(
            #     chart_top, chart_left, filename,
            #     {'image_data': chart_image,
            #      'x_scale': chart_width / chart_image.width,
            #      'y_scale': chart_height / chart_image.height})

            # Save the chart image as a PNG file
            chart_image.save(filename)

# Close the workbook
workbook.close()
