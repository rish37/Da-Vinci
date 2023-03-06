import streamlit as st
import plotly.express as px
import pandas as pd
import base64
from tqdm import tqdm

# Function to generate a progress bar for TQDM
@st.cache
def tqdm_bar(total):
    pbar = tqdm(total=total)
    return pbar

# Load the data into a Pandas DataFrame with TQDM
@st.cache
def load_data():
    pbar = tqdm_bar(len(uploaded_file.readlines()))
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, iterator=True)
    data = []
    for chunk in df:
        data.append(chunk)
        pbar.update(len(chunk))
    pbar.close()
    return pd.concat(data)

# Add the web icon to the title bar
st.markdown(
    '<link rel="shortcut icon" type="image/x-icon" href="https://www.flaticon.com/free-icon/data-analytics_2103888">',
    unsafe_allow_html=True,
)

# Add the logo to the app
st.markdown(
    '<img src="https://cdn-icons-png.flaticon.com/128/2103/2103888.png" width="100" height="100">',
    unsafe_allow_html=True,
)


# background image and designing



#configuration
st.set_option('deprecation.showfileUploaderEncoding',False)
# title of the webpage
st.title("Leonardo Da Visual")
st.caption("Data visualization is the representation of data through use of common graphics,"
        " such as charts, plots, infographics, and even animations. These visual displays of information"
        " communicate complex data relationships and data-driven insights in a way that is easy to understand.")

st.caption("This webpage is created to do simple data visualization in 5 simple graph"
        " and tells story of the data.")

#creating the sidebar for uploading the data

#creating tab to split the to concepts
tab1,tab2, tab3, tab4= st.tabs(["data cleaning","story of given data ", " Data visualization","about us"])
with tab1:
    #cleaning the raw into cleaned data...

    st.title("Data Cleaning with Streamlit")

    # Load the data into a Pandas DataFrame
    uploaded_file = st.file_uploader("Upload your data file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Check if the data is already clean
        if df.isnull().sum().sum() == 0 and len(df) == len(df.drop_duplicates()):
            st.write("Data is already clean.")
            st.write(df)
        else:
            # Check for missing values
            missing_values = df.isnull().sum()
            st.write("Missing values:")
            st.write(missing_values)

            # Fill missing values with the mean of the column
            fill_mean = st.checkbox("Fill missing values with mean")
            if fill_mean:
                df.fillna(df.mean(), inplace=True)

            # Drop rows with missing values
            drop_na = st.checkbox("Drop rows with missing values")
            if drop_na:
                df.dropna(inplace=True)

            # Remove duplicate rows
            drop_duplicates = st.checkbox("Remove duplicate rows")
            if drop_duplicates:
                df.drop_duplicates(inplace=True)

            # Download the cleaned data as a CSV file
            if st.button("Download cleaned data"):
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">Download cleaned data</a>'
                st.markdown(href, unsafe_allow_html=True)

with tab2:
    st.title("Narrative Text Generation from CSV")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv","xlsx"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("Generate Narrative"):
            narrative = "The data in the file contains information about "
            for col in df.columns:
                narrative += f"{len(df[col].dropna())} {col}, "
            narrative = narrative[:-2] + "."

            st.write("## Narrative Text")
            st.markdown(narrative)
with tab3:
    # add a sidebar
    st.subheader("visual settings")
    # setup file upload
    uploaded_file = st.file_uploader(label="Upload you CSV or Excel file.", type=['csv', 'xlsx'])
    import streamlit as st

    if uploaded_file is not None:
        print(uploaded_file)
        print("Hello")
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            df = pd.read_excel(uploaded_file)

    # data visualization
    global numeric_columns
    global non_numeric_columns
    try:
        st.write(df)
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object']).columns)
        non_numeric_columns.append(None)
        print(non_numeric_columns)

    except Exception as e:
        print(e)
        st.write("please upload data file to the application:")

    # add a select widget to sidebar
    chart_select = st.selectbox(
        label="select the chart type",
        options=['Area chart', 'Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
    )

    # numeric_columns == list(df.select_dtypes(['float','int']).columns)

    # Area chart
    if chart_select == 'Area chart':
        st.subheader("Area chart settings")
        try:
            x_values = st.selectbox('x axis', options=numeric_columns)
            y_values = st.selectbox('y axis', options=numeric_columns)
            color_value = st.selectbox('color', options=non_numeric_columns)
            plot = px.area(data_frame=df, x=y_values, color=color_value)
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    # scatterplot
    if chart_select == 'Scatterplots':
        st.subheader("Scatterplot settings")
        try:
            x_values = st.selectbox('x axis', options=numeric_columns)
            y_values = st.selectbox('y axis', options=numeric_columns)
            color_value = st.selectbox('color', options=non_numeric_columns)
            plot = px.scatter(data_frame=df, x=y_values, color=color_value)
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    # lineplot
    if chart_select == 'Lineplots':
        st.subheader("lineplots settings")
        try:
            x_values = st.selectbox('x axis', options=numeric_columns)
            y_values = st.selectbox('y axis', options=numeric_columns)
            color = st.selectbox('color', options=numeric_columns)
            plot = px.line(data_frame=df, x=y_values, color=color)
            # display the chart
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    # histogram
    if chart_select == 'Histogram':
        st.subheader("Histogram Settings")
        try:
            x = st.selectbox('Feature', options=numeric_columns)
            bin_size = st.slider("Number of Bins", min_value=10, max_value=100, value=40, step=1)

            color_value = st.selectbox("Color", options=non_numeric_columns)
            plot = px.histogram(x=x, data_frame=df, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)

    # Boxplot
    if chart_select == 'Boxplot':
        st.subheader("Boxplot Settings")
        try:
            y = st.selectbox("Y axis", options=numeric_columns)
            x = st.selectbox("X axis", options=non_numeric_columns)
            color_value = st.selectbox("Color", options=non_numeric_columns)
            plot = px.box(data_frame=df, y=y, x=x, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            print(e)


with tab4:
    st.title("About us")
    st.subheader("Welcome to our Data Visualization App!")
    st.caption('I am rishikesh vishwakarma future data engineer/standup comedian,and my app was created with the goal of providing'
               ' a simple and intuitive platform for visualizing and exploring data in a meaningful way.')
    st.caption('I am dedicated to delivering the best possible user experience with the help of chatGPT,'
               ' and I am very constantly striving to improve our app based on user feedback. '
               'Our goal is to empower individuals and organizations to make informed decisions based on data.')
    st.caption('The app was built using the latest technologies and is designed to be easy to use and highly customizable.'
               ' Our proprietary algorithms and visualizations are designed to help users quickly identify patterns,'
               ' trends, and insights in their data. We believe that data visualization should not only be functional but'
               ' also beautiful and engaging, and that is why we put a strong emphasis on design.')
    st.caption('In the future, we plan to expand the apps capabilities and add new features to make it even more powerful'
               ' and useful. We are always looking for new ways to improve our app and provide the best possible experience '
               'for our users.')
    st.caption('If you have any questions or feedback, please dont. Whould not love to hear that from you!')


    #feedback form
    import streamlit as st

    st.text("Feedback Form")
    name = st.text_input("Name")
    email = st.text_input("Email")
    rating = st.slider("Rating", 1, 5)
    comments = st.text_area("Comments")

    if st.button("Submit"):
        st.success("Thanks for the feedback, {}!".format(name))

    st.caption('This is just a draft, and you can feel free to report it or additions to make it better fit your needs 👀')
    st.subheader('Visit again, buddy!🤞')
