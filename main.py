"""
Main application entry point for College Scraper
"""

import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime
import os

# Import modules
from gui.main_window import MainWindow
from config.states import INDIAN_STATES, ENGINEERING_BRANCHES, COLLEGE_TYPES
from scraper.google_search import GoogleSearcher
from scraper.college_scraper import CollegeScraper
from data.college_data import CollegeDataManager
from data.excel_exporter import ExcelExporter
from utils.logger import setup_logger

logger = setup_logger('main')

class CollegeScraperApp:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.window = MainWindow(self.root)
        
        # Set up callbacks
        self.window.on_search_callback = self.start_search
        self.window.on_export_callback = self.export_to_excel
        
        # Initialize components
        self.searcher = GoogleSearcher()
        self.scraper = CollegeScraper()
        self.data_manager = CollegeDataManager()
        
        # Populate dropdowns
        self.window.set_states(INDIAN_STATES)
        self.window.set_branches(ENGINEERING_BRANCHES)
        self.window.set_college_types(COLLEGE_TYPES)
        
        logger.info("Application initialized")
    
    def start_search(self, state: str, branch: str, college_type: str, max_results: int):
        """
        Start the search process in a separate thread
        
        Args:
            state: Selected state
            branch: Selected branch
            college_type: Selected college type
            max_results: Maximum number of results
        """
        # Run search in separate thread to keep GUI responsive
        search_thread = threading.Thread(
            target=self._perform_search,
            args=(state, branch, college_type, max_results),
            daemon=True
        )
        search_thread.start()
    
    def _perform_search(self, state: str, branch: str, college_type: str, max_results: int):
        """
        Perform the actual search and scraping
        
        Args:
            state: Selected state
            branch: Selected branch
            college_type: Selected college type
            max_results: Maximum number of results
        """
        try:
            # Update UI
            self.window.start_search()
            self.window.update_status(f"Searching for colleges in {state}...")
            self.window.update_progress("Searching Google...")
            
            logger.info(f"Starting search: {state}, {branch}, {college_type}")
            
            # Clear previous data
            self.data_manager.clear()
            
            # Step 1: Search for college websites
            self.window.append_result(f"{'='*80}")
            self.window.append_result(f"Searching for {branch} colleges in {state}")
            self.window.append_result(f"College Type: {college_type}")
            self.window.append_result(f"{'='*80}\n")
            
            # Try DuckDuckGo first (more scraping-friendly)
            search_results = self.searcher.search_with_duckduckgo(
                state, branch, college_type, max_results
            )
            
            # Fallback to Google if DuckDuckGo returns no results
            if not search_results:
                self.window.update_progress("Trying Google search...")
                search_results = self.searcher.search_colleges(
                    state, branch, college_type, max_results
                )
            
            if not search_results:
                self.window.append_result("❌ No college websites found. Try different search parameters.")
                self.window.update_status("Search completed - No results found")
                self.window.end_search(success=False)
                return
            
            self.window.append_result(f"✓ Found {len(search_results)} potential college websites\n")
            
            # Step 2: Scrape each college website
            self.window.update_progress("Scraping college websites...")
            
            for idx, (college_name, url) in enumerate(search_results, 1):
                try:
                    self.window.update_progress(f"Scraping {idx}/{len(search_results)}: {college_name}")
                    self.window.append_result(f"[{idx}/{len(search_results)}] Scraping: {college_name}")
                    
                    # Scrape college website
                    college_info = self.scraper.scrape_college(url, college_name, state)
                    
                    if college_info and self.data_manager.add_college(college_info):
                        self.window.append_result(f"  ✓ Name: {college_info.name}")
                        self.window.append_result(f"  ✓ Email: {college_info.email or 'Not found'}")
                        self.window.append_result(f"  ✓ Contact: {college_info.admin_contact or 'Not found'}")
                        self.window.append_result(f"  ✓ Location: {college_info.location}")
                        self.window.append_result(f"  ✓ Type: {college_info.college_type}")
                        if college_info.branches:
                            self.window.append_result(f"  ✓ Branches: {', '.join(college_info.branches[:3])}")
                        self.window.append_result("")
                    else:
                        self.window.append_result(f"  ⚠ Could not extract sufficient information\n")
                    
                    # Small delay to avoid overwhelming servers
                    import time
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error scraping {url}: {e}")
                    self.window.append_result(f"  ❌ Error: {str(e)}\n")
                    continue
            
            # Summary
            total_colleges = self.data_manager.count()
            self.window.append_result(f"\n{'='*80}")
            self.window.append_result(f"Search Complete!")
            self.window.append_result(f"Total colleges found: {total_colleges}")
            self.window.append_result(f"{'='*80}")
            
            self.window.update_status(f"Search completed - Found {total_colleges} colleges")
            self.window.update_progress("Search completed")
            
            logger.info(f"Search completed: {total_colleges} colleges found")
            
            # Enable export if we have data
            if total_colleges > 0:
                self.window.end_search(success=True)
            else:
                self.window.end_search(success=False)
                self.window.show_info(
                    "No Data",
                    "No college information could be extracted. Try different search parameters."
                )
        
        except Exception as e:
            logger.error(f"Search error: {e}", exc_info=True)
            self.window.append_result(f"\n❌ Error: {str(e)}")
            self.window.update_status("Search failed")
            self.window.end_search(success=False)
            self.window.show_error("Search Error", f"An error occurred: {str(e)}")
    
    def export_to_excel(self):
        """Export collected data to Excel"""
        try:
            if self.data_manager.count() == 0:
                self.window.show_error("No Data", "No data to export. Please perform a search first.")
                return
            
            self.window.update_status("Exporting to Excel...")
            
            # Generate default filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"college_data_{timestamp}.xlsx"
            
            # Ask user for save location
            save_path = self.window.ask_save_location(default_filename)
            
            if not save_path:
                self.window.update_status("Export cancelled")
                return
            
            # Get data
            data = self.data_manager.to_list_of_dicts()
            
            # Export to Excel
            exporter = ExcelExporter()
            
            # Use the user-selected path directly
            import os
            output_dir = os.path.dirname(save_path)
            filename = os.path.basename(save_path)
            
            # Temporarily change the export directory
            original_export = exporter.export_to_excel
            
            def custom_export(data, fname):
                # Create DataFrame and export
                import pandas as pd
                df = pd.DataFrame(data)
                
                # Reorder columns
                column_order = [
                    'College Name', 'University', 'Type', 'Location',
                    'Branches', 'Email', 'HOD Contact', 'Admin Contact',
                    'Other Contacts', 'Website'
                ]
                columns = [col for col in column_order if col in df.columns]
                df = df[columns]
                
                # Export
                df.to_excel(save_path, index=False, sheet_name='Colleges')
                
                # Format
                exporter._format_excel(save_path)
                
                return save_path
            
            filepath = custom_export(data, filename)
            
            # Add summary sheet
            state = self.window.state_var.get()
            branch = self.window.branch_var.get()
            exporter.export_summary(
                self.data_manager.count(),
                state,
                branch,
                filepath
            )
            
            self.window.update_status(f"Exported to: {filepath}")
            self.window.show_info(
                "Export Successful",
                f"Data exported successfully!\n\nFile: {filepath}\nTotal colleges: {self.data_manager.count()}"
            )
            
            logger.info(f"Data exported to: {filepath}")
            
            # Open the file location
            if os.name == 'nt':  # Windows
                os.startfile(os.path.dirname(filepath))
        
        except Exception as e:
            logger.error(f"Export error: {e}", exc_info=True)
            self.window.show_error("Export Error", f"Failed to export data: {str(e)}")
            self.window.update_status("Export failed")
    
    def run(self):
        """Run the application"""
        logger.info("Starting application")
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = CollegeScraperApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
