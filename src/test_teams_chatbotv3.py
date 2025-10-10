from monocle_test_tools import TestCase, MonocleValidator
import pytest
import aiohttp
import json
from bot import bot_app
from aiohttp import web


async def send_teams_message_aiohttp(message_text: str, base_url: str = "http://localhost:3978") -> str:
    """
    Convert curl command to aiohttp client request for sending Teams messages.
    
    Args:
        message_text (str): The text message to send
        base_url (str): Base URL of the bot server
        
    Returns:
        str: Response text from the bot
    """
    # Prepare the Teams Bot Framework activity payload
    payload = {
        "type": "message",
        "text": message_text,
        "id": "7a753034-cc7d-4c61-a1eb-2f03c1f9ff90",
        "channelId": "msteams",
        "from": {
            "id": "user-id-0",
            "name": "Alex Wilber",
            "aadObjectId": "00000000-0000-0000-0000-0000000000020"
        },
        "timestamp": "2025-10-09T04:29:39.175Z",
        "localTimestamp": "2025-10-09T09:59:39.175+05:30",
        "localTimezone": "Asia/Calcutta",
        "serviceUrl": "http://localhost:56150/_connector",
        "conversation": {
            "conversationType": "personal",
            "tenantId": "00000000-0000-0000-0000-0000000000001",
            "id": "ee840ec5-fc52-474c-91d9-276abdd03a15"
        },
        "recipient": {
            "id": "00000000-0000-0000-0000-00000000000011",
            "name": "Test Bot"
        },
        "textFormat": "plain",
        "locale": "en-US",
        "entities": [
            {
                "type": "clientInfo",
                "locale": "en-US",
                "country": "US",
                "platform": "Web",
                "timezone": "Asia/Calcutta"
            }
        ],
        "channelData": {
            "tenant": {
                "id": "00000000-0000-0000-0000-0000000000001"
            }
        }
    }
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Create aiohttp client session and send request
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = f"{base_url}/api/messages"
        async with session.post(url, json=payload, headers=headers) as response:
            status = response.status
            response_text = await response.text()

            print(f"Request URL: {url}")
            print(f"Response Status: {status}")
            print(f"Response Text: {response_text}")
            if status == 201:
                return response_text
            else:
                return f"Error: Status {status}, Response: {response_text}"

# Test cases for team chat bot agent
agent_test_cases:list[TestCase] = [
    {
        "test_input": ["What is the capital of India? Give short answer", "http://localhost:3978"],
        "test_output": "Yo! The capital of India is New Delhi.",
        "comparer": "similarity"
    }
]

# Run test cases using Monocle test framework
@MonocleValidator().monocle_testcase(agent_test_cases)
async def test_run_workflows(my_test_case: TestCase):
   await MonocleValidator().test_workflow_async(send_teams_message_aiohttp, my_test_case)

if __name__ == "__main__":
    pytest.main([__file__])