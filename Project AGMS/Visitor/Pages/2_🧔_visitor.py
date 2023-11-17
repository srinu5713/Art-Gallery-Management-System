import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image
from pandas import option_context
from IPython.display import display
from streamlit_extras.switch_page_button import switch_page
import os
from datetime import datetime  # Updated import statement
import sys
sys.path.append('C:/Users/HP/Documents/GitHub/agms/AGMS_Modules')
import View_task
import View_Artwork
import Ticket_book
import View_ticket
import Guide_book
import view_guide
import view_logs
import view_credentials


if 'isVisitor' not in st.session_state:
    st.session_state.isVisitor = False

if 'username' not in st.session_state:
    st.session_state.username = ''


username=st.session_state.username


def do_book():
    Ticket_book.do_ticket_book(username)


def view_ticket():
   View_ticket.do_view_ticket(username) 

def guide_book():
    Guide_book.do_guide_book(username)


def do_logs():
    view_logs.do_logs(username)


if st.session_state.isVisitor:
    # st.header('Visitor Dashboard')

    def do_logout():
        st.markdown("### Logout")
        st.warning('Are you sure, you want to logout?', icon="⚠️")
        if st.button("Yes", key="logout_yes_button"):
            st.markdown("###Logout successfully")
            switch_page('login')

        elif st.button("No", key="logout_no_button"):
            st.markdown("### Continue")

    styles = {
        "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#03dffc"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#fcd303"},
        "nav-link-selected": {"background-color": "#fcd303", "font-size": "20px", "font-weight": "normal", "color": "black", },
    }

    menu = {
        'title': 'User',
        'items': {
            'Home': {
                'action': None, 'item_icon': 'terminal-dash', 'submenu': {
                    'title': None,
                    'items': {
                        'View Tasks': {'action': View_task.do_view_tasks, 'item_icon': 'list-task', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Ticket Booking': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'Ticket Booking': {'action': do_book, 'item_icon': 'key', 'submenu': None},
                        'View Booked Tickets': {'action':view_ticket, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Guide Booking': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'Guide Booking': {'action': guide_book, 'item_icon': 'key', 'submenu': None},
                        'View Guide Details': {'action': view_guide.do_view_guide, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'View Gallery': {
                'action': None, 'item_icon': 'ticket-perforated', 'submenu': {
                    'title': None,

                    'items': {
                        'View Artwork': {'action': View_Artwork.do_view_artw, 'item_icon': 'key', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Review Artworks': {
                'action': None, 'item_icon': 'gear', 'submenu': {
                    'title': None,
                    'items': {
                        'View Reviews': {'action': view_credentials.do_credentials, 'item_icon': 'key', 'submenu': None},
                        'Share your experience': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Logout': {
                'action': None, 'item_icon': 'box-arrow-left', 'submenu': {
                    'title': None,
                    'items': {
                        'Logout': {'action': do_logout, 'item_icon': 'key', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            }


        },
        'menu_icon': 'person-fill-check',
        'default_index': 0,
        'with_view_panel': 'sidebar',
        'orientation': 'vertical',
        'styles': styles
    }

    def show_menu(menu):
        def _get_options(menu):
            options = list(menu['items'].keys())
            return options

        def _get_icons(menu):
            icons = [v['item_icon'] for _k, v in menu['items'].items()]
            return icons

        kwargs = {
            'menu_title': menu['title'],
            'options': _get_options(menu),
            'icons': _get_icons(menu),
            'menu_icon': menu['menu_icon'],
            'default_index': menu['default_index'],
            'orientation': menu['orientation'],
            'styles': menu['styles']
        }

        with_view_panel = menu['with_view_panel']
        if with_view_panel == 'sidebar':
            with st.sidebar:
                menu_selection = option_menu(**kwargs)
        elif with_view_panel == 'main':
            menu_selection = option_menu(**kwargs)
        else:
            raise ValueError(
                f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")

        if menu['items'][menu_selection]['submenu']:
            show_menu(menu['items'][menu_selection]['submenu'])

        if menu['items'][menu_selection]['action']:
            menu['items'][menu_selection]['action']()

    show_menu(menu)


else:
    st.write("Please Login First !!")
