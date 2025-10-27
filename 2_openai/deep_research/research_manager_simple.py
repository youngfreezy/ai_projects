from search_agent import WebSearchItem, WebSearchPlan
from pydantic import BaseModel
from typing import List
import asyncio
from openai import OpenAI
import logging
import os
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReportData(BaseModel):
    short_summary: str
    markdown_report: str
    follow_up_questions: List[str]

class ResearchManager:
    def __init__(self, email_to: str = None, email_from: str = None):
        self.email_to = email_to
        self.email_from = email_from
        self.client = OpenAI()
        logger.info(f"ResearchManager initialized with email_to={email_to}, email_from={email_from}")

    async def run(self, query: str):
        """Run the research process, yielding status updates and final report"""
        logger.info(f"Starting research process for query: {query}")
        
        if not query.strip():
            yield "Please enter a research topic."
            return
        if not self.email_to or not self.email_from:
            yield "Please provide both email addresses."
            return

        try:
            # Step 1: Plan searches
            yield "Starting research..."
            search_plan = await self.plan_searches(query)
            if len(search_plan.searches) > 5:
                search_plan.searches = search_plan.searches[:5]
            yield f"Planned {len(search_plan.searches)} searches..."

            # Step 2: Execute searches
            search_results = []
            total_searches = len(search_plan.searches)
            tasks = [self.search(item) for item in search_plan.searches]
            
            for task in asyncio.as_completed(tasks):
                result = await task
                if result:
                    search_results.append(result)
                yield f"Completed {len(search_results)}/{total_searches} searches..."

            # Step 3: Generate report
            yield "Writing report..."
            report = await self.write_report(query, search_results)

            # Step 4: Send email
            yield "Sending email..."
            await self.send_email(report, query)
            yield f"✅ Email sent to {self.email_to}"

            # Step 5: Final report with AI attribution
            questions = "".join(f"- {q}\n" for q in report.follow_up_questions)
            yield (
                "# Research Report\n\n"
                f"{report.markdown_report}\n\n"
                "## Follow-up Questions\n"
                f"{questions}\n"
                "---\n\n"
                "_This report was generated using an AI research assistant that employs a multi-agent system architecture:_\n\n"
                "1. A **Planning Agent** breaks down complex queries into focused search topics\n"
                "2. **Search Agents** run parallel searches to gather comprehensive information\n"
                "3. A **Writer Agent** synthesizes the findings into a structured report\n"
                "4. An **Email Agent** formats and delivers the results\n\n"
                "_The system uses GPT-4 for natural language understanding and generation, with asynchronous processing for efficiency._"
            )

        except Exception as e:
            logger.error(f"Error in research process: {str(e)}", exc_info=True)
            yield f"❌ Error: {str(e)}"

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""
        logger.info(f"Planning searches for query: {query}")
        try:
            messages = [
                {"role": "system", "content": """You are a research planner. Break down the query into exactly 5 specific search terms that will help gather comprehensive information. Consider:
                1. Core concepts and definitions
                2. Current state and trends
                3. Expert opinions and research
                4. Practical applications
                5. Challenges and limitations"""},
                {"role": "user", "content": f"Create a focused search plan with exactly 5 search terms for: {query}"}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            search_terms = response.choices[0].message.content.split("\n")
            search_terms = [term.strip() for term in search_terms if term.strip()][:5]
            
            return WebSearchPlan(searches=[
                WebSearchItem(query=term, reason=f"Part of research for: {query}")
                for term in search_terms
            ])
        except Exception as e:
            logger.error(f"Error in search planning: {str(e)}", exc_info=True)
            raise

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""
        logger.info(f"Performing search for: {item.query}")
        try:
            messages = [
                {"role": "system", "content": """You are a research assistant performing a web search. For each search:
                1. Find the most relevant and recent information
                2. Include specific facts, statistics, and data when available
                3. Note any conflicting viewpoints or debates
                4. Cite sources or experts when possible
                5. Focus on verified information from reputable sources"""},
                {"role": "user", "content": f"Search term: {item.query}\nReason: {item.reason}"}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Search error for '{item.query}': {str(e)}", exc_info=True)
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the report for the query"""
        logger.info("Starting report writing")
        try:
            search_results_text = "\n\n".join(search_results)
            content = f"Query: {query}\n\nSearch Results:\n{search_results_text}"
            
            messages = [
                {"role": "system", "content": """You are a senior researcher writing a comprehensive report. Your report should include:

1. Executive Summary (2-3 paragraphs)
   - Key findings and insights
   - Main conclusions
   - Significance of the research

2. Detailed Analysis
   - Background and Context
   - Current State of Knowledge
   - Key Findings and Evidence
   - Expert Opinions and Research
   - Conflicting Views or Debates
   - Practical Applications
   - Challenges and Limitations

3. Future Implications
   - Trends and Predictions
   - Potential Impact
   - Areas for Further Research

4. Recommendations
   - Practical Steps
   - Best Practices
   - Strategic Considerations

5. Follow-up Questions
   - Areas needing more research
   - Emerging topics to explore
   - Practical implementation questions

Format the report in clear Markdown with proper headings, bullet points, and sections. Do not include a title or executive summary heading - those will be added separately."""},
                {"role": "user", "content": content}
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            report_text = response.choices[0].message.content
            
            # Extract sections
            sections = report_text.split("\n\n")
            summary = sections[0] if sections else "Summary not available"
            
            # Extract follow-up questions
            follow_up_section = report_text.split("# Follow-up Questions")[-1] if "# Follow-up Questions" in report_text else ""
            follow_ups = [q.strip("- ") for q in follow_up_section.split("\n") if q.strip().startswith("-")]
            if not follow_ups:
                follow_ups = [
                    "What are the most pressing areas for further research?",
                    "How can these findings be applied in practice?",
                    "What are the long-term implications of these findings?"
                ]

            return ReportData(
                short_summary=summary,
                markdown_report=report_text,
                follow_up_questions=follow_ups
            )
        except Exception as e:
            logger.error(f"Error in report writing: {str(e)}", exc_info=True)
            raise

    async def send_email(self, report: ReportData, query: str) -> None:
        """Send the report via email"""
        logger.info(f"Preparing email from {self.email_from} to {self.email_to}")
        try:
            # First, have GPT format the report into proper HTML
            messages = [
                {"role": "system", "content": """You are an email formatter. Convert the given markdown report into a well-structured HTML email.
                - Convert markdown headings to proper HTML headings
                - Format lists and bullet points properly
                - Add appropriate spacing and styling
                - Preserve all content but make it visually appealing
                - Return only the HTML content for the email body"""},
                {"role": "user", "content": f"Format this report into HTML:\n\n{report.markdown_report}"}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
            formatted_report = response.choices[0].message.content
            
            # Create the full HTML email
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #2c5282;
                        border-bottom: 2px solid #4299e1;
                        padding-bottom: 10px;
                        margin-top: 30px;
                    }}
                    h2 {{
                        color: #2b6cb0;
                        margin-top: 25px;
                        border-bottom: 1px solid #bee3f8;
                        padding-bottom: 5px;
                    }}
                    h3 {{
                        color: #2c5282;
                        margin-top: 20px;
                    }}
                    .summary {{
                        background-color: #ebf8ff;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border-left: 4px solid #4299e1;
                    }}
                    ul, ol {{
                        margin-left: 20px;
                        padding-left: 20px;
                    }}
                    li {{
                        margin: 8px 0;
                    }}
                    .footer {{
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #e2e8f0;
                        font-size: 0.9em;
                        color: #718096;
                    }}
                    .content {{
                        margin-top: 30px;
                    }}
                    .ai-note {{
                        background-color: #f7fafc;
                        padding: 15px;
                        border-radius: 8px;
                        margin-top: 30px;
                        font-style: italic;
                        border: 1px solid #e2e8f0;
                    }}
                </style>
            </head>
            <body>
                <h1>Research Report: {query}</h1>
                
                <div class="summary">
                    <h2>Executive Summary</h2>
                    <p>{report.short_summary}</p>
                </div>

                <div class="content">
                    {formatted_report}
                </div>

                <div class="ai-note">
                    <p><strong>About this Report:</strong> This research was conducted using an AI-powered research assistant that employs a multi-agent system architecture:</p>
                    <ul>
                        <li>Planning Agent: Breaks down complex queries into focused search topics</li>
                        <li>Search Agents: Run parallel searches to gather comprehensive information</li>
                        <li>Writer Agent: Synthesizes findings into a structured report</li>
                        <li>Email Agent: Formats and delivers the results</li>
                    </ul>
                    <p>The system uses GPT-4 for natural language understanding and generation, with asynchronous processing for efficiency.</p>
                </div>

                <div class="footer">
                    <p>This report was generated by the Deep Research AI Assistant.</p>
                    <p>For any questions or follow-up, please reply to this email.</p>
                </div>
            </body>
            </html>
            """
            
            # Send the email using SendGrid
            api_key = os.environ.get("SENDGRID_API_KEY")
            if not api_key:
                raise Exception("SendGrid API key not found")
                
            sg = sendgrid.SendGridAPIClient(api_key=api_key)
            from_email = Email(self.email_from)
            to_email = To(self.email_to)
            subject = f"Research Report: {query[:100]}..."
            content = Content("text/html", html_template)
            mail = Mail(from_email, to_email, subject, content)
            
            response = sg.client.mail.send.post(request_body=mail.get())
            
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Email sent successfully (status {response.status_code})")
            else:
                raise Exception(f"Failed to send email (status {response.status_code})")
                
        except Exception as e:
            logger.error(f"Error in email sending: {str(e)}", exc_info=True)
            raise