import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Startup_Cleaned.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')

df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
def load_investor(investor):
    st.title(investor)
    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightyellow;">Most Recent Investments</h1>',
                unsafe_allow_html=True)
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)
    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightyellow;">Maximum Investments</h1>',
                unsafe_allow_html=True)
    maximum = df[df['investors'].str.contains(investor,na = False)].groupby('startup')['amount'].sum().sort_values(ascending = False).head(1)
    st.dataframe(maximum)

    col1, col2= st.columns(2)

    with col1:
        big = df[df['investors'].str.contains(investor,na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Biggest Investments</h1>',
                    unsafe_allow_html=True)
        fig, ax = plt.subplots()
        ax.bar(big.index,big.values)
        st.pyplot(fig)

    with col2:
        sectors = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Sectors Invested in</h1>',
                    unsafe_allow_html=True)
        fig1, ax1 = plt.subplots()
        ax1.pie(sectors, labels = sectors.index, autopct="0.01f%%")
        st.pyplot(fig1)

    col1, col2 = st.columns(2)

    with col1:
        city = df[df['investors'].str.contains(investor,na=False)].groupby('city')['amount'].sum()
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: pink;">Cities invested in</h1>',
                unsafe_allow_html=True)
        fig2, ax2 = plt.subplots()
        ax2.pie(city, labels = city.index)
        st.pyplot(fig2)

    with col2:
        sub_vertical = df[df['investors'].str.contains(investor, na=False)].groupby('subvertical')['amount'].sum()
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: pink;">Sub-Vertical Sectors Invested in</h1>',
                    unsafe_allow_html=True)
        fig3, ax3 = plt.subplots()
        ax3.pie(sub_vertical, labels = sub_vertical.index)
        st.pyplot(fig3)

    col1, col2 = st.columns(2)

    with col1:
        rounds = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Round-Wise Investment</h1>',
                    unsafe_allow_html=True)
        fig3, ax3 = plt.subplots()
        ax3.bar(rounds.index, rounds.values)
        st.pyplot(fig3)

    with col2:
        df['year'] = pd.to_datetime(df['date']).dt.year
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">YoY Investment Graph</h1>',
                unsafe_allow_html=True)
        yoy = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
        fig, ax = plt.subplots()
        ax.plot(yoy.index, yoy.values)
        st.pyplot(fig)

def load_startup(company):
    st.title(company.upper())
    st.header("FOUNDER'S")
    founder = df[df['startup'].str.contains(company, na=False)]['investors']
    a = founder.tolist()
    for i in a:
        st.write('*', i)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Industries Invested In'.upper())
        filtered_df = df[df['startup'].str.contains(company, na=False)].dropna(subset=['vertical']).drop_duplicates(subset=['vertical'])

        # Resetting the index and printing only the 'lndustry' values
        a = filtered_df.reset_index(drop=True)['vertical'].tolist()
        for i in a:
            st.write('*',i)


    with col2:
        st.subheader('Sub-Industries Invested In'.upper())
        filtered_df = df[df['startup'].str.contains(company, na=False)].dropna(subset=['subvertical']).drop_duplicates(
            subset=['subvertical'])

        # Resetting the index and printing only the 'Sublndustry' values
        a = filtered_df.reset_index(drop=True)['subvertical'].tolist()
        for i in a:
            st.write('*',i)


    with col3:
        st.subheader('Cities Invested In'.upper())
        filtered_df = df[df['startup'].str.contains(company, na=False)].dropna(subset=['city']).drop_duplicates(
            subset=['city'])

        # Resetting the index and printing only the 'city' values
        a = filtered_df.reset_index(drop=True)['city'].tolist()
        for i in a:
            st.write('*',i)

    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Funding Rounds</h1>',
                unsafe_allow_html=True)
    funding_rounds_info = df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)

