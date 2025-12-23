import streamlit as st

from models.player_dataset import PlayerDataset
from models.upload import Upload, UploadTag

def player_upload_page():
    
    # Initialize uploads list in session state
    if 'uploads' not in st.session_state:
        st.session_state['uploads'] = []
    
    # Initialize active upload index (selecting which upload to use in other pages)
    if 'active_upload_idx' not in st.session_state:
        st.session_state['active_upload_idx'] = None

    st.write('## 📤 Player Upload')
    
    # Upload new file section
    st.write("#### Upload New File")
    
    with st.form("upload_form"):
        _player_file = st.file_uploader(
            label='Upload players `.html` file', type='html',
            help='Export file in Football Manager > Scouting > Players > Players in Range'
        )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            season = st.text_input("Season", placeholder="2025/26")
        with col2:
            in_game_date = st.text_input("In-game Date", placeholder="2026-01-01")
        with col3:
            save_name = st.text_input("Save Name", placeholder="My FM Career")
        with col4:
            min_minutes_filter = st.number_input(
                "Min Minutes Filter", min_value=0, value=450,
                help="Minimum minutes played to include player in dataset"
            )
        
        submitted = st.form_submit_button("Process Upload")
        
        if submitted and _player_file:
            try:
                # Create user tag if any metadata provided
                user_tag = None
                if season or in_game_date or save_name:
                    user_tag = UploadTag(
                        season=season if season else None,
                        in_game_date=in_game_date if in_game_date else None,
                        save_name=save_name if save_name else None
                    )
                
                # Create upload record
                upload = Upload(_player_file, user_tag=user_tag)
                
                # Process dataframe
                player_dataset = PlayerDataset()
                player_dataset.init_dataset(upload.uploaded_file, min_minutes=min_minutes_filter)
                
                # Store both together
                upload.player_dataset = player_dataset
                st.session_state['uploads'].append(upload)
                st.session_state['active_upload_idx'] = len(st.session_state['uploads']) - 1
                
                st.success(f"Successfully uploaded and processed {upload.file_name}")
                st.rerun()
                
            except Exception as e:
                st.error(f'Error processing player file: {e}')

    # Display existing uploads
    if st.session_state['uploads']:
        st.write("#### Select Active Upload")
        
        # Build radio options
        options = []
        for idx, upload in enumerate(st.session_state['uploads']):
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
            
            options.append(f"`{upload.file_name}` {tag_info}")
        
        selected = st.radio(
            label="Active upload",
            options=range(len(options)),
            format_func=lambda i: options[i],
            index=st.session_state['active_upload_idx'] if st.session_state['active_upload_idx'] is not None else 0,
            label_visibility="collapsed"
        )
        
        st.session_state['active_upload_idx'] = selected

    # Display active upload details
    if st.session_state['active_upload_idx'] is not None:
        active_idx = st.session_state['active_upload_idx']
        if active_idx < len(st.session_state['uploads']):
            upload = st.session_state['uploads'][active_idx]
            player_dataset = upload.player_dataset
            
            df_shape = player_dataset.get_shape()
            
            st.write("#### Active Upload Details")
            st.write('Number of players:', df_shape[0])
            st.write('Number of columns:', df_shape[1])
            st.write('###### Raw Dataframe')
            st.write(player_dataset.get_raw_dataframe().head())
            st.write('###### Processed Dataframe')
            st.write(player_dataset.get_dataframe().head())
