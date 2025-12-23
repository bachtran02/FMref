import pandas as pd
import streamlit as st

from typing import Optional

from models.player_dataset import PlayerDataset

class UploadTag:
    def __init__(self, season: Optional[str] = None, 
                 in_game_date: Optional[str] = None,
                 save_name: Optional[str] = None):
        self.season = season
        self.in_game_date = in_game_date
        self.save_name = save_name
        # Add more metadata fields as needed
    
    def to_dict(self):
        return {
            "season": self.season,
            "in_game_date": self.in_game_date,
            "save_name": self.save_name
        }

class Upload:
    def __init__(self, uploaded_file, user_tag: Optional[UploadTag] = None):
        """
        Initialize Upload from Streamlit UploadedFile object.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            user_tag: Optional metadata tag for the upload
        """
        self.uploaded_file = uploaded_file
        self.file_name = uploaded_file.name
        self.file_size = uploaded_file.size
        self.user_tag = user_tag
        
        self.timestamp = pd.Timestamp.utcnow()
        self.player_dataset: PlayerDataset = None
    

    def to_dict(self):
        result = {
            "file_name": self.file_name,
            "file_size": self.file_size,
            "upload_timestamp": self.timestamp
        }
        
        if self.user_tag:
            result["user_tag"] = self.user_tag.to_dict()
        
        return result