# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothies! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)


name = st.text_input('Your name')
# st.write('Your Name is: '+name)

cnx= st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',my_dataframe, max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for i in ingredients_list:
        ingredients_string +=i + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(i + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+i)
        # st.text(smoothiefroot_response.json())
        df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    my_insert_stmt = f""" insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('{ingredients_string}', '{name}')"""

    # st.write(my_insert_stmt)

    submit = st.button('Submit Order!')

    if submit:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie ({len(ingredients_list)}) is ordered, {name}!', icon="✅")
