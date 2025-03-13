# Automating PowerPoint Generation with Python

This Python program automates the process of generating PowerPoint presentations using data from an Excel sheet. The program reads the data from the Excel sheet and creates slides in a PowerPoint presentation based on the data.

## Prerequisites

Before running the program, ensure that the following libraries are installed:

- pandas
- openpyxl
- python-pptx

## Setup

1. Clone this repository to your local machine.
2. Install the required libraries using `pip`.
3. Update the `input.xlsx` file with your data.
4. Update the `config.py` file with your PowerPoint template file path and the data sheet name.
5. Run the `generate_ppt.py` script to generate the PowerPoint presentation.

## Usage

To use this program, follow the steps in the Setup section and then run the `generate_ppt.py` script.

The program will read the data from the specified Excel sheet and generate a PowerPoint presentation with slides based on the data. The program will use the specified PowerPoint template file as a starting point for the presentation.

## Configuration

The `config.py` file contains the following variables:

- `TEMPLATE_FILE`: The file path for the PowerPoint template file.
- `DATA_SHEET`: The name of the sheet in the Excel file containing the data.

You can update these variables to customize the behavior of the program.

Running the generate_ppt.py script will create a PowerPoint presentation with three slides, one for each row of data in the Excel sheet. The slides will contain text boxes with the name, age, and gender of each person.

License
This program is licensed under the MIT License. See the LICENSE file for more information.