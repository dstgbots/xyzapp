# Data utilities for GetBandish app with SQLite Database
# This file now contains database-related constants and helper functions

# Database configuration
DATABASE_NAME = "getbandish.db"

# App information
APP_INFO = {
    "name": "GetBandish",
    "version": "2.0 (SQLite Edition)",
    "author": "K Kousthubh Bhat (BCA 2nd Year Student)",
    "description": "A modern mobile app for classical Indian music compositions"
}

# Color theme constants
COLORS = {
    "primary_brown": "#8B4513",
    "dark_brown": "#4A2C2A",
    "light_cream": "#FFF8DC",
    "beige": "#F5F5DC",
    "gold": "#D4AF37",
    "white": "#FFFFFF",
    "green": "#228B22",
    "tan": "#CD853F",
    "dark_brown_text": "#654321",
    "floral_white": "#FFFAF0"
}

# UI constants
UI_SETTINGS = {
    "welcome_delay": 3,  # seconds
    "card_height": 80,   # dp
    "bandish_card_height": 120,  # dp
    "title_card_height": 100,    # dp
    "info_card_height": 120,     # dp
    "spacing": 10,       # dp
    "padding": 20,       # dp
    "elevation": 3,      # shadow
    "radius": 15         # card radius
}

# Database table schemas for reference
SCHEMA_INFO = {
    "raagas": [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "name TEXT UNIQUE NOT NULL",
        "description TEXT",
        "is_active INTEGER DEFAULT 0",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ],
    "bandish": [
        "id INTEGER PRIMARY KEY AUTOINCREMENT", 
        "title TEXT NOT NULL",
        "raaga_id INTEGER",
        "taal TEXT NOT NULL",
        "type TEXT NOT NULL",
        "lyrics TEXT NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (raaga_id) REFERENCES raagas (id)"
    ]
}

# Status messages
STATUS_MESSAGES = {
    "coming_soon": "This raaga will be available in future updates!",
    "search_coming_soon": "Search functionality will be available in future updates!",
    "no_bandish": "No bandish found for this raaga.",
    "bandish_not_found": "Bandish not found!",
    "database_initialized": "Database initialized with sample data!"
}

# Menu text template
def get_menu_text(stats):
    """Generate menu text with database statistics"""
    return f"""About GetBandish

{APP_INFO['description']} by {APP_INFO['author']}

Database Statistics:
• Total Raagas: {stats['total_raagas']}
• Active Raagas: {stats['active_raagas']} 
• Total Bandish: {stats['total_bandish']}

Version: {APP_INFO['version']}"""

# Helper functions for data formatting
def format_bandish_title(title, max_length=50):
    """Format bandish title for display"""
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title

def format_lyrics_preview(lyrics, max_lines=3):
    """Format lyrics for preview display"""
    lines = lyrics.split('\n')
    if len(lines) > max_lines:
        return '\n'.join(lines[:max_lines]) + '\n...'
    return lyrics

def get_raaga_display_name(name):
    """Format raaga name for better display"""
    # Could add logic here for better formatting
    return name

# Database validation functions
def validate_raaga_name(name):
    """Validate raaga name before database insertion"""
    if not name or len(name.strip()) == 0:
        return False, "Raaga name cannot be empty"
    if len(name) > 100:
        return False, "Raaga name too long"
    return True, ""

def validate_bandish_data(title, taal, bandish_type, lyrics):
    """Validate bandish data before database insertion"""
    errors = []
    
    if not title or len(title.strip()) == 0:
        errors.append("Title cannot be empty")
    
    if not taal or len(taal.strip()) == 0:
        errors.append("Taal cannot be empty")
    
    if not bandish_type or len(bandish_type.strip()) == 0:
        errors.append("Type cannot be empty")
    
    if not lyrics or len(lyrics.strip()) == 0:
        errors.append("Lyrics cannot be empty")
    
    if errors:
        return False, "; ".join(errors)
    return True, ""

# Data file for GetBandish app
# Contains all bandish and raaga information

RAAGA_DATA = {
    "Abhogi / Abhogi Kanada": [
        {
            "title": "LAAJA RAKHA LIJO MORI SAAHABA, SATTAARA...",
            "raag": "Abhogi / Abhogi Kanada",
            "taal": "Ek Taal",
            "type": "Chota Khayal",
            "lyrics": """LAAJA RAKHA LIJO MORI SAAHABA, SATTAARA, NIRAAKAARA, JAGA KE DAATAA |

TU RAHIMA RAAMA TU, TERI MAAYAA APARANPAARA
MOHE TORE KARAMA KO AADHAARA, JAGA KE DAATAA ||"""
        },
        {
            "title": "TU EKA SAACHAA SAAHEBA MERAA MAI NITA B...",
            "raag": "Abhogi / Abhogi Kanada", 
            "taal": "Teen Taal",
            "type": "Chota Khayal",
            "lyrics": "TU EKA SAACHAA SAAHEBA MERAA MAI NITA B...\n\nSample lyrics for this bandish would go here..."
        },
        {
            "title": "MANA RAAMA RANGILE MOHANA SHYAAMA JASOD...",
            "raag": "Abhogi / Abhogi Kanada",
            "taal": "Teen Taal", 
            "type": "Chota Khayal",
            "lyrics": "MANA RAAMA RANGILE MOHANA SHYAAMA JASOD...\n\nSample lyrics for this bandish would go here..."
        },
        {
            "title": "RASA BARASATA TORE GHARA RASIKA SAJANA...",
            "raag": "Abhogi / Abhogi Kanada",
            "taal": "Ek Taal",
            "type": "Chota Khayal", 
            "lyrics": "RASA BARASATA TORE GHARA RASIKA SAJANA...\n\nSample lyrics for this bandish would go here..."
        },
        {
            "title": "ATI MRUDU GAAYO GANDHAARA KO NISHI AUDA...",
            "raag": "Abhogi / Abhogi Kanada",
            "taal": "Jhap Taal",
            "type": "Lakshan Geet",
            "lyrics": "ATI MRUDU GAAYO GANDHAARA KO NISHI AUDA...\n\nSample lyrics for this bandish would go here..."
        },
        {
            "title": "JUGANA JIVE LAALA TERO MAAI DEHON DAAN...",
            "raag": "Abhogi / Abhogi Kanada",
            "taal": "Roopak",
            "type": "Bada Khayal",
            "lyrics": "JUGANA JIVE LAALA TERO MAAI DEHON DAAN...\n\nSample lyrics for this bandish would go here..."
        }
    ]
}

ALL_RAAGAS = [
    "Abhogi / Abhogi Kanada",
    "Abhogi, Shiv", 
    "Adana",
    "Ahir Lalat / Ahir Lalit",
    "Amrit Varshini",
    "Asavari",
    "Asavari, Jogi",
    "Asavari, Komal Rishabh / Komal Asavari",
    "Asavari, Sindhura",
    "Bageshree",
    "Bageshree, Audav (Bageshree Kauns or Purana Chandrakauns)",
    "Bageshree, Komal",
    "Bagkauns",
    "Bahar",
    "Bahar, Adana / Adana Bahar"
] 