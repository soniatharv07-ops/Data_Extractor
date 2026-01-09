import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GoogleMapsExtractor:
    def __init__(self):
        self.driver = None
        self.results = []
        self.current_keyword = ""
        self.current_location = ""
        self.total_businesses_scraped = 0
        
    def setup_driver(self):
        """Initialize Chrome driver with webdriver-manager (NO MANUAL DOWNLOAD)"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Webdriver-manager automatic download
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.driver.implicitly_wait(10)
            logging.info("Chrome driver initialized with webdriver-manager")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize driver: {e}")
            return False

    def open_google_maps(self):
        """Open Google Maps in the browser"""
        try:
            self.driver.get("https://www.google.com/maps")
            logging.info("Opened Google Maps")
            time.sleep(3)
            return True
        except Exception as e:
            logging.error(f"Failed to open Google Maps: {e}")
            return False

    def search_businesses(self, keyword, location):
        """Search for businesses on Google Maps"""
        try:
            self.current_keyword = keyword
            self.current_location = location
            
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "searchboxinput"))
            )
            search_box.clear()
            
            # Enter search query
            search_query = f"{keyword} in {location}"
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            
            logging.info(f"Searching for: {search_query}")
            time.sleep(5)
            return True
            
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return False

    def scroll_and_load(self, max_results=100):
        """Scroll through results to load more businesses"""
        try:
            results_pane = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='feed']"))
            )
            
            last_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", results_pane
            )
            
            loaded_results = 0
            scroll_attempts = 0
            max_scroll_attempts = 20
            
            while loaded_results < max_results and scroll_attempts < max_scroll_attempts:
                # Scroll down
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", results_pane
                )
                time.sleep(2)
                
                # Check for new results
                new_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight", results_pane
                )
                
                if new_height == last_height:
                    scroll_attempts += 1
                    if scroll_attempts >= 3:
                        break
                else:
                    scroll_attempts = 0
                
                last_height = new_height
                
                # Count loaded results
                current_results = self.driver.find_elements(
                    By.XPATH, "//a[contains(@href, 'maps/place')]"
                )
                loaded_results = len(current_results)
                
                logging.info(f"Loaded {loaded_results} results so far...")
                
                # Check for "Show more" button
                try:
                    show_more = self.driver.find_element(
                        By.XPATH, "//button[contains(., 'Show more results') or contains(., 'More results')]"
                    )
                    show_more.click()
                    time.sleep(2)
                except:
                    pass
            
            return True
            
        except Exception as e:
            logging.error(f"Scrolling failed: {e}")
            return False

    def extract_business_data(self):
        """Extract data from each business listing"""
        try:
            # Wait for results to load
            time.sleep(3)
            
            # Find all business cards
            business_cards = self.driver.find_elements(
                By.XPATH, "//div[contains(@role, 'article') or contains(@class, 'section-result')]"
            )
            
            if not business_cards:
                business_cards = self.driver.find_elements(
                    By.XPATH, "//a[contains(@href, 'maps/place')]/../.."
                )
            
            logging.info(f"Found {len(business_cards)} business cards")
            
            for index, card in enumerate(business_cards):
                try:
                    business_data = {
                        'Sr No.': len(self.results) + 1,
                        'Business Name': '',
                        'Address': '',
                        'Phone': '',
                        'Website': '',
                        'Rating': '',
                        'Reviews': '',
                        'Category': self.current_keyword,
                        'Location': self.current_location,
                        'Scraped Date': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    # Extract business name
                    try:
                        name_element = card.find_element(
                            By.XPATH, ".//div[contains(@role, 'heading')]//span | .//h3 | .//div[contains(@class, 'fontHeadlineSmall')]"
                        )
                        business_data['Business Name'] = name_element.text.strip()
                    except:
                        pass
                    
                    # Extract rating
                    try:
                        rating_element = card.find_element(
                            By.XPATH, ".//span[contains(@aria-label, 'stars')] | .//span[@role='img']"
                        )
                        rating_text = rating_element.get_attribute('aria-label')
                        if rating_text:
                            business_data['Rating'] = rating_text.replace('stars', '').replace('star', '').strip()
                    except:
                        pass
                    
                    # Extract number of reviews
                    try:
                        reviews_element = card.find_element(
                            By.XPATH, ".//span[contains(text(), 'reviews') or contains(text(), 'review')]"
                        )
                        business_data['Reviews'] = reviews_element.text.strip()
                    except:
                        pass
                    
                    # Extract address
                    try:
                        address_element = card.find_element(
                            By.XPATH, ".//div[contains(text(), '·')]/following-sibling::div | .//div[contains(@class, 'fontBodyMedium')]"
                        )
                        business_data['Address'] = address_element.text.strip()
                    except:
                        pass
                    
                    # Only save if we have at least a business name
                    if business_data['Business Name']:
                        self.results.append(business_data)
                        self.total_businesses_scraped += 1
                    
                except Exception as e:
                    logging.warning(f"Error extracting data from card {index}: {e}")
                    continue
            
            logging.info(f"Successfully extracted {len(self.results)} businesses")
            return True
            
        except Exception as e:
            logging.error(f"Data extraction failed: {e}")
            return False

    def save_to_excel(self, filename):
        """Save results to Excel file"""
        try:
            if not self.results:
                return False, "No data to save"
            
            df = pd.DataFrame(self.results)
            df.to_excel(filename, index=False)
            logging.info(f"Data saved to {filename}")
            return True, f"Data saved successfully to {filename}"
            
        except Exception as e:
            logging.error(f"Failed to save Excel: {e}")
            return False, f"Error saving file: {str(e)}"

    def save_to_pdf(self, filename):
        """Save results to PDF file"""
        try:
            if not self.results:
                return False, "No data to save"
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(
                f"Google Maps Business Extraction Report<br/>"
                f"Keyword: {self.current_keyword}<br/>"
                f"Location: {self.current_location}<br/>"
                f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
                f"Total Businesses: {len(self.results)}",
                styles['Heading2']
            )
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Create table data
            table_data = [list(self.results[0].keys())]  # Header row
            
            for item in self.results:
                table_data.append([
                    str(item.get('Sr No.', '')),
                    str(item.get('Business Name', '')),
                    str(item.get('Address', '')),
                    str(item.get('Phone', '')),
                    str(item.get('Website', '')),
                    str(item.get('Rating', '')),
                    str(item.get('Reviews', '')),
                    str(item.get('Category', '')),
                    str(item.get('Location', '')),
                    str(item.get('Scraped Date', ''))
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            logging.info(f"PDF saved to {filename}")
            return True, f"PDF saved successfully to {filename}"
            
        except Exception as e:
            logging.error(f"Failed to save PDF: {e}")
            return False, f"Error saving PDF: {str(e)}"

    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logging.info("Browser closed")

class GoogleMapsExtractorGUI:
    def __init__(self):
        self.extractor = GoogleMapsExtractor()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Google Maps Business Extractor")
        self.root.geometry("800x600")
        
        # Set icon
        try:
            self.root.iconbitmap(resource_path('icon.ico'))
        except:
            pass
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Google Maps Business Extractor",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Keyword input
        ttk.Label(main_frame, text="Business Type/Keyword:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(
            main_frame, textvariable=self.keyword_var, width=40
        )
        self.keyword_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Location input
        ttk.Label(main_frame, text="City/Location:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(
            main_frame, textvariable=self.location_var, width=40
        )
        self.location_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Max results
        ttk.Label(main_frame, text="Max Results:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.max_results_var = tk.StringVar(value="50")
        self.max_results_spinbox = ttk.Spinbox(
            main_frame, from_=10, to=200, textvariable=self.max_results_var, width=10
        )
        self.max_results_spinbox.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start Extraction",
            command=self.start_extraction,
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_extraction,
            state=tk.DISABLED,
            width=20
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, length=300, variable=self.progress_var, mode='determinate'
        )
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to start...")
        self.status_label = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, padding=5
        )
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        
        # Results text
        ttk.Label(main_frame, text="Results:").grid(
            row=7, column=0, sticky=tk.W, pady=(10, 5)
        )
        
        self.results_text = tk.Text(main_frame, height=10, width=70)
        self.results_text.grid(row=8, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Scrollbar for results text
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=8, column=3, sticky=(tk.N, tk.S), pady=(0, 10))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Save buttons frame
        save_frame = ttk.Frame(main_frame)
        save_frame.grid(row=9, column=0, columnspan=3, pady=10)
        
        self.save_excel_btn = ttk.Button(
            save_frame,
            text="Save as Excel",
            command=lambda: self.save_results('excel'),
            state=tk.DISABLED,
            width=15
        )
        self.save_excel_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_pdf_btn = ttk.Button(
            save_frame,
            text="Save as PDF",
            command=lambda: self.save_results('pdf'),
            state=tk.DISABLED,
            width=15
        )
        self.save_pdf_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        ttk.Button(save_frame, text="Exit", command=self.root.quit, width=15).pack(side=tk.LEFT, padx=5)
        
        # Set focus to first entry
        self.keyword_entry.focus()
        
        # Bind Enter key to start extraction
        self.root.bind('<Return>', lambda event: self.start_extraction())
        
    def update_status(self, message):
        """Update status label"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def update_results_text(self, message):
        """Update results text widget"""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_extraction(self):
        """Start the extraction process in a separate thread"""
        keyword = self.keyword_var.get().strip()
        location = self.location_var.get().strip()
        
        if not keyword or not location:
            messagebox.showerror("Error", "Please enter both keyword and location")
            return
        
        try:
            max_results = int(self.max_results_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for max results")
            return
        
        # Disable start button, enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_excel_btn.config(state=tk.DISABLED)
        self.save_pdf_btn.config(state=tk.DISABLED)
        
        # Clear previous results
        self.extractor.results = []
        self.extractor.total_businesses_scraped = 0
        self.results_text.delete(1.0, tk.END)
        
        # Start extraction in separate thread
        self.extraction_thread = threading.Thread(
            target=self.run_extraction,
            args=(keyword, location, max_results),
            daemon=True
        )
        self.extraction_thread.start()
        
    def run_extraction(self, keyword, location, max_results):
        """Run the extraction process"""
        try:
            self.update_status("Initializing Chrome browser...")
            self.update_results_text(f"Keyword: {keyword}")
            self.update_results_text(f"Location: {location}")
            self.update_results_text(f"Max Results: {max_results}")
            self.update_results_text("-" * 50)
            
            # Setup driver
            if not self.extractor.setup_driver():
                self.update_status("Failed to initialize browser")
                self.enable_buttons()
                return
            
            # Open Google Maps
            self.update_status("Opening Google Maps...")
            if not self.extractor.open_google_maps():
                self.update_status("Failed to open Google Maps")
                self.extractor.close_driver()
                self.enable_buttons()
                return
            
            # Search for businesses
            self.update_status(f"Searching for {keyword} in {location}...")
            if not self.extractor.search_businesses(keyword, location):
                self.update_status("Search failed")
                self.extractor.close_driver()
                self.enable_buttons()
                return
            
            # Scroll and load results
            self.update_status("Loading more results...")
            self.extractor.scroll_and_load(max_results)
            
            # Extract data
            self.update_status("Extracting business data...")
            self.extractor.extract_business_data()
            
            # Update UI with results
            self.update_status(f"Extraction complete! Found {len(self.extractor.results)} businesses")
            self.update_results_text(f"\nExtraction Complete!")
            self.update_results_text(f"Total businesses found: {len(self.extractor.results)}")
            
            # Show sample data
            if self.extractor.results:
                self.update_results_text("\nSample Data (first 5 results):")
                self.update_results_text("-" * 50)
                for i, business in enumerate(self.extractor.results[:5]):
                    self.update_results_text(f"{i+1}. {business.get('Business Name', 'N/A')}")
                    self.update_results_text(f"   Rating: {business.get('Rating', 'N/A')}")
                    self.update_results_text(f"   Address: {business.get('Address', 'N/A')[:50]}...")
                    self.update_results_text("")
            
            # Enable save buttons
            if self.extractor.results:
                self.save_excel_btn.config(state=tk.NORMAL)
                self.save_pdf_btn.config(state=tk.NORMAL)
            
            # Close driver
            self.extractor.close_driver()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.update_results_text(f"ERROR: {str(e)}")
            logging.error(f"Extraction error: {e}")
        finally:
            self.enable_buttons()
            
    def stop_extraction(self):
        """Stop the extraction process"""
        self.update_status("Stopping extraction...")
        self.update_results_text("\nExtraction stopped by user")
        self.extractor.close_driver()
        self.enable_buttons()
        
    def enable_buttons(self):
        """Enable/disable buttons as appropriate"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.root.update_idletasks()
        
    def save_results(self, file_type):
        """Save results to file"""
        if not self.extractor.results:
            messagebox.showwarning("No Data", "No data to save")
            return
        
        # Ask for file location
        if file_type == 'excel':
            file_ext = "xlsx"
            file_types = [("Excel files", "*.xlsx"), ("All files", "*.*")]
        else:
            file_ext = "pdf"
            file_types = [("PDF files", "*.pdf"), ("All files", "*.*")]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{file_ext}",
            filetypes=file_types,
            initialfile=f"google_maps_{self.extractor.current_keyword}_{self.extractor.current_location}.{file_ext}"
        )
        
        if filename:
            self.update_status(f"Saving to {file_type.upper()}...")
            
            if file_type == 'excel':
                success, message = self.extractor.save_to_excel(filename)
            else:
                success, message = self.extractor.save_to_pdf(filename)
            
            if success:
                messagebox.showinfo("Success", message)
                self.update_status(message)
                self.update_results_text(f"\n{message}")
            else:
                messagebox.showerror("Error", message)
                self.update_status(f"Save failed: {message}")
                
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the application"""
    print("=" * 60)
    print("GOOGLE MAPS BUSINESS EXTRACTOR")
    print("=" * 60)
    print("\nWebdriver-manager installed - No manual ChromeDriver needed!")
    print("Starting GUI application...")
    
    app = GoogleMapsExtractorGUI()
    app.run()

if __name__ == "__main__":
    # Check for required packages
    required_packages = ['selenium', 'pandas', 'openpyxl', 'reportlab', 'webdriver-manager']
    
    print("Checking for required packages...")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Please install {package} using: pip install {package}")
    
    main()