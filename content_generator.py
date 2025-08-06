import os
import json
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from prompt_templates import get_prompt_templates

# Load environment variables
load_dotenv(find_dotenv())

# Global LLM instance
_llm = None

def load_llm(groq_api_key: Optional[str] = None) -> ChatGroq:
    """Load Groq LLM instance."""
    api_key = groq_api_key or os.environ.get("GROQ_API_KEY", "---")
    if not api_key:
        raise ValueError("GROQ_API_KEY is required")
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama3-8b-8192",
        temperature=0.3,
        max_tokens=512
    )

def get_llm():
    """Get or create LLM instance."""
    global _llm
    if _llm is None:
        _llm = load_llm()
    return _llm

def make_api_call(prompt: str, max_retries: int = 3) -> str:
    """Make API call to Groq with retry logic."""
    llm = get_llm()
    for attempt in range(max_retries):
        try:
            message = HumanMessage(content=prompt)
            response = llm.invoke([message])
            if hasattr(response, 'content'):
                return response.content.strip()
            else:
                return str(response).strip()
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Groq API call failed after {max_retries} attempts: {str(e)}")
            time.sleep(2 ** attempt)
    
    raise Exception("Failed to generate content after all retries")
    
def generate_content(
    prompt: str,
    content_types: List[str],
    platforms: Optional[List[str]] = None,
    brand_context: Optional[Dict[str, Any]] = None,
    num_variations: int = 3
) -> Dict[str, List[Any]]:
    """Generate content based on prompt and specifications."""
    results = {}
    
    # Prepare brand context string
    brand_context_str = ""
    if brand_context:
        brand_context_str = format_brand_context(brand_context)
    
    for content_type in content_types:
        results[content_type] = []
        
        for variation in range(num_variations):
            try:
                if content_type == "Ad Copy":
                    content = generate_ad_copy(prompt, brand_context_str)
                elif content_type == "Social Media Captions":
                    content = generate_social_captions(prompt, platforms or ["Instagram"], brand_context_str)
                elif content_type == "Email Creative Blocks":
                    content = generate_email_blocks(prompt, brand_context_str)
                elif content_type == "Video Scripts":
                    content = generate_video_script(prompt, brand_context_str)
                elif content_type == "Image Prompts":
                    content = generate_image_prompts(prompt, brand_context_str)
                else:
                    content = "Content type not supported"
                
                results[content_type].append(content)
                
            except Exception as e:
                results[content_type].append(f"Error generating variation {variation + 1}: {str(e)}")
    
    return results
    
def generate_ad_copy(prompt: str, brand_context: str) -> Dict[str, str]:
    """Generate ad copy with headlines, subtext, and CTAs."""
    templates = get_prompt_templates()
    template = templates["ad_copy"]
    full_prompt = template.format(
        brand_context=brand_context,
        product_prompt=prompt
    )
    
    response = make_api_call(full_prompt)
    
    # Parse response into structured format
    lines = response.split('\n')
    ad_copy = {
        "headline": "",
        "subtext": "",
        "cta": ""
    }
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line.lower().startswith('headline:'):
            current_section = 'headline'
            ad_copy[current_section] = line.replace('Headline:', '').strip()
        elif line.lower().startswith('subtext:'):
            current_section = 'subtext'
            ad_copy[current_section] = line.replace('Subtext:', '').strip()
        elif line.lower().startswith('cta:'):
            current_section = 'cta'
            ad_copy[current_section] = line.replace('CTA:', '').strip()
        elif current_section and line:
            ad_copy[current_section] += " " + line
    
    # Fallback if parsing fails
    if not any(ad_copy.values()):
        parts = response.split('\n\n')
        if len(parts) >= 3:
            ad_copy = {
                "headline": parts[0].strip(),
                "subtext": parts[1].strip(),
                "cta": parts[2].strip()
            }
        else:
            ad_copy = {
                "headline": response[:100] + "...",
                "subtext": "Compelling subtext for your product",
                "cta": "Learn More"
            }
    
    return ad_copy
    
def generate_social_captions(prompt: str, platforms: List[str], brand_context: str) -> Dict[str, str]:
    """Generate social media captions for different platforms."""
    captions = {}
    templates = get_prompt_templates()
    
    for platform in platforms:
        template = templates["social_caption"]
        full_prompt = template.format(
            brand_context=brand_context,
            product_prompt=prompt,
            platform=platform
        )
        
        response = make_api_call(full_prompt)
        captions[platform] = response
    
    return captions
    
def generate_email_blocks(prompt: str, brand_context: str) -> Dict[str, str]:
    """Generate email creative blocks."""
    templates = get_prompt_templates()
    template = templates["email"]
    full_prompt = template.format(
        brand_context=brand_context,
        product_prompt=prompt
    )
    
    response = make_api_call(full_prompt)
    
    # Parse into email components
    email_blocks = {
        "subject_line": "",
        "header": "",
        "product_blurb": "",
        "cta_button": ""
    }
    
    lines = response.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.lower().startswith('subject:'):
            current_section = 'subject_line'
            email_blocks[current_section] = line.replace('Subject:', '').strip()
        elif line.lower().startswith('header:'):
            current_section = 'header'
            email_blocks[current_section] = line.replace('Header:', '').strip()
        elif line.lower().startswith('product:'):
            current_section = 'product_blurb'
            email_blocks[current_section] = line.replace('Product:', '').strip()
        elif line.lower().startswith('cta:'):
            current_section = 'cta_button'
            email_blocks[current_section] = line.replace('CTA:', '').strip()
        elif current_section and line:
            email_blocks[current_section] += " " + line
    
    return email_blocks
    
