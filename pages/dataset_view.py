


import streamlit as st

from filter_dataframe import filter_dataframe

def dataset_view_page():
    st.write("## 📊 Dataset View")
    
    # Check if there are any uploads
    if 'uploads' not in st.session_state or not st.session_state['uploads']:
        st.warning('Please upload a player file first.')
        return
    
    # Check if an active upload is selected
    if 'active_upload_idx' not in st.session_state or st.session_state['active_upload_idx'] is None:
        st.warning('Please select an active upload first.')
        return
    
    # Get active upload
    active_idx = st.session_state['active_upload_idx']
    upload = st.session_state['uploads'][active_idx]
    player_dataset = upload.player_dataset
    
    if player_dataset is None or player_dataset.is_empty():
        st.warning('No data available in selected upload.')
        return
    
    # Display upload info
    if upload.user_tag:
        tag_info = ""
        if upload.user_tag:
            parts = []
            if upload.user_tag.season:
                parts.append(upload.user_tag.season)
            if upload.user_tag.in_game_date:
                parts.append(upload.user_tag.in_game_date)
            if upload.user_tag.save_name:
                parts.append(upload.user_tag.save_name)
            tag_info = " | ".join(parts) if parts else "No metadata"
        else:
            tag_info = "No metadata"
    
    st.write(f"**Active Upload:** `{upload.file_name}` {tag_info}")
    
    # Get dataframe
    df = player_dataset.get_dataframe()
    if df is None:
        st.warning('Unable to retrieve dataframe.')
        return
    
    filtered_df = filter_dataframe(df)
    st.dataframe(filtered_df)