# Placement Automator: AI-Powered Placement Prep Tool

## 🎯 Overview

This Streamlit application streamlines the campus placement preparation process by automating key tasks:

1.  **Email Content Extraction & Analysis**: Automatically parses company details and role information from placement-related emails.
2.  **AI-Powered Company Research**: Leverages Google Gemini AI to conduct in-depth research on companies, providing crucial insights for interview preparation.
3.  **Professional Video Generation**: Creates engaging, short-form video content (e.g., YouTube Shorts) based on the researched company information, ideal for quick overviews and student dissemination.
4.  **Seamless Sharing**: Facilitates easy sharing of generated company information via WhatsApp.

## ✨ Features

-   **Intelligent Email Parsing**: Extracts company name, role, and key details from raw email text.
-   **Comprehensive Company Profiles**: Generates structured information including official website, social media links (LinkedIn, Facebook, X, Instagram), company overview, size, headquarters, and founding year.
-   **Interview Preparation Resources**: Provides direct links to company-specific interview experiences (GeeksForGeeks, Glassdoor) and role-specific technical preparation topics (DSA, System Design, Behavioral).
-   **Dynamic Video Scripting**: Utilizes AI to create concise, high-energy video scripts tailored for short-form content.
-   **Advanced Video Production**: Generates professional-grade videos with custom templates, voice-overs, and visual effects, optimized for mobile viewing.
-   **WhatsApp Integration**: Offers options to share generated information directly via WhatsApp Web links or automated messages.

## 🚀 Setup Guide

Follow these steps to get the application up and running on your local machine.

### 1. Prerequisites

Ensure you have Python 3.8+ installed.

### 2. Installation

Open your terminal and execute the following commands:

```bash
pip install streamlit google-generativeai pywhatkit moviepy==1.0.3 pillow gtts matplotlib requests python-dotenv pydub
```

### 3. Environment Variables

Create a file named `.env` in the root directory of the project (same directory as `main.py`) and add your API keys and phone number:

```dotenv
GEMINI_API_KEY="your_google_gemini_api_key_here"
WHATSAPP_PHONE="+91xxxxxxxxxx" # Your WhatsApp number with country code
```

-   **`GEMINI_API_KEY`**: Obtain this from the [Google AI Studio](https://aistudio.google.com/).
-   **`WHATSAPP_PHONE`**: Your phone number, including the country code (e.g., `+911234567890`).

## 🏃‍♀️ Usage

1.  **Run the Application**:
    Navigate to the project root directory in your terminal and run:
    ```bash
    streamlit run main.py
    ```
    This will open the application in your web browser.

2.  **Paste Email Content**:
    In the Streamlit UI, paste the full content of a company's placement email into the designated text area.

3.  **Generate Company Information**:
    Click the **"Generate Company Information"** button. The AI will process the email and provide a detailed company profile and interview preparation guide.

4.  **Generate Video (Optional)**:
    If you wish to create a video, first click **"Generate Video Script"** to get a draft script. You can review and edit this script. Then, click **"Create Professional Video"** to generate the final video. The video will be displayed in the app and you'll have options to download it.

5.  **Share & Download**:
    Utilize the **"Share via WhatsApp"** option to send the generated company information to relevant contacts or download the text files directly.

## 🛠️ Project Structure (Key Components)

-   **`main.py`**: The main Streamlit application file containing UI logic, AI model interactions, and video generation functions.
-   **`VideoConfig` (dataclass)**: Defines professional video output settings (resolution, FPS, codecs).
-   **`AdvancedVideoGenerator` (class)**: Handles the core logic for creating high-quality, visually appealing video slides, including text rendering, image effects, and audio synchronization.
-   **`extract_company_logo`**: Fetches company logos from Clearbit API or generates fallback initial logos.
-   **`enhanced_text_to_speech`**: Converts text to speech with speed control.
-   **`generate_comprehensive_prompt`**: Crafts detailed prompts for the Gemini AI to extract and research company information.
-   **`generate_shorts_script`**: Generates video scripts optimized for YouTube Shorts format.
-   **`create_professional_placement_video`**: Orchestrates the entire video creation process, assembling individual slide clips into a final video.
-   **`generate_whatsapp_web_link`**: Creates WhatsApp shareable links.

this is how the expected output of the whatsapp message must/will look like:
```
ORGANIZATION: Apple

ORGANIZATION DETAILS:
1. Base Site: https://www.apple.com/
2. LinkedIn: https://www.linkedin.com/company/apple
3. Facebook: Search manually for Apple Facebook page
4. X (Twitter): Search manually for Apple Twitter page
5. Instagram: Search manually for Apple Instagram page
6. Role/s Offered: Software Development Engineering Intern
7. Company Overview: April 1, 1976 (49 years ago) (1976-04-01), in Los Altos, California, U.S.. Founders. Steve Jobs · Steve Wozniak · Ronald Wayne. Headquarters, 1 Apple Park Way,.
8. Company Size: Research required
9. Headquarters: Research required
10. Founded: Research required

INTERVIEW REFERENCES:
1. Interview Experiences: https://www.glassdoor.com/Interview/Apple-Software-Development-Engineer-Interview-Questions-EI_IE1138.0,5_KO6,35.htm
2. Additional Interview Resources: https://www.reddit.com/r/dataanalysis/comments/1dh44yc/i_scraped_all_data_analysis_interview_questions/

ROLE-SPECIFIC PREPARATION:
To get started with the preparation for Software Development Engineering Intern, you can refer to the following resources:

1. Technical Preparation: https://www.quora.com/Preparing-for-Software-Engineer-internship-interview-what-topics-should-I-study-What-should-I-expect
2. Data Structures and Algorithms: https://www.geeksforgeeks.org/data-structures/
3. System Design: https://www.geeksforgeeks.org/system-design-tutorial/
4. Behavioral Interviews: https://www.geeksforgeeks.org/behavioral-interview-questions/

INTERVIEW HIGHLIGHTS (General Preparation):
1. Interview Preparation Resources:
- https://www.geeksforgeeks.org/company-preparation/
- https://leetcode.com/
- https://www.glassdoor.co.in/
- https://www.ambitionbox.com/

ADDITIONAL RESOURCES:
- GeeksForGeeks: https://www.geeksforgeeks.org/
- LeetCode: https://leetcode.com/
- AmbitionBox: https://www.ambitionbox.com/
- Glassdoor: https://www.glassdoor.co.in/

COMPANY CULTURE & VALUES:
Research the company's official website and LinkedIn page for detailed information about their culture, values, and work environment.

Best Regards,
Professor Animesh Giri
LinkedIn: https://www.linkedin.com/in/animesh-giri-15272531/
Youtube: https://www.youtube.com/channel/UCBFH7hssUsyipttqLxHU-cw
```

Enjoy automating yOUR placement!
