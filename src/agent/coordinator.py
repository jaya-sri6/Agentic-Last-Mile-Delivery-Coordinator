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
    log_merchant_packaging_feedback, notify_resolution, contact_recipient_via_chat,
    suggest_safe_drop_off, find_nearby_locker, calculate_alternative_route,
    notify_passenger_and_driver, check_flight_status
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
            Tool(name="Contact Recipient via Chat", func=contact_recipient_via_chat, description="Contacts a recipient via chat to get instructions. Input: {'recipient_id': str, 'initial_message': str}."),
            Tool(name="Suggest Safe Drop-off", func=suggest_safe_drop_off, description="Suggests and confirms a safe drop-off location with a recipient. Input: {'recipient_id': str, 'suggestion': str}."),
            Tool(name="Find Nearby Locker", func=find_nearby_locker, description="Finds a secure parcel locker near a location. Input: {'latitude': float, 'longitude': float}."),
            Tool(name="Calculate Alternative Route", func=calculate_alternative_route, description="Calculates an alternative route to avoid an obstruction. Input: {'current_route': dict, 'obstruction': str}."),
            Tool(name="Notify Passenger and Driver", func=notify_passenger_and_driver, description="Sends a synchronized notification to a passenger and a driver. Input: {'passenger_id': str, 'driver_id': str, 'message': str}."),
            Tool(name="Check Flight Status", func=check_flight_status, description="Checks the status of a flight. Input: flight_number."),
        ]

        # 3. Create the prompt template
        template = """
        You are an intelligent logistics coordinator for a last-mile delivery service.
        Your goal is to resolve disruptions efficiently and communicate clearly.

        ### Your Protocols ###

        **Dispute Resolution:**
        When handling a dispute between a customer and a driver, your primary goal is to be a fair and impartial mediator. Follow these steps:
        1. Initiate a mediation flow to open a communication channel.
        2. Collect evidence from all parties involved.
        3. Analyze the evidence to determine the most likely cause of the issue.
        4. Based on your analysis, form a resolution plan.
        5. Clearly communicate the final resolution to all parties.

        **Unavailable Recipient:**
        When a recipient is unavailable at the delivery location, follow this protocol:
        1. First, try to contact the recipient via chat to get instructions.
        2. Based on their response, evaluate the options. If they give permission for a safe drop-off, use the 'Suggest Safe Drop-off' tool to confirm.
        3. If no safe drop-off is possible, use the 'Find Nearby Locker' tool to see if a secure parcel locker is a viable alternative.
        4. Communicate the final plan clearly.

        **Traffic Obstruction:**
        When a major traffic obstruction is detected on a passenger's route, especially for an urgent trip like to an airport, your response must be swift and informative.
        1. Immediately check for alternative routes to understand the potential delay.
        2. If the passenger is heading to the airport, it may be useful to check their flight status to see if it is also delayed. This provides helpful context.
        3. Proactively notify both the passenger and the driver of the obstruction, the new route, and the updated ETA. Reassure them that you are handling the situation.

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
                # ... (rest of dispute mock)
                summary = f"Dispute resolved. Based on the evidence, the merchant was found at fault. The customer has been refunded, the driver exonerated, and feedback logged."
                return {"input": disruption_scenario, "output": summary}

            elif "unavailable" in disruption_scenario.lower() or "not home" in disruption_scenario.lower():
                # Mock logic for "Recipient Unavailable"
                print("Thought: The recipient is unavailable. I must contact them to find a solution.")

                # Step 1: Contact Recipient
                print("Action: Contact Recipient via Chat")
                action_input = {'recipient_id': 'recip-789', 'initial_message': "Our driver has arrived with your package, but you don't seem to be available. What should we do?"}
                print(f"Action Input: {action_input}")
                observation = contact_recipient_via_chat(**action_input)
                print(f"Observation: {observation}")

                # Step 2: Evaluate Response and Suggest Solution
                # In this mock, we assume a specific response and action
                print("Thought: The recipient suggested leaving the package with a neighbour. I will confirm this.")
                print("Action: Suggest Safe Drop-off")
                action_input = {'recipient_id': 'recip-789', 'suggestion': "leave the package with your neighbour at Unit 102"}
                print(f"Action Input: {action_input}")
                observation = suggest_safe_drop_off(**action_input)
                print(f"Observation: {observation}")

                # Step 3: Final Plan
                summary = "The recipient is unavailable but has approved a safe drop-off. The driver should leave the package with the neighbour at Unit 102."
                print(f"Thought: The recipient has approved the plan. I will now provide the final answer.")
                print(f"Final Answer: {summary}")
                print("\n> Finished chain.")
                return {"input": disruption_scenario, "output": summary}

            elif "traffic" in disruption_scenario.lower() or "obstruction" in disruption_scenario.lower():
                # Mock logic for "Sudden Major Traffic Obstruction"
                print("Thought: A major traffic obstruction has been reported for an urgent trip. I must act quickly.")

                # Step 1: Calculate Alternative Route
                print("Action: Calculate Alternative Route")
                action_input = {'current_route': {'start': 'Location A', 'end': 'Airport', 'original_eta': 30}, 'obstruction': 'major accident'}
                print(f"Action Input: {action_input}")
                observation = calculate_alternative_route(**action_input)
                print(f"Observation: {observation}")
                new_route_summary = observation['new_route']['summary']
                new_eta = observation['new_route']['updated_eta_minutes']

                # Step 2: Check Flight Status
                print("Thought: The new route adds time. Since the passenger is going to the airport, I should check their flight status for context.")
                print("Action: Check Flight Status")
                action_input = "SQ123"
                print(f"Action Input: {action_input}")
                observation = check_flight_status(action_input)
                print(f"Observation: {observation}")
                flight_status = observation['flight_status']

                # Step 3: Notify Parties
                print("Thought: The flight is also delayed, which is helpful context. I will now inform both parties of the new plan.")
                print("Action: Notify Passenger and Driver")
                message = f"Major accident detected on your route. We've found an alternative: {new_route_summary}. New ETA is {new_eta} minutes. Good news: your flight {action_input} is also {flight_status.lower()}, so you should still have plenty of time."
                action_input = {'passenger_id': 'pass-123', 'driver_id': 'driver-456', 'message': message}
                print(f"Action Input: {action_input}")
                notify_passenger_and_driver(**action_input)

                summary = f"Successfully re-routed trip to avoid traffic. New ETA is {new_eta} minutes. Both passenger and driver have been notified."
                print(f"Thought: The situation is handled. The driver has a new route and the passenger is informed.")
                print(f"Final Answer: {summary}")
                print("\n> Finished chain.")
                return {"input": disruption_scenario, "output": summary}

            else:
                # Fallback mock logic for "Overloaded Restaurant"
                print("Thought: This seems to be a merchant-related issue. I will check the merchant's status.")
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
