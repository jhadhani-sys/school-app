import os
from kivy.app import App

class StorageHelper:
    """Helper class for cross-platform storage paths"""
    
    @staticmethod
    def get_storage_path(filename=None):
        """Get the appropriate storage path for the current platform"""
        try:
            # Try to get Android app directory
            from android.storage import app_storage_path
            base_path = app_storage_path()
        except ImportError:
            # Fallback to app's user_data_dir or local directory
            try:
                base_path = App.get_running_app().user_data_dir
            except:
                base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        if filename:
            return os.path.join(base_path, filename)
        return base_path
    
    @staticmethod
    def ensure_dir(path):
        """Ensure directory exists"""
        dir_path = os.path.dirname(path) if os.path.splitext(path)[1] else path
        os.makedirs(dir_path, exist_ok=True)
        return path

