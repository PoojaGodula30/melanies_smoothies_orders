# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
# Write directly to the app
st.title(":cup_with_straw: Customise your Smoothie :cup_with_straw:")
st.write(
    """choose the fruits you want in your custom smoothie!!
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be", name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()   

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list= st.multiselect('choose up to five ingredients:',my_dataframe,max_selections=5)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_stirng=''
    for i in ingredients_list:
        ingredients_stirng+=i+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')
        st.subheader(i+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        # st.write(ingredients_stirng)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_stirng + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt) 
    time_to_insert = st.button('Submit Order')

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

# Let's Call the Fruityvice API from Our SniS App!We need to bring in a Python package library called requests.  The requests library allows us to build and sent REST API calls. 
#st.text(fruityvice_response.json())

# Let's Put the JSON into a Dataframe.People often use df as shorthand for "dataframe." We'll call our dataframe fv_df, because it's our Fruityvice Dataframe.
