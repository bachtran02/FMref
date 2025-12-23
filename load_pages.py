import streamlit as st

# from pages.player_compare import player_compare_page
# from pages.player_search import player_search_by_percentile_page
# from pages.player_stats import player_statistics_page
from pages.player_upload import player_upload_page
from pages.dataset_view import dataset_view_page

pages = {
    '': [
        st.Page(player_upload_page, title='Player Upload', icon='📤'),
        st.Page(dataset_view_page, title='Dataset View', icon='📊'),
        # st.Page(player_statistics_page, title='Player Statistics', icon='⚽'),
        # st.Page(player_compare_page, title='Player Comparison', icon='⚽'),
        # st.Page(player_search_by_percentile_page, title='Player Search', icon='⚽'),
    ], 
}