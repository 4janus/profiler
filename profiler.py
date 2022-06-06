import pandas_profiling
import st_aggrid
from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport
from  PIL import Image

st.set_page_config(layout='wide') #Choose wide mode as the default setting

#Add a logo (optional) in the sidebar
logo = Image.open(r"Intellix-logo.jpg")
st.sidebar.image(logo,  width=120)
st.sidebar.subheader('Intellix service applet')

#Add the expander to provide some information about the app
with st.sidebar.expander("About the App"):
     st.write("""
        This data profiling App was built by Sharone Li. \n\nModified by Christian Liisberg to allow different separators in .CSV files. \n\nYou can use the app to quickly generate a comprehensive data profiling and EDA report without the need to write any python code. \n\nThe app has the minimum mode (recommended) and the complete code. The complete code includes more sophisticated analysis such as correlation analysis or interactions between variables which may requires expensive computations. )
     """)

#Add an app title. Use css to style the title
st.markdown(""" <style> .font {                                          
    font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Import your data and generate a Pandas data profiling report easily...</p>', unsafe_allow_html=True)
a = st.radio('Select your separator:',['Comma - Default','semikolon - when decimal comma is used','pipe - when decimal an thousands separators is used'])
uploaded_file = st.file_uploader("Upload your csv file:", type=['csv'])
if uploaded_file is not None:
    #checking
    #file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    #st.write(file_details)
    if a == 'Comma - Default':
        sep = ','
        dec = '.'
    elif a == 'semikolon - when decimal comma is used':
        sep = ';'
        dec = ','
    else:
        sep = '|'
        dec = '.'


    df=pd.read_csv(uploaded_file, sep = sep, decimal = dec)

    option1=st.sidebar.radio(
     'What variables do you want to include in the report?',
     ('All variables', 'A subset of variables'))
    
    if option1=='All Variables':
        df=df
    
    elif option1=='A subset of variables':
        var_list=list(df.columns)
        option3=st.sidebar.multiselect(
            'Select variable(s) you want to include in the report.',
            var_list)
        df=df[option3]
   
    option2 = st.sidebar.selectbox(
     'Choose Minimal Mode or Complete Mode',
     ('Minimal Mode', 'Complete Mode'))

    if option2=='Complete Mode':
        mode='complete'
        st.sidebar.warning('The default minimal mode disables expensive computations such as correlations and duplicate row detection. Switching to complete mode may cause the app to run overtime or fail for large datasets due to computational limit.')
    elif option2=='Minimal Mode':
        mode='minimal'

    grid_response = AgGrid(
        df,
        editable=True, 
        height=300, 
        width='100%',
        )

    updated = grid_response['data']
    df1 = pd.DataFrame(updated) 

    if st.button('Generate Report'):
        if mode=='complete':
            profile=ProfileReport(df,
                title="User uploaded table",
                progress_bar=True,
                dataset={
                    "description": 'This profiling report was generated by Insights Bees',
                    "copyright_holder": 'Insights Bees',
                    "copyright_year": '2022'
                }) 
            st_profile_report(profile)
        elif mode=='minimal':
            profile=ProfileReport(df1,
                minimal=True,
                title="User uploaded table",
                progress_bar=True,
                dataset={
                    "description": 'This profiling report was generated by Insights Bees',
                    "copyright_holder": 'Insights Bees',
                    "copyright_year": '2022'
                }) 
            st_profile_report(profile)  