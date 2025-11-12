# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothies :cup_with_straw:")
st.write(
  """Choose the fruit which you want in your Smoothie.
  """
)

name_on_order = st.text_input("Name On Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

cnx = st.connection("snowflake",account = "KUQDTBH-SXB83112",
user = "VAISHALIGAMPAWAR",
password = "Ngp@1024pue_12",
role = "SYSADMIN",
warehouse = "COMPUTE_WH",
database = "SMOOTHIES",
schema = "PUBLIC")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose upto 5 ingedients :',my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+name_on_order, icon="✅")

