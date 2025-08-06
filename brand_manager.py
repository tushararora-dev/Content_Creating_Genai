import json
import os
from typing import Dict, Any, List

class BrandManager:
    """Manages brand profiles and context storage."""
    
    def __init__(self, storage_file: str = "brand_profiles.json"):
        self.storage_file = storage_file
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Load brand profiles from storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_profiles(self) -> None:
        """Save brand profiles to storage file."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise Exception(f"Failed to save brand profiles: {str(e)}")
    
    def save_brand_profile(self, brand_name: str, profile_data: Dict[str, Any]) -> None:
        """Save a brand profile."""
        if not brand_name or not isinstance(profile_data, dict):
            raise ValueError("Brand name and profile data are required")
        
        self.profiles[brand_name] = {
            **profile_data,
            "created_at": profile_data.get("created_at", self._get_timestamp()),
            "updated_at": self._get_timestamp()
        }
        self._save_profiles()
    
    def get_brand_profile(self, brand_name: str) -> Dict[str, Any]:
        """Get a specific brand profile."""
        return self.profiles.get(brand_name, {})
    
    def get_brand_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get all brand profiles."""
        return self.profiles.copy()
    
    def delete_brand_profile(self, brand_name: str) -> bool:
        """Delete a brand profile."""
        if brand_name in self.profiles:
            del self.profiles[brand_name]
            self._save_profiles()
            return True
        return False
    
    def update_brand_profile(self, brand_name: str, updates: Dict[str, Any]) -> None:
        """Update an existing brand profile."""
        if brand_name in self.profiles:
            self.profiles[brand_name].update(updates)
            self.profiles[brand_name]["updated_at"] = self._get_timestamp()
            self._save_profiles()
        else:
            raise ValueError(f"Brand profile '{brand_name}' not found")
    
    def search_profiles(self, query: str) -> List[Dict[str, Any]]:
        """Search brand profiles by name, industry, or values."""
        query_lower = query.lower()
        results = []
        
        for name, profile in self.profiles.items():
            if (query_lower in name.lower() or 
                query_lower in profile.get('industry', '').lower() or
                query_lower in profile.get('key_values', '').lower()):
                results.append({"name": name, **profile})
        
        return results
    
    def get_profile_summary(self, brand_name: str) -> str:
        """Get a formatted summary of a brand profile."""
        profile = self.get_brand_profile(brand_name)
        if not profile:
            return f"Brand profile '{brand_name}' not found"
        
        summary_parts = [f"Brand: {brand_name}"]
        
        if profile.get('target_audience'):
            summary_parts.append(f"Audience: {profile['target_audience']}")
        if profile.get('brand_tone'):
            summary_parts.append(f"Tone: {profile['brand_tone']}")
        if profile.get('industry'):
            summary_parts.append(f"Industry: {profile['industry']}")
        if profile.get('key_values'):
            summary_parts.append(f"Values: {profile['key_values']}")
        
        return " | ".join(summary_parts)
    
    def export_profiles(self) -> str:
        """Export all profiles as JSON string."""
        return json.dumps(self.profiles, indent=2, ensure_ascii=False)
    
    def import_profiles(self, profiles_json: str, overwrite: bool = False) -> int:
        """Import profiles from JSON string. Returns number of profiles imported."""
        try:
            imported_profiles = json.loads(profiles_json)
            imported_count = 0
            
            for name, profile in imported_profiles.items():
                if overwrite or name not in self.profiles:
                    self.profiles[name] = profile
                    imported_count += 1
            
            self._save_profiles()
            return imported_count
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as ISO string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def validate_profile(self, profile_data: Dict[str, Any]) -> List[str]:
        """Validate profile data and return list of errors."""
        errors = []
        
        required_fields = ['brand_name']
        for field in required_fields:
            if not profile_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Optional validation rules
        valid_tones = ["Professional", "Casual", "Humorous", "Urgent", "Friendly", "Authoritative", "Gen Z Slang"]
        if profile_data.get('brand_tone') and profile_data['brand_tone'] not in valid_tones:
            errors.append(f"Invalid brand tone. Must be one of: {', '.join(valid_tones)}")
        
        return errors
