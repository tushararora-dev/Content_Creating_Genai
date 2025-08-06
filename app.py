import streamlit as st
import json
import os
from datetime import datetime
import content_generator
from brand_manager import BrandManager
from export_manager import ExportManager

# Main app
st.set_page_config(
    page_title="AI Content Generation Platform",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'content_history' not in st.session_state:
    st.session_state.content_history = []
if 'current_brand_context' not in st.session_state:
    st.session_state.current_brand_context = {}
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

# Initialize managers
@st.cache_resource
def initialize_managers():
    brand_mgr = BrandManager()
    export_mgr = ExportManager()
    return brand_mgr, export_mgr

brand_manager, export_manager = initialize_managers()



st.title("🚀 AI Content Generation Platform")
st.markdown("Generate compelling marketing content using AI-powered open-source LLMs")

# Sidebar for brand context and settings
with st.sidebar:
    st.header("Brand Context")
    
    # Brand profile selection
    brand_profiles = brand_manager.get_brand_profiles()
    if brand_profiles:
        selected_brand = st.selectbox("Select Brand Profile", ["New Brand"] + list(brand_profiles.keys()))
        if selected_brand != "New Brand":
            st.session_state.current_brand_context = brand_profiles[selected_brand]
            st.success(f"Loaded profile: {selected_brand}")
    
    # Brand context form
    with st.form("brand_context_form"):
        st.subheader("Brand Information")
        brand_name = st.text_input("Brand Name", value=st.session_state.current_brand_context.get("brand_name", ""))
        target_audience = st.text_input("Target Audience", value=st.session_state.current_brand_context.get("target_audience", ""))
        brand_tone = st.selectbox("Brand Tone", 
                                 ["Professional", "Casual", "Humorous", "Urgent", "Friendly", "Authoritative", "Gen Z Slang"], 
                                 index=["Professional", "Casual", "Humorous", "Urgent", "Friendly", "Authoritative", "Gen Z Slang"].index(st.session_state.current_brand_context.get("brand_tone", "Professional")))
        industry = st.text_input("Industry", value=st.session_state.current_brand_context.get("industry", ""))
        key_values = st.text_area("Key Brand Values", value=st.session_state.current_brand_context.get("key_values", ""))
        
        save_profile = st.form_submit_button("Save Brand Profile")
        
        if save_profile and brand_name:
            brand_context = {
                "brand_name": brand_name,
                "target_audience": target_audience,
                "brand_tone": brand_tone,
                "industry": industry,
                "key_values": key_values
            }
            brand_manager.save_brand_profile(brand_name, brand_context)
            st.session_state.current_brand_context = brand_context
            st.success("Brand profile saved!")
            st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Content Generation")
    
    # Main prompt input
    user_prompt = st.text_area("Enter your content prompt", 
                              placeholder="e.g., Launch a matcha drink for Gen Z audience",
                              height=100)
    
    # Content type selection
    content_types = st.multiselect(
        "Select content types to generate",
        ["Ad Copy", "Social Media Captions", "Email Creative Blocks", "Video Scripts", "Image Prompts"],
        default=["Ad Copy", "Social Media Captions"]
    )
    
    # Platform selection for social media
    if "Social Media Captions" in content_types:
        platforms = st.multiselect(
            "Select social media platforms",
            ["Instagram", "TikTok", "Facebook", "Twitter", "LinkedIn"],
            default=["Instagram", "TikTok"]
        )
    else:
        platforms = []
    
    # Number of variations
    num_variations = st.slider("Number of variations per content type", 1, 5, 3)
    
    # Generate button
    if st.button("Generate Content", type="primary"):
        if user_prompt and content_types:
            with st.spinner("Generating content..."):
                try:
                    generated = content_generator.generate_content(
                        prompt=user_prompt,
                        content_types=content_types,
                        platforms=platforms,
                        brand_context=st.session_state.current_brand_context,
                        num_variations=num_variations
                    )
                    st.session_state.generated_content = generated
                    st.session_state.content_history.append({
                        "timestamp": datetime.now().isoformat(),
                        "prompt": user_prompt,
                        "content_types": content_types,
                        "platforms": platforms,
                        "content": generated
                    })
                    st.success("Content generated successfully!")
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
        else:
            st.error("Please enter a prompt and select at least one content type.")

with col2:
    st.header("Generated Content")
    
    if st.session_state.generated_content:
        # Display generated content
        for content_type, variations in st.session_state.generated_content.items():
            st.subheader(f"📝 {content_type}")
            
            for i, variation in enumerate(variations, 1):
                with st.expander(f"Variation {i}"):
                    if isinstance(variation, dict):
                        for key, value in variation.items():
                            st.write(f"**{key.title()}:** {value}")
                    else:
                        st.write(variation)
                    
                    # Edit button for each variation
                    col_edit1, col_edit2 = st.columns(2)
                    with col_edit1:
                        edit_instruction = st.text_input(f"Edit instruction for {content_type} Var {i}", 
                                                       placeholder="e.g., Make it funnier")
                    with col_edit2:
                        if st.button(f"Edit", key=f"edit_{content_type}_{i}"):
                            if edit_instruction:
                                with st.spinner("Editing content..."):
                                    try:
                                        edited = content_generator.edit_content(
                                            original_content=variation,
                                            edit_instruction=edit_instruction,
                                            content_type=content_type,
                                            brand_context=st.session_state.current_brand_context
                                        )
                                        # Replace the variation with edited content
                                        st.session_state.generated_content[content_type][i-1] = edited
                                        st.success("Content edited!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error editing content: {str(e)}")
        
        # Export section
        st.subheader("📦 Export Content")
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            if st.button("Export as JSON"):
                json_data = export_manager.export_as_json(st.session_state.generated_content)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"content_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col_exp2:
            if st.button("Export as Text"):
                text_data = export_manager.export_as_text(st.session_state.generated_content)
                st.download_button(
                    label="Download Text",
                    data=text_data,
                    file_name=f"content_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col_exp3:
            if st.button("Export as ZIP"):
                zip_data = export_manager.export_as_zip(st.session_state.generated_content)
                st.download_button(
                    label="Download ZIP",
                    data=zip_data,
                    file_name=f"content_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip"
                )

# Content history section
if st.session_state.content_history:
    st.header("📚 Content History")
    with st.expander("View Previous Generations"):
        for i, item in enumerate(reversed(st.session_state.content_history[-10:]), 1):  # Show last 10
            st.write(f"**{i}.** {item['timestamp'][:19]} - {item['prompt'][:50]}...")
            if st.button(f"Restore", key=f"restore_{len(st.session_state.content_history)-i}"):
                st.session_state.generated_content = item['content']
                st.rerun()

# Footer
st.markdown("---")
st.markdown("Powered by Groq API with Llama 3 8B (8192 context)")
