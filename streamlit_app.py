import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title("The Healthfood Diner")

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)


# Create request function
def get_fruityvice_data(a_fruit):
   # Request info from API
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + a_fruit)
    # Transform json format into pandas dataframe
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Show the dataframe on the streamlit app
    return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    fruit_info_df = get_fruityvice_data(fruit_choice)
    st.dataframe(fruit_info_df)
   

except URLError as e:
  st.error()




# Snowflake functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()
   
def insert_snowflake_row(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
      return f'Thanks for adding {new_fruit}!'
   
# Add a button to show the list of fruits we have in a snowflake table
st.header("View Our Fruit List - Add Your Favorites!")
if st.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   st.dataframe(my_data_rows)

# Allow user to add a fruit to the list
add_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   result_from_function = insert_snowflake_row(add_fruit)
   my_cnx.close()
   st.text(result_from_function)




