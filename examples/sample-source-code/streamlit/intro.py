import pandas
import numpy
import streamlit as st

st.title("Streamlit intro")
st.write("Examples below were taken from:  https://streamlit.io/docs/getting_started.html#get-started")


st.subheader("Here's our first attempt at using data to create a table:")

st.code("""
df = pandas.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
""", language='python')
df = pandas.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
# here we use 'magic', 
# any time that Streamlit sees a variable or a literal value on its own line, 
# it automatically writes that to your app using st.write()
df



st.subheader("Draw a line hart:")
st.code("""
chart_data = pandas.DataFrame(
     numpy.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)
""", language='python')

chart_data = pandas.DataFrame(
     numpy.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)


st.subheader("Let’s use Numpy to generate some sample data and plot it on a map of San Francisco:")

st.code("""
map_data = pandas.DataFrame(
    numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)
""", language='python')

map_data = pandas.DataFrame(
    numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
st.map(map_data)



st.title("Add interactivity with widgets")

st.subheader("Use checkboxes to show/hide data")

st.code("""
if st.checkbox('Show dataframe'):
    chart_data = pandas.DataFrame(
       numpy.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
""", language='python')

if st.checkbox('Show dataframe'):
    chart_data = pandas.DataFrame(
       numpy.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)


st.subheader("Put widgets in a sidebar")

st.code("""
if st.checkbox('Show in sidebar'):
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        ["a", "b","c"])

    'You selected:', option
""", language='python')

if st.checkbox('Show in sidebar'):
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        ["a", "b","c"])

    'You selected:', option



st.subheader("Show progress")

st.code("""
import time

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
""", language='python')  

import time

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'