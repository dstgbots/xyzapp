# Database manager for GetBandish app
# Handles all SQLite operations for raagas and bandish

import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="getbandish.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Create tables if they don't exist and update schema if needed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create raagas table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create bandish table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bandish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                raaga_id INTEGER,
                taal TEXT NOT NULL,
                type TEXT NOT NULL,
                lyrics TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (raaga_id) REFERENCES raagas (id)
            )
        ''')
        
        # Create concerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                user_id TEXT DEFAULT 'default_user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_bandish table (for custom bandish added by users)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_bandish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                raaga_name TEXT NOT NULL,
                taal TEXT NOT NULL,
                type TEXT NOT NULL,
                lyrics TEXT NOT NULL,
                user_id TEXT DEFAULT 'default_user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create concert_bandish table (links concerts to bandish)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS concert_bandish (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concert_id INTEGER,
                bandish_id INTEGER,
                user_bandish_id INTEGER,
                order_index INTEGER DEFAULT 0,
                FOREIGN KEY (concert_id) REFERENCES concerts (id),
                FOREIGN KEY (bandish_id) REFERENCES bandish (id),
                FOREIGN KEY (user_bandish_id) REFERENCES user_bandish (id)
            )
        ''')
        
        # Update schema if needed - add is_favorite columns
        self.update_schema()
        
        conn.commit()
        conn.close()
        
        # Populate with initial data if database is empty
        if self.is_database_empty():
            self.populate_initial_data()
            
    def update_schema(self):
        """Update database schema to add any missing columns"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if is_favorite column exists in raagas table
        cursor.execute("PRAGMA table_info(raagas)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add is_favorite column to raagas if it doesn't exist
        if 'is_favorite' not in columns:
            try:
                print("Adding is_favorite column to raagas table...")
                cursor.execute("ALTER TABLE raagas ADD COLUMN is_favorite INTEGER DEFAULT 0")
            except Exception as e:
                print(f"Error adding column: {e}")
        
        # Check if is_favorite column exists in bandish table
        cursor.execute("PRAGMA table_info(bandish)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add is_favorite column to bandish if it doesn't exist
        if 'is_favorite' not in columns:
            try:
                print("Adding is_favorite column to bandish table...")
                cursor.execute("ALTER TABLE bandish ADD COLUMN is_favorite INTEGER DEFAULT 0")
            except Exception as e:
                print(f"Error adding column: {e}")
        
        conn.commit()
        conn.close()
    
    def is_database_empty(self):
        """Check if database has any data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM raagas")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    
    def populate_initial_data(self):
        """Add initial raaga and bandish data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insert raagas
        raagas = [
            ("Abhogi / Abhogi Kanada", "Classical raaga with serene character", 1),
            ("Abhogi, Shiv", "Variation of Abhogi raaga", 0),
            ("Adana", "Evening raaga with romantic mood", 0),
            ("Ahir Lalat / Ahir Lalit", "Morning raaga", 0),
            ("Amrit Varshini", "Devotional raaga", 0),
            ("Asavari", "Morning raaga with serious mood", 0),
            ("Asavari, Jogi", "Variation of Asavari", 0),
            ("Asavari, Komal Rishabh / Komal Asavari", "Asavari with flat second", 0),
            ("Asavari, Sindhura", "Regional variation", 0),
            ("Bageshree", "Late night raaga", 0),
            ("Bageshree, Audav (Bageshree Kauns or Purana Chandrakauns)", "Pentatonic version", 0),
            ("Bageshree, Komal", "Flat version of Bageshree", 0),
            ("Bagkauns", "Night raaga", 0),
            ("Bahar", "Spring season raaga", 0),
            ("Bahar, Adana / Adana Bahar", "Fusion raaga", 0)
        ]
        
        for raaga in raagas:
            cursor.execute("INSERT OR IGNORE INTO raagas (name, description, is_active) VALUES (?, ?, ?)", raaga)
        
        # Get Abhogi raaga ID
        cursor.execute("SELECT id FROM raagas WHERE name = 'Abhogi / Abhogi Kanada'")
        abhogi_id = cursor.fetchone()[0]
        
        # Insert bandish for Abhogi raaga
        bandish_data = [
            (
                "LAAJA RAKHA LIJO MORI SAAHABA, SATTAARA...",
                abhogi_id,
                "Ek Taal",
                "Chota Khayal",
                """LAAJA RAKHA LIJO MORI SAAHABA, SATTAARA, NIRAAKAARA, JAGA KE DAATAA |

