import json
import zipfile
import io
from typing import Dict, Any
from datetime import datetime

class ExportManager:
    """Manages content export in various formats."""
    
    def export_as_json(self, content: Dict[str, Any]) -> str:
        """Export content as JSON string."""
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "content": content,
            "metadata": {
                "total_content_types": len(content),
                "total_variations": sum(len(variations) for variations in content.values())
            }
        }
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def export_as_text(self, content: Dict[str, Any]) -> str:
        """Export content as formatted text."""
        text_lines = []
        text_lines.append("CONTENT GENERATION EXPORT")
        text_lines.append("=" * 50)
        text_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        text_lines.append("")
        
        for content_type, variations in content.items():
            text_lines.append(f"\n{content_type.upper()}")
            text_lines.append("-" * len(content_type))
            
            for i, variation in enumerate(variations, 1):
                text_lines.append(f"\nVariation {i}:")
                
                if isinstance(variation, dict):
                    for key, value in variation.items():
                        if isinstance(value, list):
                            text_lines.append(f"  {key.title()}:")
                            for item in value:
                                text_lines.append(f"    - {item}")
                        else:
                            text_lines.append(f"  {key.title()}: {value}")
                else:
                    text_lines.append(f"  {variation}")
                
                text_lines.append("")
        
        return "\n".join(text_lines)
    
    def export_as_zip(self, content: Dict[str, Any]) -> bytes:
        """Export content as ZIP file with separate files for each content type."""
        buffer = io.BytesIO()
        
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add main JSON file
            json_content = self.export_as_json(content)
            zip_file.writestr("content_export.json", json_content)
            
            # Add formatted text file
            text_content = self.export_as_text(content)
            zip_file.writestr("content_export.txt", text_content)
            
            # Add individual files for each content type
            for content_type, variations in content.items():
                folder_name = content_type.lower().replace(" ", "_")
                
                for i, variation in enumerate(variations, 1):
                    filename = f"{folder_name}/variation_{i}.txt"
                    
                    if isinstance(variation, dict):
                        # Format structured content
                        content_text = []
                        for key, value in variation.items():
                            if isinstance(value, list):
                                content_text.append(f"{key.title()}:")
                                for item in value:
                                    content_text.append(f"- {item}")
                            else:
                                content_text.append(f"{key.title()}: {value}")
                        file_content = "\n".join(content_text)
                    else:
                        file_content = str(variation)
                    
                    zip_file.writestr(filename, file_content)
                
                # Add JSON file for structured data
                json_filename = f"{folder_name}/data.json"
                json_data = {
                    "content_type": content_type,
                    "variations": variations,
                    "count": len(variations)
                }
                zip_file.writestr(json_filename, json.dumps(json_data, indent=2))
            
            # Add README
            readme_content = self._generate_readme(content)
            zip_file.writestr("README.txt", readme_content)
        
        buffer.seek(0)
        return buffer.read()
    
    def _generate_readme(self, content: Dict[str, Any]) -> str:
        """Generate README content for the export."""
        readme_lines = [
            "CONTENT GENERATION EXPORT",
            "=" * 50,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "CONTENTS:",
            "- content_export.json: Complete export in JSON format",
            "- content_export.txt: Formatted text version",
            "- Individual folders for each content type:",
        ]
        
        for content_type in content.keys():
            folder_name = content_type.lower().replace(" ", "_")
            readme_lines.append(f"  - {folder_name}/: {content_type} variations")
        
        readme_lines.extend([
            "",
            "STRUCTURE:",
            "Each content type folder contains:",
            "- variation_X.txt: Individual variation files",
            "- data.json: Structured data for the content type",
            "",
            "USAGE:",
            "Import the JSON files into your marketing tools or",
            "copy text from individual variation files as needed."
        ])
        
        return "\n".join(readme_lines)
    
    def export_for_platform(self, content: Dict[str, Any], platform: str) -> str:
        """Export content formatted for specific platforms."""
        if platform.lower() == "klaviyo":
            return self._export_for_klaviyo(content)
        elif platform.lower() in ["meta", "facebook"]:
            return self._export_for_meta(content)
        elif platform.lower() == "tiktok":
            return self._export_for_tiktok(content)
        else:
            return self.export_as_json(content)
    
    def _export_for_klaviyo(self, content: Dict[str, Any]) -> str:
        """Format content for Klaviyo email campaigns."""
        klaviyo_data = {
            "email_templates": [],
            "export_timestamp": datetime.now().isoformat()
        }
        
        if "Email Creative Blocks" in content:
            for variation in content["Email Creative Blocks"]:
                if isinstance(variation, dict):
                    template = {
                        "subject_line": variation.get("subject_line", ""),
                        "header": variation.get("header", ""),
                        "body": variation.get("product_blurb", ""),
                        "cta_text": variation.get("cta_button", "")
                    }
                    klaviyo_data["email_templates"].append(template)
        
        return json.dumps(klaviyo_data, indent=2)
    
    def _export_for_meta(self, content: Dict[str, Any]) -> str:
        """Format content for Meta/Facebook Ads."""
        meta_data = {
            "ad_sets": [],
            "export_timestamp": datetime.now().isoformat()
        }
        
        if "Ad Copy" in content:
            for variation in content["Ad Copy"]:
                if isinstance(variation, dict):
                    ad_set = {
                        "headline": variation.get("headline", ""),
                        "description": variation.get("subtext", ""),
                        "call_to_action": variation.get("cta", ""),
                        "format": "single_image"
                    }
                    meta_data["ad_sets"].append(ad_set)
        
        return json.dumps(meta_data, indent=2)
    
    def _export_for_tiktok(self, content: Dict[str, Any]) -> str:
        """Format content for TikTok Ads."""
        tiktok_data = {
            "video_ads": [],
            "export_timestamp": datetime.now().isoformat()
        }
        
        if "Video Scripts" in content:
            for variation in content["Video Scripts"]:
                if isinstance(variation, dict):
                    ad = {
                        "script": variation.get("main_content", ""),
                        "hook": variation.get("hook", ""),
                        "cta": variation.get("cta", ""),
                        "duration": variation.get("duration", "30-60 seconds")
                    }
                    tiktok_data["video_ads"].append(ad)
        
        return json.dumps(tiktok_data, indent=2)
