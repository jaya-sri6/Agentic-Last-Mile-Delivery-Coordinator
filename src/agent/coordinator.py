import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool

# Import the tool functions from our logistics module
from src.tools.logistics import (
    get_merchant_status, get_driver_location, check_traffic, notify_customer,
    re_route_driver, get_nearby_merchants, initiate_mediation_flow,
    collect_evidence, analyze_evidence, issue_instant_refund, exonerate_driver,
    log_merchant_packaging_feedback, notify_resolution
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
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4")

        # 2. Define the tools
        self.tools = [
            Tool(name="Get Merchant Status", func=get_merchant_status, description="Gets the status of a merchant (e.g., 'open', 'busy'). Input: merchant_id."),
            Tool(name="Get Driver Location", func=get_driver_location, description="Gets the current GPS location of a driver. Input: driver_id."),
            Tool(name="Check Traffic", func=check_traffic, description="Checks traffic between two points. Input: {'start_point': str, 'end_point': str}."),
            Tool(name="Notify Customer", func=notify_customer, description="Sends a notification to a customer. Input: {'customer_id': str, 'message': str}."),
            Tool(name="Re-route Driver", func=re_route_driver, description="Re-routes a driver to a new destination. Input: {'driver_id': str, 'new_destination': str, 'reason': str}."),
            Tool(name="Get Nearby Merchants", func=get_nearby_merchants, description="Finds nearby merchants. Input: {'latitude': float, 'longitude': float, 'category': str}."),
            Tool(name="Initiate Mediation Flow", func=initiate_mediation_flow, description="Starts a mediation process for a dispute. Input: {'order_id': str, 'customer_id': str, 'driver_id': str}."),
            Tool(name="Collect Evidence", func=collect_evidence, description="Collects evidence from parties in a dispute. Input: {'mediation_id': str, 'parties': list[str]}."),
            Tool(name="Analyze Evidence", func=analyze_evidence, description="Analyzes collected evidence to determine fault. Input: evidence dictionary."),
            Tool(name="Issue Instant Refund", func=issue_instant_refund, description="Issues a refund to a customer. Input: {'customer_id': str, 'order_id': str, 'amount': float}."),
            Tool(name="Exonerate Driver", func=exonerate_driver, description="Clears a driver of fault. Input: {'driver_id': str, 'order_id': str}."),
            Tool(name="Log Merchant Packaging Feedback", func=log_merchant_packaging_feedback, description="Logs feedback about merchant packaging. Input: {'merchant_id': str, 'order_id': str, 'feedback_details': str}."),
            Tool(name="Notify Resolution", func=notify_resolution, description="Notifies all parties of a dispute resolution. Input: {'parties': list[str], 'order_id': str, 'resolution_summary': str}."),
        ]

        # 3. Create the prompt template
        template = """
        You are an intelligent logistics coordinator for a last-mile delivery service.
        Your goal is to resolve disruptions efficiently and communicate clearly.

        When handling a dispute between a customer and a driver, your primary goal is to be a fair and impartial mediator. Follow these steps:
        1. Initiate a mediation flow to open a communication channel.
        2. Collect evidence from all parties involved. This may include photos and statements.
        3. Analyze the evidence to determine the most likely cause of the issue.
        4. Based on your analysis, form a resolution plan. This may involve issuing a refund, clearing a driver of fault, and logging feedback for a merchant.
        5. Clearly communicate the final resolution to all parties.

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
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)

        # 5. Create the Agent Executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
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
            # Simple routing for different mock scenarios based on keywords
            if "dispute" in disruption_scenario.lower() or "damaged" in disruption_scenario.lower():
                # Mock logic for "Damaged Packaging Dispute"
                print("Thought: A dispute has been reported. I must follow the mediation and adjudication protocol.")

                # Step 1: Initiate Mediation
                print("Action: Initiate Mediation Flow")
                action_input = {'order_id': 'order-789', 'customer_id': 'cust-456', 'driver_id': 'driver-123'}
                print(f"Action Input: {action_input}")
                observation = initiate_mediation_flow(**action_input)
                print(f"Observation: {observation}")
                mediation_id = observation['mediation_id']

                # Step 2: Collect Evidence
                print("Thought: Now that mediation has started, I must collect evidence from all parties.")
                print("Action: Collect Evidence")
                action_input = {'mediation_id': mediation_id, 'parties': ['customer', 'driver']}
                print(f"Action Input: {action_input}")
                observation = collect_evidence(**action_input)
                print(f"Observation: {observation}")
                evidence = observation['evidence']

                # Step 3: Analyze Evidence
                print("Thought: I have collected the evidence. Now I must analyze it to determine fault.")
                print("Action: Analyze Evidence")
                print(f"Action Input: {evidence}")
                observation = analyze_evidence(evidence)
                print(f"Observation: {observation}")
                fault = observation['fault']
                reason = observation['reason']

                # Step 4: Formulate and Execute Resolution
                print(f"Thought: The analysis indicates the '{fault}' is at fault. I will now execute the resolution plan.")
                # Assume merchant fault for this mock
                print("Action: Issue Instant Refund")
                action_input = {'customer_id': 'cust-456', 'order_id': 'order-789', 'amount': 5.99}
                print(f"Action Input: {action_input}")
                issue_instant_refund(**action_input)

                print("Action: Exonerate Driver")
                action_input = {'driver_id': 'driver-123', 'order_id': 'order-789'}
                print(f"Action Input: {action_input}")
                exonerate_driver(**action_input)

                print("Action: Log Merchant Packaging Feedback")
                action_input = {'merchant_id': 'merchant-xyz', 'order_id': 'order-789', 'feedback_details': reason}
                print(f"Action Input: {action_input}")
                log_merchant_packaging_feedback(**action_input)

                # Step 5: Notify Parties
                print("Thought: The resolution has been executed. I will now notify the parties.")
                print("Action: Notify Resolution")
                summary = f"Dispute resolved. Based on the evidence, the merchant was found at fault. The customer has been refunded, the driver exonerated, and feedback logged."
                action_input = {'parties': ['customer', 'driver'], 'order_id': 'order-789', 'resolution_summary': summary}
                print(f"Action Input: {action_input}")
                notify_resolution(**action_input)

                print("Thought: I have successfully mediated and resolved the dispute.")
                print(f"Final Answer: {summary}")
                print("\n> Finished chain.")
                return {"input": disruption_scenario, "output": summary}

            else:
                # Mock logic for "Overloaded Restaurant"
                print("Thought: The user is asking to check on an order. The first step is to get the status of the merchant.")
                print("Action: Get Merchant Status...")
                observation = get_merchant_status("merchant-456")
                print(f"Observation: {observation}")
                print("Final Answer: The original merchant is busy. I have notified the customer about the delay and have suggested alternative nearby restaurants.")
                return {
                    "input": disruption_scenario,
                    "output": "The original merchant is busy. I have notified the customer about the delay and have suggested alternative nearby restaurants."
                }

        response = self.agent_executor.invoke({"input": disruption_scenario})
        return response
