import streamlit as st
import pandas as pd
import numpy as np
import time
import os 
import base64
from pandas.api.types import is_numeric_dtype

st.set_page_config(layout="wide")

st.title('DataDIY')

#====== DOWNLOAD FILE FUNCTION ======#

def download_link(object_to_download, download_filename, download_link_text):
    
    #Generates a link to download the given object_to_download.

    #object_to_download (str, pd.DataFrame):  The object to be downloaded.
    #download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    #download_link_text (str): Text to display for download link.

    #Examples:
    #download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    #download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

#======================================


@st.cache

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

# Notify the reader that the data was successfully loaded.
data_load_state.text("Cache Loaded! (using st.cache)")


tcol1, tcol2, tcol3,tcol4 = st.beta_columns((2,2,1,1))



file1 = tcol1.file_uploader('Upload File 1')

if file1:
    df1 = pd.read_csv(file1)


    preview_raw_expander_file_1 = tcol1.beta_expander("Show Raw Dataframe")
    preview_raw_expander_file_1.write(df1)
    preview_raw_expander_file_1.write(df1.shape)


    col_list_1 = list()

    for c in df1:
        col_list_1.append(c)

    choose_columns_expander_file_1 = tcol1.beta_expander("Trimming Dataframe Columns")

    selected_col_df1 = choose_columns_expander_file_1.multiselect('Select columns to be active in [File 1]. If no selection, all columns will be used',col_list_1)
    if selected_col_df1:
        df1_1 = df1[selected_col_df1]
    else:
        selected_col_df1 = col_list_1
        df1_1 = df1[selected_col_df1]

    #=================================

    col_list_2 = list()

    for c in df1_1:
        col_list_2.append(c)


    #=================================

    unique_value_file_1 = tcol1.beta_expander("Show Number of Unique Values")

    selected_col_df1_1_unique = unique_value_file_1.selectbox('Select columns to show total unique value of [File 1]', col_list_2)
    
    if selected_col_df1_1_unique:
        unique_set = set(df1_1[selected_col_df1_1_unique])
        unique_len = len(unique_set)
        
        unique_value_file_1.write('Number of items: ' + str(unique_len))
        unique_value_file_1.write(unique_set)

    #=================================

    replace_value_file_1 = tcol1.beta_expander("Replace Values")

    selected_col_df1_1_replace = replace_value_file_1.multiselect('Select columns to replace [File 1]', col_list_2)
    
    old_value_file_1 = replace_value_file_1.text_input('Old Value [File 1]')
    new_value_file_1 = replace_value_file_1.text_input('New Value [File 1]')

    if old_value_file_1 != "" and new_value_file_1 != "":
        if selected_col_df1_1_replace:
            df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].replace(old_value_file_1, new_value_file_1)
            replace_value_file_1.write('Values replaced')

        else:
            df1_1 = df1_1.replace(old_value_file_1,new_value_file_1)
            replace_value_file_1.write('Values replaced')


    #=================================



    remove_null_expander_file_1 = tcol1.beta_expander("Removal of NULL values")

    selected_col_df1_1_null = remove_null_expander_file_1.multiselect('Select columns to have rows removed if NULL in [File 1]. If no selection, all columns will be used', col_list_2)
    if selected_col_df1_1_null:

        pass
    else:
        selected_col_df1_1_null = selected_col_df1


    if remove_null_expander_file_1.checkbox('Remove NULL rows [File 1]'):
        df1_1 = df1_1.dropna(subset=selected_col_df1_1_null)

    #=================================

    replace_null_expander_file_1 = tcol1.beta_expander("Replace NULL values")

    selected_col_df1_1_replace = replace_null_expander_file_1.multiselect('Select Columns to replace NULL values [File 1]', col_list_2)

    if selected_col_df1_1_replace:
        pass
    else:
        selected_col_df1_1_replace = selected_col_df1

    replace_null_f1 = replace_null_expander_file_1.radio('Replace NULL with [File 1]:', ('No action','0','Mean', 'Median'))

    if replace_null_f1 == 'No action':
        pass
    if replace_null_f1 == '0':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(0)
    if replace_null_f1 == 'Mean':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(df1_1.mean())
    if replace_null_f1 == 'Median':
        df1_1[selected_col_df1_1_replace] = df1_1[selected_col_df1_1_replace].fillna(df1_1.median())



    minmax_expander_file_1 = tcol1.beta_expander("Show Numeric Range")

    selected_col_df1_1_minmax = minmax_expander_file_1.selectbox('Select to explore numeric statistics [File 1]', col_list_2)

    if selected_col_df1_1_minmax and is_numeric_dtype(df1_1[selected_col_df1_1_minmax]):

       minmax_expander_file_1.write('Minimum : ' + str(df1_1[selected_col_df1_1_minmax].min()))
       minmax_expander_file_1.write('Maximum : ' + str(df1_1[selected_col_df1_1_minmax].max()))
       minmax_expander_file_1.write('Mean : ' + str(df1_1[selected_col_df1_1_minmax].mean()))
       minmax_expander_file_1.write('Median : ' + str(df1_1[selected_col_df1_1_minmax].median()))
       minmax_expander_file_1.bar_chart(df1_1[selected_col_df1_1_minmax])
  
    else:
        minmax_expander_file_1.write('Invalid column (Non numeric)')



    preview_mod_expander_file_1 = tcol1.beta_expander("Show Modified Dataframe")
    preview_mod_expander_file_1.write(df1_1)
    preview_mod_expander_file_1.write(df1_1.shape)




    #=================================



###FILE 2####


file2 = tcol2.file_uploader('Upload File 2')

