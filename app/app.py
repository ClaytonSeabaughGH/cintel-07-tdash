# Import necessary libraries and modules
import seaborn as sns  # Used for creating scatterplots
from faicons import icon_svg  # Provides icons for the UI
from shiny import reactive  # Allows for reactive programming in Shiny
from shiny.express import input, render, ui  # Shiny components for input, rendering, and UI layout
import palmerpenguins  # Dataset containing information about penguins

# Load the penguins dataset into a DataFrame
df = palmerpenguins.load_penguins()

# Define the page title and make the layout fillable for better responsiveness
ui.page_opts(title="Penguin Insights Dashboard", fillable=True)

# Create a sidebar to house user input controls and useful links
with ui.sidebar(title="Filter and Explore Penguins"):
    # Input slider to filter penguins based on body mass
    ui.input_slider(
        "mass", "Filter by Body Mass (g)", 2000, 6000, 6000
    )

    # Checkbox group to filter penguins by species
    ui.input_checkbox_group(
        "species",
        "Select Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default: all species selected
    )
    
    # Add a horizontal rule for better UI separation
    ui.hr()
    
    # Add various resource links to help users learn more or report issues
    ui.h6("Learn More About This Dashboard:")
    ui.a("View Source Code", href="https://github.com/denisecase/cintel-07-tdash", target="_blank")
    ui.a("Try the App Online", href="https://denisecase.github.io/cintel-07-tdash/", target="_blank")
    ui.a("Report an Issue", href="https://github.com/denisecase/cintel-07-tdash/issues", target="_blank")
    ui.a("About PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Dashboard Template", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("More Penguin Dashboards", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# Create a responsive column layout to display summary metrics
with ui.layout_column_wrap(fill=False):
    # Value box showing the number of penguins after filtering
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Penguins in View"

        @render.text
        def count():
            # Return the number of rows in the filtered DataFrame
            return f"{filtered_df().shape[0]} penguins"

    # Value box showing the average bill length of filtered penguins
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Avg. Bill Length (mm)"

        @render.text
        def bill_length():
            # Calculate and display the mean bill length
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box showing the average bill depth of filtered penguins
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Avg. Bill Depth (mm)"

        @render.text
        def bill_depth():
            # Calculate and display the mean bill depth
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Create a layout with two side-by-side cards for plots and data
with ui.layout_columns():
    # Card to display a scatterplot of bill length vs. bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Bill Depth")

        @render.plot
        def length_depth():
            # Generate a scatterplot with species differentiation
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Card to display a DataFrame of filtered penguin data
    with ui.card(full_screen=True):
        ui.card_header("Filtered Penguin Data Table")

        @render.data_frame
        def summary_statistics():
            # Select specific columns to show in the data table
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            # Return the filtered data as a DataGrid with filtering enabled
            return render.DataGrid(filtered_df()[cols], filters=True)

# Uncomment this line to include custom CSS for styling
# ui.include_css(app_dir / "styles.css")

# Define a reactive function to filter the penguins dataset
@reactive.calc
def filtered_df():
    # Filter data by selected species and body mass threshold
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