TU RAHIMA RAAMA TU, TERI MAAYAA APARANPAARA
MOHE TORE KARAMA KO AADHAARA, JAGA KE DAATAA ||"""
            ),
            (
                "TU EKA SAACHAA SAAHEBA MERAA MAI NITA B...",
                abhogi_id,
                "Teen Taal",
                "Chota Khayal",
                """TU EKA SAACHAA SAAHEBA MERAA MAI NITA BHAJAN KARAUN |

TERAA NAAMA LETA RAHUN, HARI NAAMA SUKHA PAUN
SATSANGA MEIN RAHAUN, GURU CHARAN MEIN LAAGAUN ||"""
            ),
            (
                "MANA RAAMA RANGILE MOHANA SHYAAMA JASOD...",
                abhogi_id,
                "Teen Taal",
                "Chota Khayal",
                """MANA RAAMA RANGILE MOHANA SHYAAMA JASODAA NANDANA |

GOKULA MEIN KHELATA, GOVINDA GOPAAL KANHAA
MURALI DHARA MOHAN, RADHAA RAMANA KANHAA ||"""
            ),
            (
                "RASA BARASATA TORE GHARA RASIKA SAJANA...",
                abhogi_id,
                "Ek Taal",
                "Chota Khayal",
                """RASA BARASATA TORE GHARA RASIKA SAJANA AAYO |

PREMA RASA SE BHARA, HRIDAYA MEIN BASAAYO
BHAKTI BHAVA SE JHUMA, ANANDA MEIN LAAYO ||"""
            ),
            (
                "ATI MRUDU GAAYO GANDHAARA KO NISHI AUDA...",
                abhogi_id,
                "Jhap Taal",
                "Lakshan Geet",
                """ATI MRUDU GAAYO GANDHAARA KO NISHI AUDAVA JEEVAAYE |

KOMAL GANDHAARA MADHYAMA, PANCHAM SHUDDHA DHAIVATAT
SHUDDHA NISHAAD OMKAARA, ABHOGI RAAGA SAAJAAYE ||"""
            ),
            (
                "JUGANA JIVE LAALA TERO MAAI DEHON DAAN...",
                abhogi_id,
                "Roopak",
                "Bada Khayal",
                """JUGANA JIVE LAALA TERO MAAI DEHON DAAN |

