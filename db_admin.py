# Database Admin Tool for GetBandish
# Simple tool to manage raagas and bandish in SQLite database

from database import DatabaseManager
import sys

class DatabaseAdmin:
    def __init__(self):
        self.db = DatabaseManager()
        
    def show_menu(self):
        print("\n=== GetBandish Database Admin Tool ===")
        print("1. View all raagas")
        print("2. View all bandish")
        print("3. Add new raaga")
        print("4. Add new bandish")
        print("5. Activate/Deactivate raaga")
        print("6. Search bandish")
        print("7. Database statistics")
        print("8. Export data")
        print("0. Exit")
        print("=" * 40)
        
    def view_all_raagas(self):
        print("\n--- All Raagas ---")
        raagas = self.db.get_all_raagas()
        if not raagas:
            print("No raagas found!")
            return
            
        print(f"{'ID':<5} {'Name':<40} {'Status':<10}")
        print("-" * 60)
        for raaga_id, name, is_active in raagas:
            status = "Active" if is_active else "Inactive"
            print(f"{raaga_id:<5} {name:<40} {status:<10}")
            
    def view_all_bandish(self):
        print("\n--- All Bandish ---")
        # Get all raagas first
        raagas = self.db.get_all_raagas()
        
        for raaga_id, raaga_name, is_active in raagas:
            bandish_list = self.db.get_bandish_by_raaga(raaga_name)
            if bandish_list:
                print(f"\nRaaga: {raaga_name}")
                print("-" * 50)
                for bid, title, raaga, taal, btype, lyrics in bandish_list:
                    print(f"  {bid}. {title}")
                    print(f"     Taal: {taal}, Type: {btype}")
                    print(f"     Lyrics preview: {lyrics[:50]}...")
                    print()
    
    def add_new_raaga(self):
        print("\n--- Add New Raaga ---")
        name = input("Enter raaga name: ").strip()
        description = input("Enter description (optional): ").strip()
        is_active = input("Make active? (y/n): ").strip().lower() == 'y'
        
        if not name:
            print("Error: Raaga name cannot be empty!")
            return
            
        raaga_id = self.db.add_raaga(name, description, 1 if is_active else 0)
        if raaga_id:
            print(f"Raaga added successfully with ID: {raaga_id}")
        else:
            print("Error: Raaga might already exist!")
    
    def add_new_bandish(self):
        print("\n--- Add New Bandish ---")
        
        # Show available raagas
        print("Available raagas:")
        raagas = self.db.get_all_raagas()
        for raaga_id, name, is_active in raagas:
            status = " (Active)" if is_active else " (Inactive)"
            print(f"  {raaga_id}. {name}{status}")
        
        raaga_name = input("\nEnter raaga name: ").strip()
        title = input("Enter bandish title: ").strip()
        taal = input("Enter taal: ").strip()
        btype = input("Enter type (e.g., Chota Khayal, Bada Khayal): ").strip()
        
        print("Enter lyrics (press Enter twice when done):")
        lyrics_lines = []
        while True:
            line = input()
            if line == "" and lyrics_lines and lyrics_lines[-1] == "":
                break
            lyrics_lines.append(line)
        
        lyrics = "\n".join(lyrics_lines).strip()
        
        if not all([raaga_name, title, taal, btype, lyrics]):
            print("Error: All fields are required!")
            return
            
        bandish_id = self.db.add_bandish(title, raaga_name, taal, btype, lyrics)
        if bandish_id:
            print(f"Bandish added successfully with ID: {bandish_id}")
        else:
            print("Error: Could not add bandish. Check if raaga exists!")
    
    def toggle_raaga_status(self):
        print("\n--- Activate/Deactivate Raaga ---")
        self.view_all_raagas()
        
        try:
            raaga_id = int(input("\nEnter raaga ID to toggle: "))
            # This would require adding update functionality to DatabaseManager
            print("Feature not yet implemented - would need to add update method to DatabaseManager")
        except ValueError:
            print("Invalid ID!")
    
    def search_bandish(self):
        print("\n--- Search Bandish ---")
        search_term = input("Enter search term: ").strip()
        
        if not search_term:
            print("Search term cannot be empty!")
            return
            
        results = self.db.search_bandish(search_term)
        
        if not results:
            print("No bandish found!")
            return
            
        print(f"\nFound {len(results)} bandish:")
        print("-" * 60)
        
        for bid, title, raaga, taal, btype, lyrics in results:
            print(f"{bid}. {title}")
            print(f"   Raaga: {raaga}, Taal: {taal}, Type: {btype}")
            print(f"   Lyrics: {lyrics[:100]}...")
            print()
    
    def show_statistics(self):
        print("\n--- Database Statistics ---")
        stats = self.db.get_database_stats()
        
        print(f"Total Raagas: {stats['total_raagas']}")
        print(f"Active Raagas: {stats['active_raagas']}")
        print(f"Inactive Raagas: {stats['total_raagas'] - stats['active_raagas']}")
        print(f"Total Bandish: {stats['total_bandish']}")
        
        # Show bandish per raaga
        print("\nBandish per Raaga:")
        raagas = self.db.get_all_raagas()
        for raaga_id, name, is_active in raagas:
            bandish_count = len(self.db.get_bandish_by_raaga(name))
            status = " (Active)" if is_active else ""
            print(f"  {name}{status}: {bandish_count} bandish")
    
    def export_data(self):
        print("\n--- Export Data ---")
        filename = input("Enter filename (without extension): ").strip()
        if not filename:
            filename = "getbandish_export"
        
        filename += ".txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("GetBandish Database Export\n")
                f.write("=" * 50 + "\n\n")
                
                # Export statistics
                stats = self.db.get_database_stats()
                f.write(f"Statistics:\n")
                f.write(f"Total Raagas: {stats['total_raagas']}\n")
                f.write(f"Active Raagas: {stats['active_raagas']}\n")
                f.write(f"Total Bandish: {stats['total_bandish']}\n\n")
                
                # Export all data
                raagas = self.db.get_all_raagas()
                for raaga_id, raaga_name, is_active in raagas:
                    status = "ACTIVE" if is_active else "INACTIVE"
                    f.write(f"RAAGA: {raaga_name} ({status})\n")
                    f.write("-" * 50 + "\n")
                    
                    bandish_list = self.db.get_bandish_by_raaga(raaga_name)
                    if bandish_list:
                        for bid, title, raaga, taal, btype, lyrics in bandish_list:
                            f.write(f"\nBandish ID: {bid}\n")
                            f.write(f"Title: {title}\n")
                            f.write(f"Taal: {taal}\n")
                            f.write(f"Type: {btype}\n")
                            f.write(f"Lyrics:\n{lyrics}\n")
                            f.write("-" * 30 + "\n")
                    else:
                        f.write("No bandish available\n")
                    
                    f.write("\n")
            
            print(f"Data exported to {filename}")
            
        except Exception as e:
            print(f"Error exporting data: {e}")
    
    def run(self):
        print("Welcome to GetBandish Database Admin Tool!")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == "0":
                    print("Goodbye!")
                    break
                elif choice == "1":
                    self.view_all_raagas()
                elif choice == "2":
                    self.view_all_bandish()
                elif choice == "3":
                    self.add_new_raaga()
                elif choice == "4":
                    self.add_new_bandish()
                elif choice == "5":
                    self.toggle_raaga_status()
                elif choice == "6":
                    self.search_bandish()
                elif choice == "7":
                    self.show_statistics()
                elif choice == "8":
                    self.export_data()
                else:
                    print("Invalid choice! Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    admin = DatabaseAdmin()
    admin.run() 