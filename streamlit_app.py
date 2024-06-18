## Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customise your Smoothie :cup_with_straw:")
st.write(
    """choose the fruits you want in your custom smoothie!!
    """
)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list= st.multiselect('choose up to five ingredients:',my_dataframe)
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_stirng=''
    for i in ingredients_list:
        ingredients_stirng+=i+' '

    
    # st.write(ingredients_stirng)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_stirng + """')"""

    
    # st.write(my_insert_stmt) 

    
    time_to_insert = st.button('Submit Order')

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        
        st.success('Your Smoothie is ordered!', icon="✅")
    