SABA SUKHA SAMPATI TERI, TU HAIN BHAGAVAAN
JEEVAN MARAN TERAA MAAI, TUJH MEIN SAMAAN ||"""
            )
        ]
        
        for bandish in bandish_data:
            cursor.execute("""
                INSERT OR IGNORE INTO bandish (title, raaga_id, taal, type, lyrics) 
                VALUES (?, ?, ?, ?, ?)
            """, bandish)
        
        conn.commit()
        conn.close()
        print("Database initialized with sample data!")
    
    def get_all_raagas(self, favorites_only=False):
        """Get all raagas from database. If favorites_only is True, return only favorites"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if favorites_only:
            cursor.execute("SELECT id, name, is_active, is_favorite FROM raagas WHERE is_favorite = 1 ORDER BY name")
        else:
            cursor.execute("SELECT id, name, is_active, is_favorite FROM raagas ORDER BY name")
            
        raagas = cursor.fetchall()
        conn.close()
        return raagas
    
    def get_bandish_by_raaga(self, raaga_name, favorites_only=False):
        """Get all bandish for a specific raaga. If favorites_only is True, return only favorites"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if favorites_only:
            cursor.execute("""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                WHERE r.name = ? AND b.is_favorite = 1
                ORDER BY b.title
            """, (raaga_name,))
        else:
            cursor.execute("""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                WHERE r.name = ?
                ORDER BY b.title
            """, (raaga_name,))
            
        bandish = cursor.fetchall()
        conn.close()
        return bandish
    
    def get_bandish_by_id(self, bandish_id):
        """Get specific bandish by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
            FROM bandish b 
            JOIN raagas r ON b.raaga_id = r.id 
            WHERE b.id = ?
        """, (bandish_id,))
        bandish = cursor.fetchone()
        conn.close()
        return bandish
    
    def add_raaga(self, name, description="", is_active=0):
        """Add new raaga to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO raagas (name, description, is_active) VALUES (?, ?, ?)", 
                         (name, description, is_active))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def add_bandish(self, title, raaga_name, taal, type_name, lyrics):
        """Add new bandish to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get raaga ID
        cursor.execute("SELECT id FROM raagas WHERE name = ?", (raaga_name,))
        raaga_result = cursor.fetchone()
        
        if not raaga_result:
            conn.close()
            return None
        
        raaga_id = raaga_result[0]
        
        try:
            cursor.execute("""
                INSERT INTO bandish (title, raaga_id, taal, type, lyrics) 
                VALUES (?, ?, ?, ?, ?)
            """, (title, raaga_id, taal, type_name, lyrics))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding bandish: {e}")
            return None
        finally:
            conn.close()
    
    def search_bandish(self, search_term, favorites_only=False):
        """Enhanced search for bandish by title, lyrics, raaga, taal, or type with partial word matching"""
        if not search_term.strip():
            # If empty search term, return all bandish
            return self.get_all_bandish(favorites_only)
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Split search term into individual words for better matching
        search_words = search_term.strip().split()
        
        # Create search patterns for each word
        search_patterns = []
        params = []
        
        for word in search_words:
            pattern = f"%{word}%"
            search_patterns.append("""
                (b.title LIKE ? OR b.lyrics LIKE ? OR r.name LIKE ? OR b.taal LIKE ? OR b.type LIKE ?)
            """)
            params.extend([pattern, pattern, pattern, pattern, pattern])
        
        # Combine all patterns with AND (all words must match somewhere)
        where_clause = " AND ".join(search_patterns)
        
        if favorites_only:
            query = f"""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                WHERE ({where_clause}) AND b.is_favorite = 1
                ORDER BY b.title
            """
        else:
            query = f"""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                WHERE {where_clause}
                ORDER BY b.title
            """
            
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_all_bandish(self, favorites_only=False):
        """Get all bandish, optionally filtered by favorites"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if favorites_only:
            cursor.execute("""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                WHERE b.is_favorite = 1
                ORDER BY r.name, b.title
            """)
        else:
            cursor.execute("""
                SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
                FROM bandish b 
                JOIN raagas r ON b.raaga_id = r.id 
                ORDER BY r.name, b.title
            """)
            
        results = cursor.fetchall()
        conn.close()
        return results
    
    def search_raagas(self, search_term, favorites_only=False):
        """Enhanced search for raagas by name or description with partial word matching"""
        if not search_term.strip():
            # If empty search term, return all raagas
            return self.get_all_raagas(favorites_only)
            
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Split search term into individual words for better matching
        search_words = search_term.strip().split()
        
        # Create search patterns for each word
        search_patterns = []
        params = []
        
        for word in search_words:
            pattern = f"%{word}%"
            search_patterns.append("(name LIKE ? OR description LIKE ?)")
            params.extend([pattern, pattern])
        
        # Combine all patterns with AND (all words must match somewhere)
        where_clause = " AND ".join(search_patterns)
        
        if favorites_only:
            query = f"""
                SELECT id, name, is_active, is_favorite 
                FROM raagas 
                WHERE ({where_clause}) AND is_favorite = 1
                ORDER BY name
            """
        else:
            query = f"""
                SELECT id, name, is_active, is_favorite 
                FROM raagas 
                WHERE {where_clause}
                ORDER BY name
            """
            
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM raagas")
        total_raagas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM raagas WHERE is_active = 1")
        active_raagas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM raagas WHERE is_favorite = 1")
        favorite_raagas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bandish")
        total_bandish = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bandish WHERE is_favorite = 1")
        favorite_bandish = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_raagas': total_raagas,
            'active_raagas': active_raagas,
            'total_bandish': total_bandish,
            'favorite_raagas': favorite_raagas,
            'favorite_bandish': favorite_bandish
        }

    def get_all_favorites(self):
        """Get all favorite bandish from all raagas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.title, r.name, b.taal, b.type, b.lyrics, b.is_favorite 
            FROM bandish b 
            JOIN raagas r ON b.raaga_id = r.id 
            WHERE b.is_favorite = 1
            ORDER BY r.name, b.title
        """)
        bandish = cursor.fetchall()
        conn.close()
        return bandish

    def toggle_raaga_favorite(self, raaga_id):
        """Toggle the favorite status of a raaga"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current favorite status
        cursor.execute("SELECT is_favorite FROM raagas WHERE id = ?", (raaga_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
            
        current_status = result[0]
        new_status = 0 if current_status else 1
        
        # Update status
        cursor.execute("UPDATE raagas SET is_favorite = ? WHERE id = ?", (new_status, raaga_id))
        conn.commit()
        conn.close()
        
        return new_status
        
    def toggle_bandish_favorite(self, bandish_id):
        """Toggle the favorite status of a bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current favorite status
        cursor.execute("SELECT is_favorite FROM bandish WHERE id = ?", (bandish_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
            
        current_status = result[0]
        new_status = 0 if current_status else 1
        
        # Update status
        cursor.execute("UPDATE bandish SET is_favorite = ? WHERE id = ?", (new_status, bandish_id))
        conn.commit()
        conn.close()
        
        return new_status
    
    def delete_raaga(self, raaga_id):
        """Delete a raaga and all its associated bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # First delete all bandish associated with this raaga
            cursor.execute("DELETE FROM bandish WHERE raaga_id = ?", (raaga_id,))
            
            # Then delete the raaga
            cursor.execute("DELETE FROM raagas WHERE id = ?", (raaga_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting raaga: {e}")
            return False
        finally:
            conn.close()
    
    def delete_bandish(self, bandish_id):
        """Delete a specific bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM bandish WHERE id = ?", (bandish_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting bandish: {e}")
            return False
        finally:
            conn.close()
    
    def update_raaga(self, raaga_id, name, description, is_active):
        """Update raaga information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE raagas 
                SET name = ?, description = ?, is_active = ?
                WHERE id = ?
            """, (name, description, is_active, raaga_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating raaga: {e}")
            return False
        finally:
            conn.close()
    
    def update_bandish(self, bandish_id, title, raaga_name, taal, type_name, lyrics):
        """Update bandish information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get raaga ID
            cursor.execute("SELECT id FROM raagas WHERE name = ?", (raaga_name,))
            raaga_result = cursor.fetchone()
            
            if not raaga_result:
                return False
            
            raaga_id = raaga_result[0]
            
            cursor.execute("""
                UPDATE bandish 
                SET title = ?, raaga_id = ?, taal = ?, type = ?, lyrics = ?
                WHERE id = ?
            """, (title, raaga_id, taal, type_name, lyrics, bandish_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating bandish: {e}")
            return False
        finally:
            conn.close()
    
    def get_raaga_by_id(self, raaga_id):
        """Get specific raaga by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, is_active, is_favorite FROM raagas WHERE id = ?", (raaga_id,))
        raaga = cursor.fetchone()
        conn.close()
        return raaga
    
    # ===== CONCERT MANAGEMENT METHODS =====
    
    def create_concert(self, name, description="", user_id="default_user"):
        """Create a new concert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO concerts (name, description, user_id) 
                VALUES (?, ?, ?)
            """, (name, description, user_id))
            concert_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return concert_id
        except Exception as e:
            print(f"Error creating concert: {e}")
            conn.close()
            return None
    
    def get_all_concerts(self, user_id="default_user"):
        """Get all concerts for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.name, c.description, c.created_at, 
                   COUNT(cb.id) as bandish_count
            FROM concerts c
            LEFT JOIN concert_bandish cb ON c.id = cb.concert_id
            WHERE c.user_id = ?
            GROUP BY c.id, c.name, c.description, c.created_at
            ORDER BY c.created_at DESC
        """, (user_id,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_concert_by_id(self, concert_id):
        """Get concert details by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM concerts WHERE id = ?", (concert_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def update_concert(self, concert_id, name, description=""):
        """Update concert details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE concerts 
                SET name = ?, description = ? 
                WHERE id = ?
            """, (name, description, concert_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating concert: {e}")
            conn.close()
            return False
    
    def delete_concert(self, concert_id):
        """Delete a concert and its associated bandish links"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # First delete all bandish links
            cursor.execute("DELETE FROM concert_bandish WHERE concert_id = ?", (concert_id,))
            # Then delete the concert
            cursor.execute("DELETE FROM concerts WHERE id = ?", (concert_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting concert: {e}")
            conn.close()
            return False
    
    def add_bandish_to_concert(self, concert_id, bandish_id=None, user_bandish_id=None):
        """Add bandish to concert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # Get current max order index
            cursor.execute("""
                SELECT COALESCE(MAX(order_index), -1) + 1 
                FROM concert_bandish 
                WHERE concert_id = ?
            """, (concert_id,))
            next_order = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO concert_bandish (concert_id, bandish_id, user_bandish_id, order_index) 
                VALUES (?, ?, ?, ?)
            """, (concert_id, bandish_id, user_bandish_id, next_order))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding bandish to concert: {e}")
            conn.close()
            return False
    
    def remove_bandish_from_concert(self, concert_id, bandish_id=None, user_bandish_id=None):
        """Remove bandish from concert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if bandish_id:
                cursor.execute("""
                    DELETE FROM concert_bandish 
                    WHERE concert_id = ? AND bandish_id = ?
                """, (concert_id, bandish_id))
            elif user_bandish_id:
                cursor.execute("""
                    DELETE FROM concert_bandish 
                    WHERE concert_id = ? AND user_bandish_id = ?
                """, (concert_id, user_bandish_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error removing bandish from concert: {e}")
            conn.close()
            return False
    
    def get_concert_bandish(self, concert_id):
        """Get all bandish in a concert"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                cb.id as link_id,
                cb.order_index,
                b.id as bandish_id,
                b.title,
                r.name as raaga_name,
                b.taal,
                b.type,
                b.lyrics,
                'original' as source,
                ub.id as user_bandish_id
            FROM concert_bandish cb
            LEFT JOIN bandish b ON cb.bandish_id = b.id
            LEFT JOIN raagas r ON b.raaga_id = r.id
            LEFT JOIN user_bandish ub ON cb.user_bandish_id = ub.id
            WHERE cb.concert_id = ? AND b.id IS NOT NULL
            
            UNION ALL
            
            SELECT 
                cb.id as link_id,
                cb.order_index,
                NULL as bandish_id,
                ub.title,
                ub.raaga_name,
                ub.taal,
                ub.type,
                ub.lyrics,
                'user' as source,
                ub.id as user_bandish_id
            FROM concert_bandish cb
            JOIN user_bandish ub ON cb.user_bandish_id = ub.id
            WHERE cb.concert_id = ? AND ub.id IS NOT NULL
            
            ORDER BY order_index
        """, (concert_id, concert_id))
        results = cursor.fetchall()
        conn.close()
        return results
    
    # ===== USER BANDISH MANAGEMENT METHODS =====
    
    def add_user_bandish(self, title, raaga_name, taal, type_name, lyrics, user_id="default_user"):
        """Add custom bandish for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO user_bandish (title, raaga_name, taal, type, lyrics, user_id) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, raaga_name, taal, type_name, lyrics, user_id))
            bandish_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return bandish_id
        except Exception as e:
            print(f"Error adding user bandish: {e}")
            conn.close()
            return None
    
    def get_user_bandish_by_raaga(self, raaga_name, user_id="default_user"):
        """Get user's custom bandish for a specific raaga"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, raaga_name, taal, type, lyrics
            FROM user_bandish 
            WHERE raaga_name = ? AND user_id = ?
            ORDER BY created_at DESC
        """, (raaga_name, user_id))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_all_user_bandish(self, user_id="default_user"):
        """Get all user's custom bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, raaga_name, taal, type, lyrics
            FROM user_bandish 
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def update_user_bandish(self, bandish_id, title, raaga_name, taal, type_name, lyrics):
        """Update user's custom bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE user_bandish 
                SET title = ?, raaga_name = ?, taal = ?, type = ?, lyrics = ?
                WHERE id = ?
            """, (title, raaga_name, taal, type_name, lyrics, bandish_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user bandish: {e}")
            conn.close()
            return False
    
    def delete_user_bandish(self, bandish_id):
        """Delete user's custom bandish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # First remove from any concerts
            cursor.execute("DELETE FROM concert_bandish WHERE user_bandish_id = ?", (bandish_id,))
            # Then delete the user bandish
            cursor.execute("DELETE FROM user_bandish WHERE id = ?", (bandish_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user bandish: {e}")
            conn.close()
            return False 