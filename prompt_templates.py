def get_prompt_templates():
    """Get all prompt templates as a dictionary."""
    return {
        "ad_copy": """You are a professional copywriter creating compelling ad copy. Generate advertising copy based on the following context and product information.

{brand_context}

Product/Campaign: {product_prompt}

Create compelling ad copy with the following structure:
Headline: [Create an attention-grabbing headline that hooks the audience]
Subtext: [Write persuasive subtext that explains the value proposition]
CTA: [Create a strong call-to-action button text]

Make sure the copy is engaging, benefit-focused, and matches the specified brand tone. Keep headlines under 60 characters and subtext under 150 characters.""",

        "social_caption": """You are a social media expert creating engaging captions for {platform}. Generate a caption based on the following context and product information.

{brand_context}

Product/Campaign: {product_prompt}

Create an engaging {platform} caption that includes:
- Hook that grabs attention in the first line
- Compelling product description
- Relevant hashtags (5-10 hashtags)
- Call-to-action appropriate for {platform}

Match the brand tone and make it platform-appropriate. For Instagram: focus on visual storytelling. For TikTok: use trending language and emojis. For LinkedIn: professional tone.""",

        "email": """You are an email marketing specialist creating email campaign content. Generate email creative blocks based on the following context and product information.

{brand_context}

Product/Campaign: {product_prompt}

Create email content with the following structure:
Subject: [Create a compelling subject line that increases open rates]
Header: [Write an engaging email header/greeting]
Product: [Create persuasive product description with benefits]
CTA: [Create a strong call-to-action button text]

Make sure the content drives engagement and conversions. Keep subject lines under 50 characters and focus on benefits over features.""",

        "video_script": """You are a content creator writing scripts for short-form videos (30-60 seconds). Create a UGC-style video script based on the following context and product information.

{brand_context}

Product/Campaign: {product_prompt}

Create a video script with:
- Strong hook in the first 3 seconds
- Engaging main content that demonstrates value
- Clear call-to-action at the end
- Natural, conversational tone
- Specific visual directions

Format as a natural speaking script that feels authentic and not overly promotional. Include timing suggestions and key visual moments.""",

        "image_prompt": """You are an art director creating prompts for AI image generation tools like DALL-E or Midjourney. Generate detailed image prompts based on the following context and product information.

{brand_context}

Product/Campaign: {product_prompt}

Create 3 different image prompts for:
1. Product hero shot/main visual
2. Lifestyle/context shot showing product in use
3. Abstract/conceptual visual representing the brand values

Each prompt should include:
- Clear description of the main subject
- Style and aesthetic direction
- Color palette suggestions
- Composition and lighting details
- Specific technical parameters for high-quality output

Make prompts detailed enough to generate professional-quality marketing visuals.""",

        "edit": """You are a professional editor improving marketing content. Edit the following content based on the specific instruction provided.

{brand_context}

Original Content ({content_type}):
{original_content}

Edit Instruction: {edit_instruction}

Provide the improved version maintaining the same format and structure as the original. Make sure the edit follows the instruction while keeping the content effective and on-brand."""
    }
