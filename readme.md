# 🚀 AI Content Generation Platform

This repository contains a Streamlit web application designed for generating diverse marketing content using AI. It leverages the Groq API with the Llama 3 8B model to produce high-quality, brand-aligned content quickly and efficiently.

## ✨ Features

*   **Multi-Format Generation**: Create various types of content including:
    *   Ad Copy (Headlines, Subtext, CTAs)
    *   Social Media Captions (Instagram, TikTok, Facebook, etc.)
    *   Email Creative Blocks (Subject lines, Headers, Body)
    *   Short-form Video Scripts (UGC-style)
    *   AI Image Generation Prompts
*   **Brand Profile Management**: Save and load distinct brand profiles, ensuring all generated content aligns with your brand's name, target audience, tone, industry, and key values.
*   **AI-Powered Editing**: Refine generated content with natural language instructions.
*   **Content Variations**: Generate multiple unique variations for any content type to A/B test or choose the best fit.
*   **Versatile Export Options**: Export your generated content as a single JSON file, a formatted text file, or a structured ZIP archive with individual files for easy integration into your workflow.
*   **Generation History**: Keep track of previous generations and restore them with a single click.
*   **User-Friendly Interface**: A clean and intuitive UI built with Streamlit, organized into content generation, results, and brand context panels.

## 🏛️ Project Structure

The application is modularized to separate concerns, making it easy to maintain and extend.

| File/Directory              | Description                                                                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `app.py`                    | The main Streamlit application file. It handles the user interface, session state, and orchestrates other modules.                               |
| `content_generator.py`      | Contains the core logic for generating and editing content by making API calls to the Groq LLM via LangChain. |
| `brand_manager.py`          | A class-based module to manage CRUD operations for brand profiles, which are stored in `brand_profiles.json`.  |
| `export_manager.py`         | Manages the logic for exporting generated content into various formats like JSON, TXT, and ZIP.                |
| `prompt_templates.py`       | A centralized file that stores and provides all the detailed prompt templates for different content types.    |
| `brand_profiles.json`       | A JSON file that serves as a simple database for storing saved brand profiles.                                |
| `.streamlit/config.toml`  | Configuration file for the Streamlit server settings.                                                       |

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

*   Python 3.8+
*   A Groq API key. You can get one from the [GroqCloud Console](https://console.groq.com/keys).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tushararora-dev/content_creating_genai.git
    cd content_creating_genai
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install streamlit langchain-groq python-dotenv
    ```

3.  **Set up environment variables:**
    Create a file named `.env` in the root directory of the project and add your Groq API key:
    ```
    GROQ_API_KEY="your-groq-api-key-here"
    ```

### Running the Application

Launch the Streamlit app with the following command:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## 💻 How to Use

1.  **Set Brand Context (Sidebar):**
    *   Select an existing brand profile from the dropdown or create a new one.
    *   Fill in the "Brand Information" form with your brand's name, target audience, tone, industry, and key values.
    *   Click "Save Brand Profile" to save the context for future use.

2.  **Generate Content (Main Area):**
    *   In the "Content Generation" section, enter a prompt describing your product, campaign, or idea (e.g., "Launch a new line of sustainable activewear").
    *   Select the types of content you want to generate (e.g., "Ad Copy", "Social Media Captions").
    *   If you choose "Social Media Captions", select the specific platforms.
    *   Adjust the slider to set the number of variations for each content type.
    *   Click "Generate Content".

3.  **Review and Edit Content:**
    *   The generated content will appear in the "Generated Content" section on the right.
    *   Expand each variation to view the details.
    *   To make changes, enter an instruction in the text box (e.g., "Make the tone more professional") and click "Edit".

4.  **Export Content:**
    *   Once you are satisfied with the content, use the "Export Content" buttons to download it as a JSON, TXT, or ZIP file.

5.  **Restore History:**
    *   Use the "Content History" expander at the bottom to view and restore previous generation results.