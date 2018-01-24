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


def generate_html_single_var_plot(var_index = 0, x_var = [], y_var = [], plot_type = 'scatter', team_name = 'player'):
    html = "var trace" + str(var_index) + " = {\n"
    html += "x: " + str(x_var) +",\n"
    html += "y: " + str(y_var) +",\n"
    html += "type: '" + str(plot_type) +"',\n"
    html += "name: '" + str(team_name) +"',\n"
    html += "};\n"

    return html

def write_file(filename = "test.txt", content = "Hello world"):
    file = open(filename,'w')
    file.write(content)
    file.close()

def read_file(filename):
    if not os.path.isfile(filename):
        print("There is a problem reading the file " + str(filename) + " Please \
               make sure the file exists")
        return

    with open(filename) as open_file:
        return open_file.read()


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

    # Parse the dictionary and get individual colums
    time = datastore["weeks"]

    # Initialize the ploting section
    plot_section = "<center>\n <div id='tester' style='width:1200px;height:800px;'></div> \
                    \n<div id='standings' style='width:1200px;height:800px;'></div>\n <script> \
                    \nTESTER = document.getElementById('tester');\n"

    # Each section is written the same way so iterate though the list of teams and write it
    for key, value in TEAM_NAMES.iteritems():
            plot_section += generate_html_single_var_plot(key, time, datastore["teams"][value], "scatter", value)

    # Finish the plotting section of the html
    plot_section += "\n var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12]; \
                     \n var layout = { \n title:'La Gansa Standings' \n }; \n Plotly.newPlot(TESTER, data, layout);\n</script>\n</center>\n"

    # At this point we have all the information to write the html file
    write_file(HTML_TEST_FILE_LOCATION, header + plot_section + footer)

    print("Update_page script finished successfully.")

if __name__ == "__main__":
    main()
