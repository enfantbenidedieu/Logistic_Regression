

from shiny import App, Inputs,Outputs,Session,render,ui,reactive
import shinyswatch
import pandas as pd
import seaborn as sns

from shiny.types import NavSetArg
from shiny.types import FileInfo

import plotly.express as px
df = px.data.gapminder()

# Prepare a summary DataFrame
summary_df = (
    df.groupby("country")
    .agg(
        {
            "pop": ["min", "max", "mean"],
            "lifeExp": ["min", "max", "mean"],
            "gdpPercap": ["min", "max", "mean"],
        }
    )
    .reset_index()
)
summary_df.columns = ["_".join(col).strip() for col in summary_df.columns.values]
summary_df.rename(columns={"country_": "country"}, inplace=True)

summary_df =sns.load_dataset("flights")

app_ui = ui.page_navbar(
    # Available themes:
    #  cerulean, cosmo, cyborg, darkly, flatly, journal, litera, lumen, lux,
    #  materia, minty, morph, pulse, quartz, sandstone, simplex, sketchy, slate,
    #  solar, spacelab, superhero, united, vapor, yeti, zephyr
    shinyswatch.theme.superhero(),
    ui.nav("Overview",
        ui.markdown("""
        #### Overview:
        
        **Logistic  regression**, also called a logit model, is a classification algorithm. It is used to model dichotomous outcome variables and 
        to predict a binary outcome based on a set of independent variables. In the logit model the log odds of the outcome is
        modeled as a linear combinationof the predictor variables.
        
        #### Examples :
        
        * Suppose that we are interested in the factors that influence whether a political candidate wins an election. The outcome (response) variable is binary (0/1); win or lose. The predictor variables of interest are the amount of money spent on the campaign, 
        the amount of time spent campaigning negatively and whether or not the candidate is an incumbent.        
        * A researcher is interested in how variables, such as GRE (Graduate Record Exam scores), GPA (grade point average) and prestige of the undergraduate institution, 
        effect admission into graduate school. The response variable, admit/don't admit, is a binary variable.
                           
        #### Model Evaluation & Interpreting LR Results:
        
        * An overall evaluation of the logistic model; 
        * Statistical tests of individual predictors;
        * Goodness-of-fit statistics; and 
        * Assessing the predictive ability of the model.
        
        #### Reference:
        
        * Agresti, Alan. 2012. *Categorical Data Analysis*. Vol. 792. John Wiley & Sons.
        * Clogg, Clifford C, and Edward S Shihadeh. 1994. *Statistical Models for Ordinal Variables*.
        * Lemeshow, Stanley, Rodney X Sturdivant, and David W Hosmer Jr. 2013. *Applied Logistic Regression*. John Wiley & Sons.

        """)
    ),
    ui.nav("Data Processing",
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.h6("Data Process Menu"),
                ui.input_action_button('mDataUploadBtn',label = "Data Upload!",class_="btn-primary"),
                ui.br(),
                ui.input_action_button('mshowtableBtn',label='Review Dataset!',class_ = "btn-primary"),
                ui.br(),
                ui.input_action_button('mFixDependentVarBtn',label = "Choose Dependent Variable!",class_="btn-primary"),
                ui.br(),
                ui.input_action_button('mCleanseDataBtn',label = "Data Cleansing!",class_="btn-primary"),
                ui.br(),
                ui.input_action_button('mFinalProcessBtn',label = "Build Models!",class_="btn-primary"),
                ui.br(),
                ui.download_button("mDownloadmydataBtn", "Download Dataset CSV")
            ),
            ui.panel_main(
                ui.output_ui("dataset_output"),
                #ui.output_data_frame("dataset_table")
            )
        )
    ),
    ui.nav("Model Evaluation",
           ui.layout_sidebar(
               ui.panel_sidebar(
                   ui.h6("LR Model Evaluation"),
                   ui.input_action_button("mLrModelRevise","Model Revision",class_="btn-success"),
                   ui.br(),
                   ui.h6("Goodness of Fit"),
                   ui.input_action_button('mLikelihoodBtn',"Likelihood Ratio!",class_="btn-primary"),
                   ui.input_action_button('mPseudoRsqBtn',"Pseudo R2 Test!",class_="btn-primary"),
                   ui.input_action_button('mHosmerLBtn',"Hosmer & Lemeshow Test!",class_="btn-primary"),
                   ui.br(),
                   ui.h6("Statistical Test of Individual Predictors"),
                   ui.input_action_button('mWaldTestBtn',"Wald Test!",class_="btn-primary"),
                   ui.input_action_button('mAnovaTestBtn',"ANOVA Test!",class_="btn-primary"),
                   ui.input_action_button('mVariableImpBtn',"Variable Importance!",class_="btn-primary"),
                   ui.br(),
                   ui.h6("Model Result Validation"),
                   ui.input_action_button('mConfusionMtrxBtn',"Confusion Matrix!",class_="btn-primary"),
                   ui.input_action_button('mKSROCPlotBtn',"KS-Plot & ROC (AUC)!",class_="btn-primary"),
                   ui.input_action_button('mKFoldValidBtn',"K-fold Cross Validation !",class_="btn-primary"),
                   ui.input_action_button('mAICDevianceBtn',"AIC / Deviance!"),
                   #ui.input_action_button('mVarInflationBtn',"Variance Inflation Factor!",class_="btn-primary"),
                   width=3
               ),
               ui.panel_main(
                   ui.output_ui("placeholder")
               )
           )),
    ui.nav("Multi Model Table"),
    ui.nav("Multi Model Plotly"),
    title="Logistic Regression Multiple Model Statistics",
)


def server(input:Inputs,output:Outputs,session:Session):

    # Load dataset
    @reactive.Calc
    def data():
        if input.file() is None:
            pass
        f: list[FileInfo] = input.file()
        df = pd.read_csv(f[0]["datapath"],header = 0 if input.header() else None)
        return df
        
    @output
    @render.ui
    @reactive.event(input.mDataUploadBtn,ignore_none=False)
    def dataset_output():
        return ui.column(6,
                   ui.input_file("file", label="Select : csv, txt, xls, xlsx, rds, dat",multiple=False,accept=[".csv",".txt",".xls",".xlsx",".rds"]),
                    ui.row(
                        ui.column(4,ui.input_radio_buttons("sep","Separator",{",":"Comma",";":"Semicolon","\t":"Tab"},selected=",")),
                        ui.column(4,ui.input_radio_buttons("quote","Quote",{"":"None",'"':"Double Qot.","'":"Signe Qot"},selected='"')),
                        ui.column(4,ui.input_radio_buttons("header","Header",{True:"True",False:"False"},selected=True)),
                        ui.input_action_button('mgetfileclick',label = "Get Data!",class_="btn-success"),
                        ui.output_text('mfileimportmsg')
                    ) 
        )
    
    
        
    
    @output
    @render.data_frame
    def dataset_table():
        if input.file() is None:
            pass
        return render.DataGrid(data())
        #return render.DataGrid(summary_df.round(2),row_selection_mode="multiple",width="fit-content",height="100%",filters=True)
    
    @output
    @render.ui
    @reactive.event(input.mgetfileclick,ignore_none=False)
    def _():
        if len(input.file())==0:
            return ui.notification_show("Oops!", "Hi first browse, select and import ...!",)
    
    @output
    @render.text
    def mfileimportmsg():
        return "Done - uploaded"

app = App(app_ui,server)