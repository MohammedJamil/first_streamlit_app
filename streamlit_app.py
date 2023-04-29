import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create the repeatable code block
def get_fruityvice_data(fruit_choice) :
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice) 
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized
# using api calls
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("please select a fruit to get information")
 else:
  back_from_function = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
except URLError as e:
 streamlit.error()


streamlit.header("The fruit load list contains:")
# snowflake-related function
def get_fruit_load_list(my_cnx) :
 with my_cnx.cursor() as my_cur :
  my_cur.execute("select * from FRUIT_LOAD_LIST")
  return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get fruit load list') :
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list(my_cnx)
 streamlit.dataframe(my_data_rows)

 
# stop here
streamlit.stop()

# A llow the end user to add fruit to the list
def insert_row_snowflake(my_cnx, fruit) :
 with my_cnx.cursor() as my_cur :
  my_cur.execute(f"insert into FRUIT_LOAD_LIST values ('{fruit}')")
  return "Thanks for adding " + fruit

fruit_to_add = streamlit.text_input("Wanna add a fruit ?")
if streamlit.button('Add a fruit to the list') :
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(my_cnx, fruit_to_add)
 streamlit.text(back_from_function)
