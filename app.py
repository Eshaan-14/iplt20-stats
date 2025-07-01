import streamlit as st
import pandas as pd
st.write("Here's Eshaan's sss second attempt at using data to create a table:")
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# df
df = pd.read_csv('./matches.csv')

df.shape
