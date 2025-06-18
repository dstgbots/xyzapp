from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem, IconLeftWidget
from kivymd.icon_definitions import md_icons
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from database import DatabaseManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabs, MDTabsBase

class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "welcome"
        
        main_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color="#4A2C2A",  
            spacing=dp(40)
        )
        
        
        welcome_label = MDLabel(
            text="GetBandish",
            theme_text_color="Custom",
            text_color="#D4AF37",  
            halign="center",
            font_style="H3",
            bold=True,
            pos_hint={"center_y": 0.6}
        )
        
        
        loading_label = MDLabel(
            text="Loading Classical Music Database...",
            theme_text_color="Custom", 
            text_color="#8B4513",  
            halign="center",
            font_style="Body1",
            pos_hint={"center_y": 0.4}
        )
        
        main_layout.add_widget(welcome_label)
        main_layout.add_widget(loading_label)
        self.add_widget(main_layout)
        
        
        Clock.schedule_once(self.switch_to_main, 3)
    
    def switch_to_main(self, dt):
        self.manager.transition.direction = "left"
        self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        self.db_manager = db_manager
        self.wishlist_mode = False
        
        
        self.root_layout = MDBoxLayout(orientation="vertical")
        
        
        self.nav_drawer = MDNavigationDrawer(
            radius=(0, 16, 16, 0),
            elevation=4,
            close_on_click=True
        )
        
        
        nav_content = MDScrollView()
        nav_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
            padding=dp(10)
        )
        
        
        header_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            md_bg_color="#8B4513",
            radius=[0]
        )
        header_label = MDLabel(
            text="GetBandish Menu",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            halign="center",
            bold=True
        )
        header_card.add_widget(header_label)
        nav_box.add_widget(header_card)
        
        
        menu_list = MDList()
        
        
        menu_items = [
            {"icon": "music-note", "text": "Create Concert", "callback": self.create_concert},
            {"icon": "help-circle", "text": "Help", "callback": self.show_help},
            {"icon": "cog", "text": "Settings", "callback": self.show_settings},
            {"icon": "information", "text": "About Us", "callback": self.show_about},
            {"icon": "shield-account", "text": "Admin Control", "callback": self.show_admin_control},
        ]
        
        for item in menu_items:
            menu_item = OneLineIconListItem(
                text=item["text"],
                on_release=item["callback"],
                theme_text_color="Custom",
                text_color="#8B4513"
            )
            menu_item.add_widget(IconLeftWidget(
                icon=item["icon"],
                theme_icon_color="Custom",
                icon_color="#8B4513"
            ))
            menu_list.add_widget(menu_item)
        
        nav_box.add_widget(menu_list)
        nav_content.add_widget(nav_box)
        self.nav_drawer.add_widget(nav_content)
        
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        
        self.toolbar = MDTopAppBar(
            title="Search by Raaga",
            md_bg_color="#8B4513",  
            specific_text_color="#FFFFFF",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[
                ["heart-outline", lambda x: self.toggle_wishlist_mode()], 
                ["magnify", lambda x: self.show_search_dialog()]
            ]
        )
        main_layout.add_widget(self.toolbar)
        
        
        scroll = MDScrollView()
        self.raaga_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
            padding=dp(20)
        )
        
        
        self.load_raagas(self.raaga_layout)
        
        scroll.add_widget(self.raaga_layout)
        main_layout.add_widget(scroll)
        
        
        self.root_layout.add_widget(main_layout)
        
        
        self.add_widget(self.root_layout)
        self.add_widget(self.nav_drawer)
    
    def load_raagas(self, layout):

        raagas = self.db_manager.get_all_raagas(favorites_only=self.wishlist_mode)
        
        
        layout.clear_widgets()
        
        
        if self.wishlist_mode and not raagas:
            no_favorites_label = MDLabel(
                text="No favorite raagas added yet.\nClick the heart icon on any raaga to add it to your wishlist.",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=dp(200)
            )
            layout.add_widget(no_favorites_label)
            return
        
        for raaga_id, raaga_name, is_active, is_favorite in raagas:
            
            card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(80),
                elevation=3,
                md_bg_color="#FFF8DC",  
                radius=[10]
            )
            
            card.raaga_id = raaga_id
            
            
            header_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(40)
            )
            
            
            name_label = MDLabel(
                text=raaga_name,
                theme_text_color="Custom",
                text_color="#8B4513",  
                font_style="H6",
                bold=True if is_active else False,
                size_hint_x=0.9
            )
            
            
            favorite_icon = "heart" if is_favorite else "heart-outline"
            favorite_button = MDIconButton(
                icon=favorite_icon,
                theme_icon_color="Custom",
                icon_color="#D4AF37" if is_favorite else "#8B4513",  
                size_hint_x=0.1,
                on_release=lambda x, rid=raaga_id: self.toggle_raaga_favorite(rid)
            )
            
            header_layout.add_widget(name_label)
            header_layout.add_widget(favorite_button)
            
            
            status_label = MDLabel(
                text="Available" if is_active else "Coming Soon",
                theme_text_color="Custom",
                text_color="#228B22" if is_active else "#CD853F",  
                font_style="Caption",
                size_hint_y=None,
                height=dp(20)
            )
            
            
            card.bind(on_release=lambda x, name=raaga_name: self.select_raaga(name))
            
            card.add_widget(header_layout)
            card.add_widget(status_label)
            layout.add_widget(card)
    
    def select_raaga(self, raaga_name):
        """Navigate directly to bandish list regardless of raaga status"""
        bandish_screen = self.manager.get_screen("bandish_list")
        bandish_screen.load_bandish(raaga_name)
        self.manager.transition.direction = "left"
        self.manager.current = "bandish_list"
    
    def toggle_nav_drawer(self):
        """Toggle navigation drawer"""
        self.nav_drawer.set_state("open" if self.nav_drawer.state == "close" else "close")
    
    def create_concert(self, *args):
        """Navigate to concert management screen"""
        self.nav_drawer.set_state("close")
        self.manager.transition.direction = "left"
        self.manager.current = "concert_list"
    
    def show_help(self, *args):
        """Show help information"""
        self.nav_drawer.set_state("close")
        help_text = """GetBandish Help

How to use:
• Browse raagas from the main list
• Tap on 'Abhogi / Abhogi Kanada' (active raaga)
• View available bandish compositions
• Tap any bandish to see full lyrics

Navigation:
• Use the menu (☰) for more options
• Use the search (🔍) for quick access
• Use back arrows (←) to navigate

Tips:
• Only active raagas have bandish available
• More raagas will be added in future updates
• Use Admin Control to manage database"""
        
        dialog = MDDialog(
            title="Help",
            text=help_text,
            buttons=[
                MDFlatButton(
                    text="GOT IT",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_settings(self, *args):
        """Show settings"""
        self.nav_drawer.set_state("close")
        dialog = MDDialog(
            title="Settings",
            text="Settings feature coming soon!\n\nFuture settings will include:\n• Theme customization\n• Font size adjustment\n• Language preferences\n• Notification settings",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_about(self, *args):
        """Show about us information"""
        self.nav_drawer.set_state("close")
        stats = self.db_manager.get_database_stats()
        about_text = f"""About GetBandish

GetBandish is a classical Indian music app created by K Kousthubh Bhat, a BCA 2nd Year student.

Our Mission:
To preserve and share the beauty of classical Indian music compositions (bandish) with music enthusiasts worldwide.

Database Statistics:
• Total Raagas: {stats['total_raagas']}
• Active Raagas: {stats['active_raagas']}
• Total Bandish: {stats['total_bandish']}

Version: 2.0 (SQLite Edition)
Platform: Android & Windows

Contact: K Kousthubh Bhat
© 2024 GetBandish Project"""
        
        dialog = MDDialog(
            title="About Us",
            text=about_text,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def show_admin_control(self, *args):
        """Navigate to admin login screen"""
        self.nav_drawer.set_state("close")
        self.manager.transition.direction="left"
        self.manager.current="admin_login"
    
    def show_search_dialog(self):
        """Navigate to comprehensive search screen"""
        self.manager.transition.direction = "left"
        self.manager.current = "search"
    
    def show_coming_soon_dialog(self):
        dialog = MDDialog(
            title="Coming Soon",
            text="This raaga will be available in future updates!",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def toggle_wishlist_mode(self):
        """Toggle between all raagas and favorite raagas"""
        self.wishlist_mode = not self.wishlist_mode
        
        
        if self.wishlist_mode:
            self.toolbar.title = "Wishlists"
            self.toolbar.right_action_items = [["heart", lambda x: self.toggle_wishlist_mode()], ["magnify", lambda x: self.show_search_dialog()]]
            self.toolbar.left_action_items = [["arrow-left", lambda x: self.toggle_wishlist_mode()], ["menu", lambda x: self.toggle_nav_drawer()]]
        else:
            self.toolbar.title = "Search by Raaga"
            self.toolbar.right_action_items = [["heart-outline", lambda x: self.toggle_wishlist_mode()], ["magnify", lambda x: self.show_search_dialog()]]
            self.toolbar.left_action_items = [["menu", lambda x: self.toggle_nav_drawer()]]
        
        
        self.load_raagas(self.raaga_layout)

    def toggle_raaga_favorite(self, raaga_id):
        """Toggle favorite status of a raaga"""
        is_favorite = self.db_manager.toggle_raaga_favorite(raaga_id)
        
        
        if self.wishlist_mode and not is_favorite:
            self.load_raagas(self.raaga_layout)
            return
        
        
        for card in self.raaga_layout.children:
            if getattr(card, 'raaga_id', None) == raaga_id:
                
                for widget in card.children:
                    if isinstance(widget, MDBoxLayout):
                        for icon_btn in widget.children:
                            if isinstance(icon_btn, MDIconButton):
                                icon_btn.icon = "heart" if is_favorite else "heart-outline"
                                icon_btn.icon_color = "#D4AF37" if is_favorite else "#8B4513"
                                break
                break

class BandishListScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "bandish_list"
        self.db_manager = db_manager
        self.current_raaga = ""
        self.wishlist_mode = False
        
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        
        self.toolbar = MDTopAppBar(
            title="Bandish List",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["heart-outline", lambda x: self.toggle_wishlist_mode()]]
        )
        main_layout.add_widget(self.toolbar)
        
        
        self.scroll = MDScrollView()
        self.bandish_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
            padding=dp(20)
        )
        
        self.scroll.add_widget(self.bandish_layout)
        main_layout.add_widget(self.scroll)
        self.add_widget(main_layout)
    
    def load_bandish(self, raaga_name):
        """Load bandish for selected raaga from database"""
        self.current_raaga = raaga_name
        self.toolbar.title = f"Bandish - {raaga_name}" if not self.wishlist_mode else "Wishlist - Bandish"
        
        
        self.bandish_layout.clear_widgets()
        
        
        bandish_list = self.db_manager.get_bandish_by_raaga(raaga_name, favorites_only=self.wishlist_mode)
        
        if not bandish_list:
            
            message = "No favorite bandish for this raaga." if self.wishlist_mode else "No bandish found for this raaga."
            no_data_label = MDLabel(
                text=message,
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="H6"
            )
            self.bandish_layout.add_widget(no_data_label)
            return
        
        for bandish_id, title, raaga, taal, bandish_type, lyrics, is_favorite in bandish_list:
            
            card = MDCard(
                orientation="vertical",
                padding=dp(15),
                size_hint_y=None,
                height=dp(120),
                elevation=4,
                md_bg_color="#FFF8DC",  
                radius=[15]
            )
            
            
            header_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(40)
            )
            
            # Title
            title_label = MDLabel(
                text=title,
                theme_text_color="Custom",
                text_color="#8B4513",
                font_style="H6",
                bold=True,
                size_hint_x=0.9
            )
            
            # Favorite button
            favorite_icon = "heart" if is_favorite else "heart-outline"
            favorite_button = MDIconButton(
                icon=favorite_icon,
                theme_icon_color="Custom",
                icon_color="#D4AF37" if is_favorite else "#8B4513",  # Gold if favorited, brown if not
                size_hint_x=0.1,
                on_release=lambda x, bid=bandish_id: self.toggle_bandish_favorite(bid)
            )
            
            header_layout.add_widget(title_label)
            header_layout.add_widget(favorite_button)
            
            
            details_layout = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(20),
                size_hint_y=None,
                height=dp(60)
            )
            
            
            raaga_label = MDLabel(
                text=f"Raaga: {raaga}",
                theme_text_color="Custom",
                text_color="#654321",
                font_style="Body2",
                size_hint_x=0.4
            )
            
            
            taal_label = MDLabel(
                text=f"Taal: {taal}",
                theme_text_color="Custom",
                text_color="#654321",
                font_style="Body2",
                size_hint_x=0.3
            )
            
            
            type_label = MDLabel(
                text=f"Type: {bandish_type}",
                theme_text_color="Custom",
                text_color="#654321",
                font_style="Body2",
                size_hint_x=0.3
            )
            
            details_layout.add_widget(raaga_label)
            details_layout.add_widget(taal_label)
            details_layout.add_widget(type_label)
            
            
            card.bandish_id = bandish_id
            card.bind(on_release=lambda x, bid=bandish_id: self.view_bandish_details(bid))
            
            card.add_widget(header_layout)
            card.add_widget(details_layout)
            self.bandish_layout.add_widget(card)
    
    def view_bandish_details(self, bandish_id):
        """View detailed bandish information"""
        self.manager.get_screen("bandish_detail").load_bandish_detail(bandish_id)
        self.manager.transition.direction = "left"
        self.manager.current = "bandish_detail"
    
    def go_back(self):
        """Go back to main screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "main"
    
    def toggle_wishlist_mode(self):
        """Toggle between all bandish and favorite bandish"""
        self.wishlist_mode = not self.wishlist_mode
        
        
        if self.wishlist_mode:
            self.toolbar.title = "Wishlist - Bandish"
            
            self.toolbar.left_action_items = [
                ["arrow-left", lambda x: self.toggle_wishlist_mode()]
            ]
            
            self.toolbar.right_action_items = [
                ["heart", lambda x: self.toggle_wishlist_mode()]
            ]
        else:
            self.toolbar.title = f"Bandish - {self.current_raaga}"
            
            self.toolbar.left_action_items = [
                ["arrow-left", lambda x: self.go_back()]
            ]
            
            self.toolbar.right_action_items = [
                ["heart-outline", lambda x: self.toggle_wishlist_mode()]
            ]

        
        self.load_bandish(self.current_raaga)
    
    def toggle_bandish_favorite(self, bandish_id):
        """Toggle favorite status of a bandish"""
        is_favorite = self.db_manager.toggle_bandish_favorite(bandish_id)
        
        
        if self.wishlist_mode:
            self.load_bandish(self.current_raaga)
        else:
            
            for child in self.bandish_layout.children:
                if hasattr(child, 'bandish_id') and child.bandish_id == bandish_id:
                    # Update just the heart icon
                    for widget in child.children:
                        if isinstance(widget, MDBoxLayout) and len(widget.children) > 1:
                            for icon_btn in widget.children:
                                if isinstance(icon_btn, MDIconButton):
                                    icon_btn.icon = "heart" if is_favorite else "heart-outline"
                                    icon_btn.icon_color = "#D4AF37" if is_favorite else "#8B4513"
                    break
            else:
                
                self.load_bandish(self.current_raaga)

class BandishDetailScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "bandish_detail"
        self.db_manager = db_manager
        
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        
        self.toolbar = MDTopAppBar(
            title="Bandish Details",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["heart-outline", lambda x: self.toggle_favorite(0)]]
        )
        main_layout.add_widget(self.toolbar)
        
        
        self.scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            padding=dp(20)
        )
        
        self.scroll.add_widget(self.content_layout)
        main_layout.add_widget(self.scroll)
        self.add_widget(main_layout)
    
    def load_bandish_detail(self, bandish_id):
        """Load detailed bandish information from database"""
        
        self.content_layout.clear_widgets()
        
        
        bandish = self.db_manager.get_bandish_by_id(bandish_id)
        
        if not bandish:
            error_label = MDLabel(
                text="Bandish not found!",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="H6"
            )
            self.content_layout.add_widget(error_label)
            return
        
        bid, title, raaga, taal, bandish_type, lyrics, is_favorite = bandish
        
        
        self.toolbar.title = "Bandish Details"
        
        
        favorite_icon = "heart" if is_favorite else "heart-outline"
        self.toolbar.right_action_items = [
            [favorite_icon, lambda x, bid=bid: self.toggle_favorite(bid)]
        ]
        
        
        title_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=5,
            md_bg_color="#D4AF37",  
            radius=[15]
        )
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Custom",
            text_color="#FFFFFF",
            font_style="H5",
            bold=True,
            halign="center",
            text_size=(None, None),
            size_hint_y=None
        )
        
        
        def update_title_text_size(instance, size):
            title_label.text_size = (size[0] - dp(40), None)
            
        title_card.bind(size=update_title_text_size)
        title_label.bind(texture_size=title_label.setter('size'))
        
        def update_title_card_height(instance, texture_size):
            title_card.height = max(dp(80), texture_size[1] + dp(40))
            
        title_label.bind(texture_size=update_title_card_height)
        title_card.add_widget(title_label)
        
        
        info_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(140),
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[15]
        )
        
        info_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15)
        )
        
        
        raaga_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(30))
        raaga_icon = MDLabel(text="🎼", font_style="H6", size_hint_x=None, width=dp(30))
        raaga_info = MDLabel(
            text=f"Raaga: {raaga}",
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="Subtitle1",
            bold=True,
            size_hint_x=0.9
        )
        raaga_layout.add_widget(raaga_icon)
        raaga_layout.add_widget(raaga_info)
        
        
        taal_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(25))
        taal_icon = MDLabel(text="🥁", font_style="Body1", size_hint_x=None, width=dp(30))
        taal_info = MDLabel(
            text=f"Taal: {taal}",
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            size_hint_x=0.9
        )
        taal_layout.add_widget(taal_icon)
        taal_layout.add_widget(taal_info)
        
        
        type_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(25))
        type_icon = MDLabel(text="📝", font_style="Body1", size_hint_x=None, width=dp(30))
        type_info = MDLabel(
            text=f"Type: {bandish_type}",
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            size_hint_x=0.9
        )
        type_layout.add_widget(type_icon)
        type_layout.add_widget(type_info)
        
        info_layout.add_widget(raaga_layout)
        info_layout.add_widget(taal_layout)
        info_layout.add_widget(type_layout)
        info_card.add_widget(info_layout)
        
        
        lyrics_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=3,
            md_bg_color="#FFFAF0",  
            radius=[15]
        )
        
        lyrics_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        
        lyrics_header_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(35))
        lyrics_icon = MDLabel(text="📜", font_style="H6", size_hint_x=None, width=dp(30))
        lyrics_header = MDLabel(
            text="Lyrics",
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="Subtitle1",
            bold=True,
            size_hint_x=0.9
        )
        lyrics_header_layout.add_widget(lyrics_icon)
        lyrics_header_layout.add_widget(lyrics_header)
        
        
        lyrics_label = MDLabel(
            text=lyrics,
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            text_size=(None, None),
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=True
        )
        
        
        def update_lyrics_text_size(instance, size):
            lyrics_label.text_size = (size[0] - dp(40), None)
            
        lyrics_card.bind(size=update_lyrics_text_size)
        lyrics_label.bind(texture_size=lyrics_label.setter('size'))
        
        def update_lyrics_card_height(instance, texture_size):
            lyrics_card.height = lyrics_header_layout.height + texture_size[1] + dp(55)
            
        lyrics_label.bind(texture_size=update_lyrics_card_height)
        
        lyrics_layout.add_widget(lyrics_header_layout)
        lyrics_layout.add_widget(lyrics_label)
        lyrics_card.add_widget(lyrics_layout)
        
        
        self.content_layout.add_widget(title_card)
        self.content_layout.add_widget(info_card)
        self.content_layout.add_widget(lyrics_card)
    
    def go_back(self):
        """Go back to bandish list"""
        self.manager.transition.direction = "right"
        self.manager.current = "bandish_list"
    
    def toggle_favorite(self, bandish_id):
        """Toggle favorite status for this bandish"""
        is_favorite = self.db_manager.toggle_bandish_favorite(bandish_id)
        
        
        favorite_icon = "heart" if is_favorite else "heart-outline"
        self.toolbar.right_action_items = [
            [favorite_icon, lambda x, bid=bandish_id: self.toggle_favorite(bid)]
        ]


class SearchScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "search"
        self.db_manager = db_manager
        self.current_tab = "bandish"  
        
        
        main_layout = MDBoxLayout(orientation="vertical")
        
        
        toolbar = MDTopAppBar(
            title="🔍 Search",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["refresh", lambda x: self.clear_search()]]
        )
        main_layout.add_widget(toolbar)
        

        tabs = MDTabs(background_color="#FFF8DC", indicator_color="#8B4513", text_color_normal="#000000", text_color_active="#000000")
        
        
        class BandishSearchTab(MDBoxLayout, MDTabsBase):
            title = "🎵 Search Bandish"
        
        bandish_tab = BandishSearchTab(orientation="vertical", padding=dp(15), spacing=dp(15))
        
        
        search_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=3,
            md_bg_color="#FFFAF0",
            radius=[10]
        )
        
        search_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        self.bandish_search_field = MDTextField(
            hint_text="Search bandish by title, lyrics, raaga, taal, or type...",
            mode="rectangle",
            size_hint_x=0.85,
            on_text=self.search_bandish
        )
        
        search_btn = MDIconButton(
            icon="magnify",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            icon_size="35dp",
            on_release=lambda x: self.search_bandish(None, self.bandish_search_field.text)
        )
        
        search_layout.add_widget(self.bandish_search_field)
        search_layout.add_widget(search_btn)
        search_card.add_widget(search_layout)
        bandish_tab.add_widget(search_card)
        
        
        bandish_scroll = MDScrollView()
        self.bandish_results = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True)
        bandish_scroll.add_widget(self.bandish_results)
        bandish_tab.add_widget(bandish_scroll)
        tabs.add_widget(bandish_tab)
        
        
        class RaagaSearchTab(MDBoxLayout, MDTabsBase):
            title = "🎼 Search Raagas"
        
        raaga_tab = RaagaSearchTab(orientation="vertical", padding=dp(15), spacing=dp(15))
        
        
        raaga_search_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=3,
            md_bg_color="#FFFAF0",
            radius=[10]
        )
        
        raaga_search_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        self.raaga_search_field = MDTextField(
            hint_text="Search raagas by name or description...",
            mode="rectangle",
            size_hint_x=0.85,
            on_text=self.search_raagas
        )
        
        raaga_search_btn = MDIconButton(
            icon="magnify",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            icon_size="35dp",
            on_release=lambda x: self.search_raagas(None, self.raaga_search_field.text)
        )
        
        raaga_search_layout.add_widget(self.raaga_search_field)
        raaga_search_layout.add_widget(raaga_search_btn)
        raaga_search_card.add_widget(raaga_search_layout)
        raaga_tab.add_widget(raaga_search_card)
        
        
        raaga_scroll = MDScrollView()
        self.raaga_results = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True)
        raaga_scroll.add_widget(self.raaga_results)
        raaga_tab.add_widget(raaga_scroll)
        tabs.add_widget(raaga_tab)
        
        main_layout.add_widget(tabs)
        self.add_widget(main_layout)
        
        
        self.load_initial_results()
    
    def load_initial_results(self):
        """Load all bandish and raagas initially"""
        self.search_bandish(None, "")
        self.search_raagas(None, "")
    
    def search_bandish(self, instance, text):
        """Search bandish with enhanced matching"""
        self.bandish_results.clear_widgets()
        
        
        results = self.db_manager.search_bandish(text)
        
        if not results:
            no_results = MDLabel(
                text="No bandish found matching your search." if text.strip() else "No bandish available.",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="Body1",
                size_hint_y=None,
                height=dp(50)
            )
            self.bandish_results.add_widget(no_results)
            return
        
        
        info_text = f"Found {len(results)} bandish" + (f" for '{text}'" if text.strip() else " total")
        info_label = MDLabel(
            text=info_text,
            theme_text_color="Custom",
            text_color="#654321",
            halign="center",
            font_style="Caption",
            size_hint_y=None,
            height=dp(30)
        )
        self.bandish_results.add_widget(info_label)
        
        
        for bandish_id, title, raaga, taal, btype, lyrics, is_favorite in results:
            card = self.create_bandish_search_card(bandish_id, title, raaga, taal, btype, lyrics, is_favorite)
            self.bandish_results.add_widget(card)
    
    def search_raagas(self, instance, text):
        """Search raagas with enhanced matching"""
        self.raaga_results.clear_widgets()
        
        # Get search results
        results = self.db_manager.search_raagas(text)
        
        if not results:
            no_results = MDLabel(
                text="No raagas found matching your search." if text.strip() else "No raagas available.",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="Body1",
                size_hint_y=None,
                height=dp(50)
            )
            self.raaga_results.add_widget(no_results)
            return
        
        # Show search info
        info_text = f"Found {len(results)} raagas" + (f" for '{text}'" if text.strip() else " total")
        info_label = MDLabel(
            text=info_text,
            theme_text_color="Custom",
            text_color="#654321",
            halign="center",
            font_style="Caption",
            size_hint_y=None,
            height=dp(30)
        )
        self.raaga_results.add_widget(info_label)
        
        # Display results
        for raaga_id, name, is_active, is_favorite in results:
            card = self.create_raaga_search_card(raaga_id, name, is_active, is_favorite)
            self.raaga_results.add_widget(card)
    
    def create_bandish_search_card(self, bandish_id, title, raaga, taal, btype, lyrics, is_favorite):
        """Create a card for bandish search results"""
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(140),
            elevation=3,
            md_bg_color="#FFFFFF",
            radius=[10],
            on_release=lambda x: self.view_bandish_details(bandish_id)
        )
        
        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        # Header with title and favorite
        header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(35))
        
        title_label = MDLabel(
            text=title,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_x=0.85
        )
        
        favorite_icon = "heart" if is_favorite else "heart-outline"
        favorite_btn = MDIconButton(
            icon=favorite_icon,
            theme_icon_color="Custom",
            icon_color="#E91E63" if is_favorite else "#CCCCCC",
            size_hint_x=0.15,
            on_release=lambda x: self.toggle_bandish_favorite(bandish_id)
        )
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(favorite_btn)
        
        # Info layout
        info_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(25))
        
        raaga_label = MDLabel(
            text=f"🎼 {raaga}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#654321",
            size_hint_x=0.4
        )
        
        taal_label = MDLabel(
            text=f"🥁 {taal}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#654321",
            size_hint_x=0.3
        )
        
        type_label = MDLabel(
            text=f"📝 {btype}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#654321",
            size_hint_x=0.3
        )
        
        info_layout.add_widget(raaga_label)
        info_layout.add_widget(taal_label)
        info_layout.add_widget(type_label)
        
        # Lyrics preview
        lyrics_preview = lyrics[:80] + "..." if len(lyrics) > 80 else lyrics
        lyrics_label = MDLabel(
            text=f"📜 {lyrics_preview}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#999999",
            size_hint_y=None,
            height=dp(40)
        )
        
        card_layout.add_widget(header_layout)
        card_layout.add_widget(info_layout)
        card_layout.add_widget(lyrics_label)
        card.add_widget(card_layout)
        
        return card
    
    def create_raaga_search_card(self, raaga_id, name, is_active, is_favorite):
        """Create a card for raaga search results"""
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=3,
            md_bg_color="#FFFFFF" if is_active else "#F5F5F5",
            radius=[10],
            on_release=lambda x: self.select_raaga(name)
        )
        
        card_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        
        # Raaga info
        info_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.7)
        
        name_label = MDLabel(
            text=name,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        
        status_text = "🟢 Active" if is_active else "🔴 Inactive"
        favorite_text = " ❤️ Favorite" if is_favorite else ""
        status_label = MDLabel(
            text=f"{status_text}{favorite_text}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#666666",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(status_label)
        
        # Favorite button
        actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.3)
        
        favorite_icon = "heart" if is_favorite else "heart-outline"
        favorite_btn = MDIconButton(
            icon=favorite_icon,
            theme_icon_color="Custom",
            icon_color="#D4AF37" if is_favorite else "#8B4513",
            on_release=lambda x: self.toggle_raaga_favorite(raaga_id)
        )
        
        actions_layout.add_widget(favorite_btn)
        
        card_layout.add_widget(info_layout)
        card_layout.add_widget(actions_layout)
        card.add_widget(card_layout)
        
        return card
    
    def view_bandish_details(self, bandish_id):
        """Navigate to bandish details"""
        detail_screen = self.manager.get_screen("bandish_detail")
        detail_screen.load_bandish_detail(bandish_id)
        self.manager.transition.direction = "left"
        self.manager.current = "bandish_detail"
    
    def select_raaga(self, raaga_name):
        """Navigate to bandish list for selected raaga (search screen)"""
        bandish_screen = self.manager.get_screen("bandish_list")
        bandish_screen.load_bandish(raaga_name)
        self.manager.transition.direction = "left"
        self.manager.current = "bandish_list"
    
    def toggle_bandish_favorite(self, bandish_id):
        """Toggle favorite status for bandish"""
        is_favorite = self.db_manager.toggle_bandish_favorite(bandish_id)
        # Refresh search results to update the heart icon
        self.search_bandish(None, self.bandish_search_field.text)
        
        status_text = "added to" if is_favorite else "removed from"
        Snackbar(text=f"Bandish {status_text} favorites").open()
    
    def toggle_raaga_favorite(self, raaga_id):
        """Toggle favorite status for raaga"""
        is_favorite = self.db_manager.toggle_raaga_favorite(raaga_id)
        # Refresh search results to update the heart icon
        self.search_raagas(None, self.raaga_search_field.text)
        
        status_text = "added to" if is_favorite else "removed from"
        Snackbar(text=f"Raaga {status_text} favorites").open()
    
    def clear_search(self):
        """Clear search fields and show all results"""
        self.bandish_search_field.text = ""
        self.raaga_search_field.text = ""
        self.load_initial_results()
        Snackbar(text="Search cleared").open()
    
    def go_back(self):
        """Go back to main screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "main"

# --- NEW SCREENS FOR ADMIN ---
class AdminLoginScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "admin_login"
        self.db_manager = db_manager
        
        layout = MDBoxLayout(orientation="vertical", padding=dp(40), spacing=dp(20))
        
        title = MDLabel(text="Admin Login", halign="center", font_style="H5", theme_text_color="Custom", text_color="#8B4513")
        self.username_field = MDTextField(hint_text="Username", mode="rectangle")
        self.password_field = MDTextField(hint_text="Password", password=True, mode="rectangle")
        
        login_btn = MDFlatButton(text="LOGIN", pos_hint={"center_x":0.5}, on_release=self.validate_login)
        
        layout.add_widget(title)
        layout.add_widget(self.username_field)
        layout.add_widget(self.password_field)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)
    
    def validate_login(self, *_):
        if self.username_field.text=="rolex" and self.password_field.text=="kousalya@944":
            Snackbar(text="Login successful").open()
            self.manager.current="admin_panel"
        else:
            Snackbar(text="Invalid credentials").open()

class AdminPanelScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "admin_panel"
        self.db = db_manager
        self.current_edit_raaga_id = None
        self.current_edit_bandish_id = None
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Modern toolbar with better styling
        toolbar = MDTopAppBar(
            title="🎵 Admin Control Panel",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["refresh", lambda x: self.refresh_all_data()]]
        )
        main_layout.add_widget(toolbar)
        
        # Create tabs with better organization
        tabs = MDTabs(background_color="#FFF8DC", indicator_color="#8B4513", text_color_normal="#000000", text_color_active="#000000")
        
        # Tab 1: Manage Raagas (View, Edit, Delete)
        class ManageRaagasTab(MDBoxLayout, MDTabsBase):
            title = "🎼 Manage Raagas"
        
        raaga_tab = ManageRaagasTab(orientation="vertical", padding=dp(15), spacing=dp(10))
        
        # Search and filter section for raagas
        raaga_search_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=3,
            md_bg_color="#FFFAF0",
            radius=[10]
        )
        raaga_search_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        self.raaga_search_field = MDTextField(
            hint_text="Search raagas...",
            mode="rectangle",
            size_hint_x=0.7,
            on_text=self.filter_raagas
        )
        raaga_add_btn = MDIconButton(
            icon="plus-circle",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            icon_size="40dp",
            on_release=self.show_add_raaga_dialog
        )
        raaga_search_layout.add_widget(self.raaga_search_field)
        raaga_search_layout.add_widget(raaga_add_btn)
        raaga_search_card.add_widget(raaga_search_layout)
        raaga_tab.add_widget(raaga_search_card)
        
        # Scrollable raaga list
        raaga_scroll = MDScrollView()
        self.raaga_list = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True)
        raaga_scroll.add_widget(self.raaga_list)
        raaga_tab.add_widget(raaga_scroll)
        tabs.add_widget(raaga_tab)
        
        # Tab 2: Manage Bandish (View, Edit, Delete)
        class ManageBandishTab(MDBoxLayout, MDTabsBase):
            title = "🎵 Manage Bandish"
        
        bandish_tab = ManageBandishTab(orientation="vertical", padding=dp(15), spacing=dp(10))
        
        # Search and filter section for bandish
        bandish_search_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=3,
            md_bg_color="#FFFAF0",
            radius=[10]
        )
        bandish_search_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        self.bandish_search_field = MDTextField(
            hint_text="Search bandish...",
            mode="rectangle",
            size_hint_x=0.7,
            on_text=self.filter_bandish
        )
        bandish_add_btn = MDIconButton(
            icon="plus-circle",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            icon_size="40dp",
            on_release=self.show_add_bandish_dialog
        )
        bandish_search_layout.add_widget(self.bandish_search_field)
        bandish_search_layout.add_widget(bandish_add_btn)
        bandish_search_card.add_widget(bandish_search_layout)
        bandish_tab.add_widget(bandish_search_card)
        
        # Scrollable bandish list
        bandish_scroll = MDScrollView()
        self.bandish_list = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True)
        bandish_scroll.add_widget(self.bandish_list)
        bandish_tab.add_widget(bandish_scroll)
        tabs.add_widget(bandish_tab)
        
        main_layout.add_widget(tabs)
        self.add_widget(main_layout)
        
        # Load all data
        self.refresh_all_data()
    
    def refresh_all_data(self, *args):
        """Refresh all data in all tabs"""
        self.load_raagas()
        self.load_bandish()
        Snackbar(text="Data refreshed successfully!").open()
    
    def load_raagas(self):
        """Load raagas with modern cards and action buttons"""
        self.raaga_list.clear_widgets()
        raagas = self.db.get_all_raagas()
        
        for raaga_id, name, is_active, is_favorite in raagas:
            # Create card for each raaga
            card = MDCard(
                padding=dp(15),
                size_hint_y=None,
                height=dp(100),
                elevation=2,
                md_bg_color="#FFFFFF",  # Uniform background
                radius=[8]
            )
            
            card_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
            
            # Left side - raaga info
            info_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.6)
            
            name_label = MDLabel(
                text=name,
                font_style="H6",
                theme_text_color="Custom",
                text_color="#8B4513",
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            
            status_text = "🟢 Active" if is_active else "🔴 Inactive"
            favorite_text = " ❤️ Favorite" if is_favorite else ""
            status_label = MDLabel(
                text=f"{status_text}{favorite_text}",
                font_style="Caption",
                theme_text_color="Custom",
                text_color="#666666",
                size_hint_y=None,
                height=dp(20)
            )
            
            info_layout.add_widget(name_label)
            info_layout.add_widget(status_label)
            
            # Right side - action buttons
            actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.4, spacing=dp(5))
            
            edit_btn = MDIconButton(
                icon="pencil",
                theme_icon_color="Custom",
                icon_color="#2196F3",
                on_release=lambda x, rid=raaga_id: self.show_edit_raaga_dialog(rid)
            )
            
            delete_btn = MDIconButton(
                icon="delete",
                theme_icon_color="Custom",
                icon_color="#F44336",
                on_release=lambda x, rid=raaga_id, rname=name: self.confirm_delete_raaga(rid, rname)
            )
            
            toggle_btn = MDIconButton(
                icon="eye" if is_active else "eye-off",
                theme_icon_color="Custom",
                icon_color="#4CAF50" if is_active else "#FF9800",
                on_release=lambda x, rid=raaga_id: self.toggle_raaga_status(rid)
            )
            
            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(toggle_btn)
            actions_layout.add_widget(delete_btn)
            
            card_layout.add_widget(info_layout)
            card_layout.add_widget(actions_layout)
            card.add_widget(card_layout)
            
            self.raaga_list.add_widget(card)
    
    def load_bandish(self):
        """Load bandish with modern cards and action buttons"""
        self.bandish_list.clear_widgets()
        bandish_list = self.db.search_bandish("")
        
        for bandish_id, title, raaga, taal, btype, lyrics, is_favorite in bandish_list:
            # Create card for each bandish
            card = MDCard(
                padding=dp(15),
                size_hint_y=None,
                height=dp(140),
                elevation=2,
                md_bg_color="#FFFFFF",
                radius=[8]
            )
            
            card_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
            
            # Header with title and actions
            header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
            
            title_label = MDLabel(
                text=title,
                font_style="Subtitle1",
                theme_text_color="Custom",
                text_color="#8B4513",
                bold=True,
                size_hint_x=0.7
            )
            
            actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.3, spacing=dp(5))
            
            favorite_icon = "heart" if is_favorite else "heart-outline"
            favorite_btn = MDIconButton(
                icon=favorite_icon,
                theme_icon_color="Custom",
                icon_color="#E91E63" if is_favorite else "#CCCCCC",
                on_release=lambda x, bid=bandish_id: self.toggle_bandish_favorite(bid)
            )
            
            edit_btn = MDIconButton(
                icon="pencil",
                theme_icon_color="Custom",
                icon_color="#2196F3",
                on_release=lambda x, bid=bandish_id: self.show_edit_bandish_dialog(bid)
            )
            
            delete_btn = MDIconButton(
                icon="delete",
                theme_icon_color="Custom",
                icon_color="#F44336",
                on_release=lambda x, bid=bandish_id, btitle=title: self.confirm_delete_bandish(bid, btitle)
            )
            # Store the bandish ID directly on the button for easy retrieval
            delete_btn.bandish_id = bandish_id
            delete_btn.bandish_title = title
            
            actions_layout.add_widget(favorite_btn)
            actions_layout.add_widget(edit_btn)
            actions_layout.add_widget(delete_btn)
            
            header_layout.add_widget(title_label)
            header_layout.add_widget(actions_layout)
            
            # Details
            details_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
            
            raaga_label = MDLabel(
                text=f"🎼 {raaga}",
                font_style="Body2",
                theme_text_color="Custom",
                text_color="#666666",
                size_hint_x=0.5
            )
            
            taal_type_label = MDLabel(
                text=f"🥁 {taal} | 📝 {btype}",
                font_style="Body2",
                theme_text_color="Custom",
                text_color="#666666",
                size_hint_x=0.5
            )
            
            details_layout.add_widget(raaga_label)
            details_layout.add_widget(taal_type_label)
            
            # Lyrics preview
            lyrics_preview = lyrics[:50] + "..." if len(lyrics) > 50 else lyrics
            lyrics_label = MDLabel(
                text=f"📜 {lyrics_preview}",
                font_style="Caption",
                theme_text_color="Custom",
                text_color="#999999",
                size_hint_y=None,
                height=dp(30)
            )
            
            card_layout.add_widget(header_layout)
            card_layout.add_widget(details_layout)
            card_layout.add_widget(lyrics_label)
            card.add_widget(card_layout)
            
            self.bandish_list.add_widget(card)
    
    def load_statistics(self):
        """Load database statistics with beautiful cards"""
        self.stats_layout.clear_widgets()
        stats = self.db.get_database_stats()
        
        # Create stats cards
        stats_cards = [
            {"title": "Total Raagas", "value": stats['total_raagas'], "icon": "music-note", "color": "#2196F3"},
            {"title": "Active Raagas", "value": stats['active_raagas'], "icon": "eye", "color": "#4CAF50"},
            {"title": "Favorite Raagas", "value": stats['favorite_raagas'], "icon": "heart", "color": "#E91E63"},
            {"title": "Total Bandish", "value": stats['total_bandish'], "icon": "library-music", "color": "#FF9800"},
            {"title": "Favorite Bandish", "value": stats['favorite_bandish'], "icon": "star", "color": "#9C27B0"}
        ]
        
        for stat in stats_cards:
            card = MDCard(
                padding=dp(20),
                size_hint_y=None,
                height=dp(100),
                elevation=3,
                md_bg_color="#FFFFFF",
                radius=[12]
            )
            
            card_layout = MDBoxLayout(orientation="horizontal", spacing=dp(15))
            
            # Icon
            icon_widget = MDIconButton(
                icon=stat["icon"],
                theme_icon_color="Custom",
                icon_color=stat["color"],
                icon_size="40dp",
                disabled=True
            )
            
            # Text info
            text_layout = MDBoxLayout(orientation="vertical")
            
            value_label = MDLabel(
                text=str(stat["value"]),
                font_style="H4",
                theme_text_color="Custom",
                text_color=stat["color"],
                bold=True,
                size_hint_y=None,
                height=dp(40)
            )
            
            title_label = MDLabel(
                text=stat["title"],
                font_style="Subtitle1",
                theme_text_color="Custom",
                text_color="#666666",
                size_hint_y=None,
                height=dp(30)
            )
            
            text_layout.add_widget(value_label)
            text_layout.add_widget(title_label)
            
            card_layout.add_widget(icon_widget)
            card_layout.add_widget(text_layout)
            card.add_widget(card_layout)
            
            self.stats_layout.add_widget(card)
    
    def filter_raagas(self, instance, text):
        """Filter raagas based on search text"""
        if not text.strip():
            self.load_raagas()
            return
        
        self.raaga_list.clear_widgets()
        raagas = self.db.get_all_raagas()
        
        filtered_raagas = [r for r in raagas if text.lower() in r[1].lower()]
        
        for raaga_id, name, is_active, is_favorite in filtered_raagas:
            # Same card creation logic as load_raagas but with filtered data
            self.create_raaga_card(raaga_id, name, is_active, is_favorite)
    
    def filter_bandish(self, instance, text):
        """Filter bandish based on search text"""
        if not text.strip():
            self.load_bandish()
            return
        
        self.bandish_list.clear_widgets()
        bandish_list = self.db.search_bandish(text)
        
        for bandish_id, title, raaga, taal, btype, lyrics, is_favorite in bandish_list:
            # Same card creation logic as load_bandish but with filtered data
            self.create_bandish_card(bandish_id, title, raaga, taal, btype, lyrics, is_favorite)
    
    def show_add_raaga_dialog(self, *args):
        """Show dialog to add new raaga"""
        self.current_edit_raaga_id = None
        
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), size_hint_y=None, height=dp(200))
        
        self.add_raaga_name = MDTextField(hint_text="Raaga Name *", mode="rectangle")
        self.add_raaga_desc = MDTextField(hint_text="Description", mode="rectangle")
        self.add_raaga_active = MDTextField(hint_text="Active (0 or 1)", mode="rectangle", text="0")
        
        content.add_widget(self.add_raaga_name)
        content.add_widget(self.add_raaga_desc)
        content.add_widget(self.add_raaga_active)
        
        self.raaga_dialog = MDDialog(
            title="➕ Add New Raaga",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_raaga_dialog),
                MDFlatButton(text="ADD", theme_text_color="Custom", text_color="#8B4513", on_release=self.save_raaga)
            ]
        )
        self.raaga_dialog.open()
    
    def show_edit_raaga_dialog(self, raaga_id):
        """Show dialog to edit existing raaga"""
        self.current_edit_raaga_id = raaga_id
        raaga_data = self.db.get_raaga_by_id(raaga_id)
        
        if not raaga_data:
            Snackbar(text="Raaga not found!").open()
            return
        
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), size_hint_y=None, height=dp(200))
        
        self.add_raaga_name = MDTextField(hint_text="Raaga Name *", mode="rectangle", text=raaga_data[1])
        self.add_raaga_desc = MDTextField(hint_text="Description", mode="rectangle", text=raaga_data[2] or "")
        self.add_raaga_active = MDTextField(hint_text="Active (0 or 1)", mode="rectangle", text=str(raaga_data[3]))
        
        content.add_widget(self.add_raaga_name)
        content.add_widget(self.add_raaga_desc)
        content.add_widget(self.add_raaga_active)
        
        self.raaga_dialog = MDDialog(
            title="✏️ Edit Raaga",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_raaga_dialog),
                MDFlatButton(text="SAVE", theme_text_color="Custom", text_color="#8B4513", on_release=self.save_raaga)
            ]
        )
        self.raaga_dialog.open()
    
    def save_raaga(self, *args):
        """Save raaga (add or update)"""
        name = self.add_raaga_name.text.strip()
        desc = self.add_raaga_desc.text.strip()
        active = self.add_raaga_active.text.strip()
        
        if not name:
            Snackbar(text="Raaga name is required!").open()
            return
        
        try:
            is_active = int(active) if active in ['0', '1'] else 0
        except:
            is_active = 0
        
        if self.current_edit_raaga_id:
            # Update existing raaga
            if self.db.update_raaga(self.current_edit_raaga_id, name, desc, is_active):
                Snackbar(text="Raaga updated successfully!").open()
                self.load_raagas()
            else:
                Snackbar(text="Failed to update raaga!").open()
        else:
            # Add new raaga
            if self.db.add_raaga(name, desc, is_active):
                Snackbar(text="Raaga added successfully!").open()
                self.load_raagas()
                # Clear fields
                self.add_raaga_name.text = ""
                self.add_raaga_desc.text = ""
                self.add_raaga_active.text = "0"
            else:
                Snackbar(text="Failed to add raaga! Name might already exist.").open()
        
        self.close_raaga_dialog()
    
    def close_raaga_dialog(self, *args):
        """Close raaga dialog"""
        if hasattr(self, 'raaga_dialog'):
            self.raaga_dialog.dismiss()
    
    def show_add_bandish_dialog(self, *args):
        """Show dialog to add new bandish"""
        self.current_edit_bandish_id = None
        
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), size_hint_y=None, height=dp(400))
        
        self.add_bandish_title = MDTextField(hint_text="Title *", mode="rectangle")
        self.add_bandish_raaga = MDTextField(hint_text="Raaga Name *", mode="rectangle")
        self.add_bandish_taal = MDTextField(hint_text="Taal *", mode="rectangle")
        self.add_bandish_type = MDTextField(hint_text="Type *", mode="rectangle")
        self.add_bandish_lyrics = MDTextField(hint_text="Lyrics *", mode="rectangle", multiline=True, size_hint_y=None, height=dp(100))
        
        content.add_widget(self.add_bandish_title)
        content.add_widget(self.add_bandish_raaga)
        content.add_widget(self.add_bandish_taal)
        content.add_widget(self.add_bandish_type)
        content.add_widget(self.add_bandish_lyrics)
        
        self.bandish_dialog = MDDialog(
            title="➕ Add New Bandish",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_bandish_dialog),
                MDFlatButton(text="ADD", theme_text_color="Custom", text_color="#8B4513", on_release=self.save_bandish)
            ]
        )
        self.bandish_dialog.open()
    
    def show_edit_bandish_dialog(self, bandish_id):
        """Show dialog to edit existing bandish"""
        self.current_edit_bandish_id = bandish_id
        bandish_data = self.db.get_bandish_by_id(bandish_id)
        
        if not bandish_data:
            Snackbar(text="Bandish not found!").open()
            return
        
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), size_hint_y=None, height=dp(400))
        
        self.add_bandish_title = MDTextField(hint_text="Title *", mode="rectangle", text=bandish_data[1])
        self.add_bandish_raaga = MDTextField(hint_text="Raaga Name *", mode="rectangle", text=bandish_data[2])
        self.add_bandish_taal = MDTextField(hint_text="Taal *", mode="rectangle", text=bandish_data[3])
        self.add_bandish_type = MDTextField(hint_text="Type *", mode="rectangle", text=bandish_data[4])
        self.add_bandish_lyrics = MDTextField(hint_text="Lyrics *", mode="rectangle", multiline=True, text=bandish_data[5], size_hint_y=None, height=dp(100))
        
        content.add_widget(self.add_bandish_title)
        content.add_widget(self.add_bandish_raaga)
        content.add_widget(self.add_bandish_taal)
        content.add_widget(self.add_bandish_type)
        content.add_widget(self.add_bandish_lyrics)
        
        self.bandish_dialog = MDDialog(
            title="✏️ Edit Bandish",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_bandish_dialog),
                MDFlatButton(text="SAVE", theme_text_color="Custom", text_color="#8B4513", on_release=self.save_bandish)
            ]
        )
        self.bandish_dialog.open()
    
    def save_bandish(self, *args):
        """Save bandish (add or update)"""
        title = self.add_bandish_title.text.strip()
        raaga = self.add_bandish_raaga.text.strip()
        taal = self.add_bandish_taal.text.strip()
        btype = self.add_bandish_type.text.strip()
        lyrics = self.add_bandish_lyrics.text.strip()
        
        if not all([title, raaga, taal, btype, lyrics]):
            Snackbar(text="All fields are required!").open()
            return
        
        if self.current_edit_bandish_id:
            # Update existing bandish
            if self.db.update_bandish(self.current_edit_bandish_id, title, raaga, taal, btype, lyrics):
                Snackbar(text="Bandish updated successfully!").open()
                self.load_bandish()
            else:
                Snackbar(text="Failed to update bandish! Check if raaga exists.").open()
        else:
            # Add new bandish
            if self.db.add_bandish(title, raaga, taal, btype, lyrics):
                Snackbar(text="Bandish added successfully!").open()
                self.load_bandish()
                # Clear fields
                self.add_bandish_title.text = ""
                self.add_bandish_raaga.text = ""
                self.add_bandish_taal.text = ""
                self.add_bandish_type.text = ""
                self.add_bandish_lyrics.text = ""
            else:
                Snackbar(text="Failed to add bandish! Check if raaga exists.").open()
        
        self.close_bandish_dialog()
    
    def close_bandish_dialog(self, *args):
        """Close bandish dialog"""
        if hasattr(self, 'bandish_dialog'):
            self.bandish_dialog.dismiss()
    
    def confirm_delete_raaga(self, raaga_id, raaga_name):
        """Show confirmation dialog for deleting raaga"""
        self.delete_dialog = MDDialog(
            title="⚠️ Confirm Delete",
            text=f"Are you sure you want to delete the raaga '{raaga_name}' and ALL its associated bandish?\n\nThis action cannot be undone!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_delete_dialog),
                MDFlatButton(
                    text="DELETE", 
                    theme_text_color="Custom", 
                    text_color="#F44336",
                    on_release=lambda x: self.delete_raaga(raaga_id)
                )
            ]
        )
        self.delete_dialog.open()
    
    def confirm_delete_bandish(self, bandish_id, bandish_title):
        """Show confirmation dialog for deleting bandish"""
        # Print debug info
        print(f"Confirming delete for bandish ID: {bandish_id}, title: {bandish_title}")
        
        # Store the bandish ID for use in delete_bandish
        self.current_delete_bandish_id = bandish_id
        
        # Safety check
        if not bandish_id:
            print("ERROR: Attempted to delete bandish with no ID")
            Snackbar(text="Error: Missing bandish ID").open()
            return
            
        self.delete_dialog = MDDialog(
            title="⚠️ Confirm Delete",
            text=f"Are you sure you want to delete the bandish '{bandish_title}'?\n\nThis action cannot be undone!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_delete_dialog),
                MDFlatButton(
                    text="DELETE", 
                    theme_text_color="Custom", 
                    text_color="#F44336",
                    # Pass ID explicitly instead of using self.current_delete_bandish_id which could change
                    on_release=lambda x, bid=bandish_id: self.delete_bandish(bid)
                )
            ]
        )
        self.delete_dialog.open()
    
    def delete_raaga(self, raaga_id):
        """Delete raaga and associated bandish"""
        if self.db.delete_raaga(raaga_id):
            Snackbar(text="Raaga and associated bandish deleted successfully!").open()
            self.load_raagas()
            self.load_bandish()  # Refresh bandish list too
            self.load_statistics()  # Refresh stats
        else:
            Snackbar(text="Failed to delete raaga!").open()
        self.close_delete_dialog()
    
    def delete_bandish(self, bandish_id):
        """Delete bandish"""
        # Print debug info
        print(f"Attempting to delete bandish with ID: {bandish_id}")
        
        # Safety check to make sure we have a valid bandish_id
        if not bandish_id:
            print("Error: No bandish ID provided")
            Snackbar(text="Error: No bandish ID to delete").open()
            self.close_delete_dialog()
            return
        
        # Attempt deletion
        if self.db.delete_bandish(bandish_id):
            print(f"Successfully deleted bandish ID: {bandish_id}")
            Snackbar(text="Bandish deleted successfully!").open()
            self.load_bandish()  # Refresh bandish list
            
            # Refresh statistics tab if it exists
            try:
                self.load_statistics()
            except:
                pass  # Statistics tab might have been removed
        else:
            print(f"Failed to delete bandish ID: {bandish_id}")
            Snackbar(text="Failed to delete bandish!").open()
            
        # Close the dialog
        self.close_delete_dialog()
    
    def close_delete_dialog(self, *args):
        """Close delete confirmation dialog"""
        if hasattr(self, 'delete_dialog'):
            self.delete_dialog.dismiss()
    
    def toggle_raaga_status(self, raaga_id):
        """Toggle raaga active/inactive status"""
        raaga_data = self.db.get_raaga_by_id(raaga_id)
        if raaga_data:
            new_status = 0 if raaga_data[3] else 1
            if self.db.update_raaga(raaga_id, raaga_data[1], raaga_data[2], new_status):
                status_text = "activated" if new_status else "deactivated"
                Snackbar(text=f"Raaga {status_text} successfully!").open()
                self.load_raagas()
                self.load_statistics()
            else:
                Snackbar(text="Failed to update raaga status!").open()
    
    def toggle_bandish_favorite(self, bandish_id):
        """Toggle bandish favorite status"""
        is_favorite = self.db.toggle_bandish_favorite(bandish_id)
        status_text = "added to" if is_favorite else "removed from"
        Snackbar(text=f"Bandish {status_text} favorites!").open()
        self.load_bandish()
        self.load_statistics()
    
    def create_raaga_card(self, raaga_id, name, is_active, is_favorite):
        """Helper method to create raaga card (for filtering)"""
        # Same logic as in load_raagas method
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(100),
            elevation=2,
            md_bg_color="#FFFFFF" if is_active else "#F5F5F5",
            radius=[8]
        )
        
        card_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        
        # Left side - raaga info
        info_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.6)
        
        name_label = MDLabel(
            text=name,
            font_style="H6",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        
        status_text = "🟢 Active" if is_active else "🔴 Inactive"
        favorite_text = " ❤️ Favorite" if is_favorite else ""
        status_label = MDLabel(
            text=f"{status_text}{favorite_text}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#666666",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(status_label)
        
        # Right side - action buttons
        actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.4, spacing=dp(5))
        
        edit_btn = MDIconButton(
            icon="pencil",
            theme_icon_color="Custom",
            icon_color="#2196F3",
            on_release=lambda x, rid=raaga_id: self.show_edit_raaga_dialog(rid)
        )
        
        delete_btn = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color="#F44336",
            on_release=lambda x, rid=raaga_id, rname=name: self.confirm_delete_raaga(rid, rname)
        )
        
        toggle_btn = MDIconButton(
            icon="eye" if is_active else "eye-off",
            theme_icon_color="Custom",
            icon_color="#4CAF50" if is_active else "#FF9800",
            on_release=lambda x, rid=raaga_id: self.toggle_raaga_status(rid)
        )
        
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(toggle_btn)
        actions_layout.add_widget(delete_btn)
        
        card_layout.add_widget(info_layout)
        card_layout.add_widget(actions_layout)
        card.add_widget(card_layout)
        
        self.raaga_list.add_widget(card)
    
    def create_bandish_card(self, bandish_id, title, raaga, taal, btype, lyrics, is_favorite):
        """Helper method to create bandish card (for filtering)"""
        # Same logic as in load_bandish method
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(140),
            elevation=2,
            md_bg_color="#FFFFFF",
            radius=[8]
        )
        
        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        # Header with title and actions
        header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
        
        title_label = MDLabel(
            text=title,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_x=0.7
        )
        
        actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.3, spacing=dp(5))
        
        favorite_icon = "heart" if is_favorite else "heart-outline"
        favorite_btn = MDIconButton(
            icon=favorite_icon,
            theme_icon_color="Custom",
            icon_color="#E91E63" if is_favorite else "#CCCCCC",
            on_release=lambda x, bid=bandish_id: self.toggle_bandish_favorite(bid)
        )
        
        edit_btn = MDIconButton(
            icon="pencil",
            theme_icon_color="Custom",
            icon_color="#2196F3",
            on_release=lambda x, bid=bandish_id: self.show_edit_bandish_dialog(bid)
        )
        
        delete_btn = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color="#F44336",
            on_release=lambda x, bid=bandish_id, btitle=title: self.confirm_delete_bandish(bid, btitle)
        )
        # Store ID directly on the button to prevent closure issues
        delete_btn.bandish_id = bandish_id
        
        actions_layout.add_widget(favorite_btn)
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(delete_btn)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(actions_layout)
        
        # Details
        details_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        
        raaga_label = MDLabel(
            text=f"🎼 {raaga}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#666666",
            size_hint_x=0.5
        )
        
        taal_type_label = MDLabel(
            text=f"🥁 {taal} | 📝 {btype}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#666666",
            size_hint_x=0.5
        )
        
        details_layout.add_widget(raaga_label)
        details_layout.add_widget(taal_type_label)
        
        # Lyrics preview
        lyrics_preview = lyrics[:50] + "..." if len(lyrics) > 50 else lyrics
        lyrics_label = MDLabel(
            text=f"📜 {lyrics_preview}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#999999",
            size_hint_y=None,
            height=dp(30)
        )
        
        card_layout.add_widget(header_layout)
        card_layout.add_widget(details_layout)
        card_layout.add_widget(lyrics_label)
        card.add_widget(card_layout)
        
        self.bandish_list.add_widget(card)
    
    def go_back(self):
        """Go back to main screen"""
        self.manager.current = "main"

