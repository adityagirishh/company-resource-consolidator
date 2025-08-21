import os
import urllib.parse
import webbrowser
import requests
import json
import time
import re
from typing import Optional, Dict, List
from dotenv import load_dotenv

class EnhancedCompanyResearchBot:
    def __init__(self, gemini_api_key: str, csr_api_key: str, cse_id: str, phone_number: str):
        """Initialize the bot with API keys and phone number."""
        self.gemini_api_key = gemini_api_key
        self.csr_api_key = csr_api_key
        self.cse_id = cse_id
        self.phone_number = phone_number
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        
        # Pre-populate known company data
        self.company_database = self.load_company_database()
        
    def load_company_database(self) -> Dict:
        """Load pre-verified company data for major companies."""
        return {
            "apple": {
                "website": "https://www.apple.com/",
                "linkedin": "https://www.linkedin.com/company/apple/",
                "facebook": "https://www.facebook.com/Apple/",
                "twitter": "https://twitter.com/Apple",
                "instagram": "https://www.instagram.com/apple/",
                "headquarters": "Cupertino, California, USA",
                "founded": "1976",
                "size": "164,000+ employees",
                "overview": "Technology company specializing in consumer electronics, software, and online services"
            },
            "google": {
                "website": "https://www.google.com/",
                "linkedin": "https://www.linkedin.com/company/google/",
                "facebook": "https://www.facebook.com/Google/",
                "twitter": "https://twitter.com/Google",
                "instagram": "https://www.instagram.com/google/",
                "headquarters": "Mountain View, California, USA",
                "founded": "1998",
                "size": "156,000+ employees",
                "overview": "Technology company specializing in Internet-related services and products"
            },
            "microsoft": {
                "website": "https://www.microsoft.com/",
                "linkedin": "https://www.linkedin.com/company/microsoft/",
                "facebook": "https://www.facebook.com/Microsoft/",
                "twitter": "https://twitter.com/Microsoft",
                "instagram": "https://www.instagram.com/microsoft/",
                "headquarters": "Redmond, Washington, USA",
                "founded": "1975",
                "size": "221,000+ employees",
                "overview": "Technology corporation producing computer software, consumer electronics, and related services"
            },
            "amazon": {
                "website": "https://www.amazon.com/",
                "linkedin": "https://www.linkedin.com/company/amazon/",
                "facebook": "https://www.facebook.com/Amazon/",
                "twitter": "https://twitter.com/amazon",
                "instagram": "https://www.instagram.com/amazon/",
                "headquarters": "Seattle, Washington, USA",
                "founded": "1994",
                "size": "1,500,000+ employees",
                "overview": "E-commerce and cloud computing company"
            }
        }

    def validate_url(self, url: str) -> bool:
        """Check if URL is accessible and working."""
        if not url or url in ["Not found", "Not available"]:
            return False
            
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code in [200, 301, 302]
        except:
            return False

    def search_web_with_validation(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search the web and validate results."""
        try:
            params = {
                'key': self.csr_api_key,
                'cx': self.cse_id,
                'q': query,
                'num': num_results
            }
            
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            
            results = response.json()
            validated_results = []
            
            if 'items' in results:
                for item in results['items']:
                    link = item.get('link', '')
                    if self.validate_url(link):
                        validated_results.append({
                            'title': item.get('title', ''),
                            'link': link,
                            'snippet': item.get('snippet', '')
                        })
            
            return validated_results
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching web: {e}")
            return []

    def find_social_media_links(self, company_name: str) -> Dict:
        """Find and validate social media links for a company."""
        social_links = {
            'facebook': 'Not available',
            'twitter': 'Not available', 
            'instagram': 'Not available'
        }
        
        # Check pre-populated database first
        company_key = company_name.lower().replace(' ', '').replace('.', '').replace(',', '')
        if company_key in self.company_database:
            db_data = self.company_database[company_key]
            for platform in social_links.keys():
                if platform in db_data and self.validate_url(db_data[platform]):
                    social_links[platform] = db_data[platform]
            return social_links
        
        # Search for social media presence
        search_patterns = {
            'facebook': f'site:facebook.com "{company_name}" official',
            'twitter': f'site:twitter.com "{company_name}" verified',
            'instagram': f'site:instagram.com "{company_name}" official'
        }
        
        for platform, query in search_patterns.items():
            print(f"Searching for {company_name} {platform} page...")
            results = self.search_web_with_validation(query, 3)
            
            # Find the most relevant result
            for result in results:
                link = result['link']
                if self.is_valid_company_social_page(link, company_name, platform):
                    social_links[platform] = link
                    break
            
            time.sleep(1)  # Rate limiting
        
        return social_links

    def is_valid_company_social_page(self, url: str, company_name: str, platform: str) -> bool:
        """Validate if a social media URL is the official company page."""
        if not url:
            return False
            
        # Basic URL structure validation
        platform_domains = {
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'instagram': 'instagram.com'
        }
        
        if platform_domains[platform] not in url:
            return False
        
        # Check if company name appears in URL or if it's a verified/official looking URL
        company_clean = company_name.lower().replace(' ', '').replace('.', '')
        url_clean = url.lower()
        
        # Look for company name in URL path
        if company_clean in url_clean:
            return True
            
        # For well-known companies, accept certain patterns
        known_patterns = {
            'apple': ['apple', 'appleofficial'],
            'google': ['google', 'googleofficial'],
            'microsoft': ['microsoft', 'microsoftofficial'],
            'amazon': ['amazon', 'amazonofficial']
        }
        
        if company_clean in known_patterns:
            for pattern in known_patterns[company_clean]:
                if pattern in url_clean:
                    return True
        
        return False

    def research_company_comprehensive(self, company_name: str) -> Dict:
        """Comprehensive company research with multiple sources."""
        print(f"Researching {company_name} comprehensively...")
        
        # Check database first
        company_key = company_name.lower().replace(' ', '').replace('.', '').replace(',', '')
        if company_key in self.company_database:
            print(f"Found {company_name} in database!")
            db_data = self.company_database[company_key]
            
            # Validate database URLs
            validated_data = {}
            for key, value in db_data.items():
                if key in ['website', 'linkedin', 'facebook', 'twitter', 'instagram']:
                    if self.validate_url(value):
                        validated_data[key] = value
                    else:
                        validated_data[key] = 'Not available'
                else:
                    validated_data[key] = value
            
            return validated_data
        
        # If not in database, search for information
        print(f"{company_name} not in database, searching...")
        
        # Search for official website
        website_results = self.search_web_with_validation(f'"{company_name}" official website')
        website = website_results[0]['link'] if website_results else 'Not available'
        
        time.sleep(1)
        
        # Search for LinkedIn company page
        linkedin_results = self.search_web_with_validation(f'site:linkedin.com/company "{company_name}"')
        linkedin = 'Not available'
        for result in linkedin_results:
            if '/company/' in result['link'] and company_name.lower() in result['link'].lower():
                linkedin = result['link']
                break
        
        time.sleep(1)
        
        # Get social media links
        social_links = self.find_social_media_links(company_name)
        
        # Search for company information
        info_results = self.search_web_with_validation(f'"{company_name}" company headquarters founded employees')
        company_info = info_results[0]['snippet'] if info_results else 'Information not available'
        
        return {
            'website': website,
            'linkedin': linkedin,
            'facebook': social_links['facebook'],
            'twitter': social_links['twitter'],
            'instagram': social_links['instagram'],
            'overview': company_info,
            'headquarters': 'Research from official website',
            'founded': 'Research from official website',
            'size': 'Research from official website'
        }

    def find_interview_resources(self, company_name: str, role: str) -> Dict:
        """Find specific interview resources for company and role."""
        print(f"Finding interview resources for {company_name} - {role}...")
        
        # Prioritized search queries for interview experiences
        search_queries = [
            f'"{company_name}" "{role}" interview experience site:glassdoor.com',
            f'"{company_name}" software engineer interview questions site:geeksforgeeks.org',
            f'"{company_name}" interview experience site:leetcode.com',
            f'"{company_name}" coding interview site:interviewbit.com'
        ]
        
        interview_links = []
        for query in search_queries:
            results = self.search_web_with_validation(query, 2)
            for result in results:
                if result['link'] not in interview_links:
                    interview_links.append(result['link'])
                    if len(interview_links) >= 4:  # Limit to 4 good links
                        break
            time.sleep(1)
            if len(interview_links) >= 4:
                break
        
        # If no specific results found, provide general reliable resources
        if not interview_links:
            interview_links = [
                f"https://www.glassdoor.com/Interview/{company_name.replace(' ', '-')}-Interview-Questions-E.htm",
                "https://www.geeksforgeeks.org/company-preparation/",
                "https://leetcode.com/discuss/interview-experience",
                "https://www.interviewbit.com/interview-experiences/"
            ]
        
        return {'links': interview_links[:4]}  # Return only first 4

    def get_role_preparation_resources(self, role: str) -> List[str]:
        """Get verified preparation resources for specific role."""
        
        # Default reliable resources that always work
        default_resources = [
            "https://www.geeksforgeeks.org/data-structures/",
            "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
            "https://www.geeksforgeeks.org/system-design-tutorial/",
            "https://www.geeksforgeeks.org/behavioral-interview-questions/"
        ]
        
        # Role-specific searches
        role_queries = {
            "software": "software engineer interview preparation coding",
            "data": "data scientist interview preparation python statistics",
            "frontend": "frontend developer interview preparation javascript react",
            "backend": "backend developer interview preparation system design",
            "intern": "software engineering intern interview preparation"
        }
        
        # Find the best matching query
        role_lower = role.lower()
        matching_query = None
        for key, query in role_queries.items():
            if key in role_lower:
                matching_query = query
                break
        
        if matching_query:
            print(f"Searching for {role} preparation resources...")
            results = self.search_web_with_validation(matching_query, 4)
            verified_links = [r['link'] for r in results if self.validate_url(r['link'])]
            
            if len(verified_links) >= 2:
                return verified_links[:4]
        
        # Return default reliable resources if search fails
        return default_resources

    def generate_final_response_enhanced(self, company_name: str, role: str, 
                                       company_data: Dict, interview_data: Dict, 
                                       prep_resources: List[str]) -> str:
        """Generate enhanced response with verified information only."""
        
        # Clean and format company overview
        overview = company_data.get('overview', 'Technology company')
        if len(overview) > 200:
            # Extract key information from messy overview
            overview = self.clean_company_overview(overview)
        
        response = f"""ORGANIZATION: {company_name}

ORGANIZATION DETAILS:
1. Base Site: {company_data.get('website', 'Not available')}
2. LinkedIn: {company_data.get('linkedin', 'Not available')}
3. Facebook: {company_data.get('facebook', 'Not available')}
4. X (Twitter): {company_data.get('twitter', 'Not available')}
5. Instagram: {company_data.get('instagram', 'Not available')}
6. Role/s Offered: {role}
7. Company Overview: {overview}
8. Company Size: {company_data.get('size', 'Check official website')}
9. Headquarters: {company_data.get('headquarters', 'Check official website')}
10. Founded: {company_data.get('founded', 'Check official website')}

INTERVIEW REFERENCES:
1. Primary Interview Resource: {interview_data['links'][0] if interview_data['links'] else 'https://www.glassdoor.com/'}
2. Secondary Interview Resource: {interview_data['links'][1] if len(interview_data['links']) > 1 else 'https://www.geeksforgeeks.org/company-preparation/'}
3. Additional Interview Resource: {interview_data['links'][2] if len(interview_data['links']) > 2 else 'https://leetcode.com/discuss/interview-experience'}

ROLE-SPECIFIC PREPARATION:
To get started with the preparation for {role}, you can refer to the following resources:

1. Data Structures and Algorithms: {prep_resources[0]}
2. Programming Fundamentals: {prep_resources[1]}
3. System Design: {prep_resources[2]}
4. Behavioral Interviews: {prep_resources[3]}

Key topics frequently asked:
- Arrays, Linked Lists, Trees, Graphs
- Dynamic Programming, Greedy Algorithms
- Object-Oriented Programming concepts
- Database management and SQL queries
- System design basics (for senior roles)

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
Visit the company's official website careers page and LinkedIn company page for detailed information about their culture, values, mission, and work environment. Look for employee testimonials and company blog posts.

Best Regards,
Professor Animesh Giri
LinkedIn: https://www.linkedin.com/in/animesh-giri-15272531/
Youtube: https://www.youtube.com/channel/UCBFH7hssUsyipttqLxHU-cw"""

        return response

    def clean_company_overview(self, overview: str) -> str:
        """Clean messy company overview text."""
        # Remove dates and extra formatting
        overview = re.sub(r'\(.*?\)', '', overview)  # Remove parentheses content
        overview = re.sub(r'\d{4}-\d{2}-\d{2}', '', overview)  # Remove dates
        overview = re.sub(r'Founders\..*?\.', '', overview)  # Remove founder info
        overview = re.sub(r'Headquarters,.*?\.', '', overview)  # Remove HQ info
        
        # Clean extra spaces and periods
        overview = ' '.join(overview.split())
        overview = overview.strip(', .')
        
        # If still too messy or empty, provide default
        if len(overview) < 20 or not overview:
            return "Technology company - check official website for detailed information"
        
        return overview

    def extract_company_and_role(self, email_content: str) -> tuple[str, str]:
        """Extract company name and role from email using Gemini."""
        extraction_prompt = f"""
        Analyze this recruitment email and extract ONLY the company name and job role/position.
        Be very precise and extract the exact company name as mentioned.
        
        Email Content:
        {email_content}
        
        Respond in this exact format:
        COMPANY: [exact company name]
        ROLE: [exact job role/position]
        
        If you cannot find clear information, respond with:
        COMPANY: Unknown
        ROLE: Unknown
        """
        
        response = self.call_gemini_api(extraction_prompt)
        if not response:
            return "Unknown", "Unknown"
        
        # Parse the response
        company = "Unknown"
        role = "Unknown"
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('COMPANY:'):
                company = line.split(':', 1)[1].strip()
            elif line.startswith('ROLE:'):
                role = line.split(':', 1)[1].strip()
        
        return company, role

    def call_gemini_api(self, prompt: str) -> Optional[str]:
        """Call Google Gemini API with the given prompt."""
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,  # Lower temperature for more consistent results
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4096,
            }
        }
        
        try:
            url = f"{self.gemini_url}?key={self.gemini_api_key}"
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print("No response generated from Gemini API")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling Gemini API: {e}")
            return None
        except KeyError as e:
            print(f"Unexpected response format from Gemini API: {e}")
            return None

    def create_whatsapp_link(self, message: str) -> str:
        """Create a WhatsApp link with the formatted message."""
        # Truncate message if too long (WhatsApp has limits)
        if len(message) > 2000:
            message = message[:1900] + "\n\n[Message truncated - full details available on request]"
        
        encoded_message = urllib.parse.quote(message)
        return f"https://api.whatsapp.com/send/?phone={self.phone_number}&text={encoded_message}"

    def process_email_and_generate_whatsapp_link(self, email_content: str) -> tuple[str, str]:
        """Enhanced processing with actual web research."""
        
        # Step 1: Extract company and role
        print("Extracting company and role...")
        company_name, role = self.extract_company_and_role(email_content)
        print(f"Extracted: Company='{company_name}', Role='{role}'")
        
        if company_name == "Unknown":
            return "Error: Could not extract company name from email", ""
        
        # Step 2: Research company details with validation
        company_data = self.research_company_comprehensive(company_name)
        
        # Step 3: Find interview resources
        interview_data = self.find_interview_resources(company_name, role)
        
        # Step 4: Get role-specific preparation resources
        prep_resources = self.get_role_preparation_resources(role)
        
        # Step 5: Generate final response
        print("Generating enhanced response...")
        response = self.generate_final_response_enhanced(
            company_name, role, company_data, interview_data, prep_resources
        )
        
        # Step 6: Create WhatsApp link
        whatsapp_link = self.create_whatsapp_link(response)
        
        return response, whatsapp_link

    def find_interview_resources(self, company_name: str, role: str) -> Dict:
        """Find verified interview resources."""
        print(f"Finding interview resources for {company_name} - {role}...")
        
        # Priority search queries
        queries = [
            f'"{company_name}" interview questions site:glassdoor.com',
            f'"{company_name}" coding interview site:geeksforgeeks.org',
            f'"{company_name}" interview experience site:leetcode.com'
        ]
        
        all_links = []
        for query in queries:
            results = self.search_web_with_validation(query, 2)
            for result in results:
                if result['link'] not in all_links:
                    all_links.append(result['link'])
            time.sleep(1)
        
        # Ensure we have at least some reliable fallback links
        fallback_links = [
            "https://www.glassdoor.com/Interview/index.htm",
            "https://www.geeksforgeeks.org/company-preparation/",
            "https://leetcode.com/discuss/interview-experience"
        ]
        
        # Combine and limit to 4 links
        final_links = all_links[:3] + fallback_links
        return {'links': final_links[:4]}

    def run_interactive(self):
        """Run the bot in interactive mode."""
        print("=== Enhanced Company Research WhatsApp Bot ===")
        print("Paste your email content below (press Enter twice when done):")
        
        # Read multi-line email content
        email_lines = []
        empty_line_count = 0
        
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
            email_lines.append(line)
        
        # Remove the trailing empty lines
        email_content = "\n".join(email_lines[:-2])
        
        if not email_content.strip():
            print("Error: No email content provided.")
            return
        
        print("\nProcessing email content with enhanced search...")
        response, whatsapp_link = self.process_email_and_generate_whatsapp_link(email_content)
        
        if response.startswith("Error:"):
            print(f"\n{response}")
            return
        
        print("\n" + "="*50)
        print("GENERATED RESPONSE:")
        print("="*50)
        print(response)
        print("\n" + "="*50)
        print("WHATSAPP LINK:")
        print("="*50)
        print(whatsapp_link)
        
        # Ask if user wants to open WhatsApp link
        open_link = input("\nDo you want to open the WhatsApp link in your browser? (y/n): ").lower()
        if open_link in ['y', 'yes']:
            webbrowser.open(whatsapp_link)
            print("WhatsApp link opened in browser!")

load_dotenv()

def main():
    """Main function to run the enhanced bot."""
    print("=== Enhanced Company Research WhatsApp Bot Setup ===")
    
    # Get API keys and phone number from user or environment variables
    gemini_api_key = os.getenv('GEMINI_API_KEY') 
    csr_api_key = os.getenv('CSR_API_KEY') 
    cse_id = os.getenv('CSE_ID') or input("Enter Custom Search Engine ID: ").strip()
    phone_number = os.getenv('PHONE_NUMBER') or input("Enter WhatsApp phone number (with country code, no + or spaces, e.g., 919876543210): ").strip()
    
    if not gemini_api_key:
        print("Error: Gemini API key is required!")
        return
    
    if not csr_api_key:
        print("Error: Custom Search API key is required!")
        return
        
    if not cse_id:
        print("Error: Custom Search Engine ID is required!")
        return
    
    if not phone_number:
        print("Error: Phone number is required!")
        return
    
    # Initialize and run the enhanced bot
    bot = EnhancedCompanyResearchBot(gemini_api_key, csr_api_key, cse_id, phone_number)
    bot.run_interactive()

if __name__ == "__main__":
    main()