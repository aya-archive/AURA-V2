# A.U.R.A (Adaptive User Retention Assistant) - Chatbot Interface Component
# This module provides the interactive chatbot interface component
# with NLP integration and conversational AI capabilities

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import json
from src.config.constants import Colors, Typography

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotInterface:
    """
    Interactive chatbot interface component for A.U.R.A platform.
    
    This class provides a conversational AI interface for customer
    analysis, strategy recommendations, and data insights through
    natural language interactions.
    """
    
    def __init__(self):
        """Initialize the chatbot interface component."""
        self.colors = Colors()
        
        # Initialize chatbot state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'user_context' not in st.session_state:
            st.session_state.user_context = {}
        
        logger.info("Chatbot interface component initialized")
    
    def render_chat_interface(self, customer_data: pd.DataFrame) -> None:
        """
        Render the main chat interface.
        
        This method creates the main chat interface with message history,
        input field, and interactive features for natural language
        customer analysis and strategy recommendations.
        
        Args:
            customer_data: Customer data DataFrame
        """
        logger.info("Rendering chat interface")
        
        st.subheader("🤖 A.U.R.A AI Assistant")
        st.markdown("*Ask me anything about your customers, strategies, or data insights*")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.chat_history:
                self._display_message(message)
        
        # User input
        user_input = st.text_input(
            "Type your message here...",
            key="user_input",
            placeholder="e.g., 'Show me customers at high risk' or 'What strategies work best for SMB customers?'"
        )
        
        # Send button
        col1, col2, col3 = st.columns([1, 1, 8])
        
        with col1:
            if st.button("💬 Send", key="send_button"):
                if user_input:
                    self._process_user_input(user_input, customer_data)
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear", key="clear_button"):
                st.session_state.chat_history = []
                st.session_state.user_context = {}
                st.rerun()
        
        # Quick action buttons
        st.markdown("#### Quick Actions")
        self._render_quick_actions(customer_data)
    
    def _display_message(self, message: Dict[str, Any]) -> None:
        """
        Display a chat message.
        
        Args:
            message: Message dictionary with content and type
        """
        if message['type'] == 'user':
            with st.chat_message("user"):
                st.markdown(message['content'])
        else:
            with st.chat_message("assistant"):
                st.markdown(message['content'])
                
                # Display additional data if available
                if 'data' in message:
                    self._display_message_data(message['data'])
    
    def _display_message_data(self, data: Dict[str, Any]) -> None:
        """
        Display additional data associated with a message.
        
        Args:
            data: Data dictionary to display
        """
        if 'customers' in data:
            st.markdown("**Customer Details:**")
            customer_df = pd.DataFrame(data['customers'])
            st.dataframe(customer_df, use_container_width=True)
        
        if 'chart' in data:
            st.markdown("**Visualization:**")
            st.plotly_chart(data['chart'], use_container_width=True)
        
        if 'recommendations' in data:
            st.markdown("**Recommendations:**")
            for rec in data['recommendations']:
                st.markdown(f"- {rec}")
    
    def _process_user_input(self, user_input: str, customer_data: pd.DataFrame) -> None:
        """
        Process user input and generate response.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
        """
        logger.info(f"Processing user input: {user_input}")
        
        # Add user message to history
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Analyze user intent
        intent = self._analyze_user_intent(user_input)
        
        # Generate response based on intent
        response = self._generate_response(intent, user_input, customer_data)
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            'type': 'assistant',
            'content': response['content'],
            'data': response.get('data', {}),
            'timestamp': datetime.now()
        })
    
    def _analyze_user_intent(self, user_input: str) -> str:
        """
        Analyze user intent from input text.
        
        Args:
            user_input: User's input message
            
        Returns:
            str: Detected intent
        """
        user_input_lower = user_input.lower()
        
        # Intent classification based on keywords
        if any(word in user_input_lower for word in ['show', 'list', 'display', 'find', 'search']):
            if any(word in user_input_lower for word in ['customer', 'client', 'user']):
                return 'query_customers'
            elif any(word in user_input_lower for word in ['strategy', 'strategies', 'recommendation']):
                return 'query_strategies'
            else:
                return 'query_data'
        
        elif any(word in user_input_lower for word in ['risk', 'churn', 'health']):
            return 'analyze_risk'
        
        elif any(word in user_input_lower for word in ['strategy', 'recommend', 'suggest', 'advice']):
            return 'get_recommendations'
        
        elif any(word in user_input_lower for word in ['simulate', 'test', 'what if', 'impact']):
            return 'simulate_strategy'
        
        elif any(word in user_input_lower for word in ['help', 'how', 'what', 'explain']):
            return 'get_help'
        
        else:
            return 'general_query'
    
    def _generate_response(self, intent: str, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate response based on user intent.
        
        Args:
            intent: Detected user intent
            user_input: Original user input
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response with content and optional data
        """
        if intent == 'query_customers':
            return self._handle_customer_query(user_input, customer_data)
        
        elif intent == 'analyze_risk':
            return self._handle_risk_analysis(user_input, customer_data)
        
        elif intent == 'get_recommendations':
            return self._handle_recommendations_query(user_input, customer_data)
        
        elif intent == 'simulate_strategy':
            return self._handle_simulation_query(user_input, customer_data)
        
        elif intent == 'get_help':
            return self._handle_help_query()
        
        else:
            return self._handle_general_query(user_input, customer_data)
    
    def _handle_customer_query(self, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Handle customer data queries.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response with customer data
        """
        # Extract filters from user input
        filters = self._extract_filters_from_input(user_input)
        
        # Apply filters to customer data
        filtered_data = customer_data.copy()
        
        if 'risk_level' in filters:
            filtered_data = filtered_data[filtered_data['churn_risk_level'] == filters['risk_level']]
        
        if 'segment' in filters:
            filtered_data = filtered_data[filtered_data['client_segment'] == filters['segment']]
        
        if 'plan' in filters:
            filtered_data = filtered_data[filtered_data['current_subscription_plan'] == filters['plan']]
        
        # Generate response
        if len(filtered_data) == 0:
            content = "No customers found matching your criteria."
            data = {}
        else:
            content = f"Found {len(filtered_data)} customers matching your criteria:"
            data = {
                'customers': filtered_data[['customer_pk', 'first_name', 'last_name', 
                                         'churn_risk_level', 'current_health_score']].to_dict('records')
            }
        
        return {'content': content, 'data': data}
    
    def _handle_risk_analysis(self, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Handle risk analysis queries.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response with risk analysis
        """
        # Calculate risk metrics
        total_customers = len(customer_data)
        high_risk_count = len(customer_data[customer_data['churn_risk_level'] == 'High'])
        medium_risk_count = len(customer_data[customer_data['churn_risk_level'] == 'Medium'])
        low_risk_count = len(customer_data[customer_data['churn_risk_level'] == 'Low'])
        
        avg_health_score = customer_data['current_health_score'].mean()
        
        content = f"""
        **Risk Analysis Summary:**
        
        - **Total Customers:** {total_customers:,}
        - **High Risk:** {high_risk_count:,} ({high_risk_count/total_customers*100:.1f}%)
        - **Medium Risk:** {medium_risk_count:,} ({medium_risk_count/total_customers*100:.1f}%)
        - **Low Risk:** {low_risk_count:,} ({low_risk_count/total_customers*100:.1f}%)
        - **Average Health Score:** {avg_health_score:.1f}
        
        {'⚠️ **Alert:** High risk customers detected!' if high_risk_count > 0 else '✅ **Good:** No high risk customers detected.'}
        """
        
        return {'content': content}
    
    def _handle_recommendations_query(self, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Handle strategy recommendations queries.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response with recommendations
        """
        # Analyze customer segments
        risk_analysis = customer_data['churn_risk_level'].value_counts()
        
        recommendations = []
        
        if risk_analysis.get('High', 0) > 0:
            recommendations.append("🚨 **Immediate Action:** Implement proactive outreach for high-risk customers")
        
        if risk_analysis.get('Medium', 0) > 0:
            recommendations.append("📚 **Engagement:** Launch educational content campaigns for medium-risk customers")
        
        if risk_analysis.get('Low', 0) > 0:
            recommendations.append("💰 **Upsell:** Identify upsell opportunities for low-risk customers")
        
        content = f"""
        **Strategy Recommendations:**
        
        Based on your customer risk distribution, here are my recommendations:
        
        {chr(10).join(recommendations)}
        
        **Next Steps:**
        1. Review the Retention Strategies section for detailed implementation
        2. Use the Strategy Simulation tool to test different approaches
        3. Monitor results and adjust strategies based on outcomes
        """
        
        return {'content': content, 'data': {'recommendations': recommendations}}
    
    def _handle_simulation_query(self, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Handle strategy simulation queries.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response with simulation guidance
        """
        content = """
        **Strategy Simulation:**
        
        To simulate different retention strategies:
        
        1. **Go to the Retention Strategies section**
        2. **Select a strategy** from the available options
        3. **Use the Strategy Simulation tool** to test different scenarios
        4. **Review the results** and ROI projections
        
        **Available Strategies:**
        - Proactive Outreach Program
        - Retention Discount Program
        - Educational Content Campaign
        - Feature Training Program
        - Upsell Opportunity Identification
        - Support Escalation Protocol
        
        Each strategy includes detailed implementation steps and success metrics.
        """
        
        return {'content': content}
    
    def _handle_help_query(self) -> Dict[str, Any]:
        """
        Handle help queries.
        
        Returns:
            Dict[str, Any]: Response with help information
        """
        content = """
        **A.U.R.A AI Assistant Help:**
        
        I can help you with:
        
        **📊 Customer Analysis:**
        - "Show me high-risk customers"
        - "List customers by segment"
        - "Find customers with low health scores"
        
        **⚠️ Risk Analysis:**
        - "Analyze customer risk levels"
        - "What's our churn risk distribution?"
        - "Show me risk trends"
        
        **💡 Strategy Recommendations:**
        - "What strategies should I use?"
        - "Recommend strategies for SMB customers"
        - "How can I improve retention?"
        
        **🎮 Strategy Simulation:**
        - "Simulate retention strategies"
        - "Test different approaches"
        - "What's the ROI of proactive outreach?"
        
        **💬 General Queries:**
        - "Help me understand my data"
        - "What insights can you provide?"
        - "How can I improve customer success?"
        
        Just ask me anything in natural language!
        """
        
        return {'content': content}
    
    def _handle_general_query(self, user_input: str, customer_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Handle general queries.
        
        Args:
            user_input: User's input message
            customer_data: Customer data DataFrame
            
        Returns:
            Dict[str, Any]: Response to general query
        """
        # Generate a helpful response based on available data
        total_customers = len(customer_data)
        avg_health_score = customer_data['current_health_score'].mean()
        
        content = f"""
        **A.U.R.A Insights:**
        
        Based on your current data:
        
        - **Total Customers:** {total_customers:,}
        - **Average Health Score:** {avg_health_score:.1f}
        - **Risk Distribution:** {customer_data['churn_risk_level'].value_counts().to_dict()}
        
        **Quick Actions:**
        - Ask me to "show high-risk customers" for immediate attention
        - Request "strategy recommendations" for retention planning
        - Use "simulate strategies" to test different approaches
        
        **Need Help?** Just ask "help" for a full list of capabilities!
        """
        
        return {'content': content}
    
    def _extract_filters_from_input(self, user_input: str) -> Dict[str, str]:
        """
        Extract filters from user input.
        
        Args:
            user_input: User's input message
            
        Returns:
            Dict[str, str]: Extracted filters
        """
        filters = {}
        user_input_lower = user_input.lower()
        
        # Risk level filters
        if 'high risk' in user_input_lower or 'high-risk' in user_input_lower:
            filters['risk_level'] = 'High'
        elif 'medium risk' in user_input_lower or 'medium-risk' in user_input_lower:
            filters['risk_level'] = 'Medium'
        elif 'low risk' in user_input_lower or 'low-risk' in user_input_lower:
            filters['risk_level'] = 'Low'
        
        # Segment filters
        if 'smb' in user_input_lower or 'small business' in user_input_lower:
            filters['segment'] = 'SMB'
        elif 'enterprise' in user_input_lower:
            filters['segment'] = 'Enterprise'
        elif 'high-value' in user_input_lower or 'high value' in user_input_lower:
            filters['segment'] = 'High-Value'
        
        # Plan filters
        if 'basic' in user_input_lower:
            filters['plan'] = 'Basic'
        elif 'premium' in user_input_lower:
            filters['plan'] = 'Premium'
        elif 'enterprise' in user_input_lower:
            filters['plan'] = 'Enterprise'
        
        return filters
    
    def _render_quick_actions(self, customer_data: pd.DataFrame) -> None:
        """
        Render quick action buttons.
        
        Args:
            customer_data: Customer data DataFrame
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Show High-Risk Customers", key="quick_high_risk"):
                self._process_user_input("Show me high-risk customers", customer_data)
                st.rerun()
        
        with col2:
            if st.button("📊 Analyze Risk Distribution", key="quick_risk_analysis"):
                self._process_user_input("Analyze customer risk levels", customer_data)
                st.rerun()
        
        with col3:
            if st.button("💡 Get Strategy Recommendations", key="quick_recommendations"):
                self._process_user_input("What strategies should I use?", customer_data)
                st.rerun()
        
        # Additional quick actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Show Customer Health", key="quick_health"):
                self._process_user_input("Show me customer health scores", customer_data)
                st.rerun()
        
        with col2:
            if st.button("🎮 Simulate Strategies", key="quick_simulation"):
                self._process_user_input("How can I simulate retention strategies?", customer_data)
                st.rerun()
        
        with col3:
            if st.button("❓ Help", key="quick_help"):
                self._process_user_input("Help me understand what I can do", customer_data)
                st.rerun()

def main():
    """Main function to demonstrate chatbot interface functionality."""
    logger.info("Starting A.U.R.A chatbot interface demonstration")
    
    # Initialize chatbot interface
    chatbot_interface = ChatbotInterface()
    
    # Create sample customer data
    sample_data = pd.DataFrame({
        'customer_pk': [f'CUST_{i:03d}' for i in range(1, 21)],
        'first_name': ['John', 'Jane', 'Mike', 'Sarah'] * 5,
        'last_name': ['Smith', 'Johnson', 'Williams', 'Brown'] * 5,
        'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], 20, p=[0.6, 0.3, 0.1]),
        'current_health_score': np.random.normal(60, 20, 20),
        'client_segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], 20, p=[0.5, 0.3, 0.2]),
        'current_subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], 20)
    })
    
    print("\n" + "="*50)
    print("A.U.R.A Chatbot Interface Results")
    print("="*50)
    print(f"Sample data: {len(sample_data)} customers")
    print(f"Risk distribution: {sample_data['churn_risk_level'].value_counts().to_dict()}")
    print("Chatbot interface ready for interaction")
    
    logger.info("A.U.R.A chatbot interface demonstration completed")

if __name__ == "__main__":
    main()
