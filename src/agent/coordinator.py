import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool

# Import the tool functions from our logistics module
from src.tools.logistics import (
    get_merchant_status,
    get_driver_location,
    check_traffic,
    notify_customer,
    re_route_driver,
    get_nearby_merchants,
)

class Coordinator:
    """
    The Coordinator agent that uses LangChain to resolve disruptions.
    """
    def __init__(self, use_mock_llm=False):
        self.use_mock_llm = use_mock_llm
        if self.use_mock_llm:
            print("Coordinator agent initialized in MOCK mode.")
            return

        # 1. Initialize the LLM
        # Assumes OPENAI_API_KEY is set in the environment
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4")

        # 2. Define the tools
        self.tools = [
            Tool(
                name="Get Merchant Status",
                func=get_merchant_status,
                description="Useful for getting the status of a merchant (e.g., 'open', 'closed', 'busy'). Input should be a merchant_id string.",
            ),
            Tool(
                name="Get Driver Location",
                func=get_driver_location,
                description="Useful for getting the current GPS location of a driver. Input should be a driver_id string.",
            ),
            Tool(
                name="Check Traffic",
                func=check_traffic,
                description="Useful for checking the traffic conditions between two points. Input should be a dictionary with 'start_point' and 'end_point'.",
            ),
            Tool(
                name="Notify Customer",
                func=notify_customer,
                description="Useful for sending a notification to a customer. Input should be a dictionary with 'customer_id' and 'message'.",
            ),
            Tool(
                name="Re-route Driver",
                func=re_route_driver,
                description="Useful for re-routing a driver to a new destination. Input should be a dictionary with 'driver_id', 'new_destination', and 'reason'.",
            ),
            Tool(
                name="Get Nearby Merchants",
                func=get_nearby_merchants,
                description="Useful for finding nearby merchants of a certain category. Input should be a dictionary with 'latitude', 'longitude', and 'category'.",
            ),
        ]

        # 3. Create the prompt template
        template = """
        You are an intelligent logistics coordinator for a last-mile delivery service.
        Your goal is to resolve disruptions efficiently and communicate clearly.
        You have access to the following tools:

        {tools}

        To use a tool, you must use the following format:
        ```
        Thought: Do I need to use a tool? Yes
        Action: The name of the tool to use.
        Action Input: The input to the tool, as a dictionary if required.
        Observation: The result of the tool.
        ```

        When you have a final answer or a complete plan, you must use the format:
        ```
        Thought: Do I need to use a tool? No
        Final Answer: The final plan or resolution statement.
        ```

        Begin!

        Disruption: {input}
        Thought: {agent_scratchpad}
        """
        self.prompt = PromptTemplate.from_template(template)

        # 4. Create the agent
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # 5. Create the Agent Executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,  # Set to True to see the agent's chain of thought
            handle_parsing_errors=True,
        )

        print("Coordinator agent initialized with LangChain.")

    def handle_disruption(self, disruption_scenario: str):
        """
        Handles a disruption event using the LangChain agent.
        """
        print(f"Coordinator handling disruption: {disruption_scenario}")

        if self.use_mock_llm:
            print("\n> Entering new AgentExecutor chain...")
            print("Thought: The user is asking to check on an order. The first step is to get the status of the merchant.")
            print("Action: Get Merchant Status")
            print(f"Action Input: merchant-456")
            # Simulate tool execution
            observation = get_merchant_status("merchant-456")
            print(f"Observation: {observation}")
            print("Thought: The merchant is busy. I should notify the customer of a potential delay and look for alternatives.")
            print("Action: Notify Customer")
            print(f"Action Input: {{'customer_id': 'cust-123', 'message': 'Your restaurant is currently very busy, and there may be a delay with your order.'}}")
            observation = notify_customer("cust-123", "Your restaurant is currently very busy, and there may be a delay with your order.")
            print(f"Observation: {observation}")
            print("Thought: Now I should find nearby alternative merchants for the customer.")
            print("Action: Get Nearby Merchants")
            print(f"Action Input: {{'latitude': 3.1352, 'longitude': 101.6865, 'category': 'restaurant'}}")
            observation = get_nearby_merchants(3.1352, 101.6865, 'restaurant')
            print(f"Observation: {observation}")
            print("Thought: I have found alternatives. I will notify the customer about them.")
            print("Action: Notify Customer")
            alt_message = f"We've found some alternative restaurants nearby with shorter wait times: {observation['merchants'][0]['name']} (15 min), {observation['merchants'][1]['name']} (10 min). Would you like to switch your order?"
            print(f"Action Input: {{'customer_id': 'cust-123', 'message': '{alt_message}'}}")
            observation = notify_customer("cust-123", alt_message)
            print(f"Observation: {observation}")
            print("Thought: I have notified the customer of the delay and offered alternatives. My work here is done for now.")
            print("Final Answer: The original merchant is busy. I have notified the customer about the delay and have suggested alternative nearby restaurants. I am awaiting the customer's response.")
            print("\n> Finished chain.")
            return {
                "input": disruption_scenario,
                "output": "The original merchant is busy. I have notified the customer about the delay and have suggested alternative nearby restaurants. I am awaiting the customer's response."
            }

        response = self.agent_executor.invoke({
            "input": disruption_scenario
        })

        return response
