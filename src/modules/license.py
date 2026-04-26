import hashlib
import json
import uuid
import os
from datetime import datetime

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.helpers import StorageHelper

class LicenseManager:
    """Manages license key generation and validation"""
    
    LICENSE_FILE = None
    DEVICE_ID_FILE = None
    
    @classmethod
    def _get_paths(cls):
        if cls.LICENSE_FILE is None:
            base = StorageHelper.get_storage_path()
            cls.LICENSE_FILE = os.path.join(base, 'data', 'license.json')
            cls.DEVICE_ID_FILE = os.path.join(base, 'data', 'device.id')
            StorageHelper.ensure_dir(cls.LICENSE_FILE)
            StorageHelper.ensure_dir(cls.DEVICE_ID_FILE)
    
    @staticmethod
    def generate_device_id():
        """Generate a unique device ID that works on Android and desktop"""
        LicenseManager._get_paths()
        # Try to read existing device ID first (for persistence)
        if os.path.exists(LicenseManager.DEVICE_ID_FILE):
            try:
                with open(LicenseManager.DEVICE_ID_FILE, 'r') as f:
                    stored_id = f.read().strip()
                    if stored_id:
                        return stored_id
            except Exception:
                pass
        
        # Try to get Android ID via plyer
        device_id = None
        try:
            from plyer import uniqueid
            device_id = uniqueid.id
        except Exception:
            pass
        
        # Fallback to platform info (desktop) or random UUID
        if not device_id:
            try:
                import platform
                system_info = platform.platform() + platform.machine()
                # platform.node() can fail on Android, so avoid it
                device_id = hashlib.sha256(system_info.encode()).hexdigest()[:16].upper()
            except Exception:
                device_id = str(uuid.uuid4()).replace('-', '')[:16].upper()
        
        # Store for persistence
        try:
            os.makedirs(os.path.dirname(LicenseManager.DEVICE_ID_FILE), exist_ok=True)
            with open(LicenseManager.DEVICE_ID_FILE, 'w') as f:
                f.write(device_id)
        except Exception:
            pass
        
        return device_id
    
    @staticmethod
    def generate_license_key(device_id):
        """Generate a license key for a specific device"""
        device_hash = hashlib.sha256(device_id.encode()).hexdigest()
        license_key = device_hash[:32].upper()
        license_key = f"{license_key[0:8]}-{license_key[8:16]}-{license_key[16:24]}-{license_key[24:32]}"
        return license_key
    
    @staticmethod
    def validate_license(license_key, device_id):
        """Validate if a license key matches the device ID"""
        expected_key = LicenseManager.generate_license_key(device_id)
        return license_key.upper() == expected_key
    
    @staticmethod
    def save_license(device_id, license_key):
        """Save license information to file"""
        LicenseManager._get_paths()
        os.makedirs(os.path.dirname(LicenseManager.LICENSE_FILE), exist_ok=True)
        
        license_data = {
            'device_id': device_id,
            'license_key': license_key,
            'activated_at': datetime.now().isoformat(),
            'activated': True
        }
        
        try:
            with open(LicenseManager.LICENSE_FILE, 'w') as f:
                json.dump(license_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving license: {e}")
            return False
    
    @staticmethod
    def load_license():
        """Load license information from file"""
        LicenseManager._get_paths()
        if not os.path.exists(LicenseManager.LICENSE_FILE):
            return None
        
        try:
            with open(LicenseManager.LICENSE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading license: {e}")
            return None
    
    @staticmethod
    def is_licensed():
        """Check if the application is licensed"""
        license_data = LicenseManager.load_license()
        if not license_data:
            return False
        
        device_id = LicenseManager.generate_device_id()
        license_key = license_data.get('license_key')
        
        return LicenseManager.validate_license(license_key, device_id)
    
    @staticmethod
    def activate_license(license_key):
        """Activate license on this device"""
        device_id = LicenseManager.generate_device_id()
        
        if not LicenseManager.validate_license(license_key, device_id):
            return False, "Invalid license key for this device"
        
        if LicenseManager.save_license(device_id, license_key):
            return True, "License activated successfully"
        else:
            return False, "Failed to save license"

