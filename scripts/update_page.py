# -*- coding: utf-8 -*-
import json
import os.path


# Constant filenames
JSON_FILE_LOCATION = "../json/data.json"
HTML_HEADER_FILE_LOCATION = "../html/header.html"
HTML_FOOTER_FILE_LOCATION = "../html/footer.html"
HTML_TEST_FILE_LOCATION = "../test.html"

# Teams with current yahoo order
TEAM_NAMES = {"1" : "Tibu de la gente",
              "2" : "[b.A] El Chacho",
              "3" : "Arios Rompebolas",
              "4" : "Cydonia Knights BBC",
              "5" : "Dr Respect & Mr Rage",
              "6" : "JPs Logrono Rockies",
              "7" : "Las Taras de Doug",
              "8" : "Los Grandes",
              "9" : "OGM_Gansa",
              "10": "Red Sox Pohio",
              "11": "TheMBullets",
              "12": "Nordics" }


def generate_html_single_var_plot(var_index = '0', x_var = [], y_var = [], plot_type = 'scatter', legend = ''):
    """Generate html text string for plotting a single variable.

    Args:
        var_index (str): Index for current plotting variable.
        x_var (array): X axis variable to plot.
        y_var (array): Y axis variable to plot.
        plot_type (str): Type of plot to use.
        legend (str): Variable legend string.

    Returns:
        str: A string containing a single variable plot using plotly.
    """

    if not x_var or not y_var:
        print("You passed an empty array to plot. ")

    html = "var trace" + str(var_index) + " = {\n"
    html += "x: " + str(x_var) +",\n"
    html += "y: " + str(y_var) +",\n"
    html += "type: '" + str(plot_type) +"',\n"
    html += "name: '" + str(legend) +"',\n"
    html += "};\n"

    return html

def write_file(filename = "test.txt", content = "Hello world"):
    """General function to write a new file.

    Args:
        filename (str): Name of the file to create. Function accept relative and global file paths.
        content (str): Content of the file to write.
    """

    file = open(filename,'w')
    file.write(content)
    file.close()

def read_file(filename):
    """General function to read a text file.

    Args:
        filename (str): Name of the file to read. Function accept relative and global file paths.

    Returns:
        str: A string with the content of the file. Empty string if no found available.
    """

    if not os.path.isfile(filename):
        print("There is a problem reading the file " + str(filename) + " Please \
               make sure the file exists")
        return ""

    with open(filename) as open_file:
        return open_file.read()

def create_standing_plot(json_dictionary, team_names):
    """ Create the standing html plotting section from the json_dictionary and teams.

    Args:
        json_dictionary (dic): Dictionary containing points per week per team.
        team_names (dic): Disctionary containing the number and name of each team.

    Returns:
        str: A string with the html plotting section of the standings.
    """

    # Parse the dictionary and get individual colums
    time = json_dictionary["weeks"]

    # Initialize the ploting section
    plot_section = "<center>\n <div id='tester' style='width:1200px;height:800px;'></div> \
                    \n<div id='standings' style='width:1200px;height:800px;'></div>\n <script> \
                    \nTESTER = document.getElementById('tester');\n"

    # Each section is written the same way so iterate though the list of teams and write it
    for key, value in team_names.iteritems():
            plot_section += generate_html_single_var_plot(key, time, json_dictionary["teams"][value], "scatter", value)

    # Finish the plotting section of the html
    plot_section += "\n var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12]; \
                     \n var layout = { \n title:'La Gansa Standings' \n }; \n Plotly.newPlot(TESTER, data, layout);\n</script>\n</center>\n"

    return plot_section

def main():

    # Dictionary to save the current stats
    datastore = {}

    # Load json content
    with open(JSON_FILE_LOCATION) as json_file:
        datastore = json.loads(json_file.read())
        print(datastore)

    # This is a hacky way to update the website. As we have all the data required
    # we could re-generate the html. Find a proper way to interact with the site
    # Maybe send a json file? or find how to load a local json file?

    # Read the header section of the html
    header = read_file(HTML_HEADER_FILE_LOCATION)
    # Read the footer section of the html
    footer = read_file(HTML_FOOTER_FILE_LOCATION)

    if not header or not footer:
        return

    # Create the standing plotting section
    plot_section = create_standing_plot(datastore, TEAM_NAMES)

    # At this point we have all the information to write the html file
    write_file(HTML_TEST_FILE_LOCATION, header + plot_section + footer)

    print("Update_page script finished successfully.")

if __name__ == "__main__":
    main()
