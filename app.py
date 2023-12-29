

from shiny import ui,Inputs,Outputs,Session,App, render,reactive
import shinyswatch
from pathlib import Path




css_path = Path(__file__).parent / "www" / "style.css"

app_ui = ui.page_fluid(
    ui.include_css(css_path),
    shinyswatch.theme.superhero(),
    ui.page_navbar(
        ui.nav(
            title="Overview",
            icon=None
        ),
        title=ui.div(ui.panel_title(ui.h2("Logistic Regression Multiple Model Statistics"),window_title="LogisticRegression"),align="center"),
        inverse=True,
        id="navbar_id"
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_action_button(id="taboverview",label="Overview",style='padding:5px; background-color: #fcac44;text-align:center;white-space: normal;'),
            ui.input_action_button(id="tabdata",label="Data Processing",style='padding:5px; background-color: #fcac44;text-align:center;white-space: normal;'),
            ui.input_action_button(id="tabModelEval",label="Model Evaluation",style='padding:5px; background-color: #fcac44;text-align:center;white-space: normal;'),
            ui.input_action_button(id="tabsmodelstbl",label="Multi Model Tablle",style='padding:5px; background-color: #fcac44;text-align:center;white-space: normal;'),
            ui.input_action_button(id="tabsmodelsplotly",label="Multi Model Plotly",style='padding:5px; background-color: #fcac44;text-align:center;white-space: normal;') 
        ),
        ui.output_ui("Output")
    )
    
)


def server(input:Inputs, output:Outputs, session:Session):

    @output
    @render.ui
    def Output():
        if input.taboverview():
            return ui.TagList(
            ui.p("Bonjour")
        )
        elif input.tabdata():
            return ui.TagList(
            ui.p("Data")
        )
        

app = App(ui=app_ui,server=server)