if file2:
    df2 = pd.read_csv(file2)


    preview_raw_expander_file_2 = tcol2.beta_expander("Show Raw Dataframe")
    preview_raw_expander_file_2.write(df2)
    preview_raw_expander_file_2.write(df2.shape)


    col_list_3 = list()

    for c in df2:
        col_list_3.append(c)

    choose_columns_expander_file_2 = tcol2.beta_expander("Trimming Dataframe Columns")

    selected_col_df2 = choose_columns_expander_file_2.multiselect('Select columns to be active in [File 2]. If no selection, all columns will be used',col_list_3)
    if selected_col_df2:
        df2_1 = df2[selected_col_df2]
    else:
        selected_col_df2 = col_list_1
        df2_1 = df2[selected_col_df2]

    #=================================

    col_list_4 = list()

    for c in df2_1:
        col_list_4.append(c)


    #=================================

    unique_value_file_2 = tcol2.beta_expander("Show Number of Unique Values")

    selected_col_df2_1_unique = unique_value_file_2.selectbox('Select columns to show total unique value of [File 2]', col_list_4)
    
    if selected_col_df2_1_unique:
        unique_set = set(df2_1[selected_col_df2_1_unique])
        unique_len = len(unique_set)
        
        unique_value_file_2.write('Number of items: ' + str(unique_len))
        unique_value_file_2.write(unique_set)

    #=================================

    replace_value_file_2 = tcol2.beta_expander("Replace Values")

    selected_col_df2_1_replace = replace_value_file_2.multiselect('Select columns to replace [File 2]', col_list_4)
    
    old_value_file_2 = replace_value_file_2.text_input('Old Value [File 2]')
    new_value_file_2 = replace_value_file_2.text_input('New Value [File 2]')

    if old_value_file_2 != "" and new_value_file_2 != "":
        if selected_col_df2_1_replace:
            df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].replace(old_value_file_2, new_value_file_2)
            replace_value_file_2.write('Values replaced')

        else:
            df2_1 = df2_1.replace(old_value_file_2,new_value_file_2)
            replace_value_file_2.write('Values replaced')


    #=================================



    remove_null_expander_file_2 = tcol2.beta_expander("Removal of NULL values")

    selected_col_df2_1_null = remove_null_expander_file_2.multiselect('Select columns to have rows removed if NULL in [File 2]. If no selection, all columns will be used', col_list_4)
    if selected_col_df2_1_null:

        pass
    else:
        selected_col_df2_1_null = selected_col_df2


    if remove_null_expander_file_2.checkbox('Remove NULL rows [File 2]'):
        df2_1 = df2_1.dropna(subset=selected_col_df2_1_null)

    #=================================

    replace_null_expander_file_2 = tcol2.beta_expander("Replace NULL values")

    selected_col_df2_1_replace = replace_null_expander_file_2.multiselect('Select Columns to replace NULL values [File 2]', col_list_4)

    if selected_col_df2_1_replace:
        pass
    else:
        selected_col_df2_1_replace = selected_col_df2

    replace_null_f1 = replace_null_expander_file_2.radio('Replace NULL with [File 2]:', ('No action','0','Mean', 'Median'))

    if replace_null_f1 == 'No action':
        pass
    if replace_null_f1 == '0':
        df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].fillna(0)
    if replace_null_f1 == 'Mean':
        df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].fillna(df2_1.mean())
    if replace_null_f1 == 'Median':
        df2_1[selected_col_df2_1_replace] = df2_1[selected_col_df2_1_replace].fillna(df2_1.median())



    minmax_expander_file_2 = tcol2.beta_expander("Show Numeric Range")

    selected_col_df2_1_minmax = minmax_expander_file_2.selectbox('Select to explore numeric statistics [File 2]', col_list_2)

    if selected_col_df2_1_minmax and is_numeric_dtype(df2_1[selected_col_df2_1_minmax]):

       minmax_expander_file_2.write('Minimum : ' + str(df2_1[selected_col_df2_1_minmax].min()))
       minmax_expander_file_2.write('Maximum : ' + str(df2_1[selected_col_df2_1_minmax].max()))
       minmax_expander_file_2.write('Mean : ' + str(df2_1[selected_col_df2_1_minmax].mean()))
       minmax_expander_file_2.write('Median : ' + str(df2_1[selected_col_df2_1_minmax].median()))
       minmax_expander_file_2.bar_chart(df2_1[selected_col_df2_1_minmax])
  
    else:
        minmax_expander_file_2.write('Invalid column (Non numeric)')



    preview_mod_expander_file_2 = tcol2.beta_expander("Show Modified Dataframe")
    preview_mod_expander_file_2.write(df2_1)
    preview_mod_expander_file_2.write(df2_1.shape)




    #=================================



###FILE MERGE####

try:
    if (df1_1, df2_1) is not None:
        tcol3.header('Join Dataframe')
        key1 = tcol3.selectbox('[File 1] Column',col_list_2)
        key2 = tcol3.selectbox('[File 2] Column',col_list_4)

        join_type = tcol3.selectbox('Type of Join',['inner','outer','right'])

        if tcol3.button('Execute Join'):
            df_merge = pd.merge(df1_1, df2_1, how=join_type, on=[key1, key2])
            bcol3.write(df_merge)
            tmp_download_link_file_merge = download_link(df_merge, 'file_merge.csv', 'Click here to download your data!')
            tcol3.markdown(tmp_download_link_file_merge, unsafe_allow_html=True)


        tcol4.header('Append DataFrame')

        if tcol4.button('Execute Append'):
            df_append = df1_1.append(df2_1, ignore_index=True, sort=False)
            bcol3.write(df_append)
            tmp_download_link_file_append = download_link(df_append, 'file_append.csv', 'Click here to download your data!')
            tcol4.markdown(tmp_download_link_file_append, unsafe_allow_html=True)


except:
    pass



