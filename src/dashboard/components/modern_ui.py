# A.U.R.A (Adaptive User Retention Assistant) - Modern UI Components
# This module provides React-like components for Streamlit with modern design patterns
# and enhanced user experience through custom HTML/CSS/JavaScript

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModernUI:
    """
    Modern UI components for A.U.R.A platform with React-like patterns.
    
    This class provides modern, interactive UI components that enhance
    the Streamlit experience with custom HTML, CSS, and JavaScript.
    """
    
    def __init__(self):
        """Initialize the modern UI components."""
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
        logger.info("Modern UI components initialized")
    
    def render_hero_section(self, title: str, subtitle: str, 
                          background_image: Optional[str] = None) -> None:
        """
        Render a modern hero section with gradient background.
        
        Args:
            title: Main hero title
            subtitle: Hero subtitle
            background_image: Optional background image URL
        """
        logger.info("Rendering hero section")
        
        hero_html = f"""
        <div class="hero-section" style="
            background: linear-gradient(135deg, {self.colors['primary']} 0%, {self.colors['secondary']} 100%);
            padding: 4rem 2rem;
            text-align: center;
            color: white;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        ">
            <div class="hero-content" style="
                position: relative;
                z-index: 2;
            ">
                <h1 style="
                    font-size: 3rem;
                    font-weight: 800;
                    margin-bottom: 1rem;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                ">{title}</h1>
                <p style="
                    font-size: 1.25rem;
                    margin-bottom: 2rem;
                    opacity: 0.9;
                ">{subtitle}</p>
                <div class="hero-actions" style="
                    display: flex;
                    gap: 1rem;
                    justify-content: center;
                    flex-wrap: wrap;
                ">
                    <button class="hero-btn primary" style="
                        background: rgba(255, 255, 255, 0.2);
                        border: 2px solid white;
                        color: white;
                        padding: 12px 24px;
                        border-radius: 50px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        backdrop-filter: blur(10px);
                    " onmouseover="this.style.background='rgba(255,255,255,0.3)'" 
                       onmouseout="this.style.background='rgba(255,255,255,0.2)'">
                        Get Started
                    </button>
                    <button class="hero-btn secondary" style="
                        background: transparent;
                        border: 2px solid white;
                        color: white;
                        padding: 12px 24px;
                        border-radius: 50px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    " onmouseover="this.style.background='white'; this.style.color='{self.colors['primary']}'" 
                       onmouseout="this.style.background='transparent'; this.style.color='white'">
                        Learn More
                    </button>
                </div>
            </div>
            <div class="hero-decoration" style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: float 6s ease-in-out infinite;
            "></div>
        </div>
        
        <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-20px) rotate(180deg); }}
        }}
        </style>
        """
        
        st.markdown(hero_html, unsafe_allow_html=True)
    
    def render_metric_cards(self, metrics: List[Dict[str, Any]], 
                          columns: int = 3) -> None:
        """
        Render modern metric cards with animations.
        
        Args:
            metrics: List of metric dictionaries with title, value, change, etc.
            columns: Number of columns for the grid
        """
        logger.info(f"Rendering {len(metrics)} metric cards")
        
        # Create grid layout
        cols = st.columns(columns)
        
        for i, metric in enumerate(metrics):
            with cols[i % columns]:
                self._render_single_metric_card(metric)
    
    def _render_single_metric_card(self, metric: Dict[str, Any]) -> None:
        """Render a single metric card with modern styling."""
        
        # Extract metric data
        title = metric.get('title', 'Metric')
        value = metric.get('value', '0')
        change = metric.get('change', None)
        change_type = metric.get('change_type', 'neutral')
        icon = metric.get('icon', '📊')
        color = metric.get('color', 'primary')
        
        # Determine change styling
        change_color = {
            'positive': self.colors['success'],
            'negative': self.colors['error'],
            'neutral': self.colors['info']
        }.get(change_type, self.colors['info'])
        
        change_icon = {
            'positive': '↗️',
            'negative': '↘️',
            'neutral': '→'
        }.get(change_type, '→')
        
        card_html = f"""
        <div class="metric-card" style="
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 40px rgba(0,0,0,0.15)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0,0,0,0.1)'">
            
            <div class="metric-header" style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            ">
                <div class="metric-icon" style="
                    font-size: 2rem;
                    opacity: 0.8;
                ">{icon}</div>
                <div class="metric-change" style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    color: {change_color};
                    font-weight: 600;
                    font-size: 0.9rem;
                ">
                    <span>{change_icon}</span>
                    <span>{change if change else '0%'}</span>
                </div>
            </div>
            
            <div class="metric-content">
                <div class="metric-title" style="
                    font-size: 0.9rem;
                    color: #666;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                ">{title}</div>
                <div class="metric-value" style="
                    font-size: 2rem;
                    font-weight: 800;
                    color: {self.colors[color]};
                    line-height: 1;
                ">{value}</div>
            </div>
            
            <div class="metric-decoration" style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, {self.colors[color]}20 0%, transparent 70%);
                pointer-events: none;
            "></div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
    
    def render_data_table(self, data: pd.DataFrame, 
                         title: str = "Data Table",
                         searchable: bool = True,
                         sortable: bool = True) -> None:
        """
        Render a modern data table with search and sort functionality.
        
        Args:
            data: DataFrame to display
            title: Table title
            searchable: Enable search functionality
            sortable: Enable sort functionality
        """
        logger.info(f"Rendering data table: {title}")
        
        # Table header
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0; color: {self.colors['dark']};">{title}</h3>
            <div style="
                display: flex;
                gap: 0.5rem;
                align-items: center;
            ">
                <span style="
                    background: {self.colors['info']};
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                ">{len(data)} records</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Search functionality
        if searchable:
            search_term = st.text_input(
                "🔍 Search",
                placeholder="Search in table...",
                key=f"search_{title}"
            )
            if search_term:
                # Simple search across all columns
                mask = data.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                data = data[mask]
        
        # Display table with modern styling
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )
    
    def render_chart_container(self, chart_html: str, 
                              title: str = "Chart",
                              description: str = "") -> None:
        """
        Render a modern chart container with title and description.
        
        Args:
            chart_html: HTML content for the chart
            title: Chart title
            description: Chart description
        """
        logger.info(f"Rendering chart container: {title}")
        
        container_html = f"""
        <div class="chart-container" style="
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        " onmouseover="this.style.transform='translateY(-2px)'" 
           onmouseout="this.style.transform='translateY(0)'">
            
            <div class="chart-header" style="
                margin-bottom: 1rem;
            ">
                <h3 style="
                    margin: 0 0 0.5rem 0;
                    color: {self.colors['dark']};
                    font-size: 1.5rem;
                    font-weight: 700;
                ">{title}</h3>
                {f'<p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>' if description else ''}
            </div>
            
            <div class="chart-content">
                {chart_html}
            </div>
        </div>
        """
        
        st.markdown(container_html, unsafe_allow_html=True)
    
    def render_loading_spinner(self, message: str = "Loading...") -> None:
        """
        Render a modern loading spinner.
        
        Args:
            message: Loading message
        """
        spinner_html = f"""
        <div class="loading-container" style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 3rem;
            text-align: center;
        ">
            <div class="spinner" style="
                width: 50px;
                height: 50px;
                border: 4px solid {self.colors['light']};
                border-top: 4px solid {self.colors['primary']};
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-bottom: 1rem;
            "></div>
            <p style="
                color: {self.colors['dark']};
                font-weight: 600;
                margin: 0;
            ">{message}</p>
        </div>
        
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
        """
        
        st.markdown(spinner_html, unsafe_allow_html=True)
    
    def render_notification(self, message: str, 
                           notification_type: str = "info",
                           duration: int = 3000) -> None:
        """
        Render a modern notification toast.
        
        Args:
            message: Notification message
            notification_type: Type of notification (success, error, warning, info)
            duration: Duration in milliseconds
        """
        colors = {
            'success': self.colors['success'],
            'error': self.colors['error'],
            'warning': self.colors['warning'],
            'info': self.colors['info']
        }
        
        icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        notification_html = f"""
        <div class="notification" style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: {colors.get(notification_type, self.colors['info'])};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 600;
            animation: slideInRight 0.3s ease-out;
            max-width: 400px;
        ">
            <span style="font-size: 1.2rem;">{icons.get(notification_type, 'ℹ️')}</span>
            <span>{message}</span>
        </div>
        
        <style>
        @keyframes slideInRight {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        
        <script>
        setTimeout(() => {{
            const notification = document.querySelector('.notification');
            if (notification) {{
                notification.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => notification.remove(), 300);
            }}
        }}, {duration});
        
        @keyframes slideOutRight {{
            from {{ transform: translateX(0); opacity: 1; }}
            to {{ transform: translateX(100%); opacity: 0; }}
        }}
        </script>
        """
        
        st.markdown(notification_html, unsafe_allow_html=True)
    
    def render_progress_bar(self, value: float, max_value: float = 100,
                          label: str = "", color: str = "primary") -> None:
        """
        Render a modern progress bar.
        
        Args:
            value: Current value
            max_value: Maximum value
            label: Progress bar label
            color: Progress bar color
        """
        percentage = (value / max_value) * 100
        
        progress_html = f"""
        <div class="progress-container" style="
            margin: 1rem 0;
        ">
            {f'<div style="margin-bottom: 0.5rem; font-weight: 600; color: {self.colors["dark"]};">{label}</div>' if label else ''}
            <div class="progress-bar-bg" style="
                background: {self.colors['light']};
                border-radius: 10px;
                height: 12px;
                overflow: hidden;
                position: relative;
            ">
                <div class="progress-bar-fill" style="
                    background: linear-gradient(90deg, {self.colors[color]} 0%, {self.colors['secondary']} 100%);
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 10px;
                    transition: width 0.5s ease;
                    position: relative;
                ">
                    <div class="progress-shine" style="
                        position: absolute;
                        top: 0;
                        left: -100%;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
                        animation: shine 2s infinite;
                    "></div>
                </div>
            </div>
            <div style="
                text-align: right;
                margin-top: 0.25rem;
                font-size: 0.9rem;
                color: {self.colors['dark']};
                font-weight: 600;
            ">{value}/{max_value} ({percentage:.1f}%)</div>
        </div>
        
        <style>
        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        </style>
        """
        
        st.markdown(progress_html, unsafe_allow_html=True)
    
    def render_modal(self, title: str, content: str, 
                    modal_id: str = "modal") -> None:
        """
        Render a modern modal dialog.
        
        Args:
            title: Modal title
            content: Modal content
            modal_id: Unique modal ID
        """
        modal_html = f"""
        <div id="{modal_id}" class="modal" style="
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 10000;
            backdrop-filter: blur(5px);
        ">
            <div class="modal-content" style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                border-radius: 20px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                animation: modalSlideIn 0.3s ease-out;
            ">
                <div class="modal-header" style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 1rem;
                ">
                    <h3 style="margin: 0; color: {self.colors['dark']};">{title}</h3>
                    <button onclick="document.getElementById('{modal_id}').style.display='none'" style="
                        background: none;
                        border: none;
                        font-size: 1.5rem;
                        cursor: pointer;
                        color: {self.colors['dark']};
                    ">×</button>
                </div>
                <div class="modal-body">
                    {content}
                </div>
            </div>
        </div>
        
        <style>
        @keyframes modalSlideIn {{
            from {{ opacity: 0; transform: translate(-50%, -60%); }}
            to {{ opacity: 1; transform: translate(-50%, -50%); }}
        }}
        </style>
        """
        
        st.markdown(modal_html, unsafe_allow_html=True)
    
    def render_tabs(self, tabs: List[Dict[str, str]], 
                   active_tab: str = None) -> str:
        """
        Render modern tab navigation.
        
        Args:
            tabs: List of tab dictionaries with 'id', 'label', 'icon'
            active_tab: Currently active tab ID
            
        Returns:
            str: Active tab ID
        """
        logger.info(f"Rendering {len(tabs)} tabs")
        
        tabs_html = f"""
        <div class="tabs-container" style="
            margin-bottom: 2rem;
        ">
            <div class="tabs-nav" style="
                display: flex;
                gap: 0.5rem;
                border-bottom: 2px solid {self.colors['light']};
                margin-bottom: 1rem;
            ">
        """
        
        for tab in tabs:
            tab_id = tab['id']
            label = tab['label']
            icon = tab.get('icon', '')
            is_active = active_tab == tab_id if active_tab else tab_id == tabs[0]['id']
            
            active_style = f"""
                background: {self.colors['primary']};
                color: white;
                border-bottom: 2px solid {self.colors['primary']};
            """ if is_active else f"""
                background: transparent;
                color: {self.colors['dark']};
                border-bottom: 2px solid transparent;
            """
            
            tabs_html += f"""
                <button class="tab-button" data-tab="{tab_id}" style="
                    {active_style}
                    border: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px 10px 0 0;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                " onmouseover="if(!this.classList.contains('active')) this.style.background='{self.colors['light']}'" 
                   onmouseout="if(!this.classList.contains('active')) this.style.background='transparent'">
                    <span>{icon}</span>
                    <span>{label}</span>
                </button>
            """
        
        tabs_html += """
            </div>
        </div>
        
        <script>
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.dataset.tab;
                
                // Update button states
                document.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                    btn.style.background = 'transparent';
                    btn.style.color = '#343a40';
                    btn.style.borderBottom = '2px solid transparent';
                });
                
                this.classList.add('active');
                this.style.background = '#667eea';
                this.style.color = 'white';
                this.style.borderBottom = '2px solid #667eea';
                
                // Trigger Streamlit rerun with tab selection
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    key: 'selected_tab',
                    value: tabId
                }, '*');
            });
        });
        </script>
        """
        
        st.markdown(tabs_html, unsafe_allow_html=True)
        
        # Return the active tab (this would need to be handled by the parent component)
        return active_tab or tabs[0]['id']

def main():
    """Main function to demonstrate modern UI components."""
    logger.info("Starting A.U.R.A modern UI components demonstration")
    
    # Initialize modern UI
    ui = ModernUI()
    
    print("\n" + "="*50)
    print("A.U.R.A Modern UI Components")
    print("="*50)
    print("Available components:")
    print("- Hero Section")
    print("- Metric Cards")
    print("- Data Tables")
    print("- Chart Containers")
    print("- Loading Spinners")
    print("- Notifications")
    print("- Progress Bars")
    print("- Modals")
    print("- Tabs")
    
    logger.info("A.U.R.A modern UI components demonstration completed")

if __name__ == "__main__":
    main()
