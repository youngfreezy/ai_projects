CRISIS_RESOURCES = {
    "domestic_violence": {
        "name": "National Domestic Violence Hotline",
        "phone": "1-800-799-SAFE (7233)",
        "website": "https://www.thehotline.org",
        "available": "24/7, confidential"
    },
    "forced_marriage": {
        "name": "Tahirih Justice Center",
        "phone": "571-282-6161",
        "website": "https://www.tahirih.org",
        "available": "Legal and social services for forced marriage"
    },
    "reproductive_rights": {
        "name": "Reproductive Health Hotline",
        "phone": "1-800-230-PLAN",
        "website": "https://www.plannedparenthood.org",
        "available": "24/7 health information and support"
    },
    "legal_aid_maryland": {
        "name": "Maryland Legal Aid",
        "phone": "1-866-635-2948",
        "website": "https://www.mdlab.org",
        "available": "Free legal services for eligible Maryland residents"
    },
    "emergency": {
        "name": "Emergency Services",
        "phone": "911",
        "available": "Immediate emergency response"
    }
}

def get_crisis_resources(query: str) -> dict:
    """Returns relevant crisis resources based on query content."""
    resources = {}
    
    # Add emergency resources for immediate danger
    if any(word in query.lower() for word in ["force", "coerce", "threat", "danger"]):
        resources["emergency"] = CRISIS_RESOURCES["emergency"]
    
    # Add forced marriage resources
    if any(word in query.lower() for word in ["marriage", "arranged", "forced"]):
        resources["forced_marriage"] = CRISIS_RESOURCES["forced_marriage"]
        resources["legal_aid"] = CRISIS_RESOURCES["legal_aid_maryland"]
    
    # Add reproductive rights resources
    if any(word in query.lower() for word in ["abortion", "pregnancy"]):
        resources["reproductive_rights"] = CRISIS_RESOURCES["reproductive_rights"]
    
    # Add domestic violence resources
    if any(word in query.lower() for word in ["abuse", "violence", "force", "coerce"]):
        resources["domestic_violence"] = CRISIS_RESOURCES["domestic_violence"]
    
    return resources

def format_resources_markdown(resources: dict) -> str:
    """Formats crisis resources as markdown."""
    if not resources:
        return ""
        
    markdown = "\n\n## Important Resources and Support\n\n"
    markdown += "**If you are in immediate danger, please call 911.**\n\n"
    
    for resource in resources.values():
        markdown += f"### {resource['name']}\n"
        markdown += f"- Phone: {resource['phone']}\n"
        if 'website' in resource:
            markdown += f"- Website: [{resource['website']}]({resource['website']})\n"
        markdown += f"- Availability: {resource['available']}\n\n"
    
    markdown += "\nThese organizations provide confidential support and assistance. You are not alone.\n"
    return markdown
