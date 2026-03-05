# 🐾 Pune Comicon 2026 Meme Automation

Automated pipeline for generating and publishing high-quality, Pune-centric posters and memes for **Pune Comicon 2026**.

## 🚀 Overview

This project uses AI to brainstorm funny, culturally relevant concepts, generate cinematic images, and format them with professional-grade typography and branding.

### 🛠️ Tech Stack
- **Brainstorming:** Google Gemini (Gemma 3 1B)
- **Imaging:** Stable Diffusion XL (via Hugging Face)
- **Editing:** Python Pillow (PIL)
- **Typography:** Bebas Neue (Auto-downloaded from Google Fonts)
- **Publishing:** Instagrapi (Instagram) / Meta Graph API

## 📂 Project Structure
- `main.py`: Orchestrates the flow.
- `src/brainstormer.py`: Generates themes, prompts, and captions.
- `src/generator.py`: Fetches AI-generated images.
- `src/editor.py`: Handles text wrapping, branding, and logo overlays.
- `src/publisher.py`: Handles Instagram uploads.
- `assets/logos/`: Place your sponsorship/event logos here.

## 🛠️ Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Edit `.env` and add your API keys:
   - `GEMINI_API_KEY`: Get from Google AI Studio.
   - `HF_TOKEN`: Get from Hugging Face.
   - `IG_USER` & `IG_PASS`: Your Instagram credentials.

3. **Run a Test:**
   ```bash
   python3 test_flow.py "Anime x Harry Potter"
   ```

## 🎯 Project Goals & Logic

### Base Prompt Logic
The automation follows a specific "Base Thinking" to ensure brand consistency for **Pune Comicon 2026**. It supports two distinct styles:

- **Posters:** Focus on epic, vibrant visuals with fixed branding text.
  - **Top Text:** Always "Pune Comicon 2026".
  - **Bottom Text:** "Experience the magic of [theme] at Pune Comicon! March 21-22, Pune!".
- **Memes:** Focus on funny, relatable visuals (e.g., characters stuck in Pune traffic) with AI-generated funny captions.

- **Themes:** Gaming, Anime, Harry Potter, Pokemon, etc.
- **Mandatory Branding:** Every image includes a "PUNE COMICON 2026" watermark at the bottom.
- **Visual Style:** 
    - **Gaming:** Popular icons/controllers with Pune landmarks backdrop.
    - **Anime/Pokemon:** Vibrant characters integrated with local Pune elements.
    - **Harry Potter:** Magical visuals mashed up with Pune’s skyline.

## 🎯 Future Plan (TODO)

- [ ] **Google Drive Integration:** Automate image backup to a specific shared folder.
  - *Instruction:* Use a Service Account JSON key. Shared the target folder with the service account email. Implement `src/uploader.py` using `google-api-python-client`.
- [ ] **Multi-Logo Support:** Dynamically place multiple sponsor logos in the footer.
- [ ] **Schedule Posting:** Integrate a cron job to post memes at peak engagement times.
- [ ] **Community Suggestions:** Hook into a Discord or Telegram bot to take theme suggestions from fans.

---
Created by **Clawe 🐾** for **Destiny**.
