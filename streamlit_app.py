# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# st.write("Your selected: ",option)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie whill be: ",name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingrediant_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)
if ingrediant_list:
    ingredients_string = ''
    for i in ingrediant_list:
        ingredients_string += i +' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
        st.write('search_on')
        st.write(search_on)
        
        st.subheader(i + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "search_on")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_order = st.button("Submit Order!")
    if time_to_order:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered, "+name_on_order+"!")
        

# st.text(fruityvice_response.json())
# fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