# ===== CONCERT MANAGEMENT SCREENS =====

class ConcertListScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "concert_list"
        self.db_manager = db_manager
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="🎵 My Concerts",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["refresh", lambda x: self.load_concerts()]]
        )
        main_layout.add_widget(toolbar)
        
        # Scrollable concert list
        scroll = MDScrollView()
        self.concerts_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            adaptive_height=True,
            padding=dp(20)
        )
        scroll.add_widget(self.concerts_layout)
        main_layout.add_widget(scroll)
        
        # Create new concert button
        create_button = MDFlatButton(
            text="🎼 CREATE NEW CONCERT",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            md_bg_color="#8B4513",
            size_hint_y=None,
            height=dp(50),
            pos_hint={"center_x": 0.5},
            on_release=self.create_new_concert
        )
        main_layout.add_widget(create_button)
        
        self.add_widget(main_layout)
        
        # Load concerts when screen is created
        self.load_concerts()
    
    def load_concerts(self, *args):
        """Load all concerts for the user"""
        self.concerts_layout.clear_widgets()
        concerts = self.db_manager.get_all_concerts()
        
        if not concerts:
            # Show empty state
            empty_label = MDLabel(
                text="No concerts created yet.\nClick 'CREATE NEW CONCERT' to get started!",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="H6",
                size_hint_y=None,
                height=dp(100)
            )
            self.concerts_layout.add_widget(empty_label)
            return
        
        # Create cards for each concert
        for concert_id, name, description, created_at, bandish_count in concerts:
            card = self.create_concert_card(concert_id, name, description, created_at, bandish_count)
            self.concerts_layout.add_widget(card)
    
    def create_concert_card(self, concert_id, name, description, created_at, bandish_count):
        """Create a card for each concert"""
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(120),
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[10]
        )
        
        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        # Header with name and actions
        header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(35))
        
        name_label = MDLabel(
            text=name,
            font_style="H6",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_x=0.7
        )
        
        actions_layout = MDBoxLayout(orientation="horizontal", size_hint_x=0.3, spacing=dp(5))
        
        view_btn = MDIconButton(
            icon="eye",
            theme_icon_color="Custom",
            icon_color="#2196F3",
            on_release=lambda x, cid=concert_id: self.view_concert(cid)
        )
        
        edit_btn = MDIconButton(
            icon="pencil",
            theme_icon_color="Custom",
            icon_color="#FF9800",
            on_release=lambda x, cid=concert_id: self.edit_concert(cid)
        )
        
        delete_btn = MDIconButton(
            icon="delete",
            theme_icon_color="Custom",
            icon_color="#F44336",
            on_release=lambda x, cid=concert_id, cname=name: self.confirm_delete_concert(cid, cname)
        )
        
        actions_layout.add_widget(view_btn)
        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(delete_btn)
        
        header_layout.add_widget(name_label)
        header_layout.add_widget(actions_layout)
        
        # Description
        desc_text = description if description else "No description"
        desc_label = MDLabel(
            text=f"📝 {desc_text}",
            font_style="Body2",
            theme_text_color="Custom",
            text_color="#666666",
            size_hint_y=None,
            height=dp(25)
        )
        
        # Stats
        stats_label = MDLabel(
            text=f"🎵 {bandish_count} bandish • 📅 {created_at[:10] if created_at else 'Unknown'}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color="#999999",
            size_hint_y=None,
            height=dp(20)
        )
        
        card_layout.add_widget(header_layout)
        card_layout.add_widget(desc_label)
        card_layout.add_widget(stats_label)
        card.add_widget(card_layout)
        
        return card
    
    def create_new_concert(self, *args):
        """Navigate to create concert screen"""
        create_screen = self.manager.get_screen("create_concert")
        create_screen.setup_for_new_concert()
        self.manager.transition.direction = "left"
        self.manager.current = "create_concert"
    
    def view_concert(self, concert_id):
        """View concert details"""
        view_screen = self.manager.get_screen("view_concert")
        view_screen.load_concert(concert_id)
        self.manager.transition.direction = "left"
        self.manager.current = "view_concert"
    
    def edit_concert(self, concert_id):
        """Edit concert"""
        create_screen = self.manager.get_screen("create_concert")
        create_screen.setup_for_edit_concert(concert_id)
        self.manager.transition.direction = "left"
        self.manager.current = "create_concert"
    
    def confirm_delete_concert(self, concert_id, concert_name):
        """Show confirmation dialog for deleting concert"""
        self.delete_dialog = MDDialog(
            title="⚠️ Confirm Delete",
            text=f"Are you sure you want to delete the concert '{concert_name}'?\n\nThis action cannot be undone!",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_delete_dialog),
                MDFlatButton(
                    text="DELETE", 
                    theme_text_color="Custom", 
                    text_color="#F44336",
                    on_release=lambda x: self.delete_concert(concert_id)
                )
            ]
        )
        self.delete_dialog.open()
    
    def delete_concert(self, concert_id):
        """Delete concert"""
        if self.db_manager.delete_concert(concert_id):
            Snackbar(text="Concert deleted successfully!").open()
            self.load_concerts()
        else:
            Snackbar(text="Failed to delete concert!").open()
        self.close_delete_dialog()
    
    def close_delete_dialog(self, *args):
        """Close delete confirmation dialog"""
        if hasattr(self, 'delete_dialog'):
            self.delete_dialog.dismiss()
    
    def go_back(self):
        """Go back to main screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "main"

class CreateConcertScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "create_concert"
        self.db_manager = db_manager
        self.current_concert_id = None
        self.selected_raagas = []
        self.selected_bandish = []
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="🎼 Create Concert",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["check", lambda x: self.save_concert()]]
        )
        main_layout.add_widget(self.toolbar)
        
        # Scroll content
        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            padding=dp(20)
        )
        
        # Concert details card
        details_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[10]
        )
        
        details_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        details_header = MDLabel(
            text="📝 Concert Details",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        )
        
        self.name_field = MDTextField(
            hint_text="Concert Name *",
            mode="rectangle",
            size_hint_y=None,
            height=dp(60)
        )
        
        self.description_field = MDTextField(
            hint_text="Description (Optional)",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(80)
        )
        
        details_layout.add_widget(details_header)
        details_layout.add_widget(self.name_field)
        details_layout.add_widget(self.description_field)
        details_card.add_widget(details_layout)
        
        details_card.bind(size=lambda instance, size: setattr(details_card, 'height', details_layout.minimum_height + dp(40)))
        
        # Raaga selection card
        raaga_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[10]
        )
        
        raaga_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        raaga_header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        
        raaga_header = MDLabel(
            text="🎼 Select Raagas",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_x=0.8
        )
        
        add_raaga_btn = MDIconButton(
            icon="plus",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            size_hint_x=0.2,
            on_release=self.select_raagas
        )
        
        raaga_header_layout.add_widget(raaga_header)
        raaga_header_layout.add_widget(add_raaga_btn)
        
        self.selected_raagas_layout = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(10),
            adaptive_height=True
        )
        
        raaga_layout.add_widget(raaga_header_layout)
        raaga_layout.add_widget(self.selected_raagas_layout)
        raaga_card.add_widget(raaga_layout)
        
        raaga_card.bind(size=lambda instance, size: setattr(raaga_card, 'height', raaga_layout.minimum_height + dp(40)))
        
        # Bandish selection card
        bandish_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[10]
        )
        
        bandish_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        bandish_header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        
        bandish_header = MDLabel(
            text="🎵 Selected Bandish",
            font_style="H6",
            theme_text_color="Custom",
            text_color="#8B4513",
            bold=True,
            size_hint_x=0.8
        )
        
        add_bandish_btn = MDIconButton(
            icon="plus",
            theme_icon_color="Custom",
            icon_color="#8B4513",
            size_hint_x=0.2,
            on_release=self.select_bandish
        )
        
        bandish_header_layout.add_widget(bandish_header)
        bandish_header_layout.add_widget(add_bandish_btn)
        
        self.selected_bandish_layout = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(10),
            adaptive_height=True
        )
        
        bandish_layout.add_widget(bandish_header_layout)
        bandish_layout.add_widget(self.selected_bandish_layout)
        bandish_card.add_widget(bandish_layout)
        
        bandish_card.bind(size=lambda instance, size: setattr(bandish_card, 'height', bandish_layout.minimum_height + dp(40)))
        
        content.add_widget(details_card)
        content.add_widget(raaga_card)
        content.add_widget(bandish_card)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def setup_for_new_concert(self):
        """Setup screen for creating new concert"""
        self.current_concert_id = None
        self.toolbar.title = "🎼 Create Concert"
        self.name_field.text = ""
        self.description_field.text = ""
        self.selected_raagas = []
        self.selected_bandish = []
        self.update_selected_raagas_display()
        self.update_selected_bandish_display()
    
    def setup_for_edit_concert(self, concert_id):
        """Setup screen for editing existing concert"""
        self.current_concert_id = concert_id
        self.toolbar.title = "✏️ Edit Concert"
        
        # Load concert data
        concert = self.db_manager.get_concert_by_id(concert_id)
        if concert:
            self.name_field.text = concert[1]
            self.description_field.text = concert[2] or ""
        
        # Load bandish in concert
        concert_bandish = self.db_manager.get_concert_bandish(concert_id)
        self.selected_bandish = []
        self.selected_raagas = []
        
        for item in concert_bandish:
            link_id, order_index, bandish_id, title, raaga_name, taal, btype, lyrics, source, user_bandish_id = item
            
            if source == "original":
                self.selected_bandish.append({
                    'id': bandish_id,
                    'type': 'original',
                    'title': title,
                    'raaga': raaga_name,
                    'taal': taal,
                    'btype': btype,
                    'lyrics': lyrics
                })
            else:
                self.selected_bandish.append({
                    'id': user_bandish_id,
                    'type': 'user',
                    'title': title,
                    'raaga': raaga_name,
                    'taal': taal,
                    'btype': btype,
                    'lyrics': lyrics
                })
            
            # Add raaga to selected raagas if not already present
            if raaga_name not in self.selected_raagas:
                self.selected_raagas.append(raaga_name)
        
        self.update_selected_raagas_display()
        self.update_selected_bandish_display()
    
    def select_raagas(self, *args):
        """Navigate to raaga selection screen"""
        select_screen = self.manager.get_screen("select_raagas")
        select_screen.load_raagas(self.selected_raagas)
        self.manager.transition.direction = "left"
        self.manager.current = "select_raagas"
    
    def select_bandish(self, *args):
        """Navigate to bandish selection screen"""
        if not self.selected_raagas:
            Snackbar(text="Please select raagas first!").open()
            return
        
        select_screen = self.manager.get_screen("select_bandish")
        select_screen.load_bandish(self.selected_raagas, self.selected_bandish)
        self.manager.transition.direction = "left"
        self.manager.current = "select_bandish"
    
    def update_selected_raagas_display(self):
        """Update the display of selected raagas"""
        self.selected_raagas_layout.clear_widgets()
        
        if not self.selected_raagas:
            placeholder = MDLabel(
                text="No raagas selected. Click + to add raagas.",
                theme_text_color="Custom",
                text_color="#999999",
                font_style="Caption",
                size_hint_y=None,
                height=dp(30)
            )
            self.selected_raagas_layout.add_widget(placeholder)
            return
        
        for raaga in self.selected_raagas:
            raaga_chip = self.create_raaga_chip(raaga)
            self.selected_raagas_layout.add_widget(raaga_chip)
    
    def create_raaga_chip(self, raaga_name):
        """Create a chip for selected raaga"""
        chip_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(35),
            spacing=dp(10)
        )
        
        chip_card = MDCard(
            padding=dp(10),
            size_hint_y=None,
            height=dp(35),
            elevation=1,
            md_bg_color="#E8F5E8",
            radius=[15]
        )
        
        chip_content = MDBoxLayout(orientation="horizontal", spacing=dp(5))
        
        raaga_label = MDLabel(
            text=f"🎼 {raaga_name}",
            theme_text_color="Custom",
            text_color="#2E7D32",
            font_style="Caption",
            size_hint_x=0.9
        )
        
        remove_btn = MDIconButton(
            icon="close",
            theme_icon_color="Custom",
            icon_color="#F44336",
            icon_size="20dp",
            size_hint_x=0.1,
            on_release=lambda x, rname=raaga_name: self.remove_raaga(rname)
        )
        
        chip_content.add_widget(raaga_label)
        chip_content.add_widget(remove_btn)
        chip_card.add_widget(chip_content)
        chip_layout.add_widget(chip_card)
        
        return chip_layout
    
    def remove_raaga(self, raaga_name):
        """Remove raaga from selection"""
        if raaga_name in self.selected_raagas:
            self.selected_raagas.remove(raaga_name)
            
            # Remove associated bandish
            self.selected_bandish = [b for b in self.selected_bandish if b['raaga'] != raaga_name]
            
            self.update_selected_raagas_display()
            self.update_selected_bandish_display()
    
    def update_selected_bandish_display(self):
        """Update the display of selected bandish"""
        self.selected_bandish_layout.clear_widgets()
        
        if not self.selected_bandish:
            placeholder = MDLabel(
                text="No bandish selected. Click + to add bandish.",
                theme_text_color="Custom",
                text_color="#999999",
                font_style="Caption",
                size_hint_y=None,
                height=dp(30)
            )
            self.selected_bandish_layout.add_widget(placeholder)
            return
        
        for bandish in self.selected_bandish:
            bandish_card = self.create_bandish_chip(bandish)
            self.selected_bandish_layout.add_widget(bandish_card)
    
    def create_bandish_chip(self, bandish):
        """Create a chip for selected bandish"""
        chip_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        chip_card = MDCard(
            padding=dp(10),
            size_hint_y=None,
            height=dp(50),
            elevation=1,
            md_bg_color="#FFF3E0",
            radius=[10]
        )
        
        chip_content = MDBoxLayout(orientation="horizontal", spacing=dp(5))
        
        info_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.9)
        
        title_label = MDLabel(
            text=f"🎵 {bandish['title'][:40]}{'...' if len(bandish['title']) > 40 else ''}",
            theme_text_color="Custom",
            text_color="#E65100",
            font_style="Caption",
            bold=True,
            size_hint_y=None,
            height=dp(20)
        )
        
        details_label = MDLabel(
            text=f"🎼 {bandish['raaga']} • 🥁 {bandish['taal']} • {'👤' if bandish['type'] == 'user' else '📚'} {bandish['btype']}",
            theme_text_color="Custom",
            text_color="#666666",
            font_style="Caption",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_layout.add_widget(title_label)
        info_layout.add_widget(details_label)
        
        remove_btn = MDIconButton(
            icon="close",
            theme_icon_color="Custom",
            icon_color="#F44336",
            icon_size="20dp",
            size_hint_x=0.1,
            on_release=lambda x, b=bandish: self.remove_bandish(b)
        )
        
        chip_content.add_widget(info_layout)
        chip_content.add_widget(remove_btn)
        chip_card.add_widget(chip_content)
        chip_layout.add_widget(chip_card)
        
        return chip_layout
    
    def remove_bandish(self, bandish):
        """Remove bandish from selection"""
        if bandish in self.selected_bandish:
            self.selected_bandish.remove(bandish)
            self.update_selected_bandish_display()
    
    def save_concert(self):
        """Save the concert"""
        name = self.name_field.text.strip()
        description = self.description_field.text.strip()
        
        if not name:
            Snackbar(text="Concert name is required!").open()
            return
        
        if not self.selected_bandish:
            Snackbar(text="Please select at least one bandish!").open()
            return
        
        # Save or update concert
        if self.current_concert_id:
            # Update existing concert
            if self.db_manager.update_concert(self.current_concert_id, name, description):
                # Clear existing bandish links
                concert_bandish = self.db_manager.get_concert_bandish(self.current_concert_id)
                for item in concert_bandish:
                    link_id, _, bandish_id, _, _, _, _, _, source, user_bandish_id = item
                    if source == "original":
                        self.db_manager.remove_bandish_from_concert(self.current_concert_id, bandish_id=bandish_id)
                    else:
                        self.db_manager.remove_bandish_from_concert(self.current_concert_id, user_bandish_id=user_bandish_id)
                
                # Add new bandish links
                for bandish in self.selected_bandish:
                    if bandish['type'] == 'original':
                        self.db_manager.add_bandish_to_concert(self.current_concert_id, bandish_id=bandish['id'])
                    elif bandish['type'] == 'user':
                        self.db_manager.add_bandish_to_concert(self.current_concert_id, user_bandish_id=bandish['id'])
                    else:
                        # Fallback for safety
                        self.db_manager.add_bandish_to_concert(self.current_concert_id, user_bandish_id=bandish['id'])
                
                Snackbar(text="Concert updated successfully!").open()
                self.go_back()
            else:
                Snackbar(text="Failed to update concert!").open()
        else:
            # Create new concert
            concert_id = self.db_manager.create_concert(name, description)
            if concert_id:
                # Add bandish to concert
                for bandish in self.selected_bandish:
                    if bandish['type'] == 'original':
                        self.db_manager.add_bandish_to_concert(concert_id, bandish_id=bandish['id'])
                    elif bandish['type'] == 'user':
                        self.db_manager.add_bandish_to_concert(concert_id, user_bandish_id=bandish['id'])
                    else:
                        # Fallback for safety
                        self.db_manager.add_bandish_to_concert(concert_id, user_bandish_id=bandish['id'])
                
                Snackbar(text="Concert created successfully!").open()
                self.go_back()
            else:
                Snackbar(text="Failed to create concert!").open()
    
    def go_back(self):
        """Go back to concert list"""
        self.manager.transition.direction = "right"
        self.manager.current = "concert_list"

# ===== CONCERT SELECTION SCREENS =====

class SelectRaagasScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "select_raagas"
        self.db_manager = db_manager
        self.selected_raagas = []
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="🎼 Select Raagas",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["check", lambda x: self.confirm_selection()]]
        )
        main_layout.add_widget(toolbar)
        
        # Search bar
        search_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=1,
            md_bg_color="#FFFAF0",
            radius=[0]
        )
        
        self.search_field = MDTextField(
            hint_text="Search raagas...",
            mode="rectangle",
            on_text=self.filter_raagas
        )
        search_card.add_widget(self.search_field)
        main_layout.add_widget(search_card)
        
        # Scrollable raaga list
        scroll = MDScrollView()
        self.raaga_list = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
            padding=dp(15)
        )
        scroll.add_widget(self.raaga_list)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def load_raagas(self, pre_selected=None):
        """Load raagas with selection state"""
        self.selected_raagas = pre_selected if pre_selected else []
        self.raaga_list.clear_widgets()
        
        raagas = self.db_manager.get_all_raagas()
        
        for raaga_id, raaga_name, is_active, is_favorite in raagas:
            card = self.create_raaga_selection_card(raaga_name, raaga_name in self.selected_raagas)
            self.raaga_list.add_widget(card)
    
    def create_raaga_selection_card(self, raaga_name, is_selected):
        """Create selectable raaga card"""
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(70),
            elevation=2,
            md_bg_color="#E8F5E8" if is_selected else "#FFFFFF",
            radius=[8],
            on_release=lambda x: self.toggle_raaga_selection(raaga_name)
        )
        
        card_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        
        # Checkbox icon
        checkbox_icon = "checkbox-marked" if is_selected else "checkbox-blank-outline"
        checkbox = MDIconButton(
            icon=checkbox_icon,
            theme_icon_color="Custom",
            icon_color="#4CAF50" if is_selected else "#CCCCCC",
            size_hint_x=None,
            width=dp(40)
        )
        
        # Raaga info
        raaga_label = MDLabel(
            text=f"🎼 {raaga_name}",
            theme_text_color="Custom",
            text_color="#2E7D32" if is_selected else "#8B4513",
            font_style="Subtitle1",
            bold=is_selected
        )
        
        card_layout.add_widget(checkbox)
        card_layout.add_widget(raaga_label)
        card.add_widget(card_layout)
        
        return card
    
    def toggle_raaga_selection(self, raaga_name):
        """Toggle raaga selection"""
        if raaga_name in self.selected_raagas:
            self.selected_raagas.remove(raaga_name)
        else:
            self.selected_raagas.append(raaga_name)
        
        # Update display
        self.load_raagas(self.selected_raagas)
    
    def filter_raagas(self, instance, text):
        """Filter raagas based on search"""
        self.raaga_list.clear_widgets()
        
        raagas = self.db_manager.search_raagas(text)
        
        for raaga_id, raaga_name, is_active, is_favorite in raagas:
            card = self.create_raaga_selection_card(raaga_name, raaga_name in self.selected_raagas)
            self.raaga_list.add_widget(card)
    
    def confirm_selection(self):
        """Confirm raaga selection and go back"""
        create_screen = self.manager.get_screen("create_concert")
        create_screen.selected_raagas = self.selected_raagas
        create_screen.update_selected_raagas_display()
        self.go_back()
    
    def go_back(self):
        """Go back to create concert screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "create_concert"

class SelectBandishScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "select_bandish"
        self.db_manager = db_manager
        self.selected_raagas = []
        self.selected_bandish = []
        self.all_bandish = []
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        toolbar = MDTopAppBar(
            title="🎵 Select Bandish",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["plus-circle", lambda x: self.add_custom_bandish()],
                ["check", lambda x: self.confirm_selection()]
            ]
        )
        main_layout.add_widget(toolbar)
        
        # Search and filter bar
        filter_card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(80),
            elevation=1,
            md_bg_color="#FFFAF0",
            radius=[0]
        )
        
        filter_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        
        self.search_field = MDTextField(
            hint_text="Search bandish...",
            mode="rectangle",
            size_hint_x=0.7,
            on_text=self.filter_bandish
        )
        
        self.raaga_filter = MDTextField(
            hint_text="Filter by raaga",
            mode="rectangle",
            size_hint_x=0.3,
            on_text=self.filter_bandish
        )
        
        filter_layout.add_widget(self.search_field)
        filter_layout.add_widget(self.raaga_filter)
        filter_card.add_widget(filter_layout)
        main_layout.add_widget(filter_card)
        
        # Scrollable bandish list
        scroll = MDScrollView()
        self.bandish_list = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True,
            padding=dp(15)
        )
        scroll.add_widget(self.bandish_list)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def load_bandish(self, selected_raagas, pre_selected_bandish=None):
        """Load bandish for selected raagas"""
        self.selected_raagas = selected_raagas
        self.selected_bandish = pre_selected_bandish if pre_selected_bandish else []
        
        # Get all bandish for selected raagas (original + user bandish)
        self.all_bandish = []
        
        for raaga_name in selected_raagas:
            # Get original bandish
            original_bandish = self.db_manager.get_bandish_by_raaga(raaga_name)
            for bandish_id, title, raaga, taal, btype, lyrics, is_favorite in original_bandish:
                self.all_bandish.append({
                    'id': bandish_id,
                    'type': 'original',
                    'title': title,
                    'raaga': raaga,
                    'taal': taal,
                    'btype': btype,
                    'lyrics': lyrics,
                    'is_favorite': is_favorite
                })
            
            # Get user bandish
            user_bandish = self.db_manager.get_user_bandish_by_raaga(raaga_name)
            for user_bandish_id, title, raaga, taal, btype, lyrics in user_bandish:
                self.all_bandish.append({
                    'id': user_bandish_id,
                    'type': 'user',
                    'title': title,
                    'raaga': raaga,
                    'taal': taal,
                    'btype': btype,
                    'lyrics': lyrics,
                    'is_favorite': False
                })
        
        self.display_bandish(self.all_bandish)
    
    def display_bandish(self, bandish_list):
        """Display bandish list"""
        self.bandish_list.clear_widgets()
        
        if not bandish_list:
            empty_label = MDLabel(
                text="No bandish found for selected raagas.\nClick + to add custom bandish.",
                theme_text_color="Custom",
                text_color="#999999",
                halign="center",
                font_style="Body1",
                size_hint_y=None,
                height=dp(80)
            )
            self.bandish_list.add_widget(empty_label)
            return
        
        for bandish in bandish_list:
            is_selected = any(b['id'] == bandish['id'] and b['type'] == bandish['type'] for b in self.selected_bandish)
            card = self.create_bandish_selection_card(bandish, is_selected)
            self.bandish_list.add_widget(card)
    
    def create_bandish_selection_card(self, bandish, is_selected):
        """Create selectable bandish card"""
        card = MDCard(
            padding=dp(15),
            size_hint_y=None,
            height=dp(120),
            elevation=2,
            md_bg_color="#FFF3E0" if is_selected else "#FFFFFF",
            radius=[8],
            on_release=lambda x: self.toggle_bandish_selection(bandish)
        )
        
        card_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        # Header with checkbox and title
        header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(35))
        
        checkbox_icon = "checkbox-marked" if is_selected else "checkbox-blank-outline"
        checkbox = MDIconButton(
            icon=checkbox_icon,
            theme_icon_color="Custom",
            icon_color="#FF9800" if is_selected else "#CCCCCC",
            size_hint_x=None,
            width=dp(40)
        )
        
        title_label = MDLabel(
            text=f"🎵 {bandish['title'][:45]}{'...' if len(bandish['title']) > 45 else ''}",
            theme_text_color="Custom",
            text_color="#E65100" if is_selected else "#8B4513",
            font_style="Subtitle1",
            bold=is_selected,
            size_hint_x=0.9
        )
        
        header_layout.add_widget(checkbox)
        header_layout.add_widget(title_label)
        
        # Details
        details_label = MDLabel(
            text=f"🎼 {bandish['raaga']} • 🥁 {bandish['taal']} • {'👤' if bandish['type'] == 'user' else '📚'} {bandish['btype']}",
            theme_text_color="Custom",
            text_color="#666666",
            font_style="Body2",
            size_hint_y=None,
            height=dp(25)
        )
        
        # Lyrics preview
        lyrics_preview = bandish['lyrics'][:60] + "..." if len(bandish['lyrics']) > 60 else bandish['lyrics']
        lyrics_label = MDLabel(
            text=f"📜 {lyrics_preview}",
            theme_text_color="Custom",
            text_color="#999999",
            font_style="Caption",
            size_hint_y=None,
            height=dp(30)
        )
        
        card_layout.add_widget(header_layout)
        card_layout.add_widget(details_label)
        card_layout.add_widget(lyrics_label)
        card.add_widget(card_layout)
        
        return card
    
    def toggle_bandish_selection(self, bandish):
        """Toggle bandish selection"""
        # Check if already selected
        for i, selected in enumerate(self.selected_bandish):
            if selected['id'] == bandish['id'] and selected['type'] == bandish['type']:
                # Remove from selection
                self.selected_bandish.pop(i)
                self.display_bandish(self.all_bandish)
                return
        
        # Add to selection
        self.selected_bandish.append(bandish)
        self.display_bandish(self.all_bandish)
    
    def filter_bandish(self, instance, text):
        """Filter bandish based on search"""
        search_text = self.search_field.text.lower()
        raaga_filter = self.raaga_filter.text.lower()
        
        filtered_bandish = []
        
        for bandish in self.all_bandish:
            # Check search text match
            search_match = (
                search_text in bandish['title'].lower() or
                search_text in bandish['lyrics'].lower() or
                search_text in bandish['taal'].lower() or
                search_text in bandish['btype'].lower()
            ) if search_text else True
            
            # Check raaga filter match
            raaga_match = raaga_filter in bandish['raaga'].lower() if raaga_filter else True
            
            if search_match and raaga_match:
                filtered_bandish.append(bandish)
        
        self.display_bandish(filtered_bandish)
    
    def add_custom_bandish(self):
        """Show dialog to add custom bandish"""
        content = MDBoxLayout(orientation="vertical", spacing=dp(15), size_hint_y=None, height=dp(400))
        
        self.custom_title = MDTextField(hint_text="Title *", mode="rectangle")
        self.custom_raaga = MDTextField(hint_text="Raaga Name *", mode="rectangle")
        self.custom_taal = MDTextField(hint_text="Taal *", mode="rectangle")
        self.custom_type = MDTextField(hint_text="Type *", mode="rectangle")
        self.custom_lyrics = MDTextField(hint_text="Lyrics *", mode="rectangle", multiline=True, size_hint_y=None, height=dp(100))
        
        content.add_widget(self.custom_title)
        content.add_widget(self.custom_raaga)
        content.add_widget(self.custom_taal)
        content.add_widget(self.custom_type)
        content.add_widget(self.custom_lyrics)
        
        self.custom_dialog = MDDialog(
            title="➕ Add Custom Bandish",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.close_custom_dialog),
                MDFlatButton(text="ADD", theme_text_color="Custom", text_color="#8B4513", on_release=self.save_custom_bandish)
            ]
        )
        self.custom_dialog.open()
    
    def save_custom_bandish(self, *args):
        """Save custom bandish"""
        title = self.custom_title.text.strip()
        raaga = self.custom_raaga.text.strip()
        taal = self.custom_taal.text.strip()
        btype = self.custom_type.text.strip()
        lyrics = self.custom_lyrics.text.strip()
        
        if not all([title, raaga, taal, btype, lyrics]):
            Snackbar(text="All fields are required!").open()
            return
        
        # Add user bandish to database
        bandish_id = self.db_manager.add_user_bandish(title, raaga, taal, btype, lyrics)
        
        if bandish_id:
            # Add to current selection if raaga matches
            if raaga in self.selected_raagas:
                new_bandish = {
                    'id': bandish_id,
                    'type': 'user',  # This will be used in save_concert
                    'title': title,
                    'raaga': raaga,
                    'taal': taal,
                    'btype': btype,
                    'lyrics': lyrics,
                    'is_favorite': False
                }
                self.all_bandish.append(new_bandish)
                self.selected_bandish.append(new_bandish)
                self.display_bandish(self.all_bandish)
            
            Snackbar(text="Custom bandish added successfully!").open()
            self.close_custom_dialog()
        else:
            Snackbar(text="Failed to add custom bandish!").open()
    
    def close_custom_dialog(self, *args):
        """Close custom bandish dialog"""
        if hasattr(self, 'custom_dialog'):
            self.custom_dialog.dismiss()
    
    def confirm_selection(self):
        """Confirm bandish selection and go back"""
        create_screen = self.manager.get_screen("create_concert")
        create_screen.selected_bandish = self.selected_bandish
        create_screen.update_selected_bandish_display()
        self.go_back()
    
    def go_back(self):
        """Go back to create concert screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "create_concert"

class ViewConcertScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "view_concert"
        self.db_manager = db_manager
        self.current_concert_id = None
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="🎵 Concert Details",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        main_layout.add_widget(self.toolbar)
        
        # Scroll content
        scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            adaptive_height=True,
            padding=dp(20)
        )
        scroll.add_widget(self.content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def load_concert(self, concert_id):
        """Load concert details"""
        self.current_concert_id = concert_id
        self.content_layout.clear_widgets()
        
        # Get concert info
        concert = self.db_manager.get_concert_by_id(concert_id)
        if not concert:
            error_label = MDLabel(
                text="Concert not found!",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="H6"
            )
            self.content_layout.add_widget(error_label)
            return
        
        concert_id, name, description, user_id, created_at = concert
        self.toolbar.title = f"🎵 {name}"
        
        # Concert info card
        info_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            height=dp(120),
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[15]
        )
        
        info_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        name_label = MDLabel(
            text=name,
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(35)
        )
        
        details_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(25), spacing=dp(20))
        
        if description:
            desc_label = MDLabel(
                text=f"📝 {description}",
                theme_text_color="Custom",
                text_color="#666666",
                font_style="Body2",
                size_hint_x=0.7
            )
            details_row.add_widget(desc_label)
        
        date_label = MDLabel(
            text=f"📅 {created_at[:10] if created_at else 'Unknown'}",
            theme_text_color="Custom",
            text_color="#999999",
            font_style="Body2",
            size_hint_x=0.3,
            halign="right"
        )
        details_row.add_widget(date_label)
        
        info_layout.add_widget(name_label)
        info_layout.add_widget(details_row)
        info_card.add_widget(info_layout)
        
        self.content_layout.add_widget(info_card)
        
        # Bandish list
        bandish_list = self.db_manager.get_concert_bandish(concert_id)
        
        if not bandish_list:
            empty_card = MDCard(
                padding=dp(20),
                size_hint_y=None,
                height=dp(80),
                elevation=2,
                md_bg_color="#FFFAF0",
                radius=[10]
            )
            
            empty_label = MDLabel(
                text="No bandish in this concert.",
                theme_text_color="Custom",
                text_color="#999999",
                halign="center",
                font_style="Body1"
            )
            empty_card.add_widget(empty_label)
            self.content_layout.add_widget(empty_card)
            return
        
        # Bandish header
        bandish_header = MDLabel(
            text=f"🎵 Bandish ({len(bandish_list)})",
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="H6",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        self.content_layout.add_widget(bandish_header)
        
        # Create cards for each bandish
        for i, item in enumerate(bandish_list, 1):
            link_id, order_index, bandish_id, title, raaga_name, taal, btype, lyrics, source, user_bandish_id = item
            
            card = MDCard(
                padding=dp(20),
                size_hint_y=None,
                height=dp(160),
                elevation=3,
                md_bg_color="#FFFFFF",
                radius=[15],
                on_release=lambda x, bid=bandish_id, ubid=user_bandish_id, src=source: self.view_bandish_detail(bid, ubid, src)
            )
            
            # Main card content
            card_content = MDBoxLayout(orientation="vertical", spacing=dp(10))
            
            # Title row with number
            title_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(35), spacing=dp(10))
            
            # Number badge
            number_label = MDLabel(
                text=f"{i}",
                theme_text_color="Custom",
                text_color="#FFFFFF",
                font_style="H6",
                bold=True,
                size_hint_x=None,
                width=dp(30),
                halign="center",
                valign="middle"
            )
            
            number_card = MDCard(
                size_hint_x=None,
                width=dp(30),
                size_hint_y=None,
                height=dp(30),
                md_bg_color="#8B4513",
                radius=[15],
                elevation=0
            )
            number_card.add_widget(number_label)
            
            # Title
            title_label = MDLabel(
                text=title,
                theme_text_color="Custom",
                text_color="#8B4513",
                font_style="Subtitle1",
                bold=True,
                markup=True
            )
            
            title_row.add_widget(number_card)
            title_row.add_widget(title_label)
            
            # Details row
            details_row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(25), spacing=dp(20))
            
            # Raaga
            raaga_label = MDLabel(
                text=f"🎼 {raaga_name}",
                theme_text_color="Custom",
                text_color="#2E7D32",
                font_style="Body2",
                bold=True,
                size_hint_x=0.4
            )
            
            # Taal
            taal_label = MDLabel(
                text=f"🥁 {taal}",
                theme_text_color="Custom",
                text_color="#1976D2",
                font_style="Body2",
                bold=True,
                size_hint_x=0.3
            )
            
            # Type & Source
            source_icon = "👤" if source == 'user' else "📚"
            type_label = MDLabel(
                text=f"{source_icon} {btype}",
                theme_text_color="Custom",
                text_color="#E91E63" if source == 'user' else "#FF5722",
                font_style="Body2",
                bold=True,
                size_hint_x=0.3
            )
            
            details_row.add_widget(raaga_label)
            details_row.add_widget(taal_label)
            details_row.add_widget(type_label)
            
            # Lyrics preview
            lyrics_preview = lyrics[:60] + "..." if len(lyrics) > 60 else lyrics
            lyrics_label = MDLabel(
                text=f"📜 {lyrics_preview}",
                theme_text_color="Custom",
                text_color="#666666",
                font_style="Caption",
                size_hint_y=None,
                height=dp(40),
                text_size=(None, None),
                valign="top"
            )
            
            # Add rows to card content
            card_content.add_widget(title_row)
            card_content.add_widget(details_row)
            card_content.add_widget(lyrics_label)
            
            # Bind for text wrapping
            def update_lyrics_text_size(instance, size, lyrics_lbl=lyrics_label):
                lyrics_lbl.text_size = (size[0] - dp(40), None)
            
            card.bind(size=update_lyrics_text_size)
            card.add_widget(card_content)
            
            self.content_layout.add_widget(card)
    
    def view_bandish_detail(self, bandish_id, user_bandish_id, source):
        """View bandish details"""
        if source == "original" and bandish_id:
            # Navigate to original bandish detail screen
            detail_screen = self.manager.get_screen("bandish_detail")
            detail_screen.load_bandish_detail(bandish_id)
            self.manager.transition.direction = "left"
            self.manager.current = "bandish_detail"
        elif source == "user" and user_bandish_id:
            # Navigate to user bandish detail screen
            detail_screen = self.manager.get_screen("user_bandish_detail")
            detail_screen.load_user_bandish_detail(user_bandish_id)
            self.manager.transition.direction = "left"
            self.manager.current = "user_bandish_detail"
    
    def go_back(self):
        """Go back to concert list"""
        self.manager.transition.direction = "right"
        self.manager.current = "concert_list"

class UserBandishDetailScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = "user_bandish_detail"
        self.db_manager = db_manager
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical")
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Custom Bandish Details",
            md_bg_color="#8B4513",
            specific_text_color="#FFFFFF",
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        main_layout.add_widget(self.toolbar)
        
        # Scroll content
        self.scroll = MDScrollView()
        self.content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            adaptive_height=True,
            padding=dp(20)
        )
        
        self.scroll.add_widget(self.content_layout)
        main_layout.add_widget(self.scroll)
        self.add_widget(main_layout)
    
    def load_user_bandish_detail(self, user_bandish_id):
        """Load user bandish details"""
        self.content_layout.clear_widgets()
        
        # Get user bandish details
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_bandish WHERE id = ?", (user_bandish_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            error_label = MDLabel(
                text="Custom bandish not found!",
                theme_text_color="Custom",
                text_color="#8B4513",
                halign="center",
                font_style="H6"
            )
            self.content_layout.add_widget(error_label)
            return
        
        user_bandish_id, title, raaga, taal, btype, lyrics, user_id, created_at = result
        
        # Title card with custom indicator
        title_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=5,
            md_bg_color="#E91E63",  # Pink for custom bandish
            radius=[15]
        )
        
        title_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        custom_indicator = MDLabel(
            text="👤 CUSTOM BANDISH",
            theme_text_color="Custom",
            text_color="#FFFFFF",
            font_style="Caption",
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        title_label = MDLabel(
            text=title,
            theme_text_color="Custom",
            text_color="#FFFFFF",
            font_style="H5",
            bold=True,
            halign="center",
            text_size=(None, None),
            size_hint_y=None
        )
        
        title_layout.add_widget(custom_indicator)
        title_layout.add_widget(title_label)
        
        def update_title_text_size(instance, size):
            title_label.text_size = (size[0] - dp(40), None)
            
        title_card.bind(size=update_title_text_size)
        title_label.bind(texture_size=title_label.setter('size'))
        
        def update_title_card_height(instance, texture_size):
            title_card.height = max(dp(100), texture_size[1] + dp(60))
            
        title_label.bind(texture_size=update_title_card_height)
        title_card.add_widget(title_layout)
        
        # Info card
        info_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            size_hint_y=None,
            height=dp(140),
            elevation=3,
            md_bg_color="#FFF8DC",
            radius=[15]
        )
        
        info_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        # Raaga
        raaga_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(30))
        raaga_icon = MDLabel(text="🎼", font_style="H6", size_hint_x=None, width=dp(30))
        raaga_info = MDLabel(
            text=f"Raaga: {raaga}",
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="Subtitle1",
            bold=True,
            size_hint_x=0.9
        )
        raaga_layout.add_widget(raaga_icon)
        raaga_layout.add_widget(raaga_info)
        
        # Taal
        taal_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(25))
        taal_icon = MDLabel(text="🥁", font_style="Body1", size_hint_x=None, width=dp(30))
        taal_info = MDLabel(
            text=f"Taal: {taal}",
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            size_hint_x=0.9
        )
        taal_layout.add_widget(taal_icon)
        taal_layout.add_widget(taal_info)
        
        # Type
        type_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(25))
        type_icon = MDLabel(text="📝", font_style="Body1", size_hint_x=None, width=dp(30))
        type_info = MDLabel(
            text=f"Type: {btype}",
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            size_hint_x=0.9
        )
        type_layout.add_widget(type_icon)
        type_layout.add_widget(type_info)
        
        info_layout.add_widget(raaga_layout)
        info_layout.add_widget(taal_layout)
        info_layout.add_widget(type_layout)
        info_card.add_widget(info_layout)
        
        # Lyrics card
        lyrics_card = MDCard(
            padding=dp(20),
            size_hint_y=None,
            elevation=3,
            md_bg_color="#FFFAF0",
            radius=[15]
        )
        
        lyrics_layout = MDBoxLayout(orientation="vertical", spacing=dp(15))
        
        lyrics_header_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(35))
        lyrics_icon = MDLabel(text="📜", font_style="H6", size_hint_x=None, width=dp(30))
        lyrics_header = MDLabel(
            text="Lyrics",
            theme_text_color="Custom",
            text_color="#8B4513",
            font_style="Subtitle1",
            bold=True,
            size_hint_x=0.9
        )
        lyrics_header_layout.add_widget(lyrics_icon)
        lyrics_header_layout.add_widget(lyrics_header)
        
        lyrics_label = MDLabel(
            text=lyrics,
            theme_text_color="Custom",
            text_color="#654321",
            font_style="Body1",
            text_size=(None, None),
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=True
        )
        
        def update_lyrics_text_size(instance, size):
            lyrics_label.text_size = (size[0] - dp(40), None)
            
        lyrics_card.bind(size=update_lyrics_text_size)
        lyrics_label.bind(texture_size=lyrics_label.setter('size'))
        
        def update_lyrics_card_height(instance, texture_size):
            lyrics_card.height = lyrics_header_layout.height + texture_size[1] + dp(55)
            
        lyrics_label.bind(texture_size=update_lyrics_card_height)
        
        lyrics_layout.add_widget(lyrics_header_layout)
        lyrics_layout.add_widget(lyrics_label)
        lyrics_card.add_widget(lyrics_layout)
        
        self.content_layout.add_widget(title_card)
        self.content_layout.add_widget(info_card)
        self.content_layout.add_widget(lyrics_card)
    
    def go_back(self):
        """Go back to previous screen"""
        self.manager.transition.direction = "right"
        self.manager.current = "view_concert"

class GetBandishApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize database
        self.db_manager = DatabaseManager()
        
    def build(self):
        # Set app theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent_palette = "Amber"
        
        # Create screen manager
        sm = MDScreenManager()
        
        # Add screens
        sm.add_widget(WelcomeScreen())
        sm.add_widget(MainScreen(self.db_manager))
        sm.add_widget(BandishListScreen(self.db_manager))
        sm.add_widget(BandishDetailScreen(self.db_manager))
        sm.add_widget(SearchScreen(self.db_manager))
        sm.add_widget(AdminLoginScreen(self.db_manager))
        sm.add_widget(AdminPanelScreen(self.db_manager))
        
        # Add concert screens
        sm.add_widget(ConcertListScreen(self.db_manager))
        sm.add_widget(CreateConcertScreen(self.db_manager))
        sm.add_widget(SelectRaagasScreen(self.db_manager))
        sm.add_widget(SelectBandishScreen(self.db_manager))
        sm.add_widget(ViewConcertScreen(self.db_manager))
        sm.add_widget(UserBandishDetailScreen(self.db_manager))
        
        return sm

# Run the app
if __name__ == "__main__":
    GetBandishApp().run() 