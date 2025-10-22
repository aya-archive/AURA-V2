# A.U.R.A (Adaptive User Retention Assistant) - Styling Utilities
# This module provides custom styling and theming for the A.U.R.A platform
# with consistent branding and user experience

import streamlit as st
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AURAStyling:
    """
    A.U.R.A styling utilities for consistent branding and user experience.
    
    This class provides comprehensive styling functions for the A.U.R.A platform
    including custom CSS, color schemes, typography, and component styling
    for a professional and cohesive user interface.
    """
    
    def __init__(self):
        """Initialize the A.U.R.A styling utilities."""
        self.colors = {
            'primary': '#004D7A',  # A.U.R.A Blue Deep
            'primary_light': '#E0EFF7',  # A.U.R.A Blue Light
            'accent': '#00B3B3',  # A.U.R.A Teal
            'success': '#28A745',  # Success Green
            'warning': '#FFC107',  # Warning Yellow
            'error': '#DC3545',  # Error Red
            'info': '#17A2B8',  # Info Blue
            'light_gray': '#F8F9FA',  # Light Gray
            'medium_gray': '#6C757D',  # Medium Gray
            'dark_gray': '#343A40',  # Dark Gray
            'white': '#FFFFFF',  # White
            'black': '#000000'  # Black
        }
        
        self.typography = {
            'font_family': 'Lato, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'font_size_base': '16px',
            'font_size_small': '14px',
            'font_size_large': '18px',
            'font_size_h1': '2.5rem',
            'font_size_h2': '2rem',
            'font_size_h3': '1.75rem',
            'font_size_h4': '1.5rem',
            'font_size_h5': '1.25rem',
            'font_size_h6': '1rem',
            'line_height': '1.5',
            'font_weight_normal': '400',
            'font_weight_bold': '700'
        }
        
        self.spacing = {
            'xs': '4px',
            'sm': '8px',
            'md': '16px',
            'lg': '24px',
            'xl': '32px',
            'xxl': '48px'
        }
        
        self.border_radius = {
            'sm': '4px',
            'md': '8px',
            'lg': '12px',
            'xl': '16px'
        }
        
        self.shadows = {
            'sm': '0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)',
            'md': '0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23)',
            'lg': '0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23)',
            'xl': '0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22)'
        }
        
        logger.info("A.U.R.A styling utilities initialized")
    
    def apply_custom_css(self) -> None:
        """
        Apply modern, beautiful CSS styling to the Streamlit application.
        
        This method injects modern CSS styles with animations, gradients,
        and contemporary design patterns for a stunning A.U.R.A experience.
        """
        logger.info("Applying modern CSS styling")
        
        custom_css = f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* A.U.R.A Modern Styling */
        
        /* Global Reset and Base Styles */
        * {{
            box-sizing: border-box;
        }}
        
        .main {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: {self.typography['font_size_base']};
            line-height: {self.typography['line_height']};
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }}
        
        /* Main Container */
        .main .block-container {{
            padding: 2rem 1rem;
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        /* Sidebar Styling */
        .css-1d391kg {{
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 0 20px 20px 0;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
        }}
        
        .css-1d391kg .css-1v0mbdj {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 1rem;
            margin: 1rem;
            backdrop-filter: blur(10px);
        }}
        
        /* Headers with Modern Typography */
        h1 {{
            color: {self.colors['primary']};
            font-size: {self.typography['font_size_h1']};
            font-weight: 800;
            margin-bottom: {self.spacing['lg']};
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        h2 {{
            color: {self.colors['primary']};
            font-size: {self.typography['font_size_h2']};
            font-weight: 700;
            margin-bottom: {self.spacing['md']};
            position: relative;
            padding-left: 1rem;
        }}
        
        h2::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 60%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}
        
        h3 {{
            color: {self.colors['dark_gray']};
            font-size: {self.typography['font_size_h3']};
            font-weight: 600;
            margin-bottom: {self.spacing['sm']};
        }}
        
        /* Modern Cards and Containers */
        .stMetric {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        
        .stMetric:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }}
        
        /* Modern Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Modern Selectbox */
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }}
        
        /* Modern Data Tables */
        .stDataFrame {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        /* Modern Charts */
        .stPlotlyChart {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        /* Loading Animation */
        .stSpinner {{
            color: #667eea;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.1);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .main .block-container {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding: 1rem 0.5rem;
                border-radius: 15px;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            h2 {{
                font-size: 1.5rem;
            }}
        }}
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {{
            .main {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }}
            
            .main .block-container {{
                background: rgba(0, 0, 0, 0.8);
                color: white;
            }}
        }}
        
        /* Custom Components */
        .aura-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        
        .aura-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }}
        
        .aura-gradient-text {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
        }}
        
        /* Status Indicators */
        .status-success {{
            color: #28a745;
            font-weight: 600;
        }}
        
        .status-warning {{
            color: #ffc107;
            font-weight: 600;
        }}
        
        .status-error {{
            color: #dc3545;
            font-weight: 600;
        }}
        
        /* Interactive Elements */
        .interactive-element {{
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .interactive-element:hover {{
            transform: scale(1.02);
        }}
        
        /* Modern Form Elements */
        .stTextInput > div > div > input {{
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        /* Modern Progress Bars */
        .stProgress > div > div > div {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }}
        
        /* Custom Alert Styles */
        .stAlert {{
            border-radius: 12px;
            border: none;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .stAlert[data-testid="stAlert"] {{
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
        }}
        
        /* Footer Styling */
        .stMarkdown {{
            text-align: center;
            color: {self.colors['medium_gray']};
            font-size: 0.9rem;
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 10px;
        }}
        
        /* Mobile Optimizations */
        @media (max-width: 480px) {{
            .main .block-container {{
                padding: 0.5rem;
                border-radius: 10px;
            }}
            
            .stMetric {{
                padding: 1rem;
            }}
            
            .stButton > button {{
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            .main {{
                background: white;
            }}
            
            .main .block-container {{
                background: white;
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
        
        /* Accessibility Improvements */
        .sr-only {{
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }}
        
        /* Focus States for Accessibility */
        button:focus,
        input:focus,
        select:focus {{
            outline: 2px solid #667eea;
            outline-offset: 2px;
        }}
        
        /* High Contrast Mode Support */
        @media (prefers-contrast: high) {{
            .main {{
                background: white;
            }}
            
            .main .block-container {{
                background: white;
                border: 2px solid black;
            }}
        }}
        
        /* Reduced Motion Support */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        </style>
        """
        
        st.markdown(custom_css, unsafe_allow_html=True)
        logger.info("Modern CSS styling applied successfully")
    
    def add_javascript_enhancements(self) -> None:
        """
        Add JavaScript enhancements for better interactivity.
        
        This method injects JavaScript code to enhance the user experience
        with animations, smooth scrolling, and interactive elements.
        """
        logger.info("Adding JavaScript enhancements")
        
        js_code = """
        <script>
        // A.U.R.A JavaScript Enhancements
        
        // Smooth scrolling for anchor links
        document.addEventListener('DOMContentLoaded', function() {
            // Add smooth scrolling
            const links = document.querySelectorAll('a[href^="#"]');
            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
            
            // Add loading animations
            const elements = document.querySelectorAll('.stMetric, .aura-card, .stDataFrame');
            elements.forEach((element, index) => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    element.style.transition = 'all 0.6s ease-out';
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, index * 100);
            });
            
            // Add hover effects for interactive elements
            const interactiveElements = document.querySelectorAll('.stButton button, .stMetric, .aura-card');
            interactiveElements.forEach(element => {
                element.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
                });
                
                element.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
                });
            });
            
            // Add click animations for buttons
            const buttons = document.querySelectorAll('.stButton button');
            buttons.forEach(button => {
                button.addEventListener('click', function() {
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                    }, 150);
                });
            });
            
            // Add typing animation for text elements
            const textElements = document.querySelectorAll('h1, h2, h3');
            textElements.forEach(element => {
                const text = element.textContent;
                element.textContent = '';
                element.style.borderRight = '2px solid #667eea';
                
                let i = 0;
                const typeWriter = () => {
                    if (i < text.length) {
                        element.textContent += text.charAt(i);
                        i++;
                        setTimeout(typeWriter, 50);
                    } else {
                        element.style.borderRight = 'none';
                    }
                };
                
                setTimeout(typeWriter, 500);
            });
            
            // Add parallax effect for background
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const parallax = document.querySelector('.main');
                if (parallax) {
                    const speed = scrolled * 0.5;
                    parallax.style.transform = `translateY(${speed}px)`;
                }
            });
            
            // Add tooltip functionality
            const tooltipElements = document.querySelectorAll('[data-tooltip]');
            tooltipElements.forEach(element => {
                element.addEventListener('mouseenter', function() {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'aura-tooltip';
                    tooltip.textContent = this.getAttribute('data-tooltip');
                    tooltip.style.cssText = `
                        position: absolute;
                        background: rgba(0, 0, 0, 0.8);
                        color: white;
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-size: 14px;
                        z-index: 1000;
                        pointer-events: none;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    `;
                    document.body.appendChild(tooltip);
                    
                    const rect = this.getBoundingClientRect();
                    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
                    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
                    
                    setTimeout(() => tooltip.style.opacity = '1', 10);
                });
                
                element.addEventListener('mouseleave', function() {
                    const tooltip = document.querySelector('.aura-tooltip');
                    if (tooltip) {
                        tooltip.style.opacity = '0';
                        setTimeout(() => tooltip.remove(), 300);
                    }
                });
            });
            
            // Add keyboard navigation
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Tab') {
                    document.body.classList.add('keyboard-navigation');
                }
            });
            
            document.addEventListener('mousedown', function() {
                document.body.classList.remove('keyboard-navigation');
            });
            
            // Add focus indicators for accessibility
            const focusableElements = document.querySelectorAll('button, input, select, a');
            focusableElements.forEach(element => {
                element.addEventListener('focus', function() {
                    this.style.outline = '2px solid #667eea';
                    this.style.outlineOffset = '2px';
                });
                
                element.addEventListener('blur', function() {
                    this.style.outline = 'none';
                });
            });
            
            // Add dark mode toggle functionality
            const darkModeToggle = document.querySelector('[data-dark-mode]');
            if (darkModeToggle) {
                darkModeToggle.addEventListener('click', function() {
                    document.body.classList.toggle('dark-mode');
                    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
                });
                
                // Load saved dark mode preference
                if (localStorage.getItem('darkMode') === 'true') {
                    document.body.classList.add('dark-mode');
                }
            }
            
            // Add performance monitoring
            if ('performance' in window) {
                window.addEventListener('load', function() {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                });
            }
            
            // Add error handling for failed images
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                img.addEventListener('error', function() {
                    this.style.display = 'none';
                });
            });
            
            // Add responsive image loading
            const lazyImages = document.querySelectorAll('img[data-src]');
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        });
        
        // Add custom event listeners for Streamlit components
        window.addEventListener('load', function() {
            // Monitor Streamlit component updates
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        // Re-apply animations to new elements
                        const newElements = Array.from(mutation.addedNodes).filter(node => 
                            node.nodeType === Node.ELEMENT_NODE
                        );
                        
                        newElements.forEach(element => {
                            if (element.classList.contains('stMetric') || 
                                element.classList.contains('aura-card')) {
                                element.style.opacity = '0';
                                element.style.transform = 'translateY(20px)';
                                
                                setTimeout(() => {
                                    element.style.transition = 'all 0.6s ease-out';
                                    element.style.opacity = '1';
                                    element.style.transform = 'translateY(0)';
                                }, 100);
                            }
                        });
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
        
        // Add utility functions
        window.AURA = {
            // Smooth scroll to element
            scrollTo: function(elementId) {
                const element = document.getElementById(elementId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                }
            },
            
            // Show notification
            notify: function(message, type = 'info') {
                const notification = document.createElement('div');
                notification.className = `aura-notification aura-notification-${type}`;
                notification.textContent = message;
                notification.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    z-index: 10000;
                    opacity: 0;
                    transform: translateX(100%);
                    transition: all 0.3s ease;
                `;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.opacity = '1';
                    notification.style.transform = 'translateX(0)';
                }, 10);
                
                setTimeout(() => {
                    notification.style.opacity = '0';
                    notification.style.transform = 'translateX(100%)';
                    setTimeout(() => notification.remove(), 300);
                }, 3000);
            },
            
            // Toggle theme
            toggleTheme: function() {
                document.body.classList.toggle('dark-mode');
                localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
            }
        };
        </script>
        """
        
        st.markdown(js_code, unsafe_allow_html=True)
        logger.info("JavaScript enhancements added successfully")
    
    def create_metric_card(self, title: str, value: str, delta: Optional[str] = None, 
                         color: str = 'primary') -> str:
        """
        Create a styled metric card.
        
        Args:
            title: Metric title
            value: Metric value
            delta: Optional delta value
            color: Color theme for the card
            
        Returns:
            str: HTML for the metric card
        """
        color_class = f"text-{color}" if color in ['primary', 'accent', 'success', 'warning', 'error'] else "text-primary"
        
        delta_html = f'<div class="text-muted">{delta}</div>' if delta else ''
        
        return f"""
        <div class="metric-container fade-in">
            <div class="metric-label">{title}</div>
            <div class="metric-value {color_class}">{value}</div>
            {delta_html}
        </div>
        """
    
    def create_info_card(self, title: str, content: str, icon: str = "ℹ️") -> str:
        """
        Create a styled info card.
        
        Args:
            title: Card title
            content: Card content
            icon: Optional icon for the card
            
        Returns:
            str: HTML for the info card
        """
        return f"""
        <div class="aura-card fade-in">
            <h4>{icon} {title}</h4>
            <p>{content}</p>
        </div>
        """
    
    def create_alert(self, message: str, alert_type: str = 'info') -> str:
        """
        Create a styled alert message.
        
        Args:
            message: Alert message
            alert_type: Type of alert (success, warning, error, info)
            
        Returns:
            str: HTML for the alert
        """
        alert_class = f"st{alert_type.capitalize()}" if alert_type in ['success', 'warning', 'error', 'info'] else 'stInfo'
        
        return f"""
        <div class="{alert_class} slide-in">
            {message}
        </div>
        """
    
    def create_badge(self, text: str, color: str = 'primary') -> str:
        """
        Create a styled badge.
        
        Args:
            text: Badge text
            color: Badge color theme
            
        Returns:
            str: HTML for the badge
        """
        color_class = f"bg-{color}" if color in ['primary', 'accent', 'success', 'warning', 'error'] else "bg-primary"
        
        return f"""
        <span class="badge {color_class} text-white rounded p-sm m-xs">
            {text}
        </span>
        """
    
    def create_progress_bar(self, value: float, max_value: float = 100, 
                           color: str = 'primary') -> str:
        """
        Create a styled progress bar.
        
        Args:
            value: Current value
            max_value: Maximum value
            color: Progress bar color
            
        Returns:
            str: HTML for the progress bar
        """
        percentage = (value / max_value) * 100
        color_class = f"bg-{color}" if color in ['primary', 'accent', 'success', 'warning', 'error'] else "bg-primary"
        
        return f"""
        <div class="progress-container">
            <div class="progress-bar {color_class} rounded" 
                 style="width: {percentage}%; height: 8px; background-color: {self.colors.get(color, self.colors['primary'])};">
            </div>
        </div>
        """
    
    def apply_theme_colors(self) -> Dict[str, str]:
        """
        Get theme colors for use in components.
        
        Returns:
            Dict[str, str]: Dictionary of theme colors
        """
        return self.colors.copy()
    
    def get_typography_styles(self) -> Dict[str, str]:
        """
        Get typography styles for use in components.
        
        Returns:
            Dict[str, str]: Dictionary of typography styles
        """
        return self.typography.copy()
    
    def get_spacing_values(self) -> Dict[str, str]:
        """
        Get spacing values for use in components.
        
        Returns:
            Dict[str, str]: Dictionary of spacing values
        """
        return self.spacing.copy()

def main():
    """Main function to demonstrate styling utilities."""
    logger.info("Starting A.U.R.A styling utilities demonstration")
    
    # Initialize styling utilities
    styling = AURAStyling()
    
    print("\n" + "="*50)
    print("A.U.R.A Styling Utilities")
    print("="*50)
    print(f"Colors: {len(styling.colors)} defined")
    print(f"Typography: {len(styling.typography)} styles")
    print(f"Spacing: {len(styling.spacing)} values")
    print(f"Border radius: {len(styling.border_radius)} sizes")
    print(f"Shadows: {len(styling.shadows)} levels")
    
    logger.info("A.U.R.A styling utilities demonstration completed")

if __name__ == "__main__":
    main()
