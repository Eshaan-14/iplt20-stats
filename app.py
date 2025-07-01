import streamlit as st
import pandas as pd
import altair as alt
st.title("Eshaan's First Streamlit App")
st.write("Here's Eshaan's sss second attempt at using data to create a table:")
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# df
df = pd.read_csv('./matches.csv')
 
st.write(df.shape)

df['yr']=df.date.str[:4]
df.head()

col=st.multiselect("Col",df.columns,default=['winner'])
row=st.multiselect("Row",df.columns,default=['yr'])

df_piv1=df.pivot_table( index=row, 
                        columns=col, 
                        aggfunc='count',
                        values='venue'
                    ).fillna('')
st.write(df_piv1)


chart1 =alt.Chart(df).mark_circle().encode(
    x='winner',
    y='yr',
    size='count()',
    color='yr',
    tooltip=['count()']
    )

st.write(chart1)