def generate_video_script(prompt: str, brand_context: str) -> Dict[str, str]:
    """Generate UGC-style video script."""
    templates = get_prompt_templates()
    template = templates["video_script"]
    full_prompt = template.format(
        brand_context=brand_context,
        product_prompt=prompt
    )
    
    response = make_api_call(full_prompt)
    
    # Structure the script
    script = {
        "hook": "",
        "main_content": "",
        "cta": "",
        "duration": "30-60 seconds"
    }
    
    # Try to parse structured response
    sections = response.split('\n\n')
    if len(sections) >= 3:
        script["hook"] = sections[0].strip()
        script["main_content"] = sections[1].strip()
        script["cta"] = sections[2].strip()
    else:
        script["main_content"] = response
    
    return script
    
def generate_image_prompts(prompt: str, brand_context: str) -> List[str]:
    """Generate image prompts for AI art tools."""
    templates = get_prompt_templates()
    template = templates["image_prompt"]
    full_prompt = template.format(
        brand_context=brand_context,
        product_prompt=prompt
    )
    
    response = make_api_call(full_prompt)
    
    # Extract multiple prompts
    prompts = []
    lines = response.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Clean up numbering or bullets
            cleaned = line.lstrip('123456789.-• ').strip()
            if len(cleaned) > 10:  # Valid prompt
                prompts.append(cleaned)
    
    return prompts[:3] if prompts else [response]
    
def edit_content(
    original_content: Any,
    edit_instruction: str,
    content_type: str,
    brand_context: Optional[Dict[str, Any]] = None
) -> Any:
    """Edit existing content based on instruction."""
    brand_context_str = ""
    if brand_context:
        brand_context_str = format_brand_context(brand_context)
    
    templates = get_prompt_templates()
    template = templates["edit"]
    
    # Convert content to string for editing
    if isinstance(original_content, dict):
        content_str = json.dumps(original_content, indent=2)
    else:
        content_str = str(original_content)
    
    full_prompt = template.format(
        brand_context=brand_context_str,
        original_content=content_str,
        edit_instruction=edit_instruction,
        content_type=content_type
    )
    
    response = make_api_call(full_prompt)
    
    # Try to maintain original structure
    if isinstance(original_content, dict):
        try:
            # Try to parse as JSON first
            return json.loads(response)
        except:
            # If JSON parsing fails, try to extract structured data
            if content_type == "Ad Copy":
                return parse_ad_copy_from_text(response)
            elif content_type == "Email Creative Blocks":
                return parse_email_blocks_from_text(response)
            else:
                return {"edited_content": response}
    
    return response

def format_brand_context(brand_context: Dict[str, Any]) -> str:
    """Format brand context into a string for prompts."""
    if not brand_context:
        return ""
    
    context_parts = []
    if brand_context.get('brand_name'):
        context_parts.append(f"Brand: {brand_context['brand_name']}")
    if brand_context.get('target_audience'):
        context_parts.append(f"Target Audience: {brand_context['target_audience']}")
    if brand_context.get('brand_tone'):
        context_parts.append(f"Tone: {brand_context['brand_tone']}")
    if brand_context.get('industry'):
        context_parts.append(f"Industry: {brand_context['industry']}")
    if brand_context.get('key_values'):
        context_parts.append(f"Key Values: {brand_context['key_values']}")
    
    return "\n".join(context_parts)

def parse_ad_copy_from_text(text: str) -> Dict[str, str]:
    """Parse ad copy from unstructured text."""
    ad_copy = {"headline": "", "subtext": "", "cta": ""}
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.lower().startswith('headline:'):
            ad_copy['headline'] = line.replace('Headline:', '').strip()
        elif line.lower().startswith('subtext:'):
            ad_copy['subtext'] = line.replace('Subtext:', '').strip()
        elif line.lower().startswith('cta:'):
            ad_copy['cta'] = line.replace('CTA:', '').strip()
    
    return ad_copy

def parse_email_blocks_from_text(text: str) -> Dict[str, str]:
    """Parse email blocks from unstructured text."""
    email_blocks = {"subject_line": "", "header": "", "product_blurb": "", "cta_button": ""}
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.lower().startswith('subject:'):
            email_blocks['subject_line'] = line.replace('Subject:', '').strip()
        elif line.lower().startswith('header:'):
            email_blocks['header'] = line.replace('Header:', '').strip()
        elif line.lower().startswith('product:'):
            email_blocks['product_blurb'] = line.replace('Product:', '').strip()
        elif line.lower().startswith('cta:'):
            email_blocks['cta_button'] = line.replace('CTA:', '').strip()
    
    return email_blocks
