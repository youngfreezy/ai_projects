from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from safety_resources import get_crisis_resources, format_resources_markdown
import asyncio

class ResearchManager:
    def __init__(self, email_to: str = None, email_from: str = None):
        self.email_to = email_to
        self.email_from = email_from

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            yield "🔍 Starting research..."
            search_plan = await self.plan_searches(query)
            yield "📋 Searches planned, starting to search..."     
            
            # Perform searches and show progress
            print("Searching...")
            num_completed = 0
            tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
            search_results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    search_results.append(result)
                num_completed += 1
                print(f"Searching... {num_completed}/{len(tasks)} completed")
                yield f"🔍 Search {num_completed}/{len(tasks)} completed"
            print("Finished searching")
            
            yield "✍️ Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            
            # Add crisis resources if needed
            resources = get_crisis_resources(query)
            if resources:
                report.markdown_report += format_resources_markdown(resources)
                yield "ℹ️ Added important support resources to report..."
            
            yield "📧 Report written, sending email..."
            await self.send_email(report)
            yield f"✅ Email sent to {self.email_to}"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        input = {
            "report": report.markdown_report,
            "from_email": self.email_from,
            "to_email": self.email_to
        }
        result = await Runner.run(
            email_agent,
            input,
        )
        print("Email sent")
        return report