def load_overall_details():

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1).values[0]
    # average ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_start = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total),'Cr')
    with col2:
        st.metric('Max',str(max_funding),'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding)),'Cr')
    with col4:
        st.metric('Funded Startups',num_start)

    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">MoM Graph</h1>',
                unsafe_allow_html=True)
    selected = st.selectbox('Select Type',['Total','Count'])
    if selected == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)

    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: pink;">Sector Analysis Pie</h1>',
                unsafe_allow_html=True)
    selected_option = st.selectbox('Select Type', ['Sum', 'Count'])
    if selected_option == 'Sum':
        temp_df = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(500)
    else:
        temp_df = df.groupby('vertical')['amount'].count()

    fig3, ax3 = plt.subplots()
    ax3.pie(temp_df,labels = temp_df.index)
    st.pyplot(fig3)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">City wise Funding</h1>',
                    unsafe_allow_html=True)
        # Group by city and sum the investment amounts, filling missing values with 0
        total_investment_by_city = df.groupby('city')['amount'].sum().fillna(0)
        # Sorting the result by total investment amount
        total_investment_by_city = total_investment_by_city.sort_values(ascending=False)
        # Resetting index to make city a column again
        total_investment_by_city = total_investment_by_city.reset_index()

        # Streamlit code
        st.write('TOTAL INVESTMENT BY CITY')
        # Plotting a pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(total_investment_by_city['amount'], labels=total_investment_by_city['city'], autopct='%1.1f%%')
        ax.set_title('Total Investment by City')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # Displaying the plot
        st.pyplot(fig)

    with col2:
        # Group by investors and find the maximum investment amount for each investor

        df['date'] = pd.to_datetime(df['date'])

        # Extract year from the date column
        df['year'] = df['date'].dt.year

        # Group by year and startup, summing the investment amounts, and finding the top startup each year
        top_startups_yearly = df.groupby(['year'])['startup'].agg(lambda x: x.value_counts().idxmax()).reset_index()


        # bar graph
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Top Startup,Year-wise </h1>',
                    unsafe_allow_html=True)
        # Plotting a bar graph
        fig, ax = plt.subplots()
        ax.bar(top_startups_yearly['year'], top_startups_yearly['startup'], color='skyblue')
        ax.set_xlabel('Year')
        ax.set_ylabel('Top Startup')
        ax.set_title('Top Startup Each Year Overall')
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        # Displaying the plot
        st.pyplot(fig)

    with col3:
        st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: lightgreen;">Top Investors</h1>',
                    unsafe_allow_html=True)

        # Aggregate investment amounts for each investor
        investor_totals = df.groupby('investors')['amount'].sum().reset_index()
        # Rank investors based on total investment amount
        investor_totals = investor_totals.sort_values(by='amount', ascending=False)
        # Select top investors (e.g., top 10)
        top_investors = investor_totals.head(10)
        # Plotting the pie chart
        fig, ax = plt.subplots()
        ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
        ax.set_title('Top Investors')
        # ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # Display the pie chart using Streamlit
        st.pyplot(fig)

    st.markdown('<h1 style="font-family: \'Times New Roman\', serif; color: pink;">Funding Heatmap</h1>',
                unsafe_allow_html=True)

    # Pivot the DataFrame to create a matrix suitable for a heatmap
    heatmap_data = df.pivot_table(index='startup', columns='year', values='amount', aggfunc='sum', fill_value=0)

    # Create a heatmap using Seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".0f", linewidths=.5)
    plt.title('Funding Heatmap by Startup and Year')
    st.pyplot(plt)

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    st.header('Divya Dattu Shelke: FS23AI002')
    st.markdown('<h1 style="font-family: Algerian, sans-serif; color:  #87CEEB;">OVERALL ANALYSIS</h1>',
                unsafe_allow_html=True)
    load_overall_details()

elif option == 'StartUp':
    st.markdown('<h1 style="font-family: Algerian, sans-serif; color:  #87CEEB;">STARTUP ANALYSIS</h1>',
                unsafe_allow_html=True)
    company = st.sidebar.selectbox('Select box',sorted(set(df['startup'])))
    btn = st.sidebar.button('Find Startup Details')
    if btn:
        load_startup(company)

else:
    st.markdown('<h1 style="font-family: Algerian, sans-serif; color:  #87CEEB;">INVESTOR</h1>',
                unsafe_allow_html=True)
    selected_investor = st.sidebar.selectbox('Select One',sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn = st.sidebar.button('Find Investors Details')
    if btn:
        load_investor(selected_investor)
