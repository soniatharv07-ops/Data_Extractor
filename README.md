# 🌍 Google Maps Business Scraper

Professional tool for extracting business information from Google Maps with one-click automation.

## ✨ Features

- 🚀 **One-Click Extraction** - Enter keyword & location, click once, get everything
- 📊 **Auto Excel Export** - Professional formatted Excel files with styling
- 📄 **Auto PDF Reports** - Detailed PDF reports with business data
- 🎯 **Smart Clicking** - Automatically clicks on each business for detailed info
- 🔄 **Auto Scrolling** - Loads more results automatically
- 💾 **Multiple Formats** - Excel, PDF, and JSON export
- 🖥️ **GUI Interface** - User-friendly graphical interface
- 🛡️ **Error Handling** - Robust error handling and recovery

## 📥 Download

### 🚀 Ready-to-Use EXE File (Recommended)
**No Python installation required!**

[![Download EXE](https://img.shields.io/badge/Download-EXE%20File-blue?style=for-the-badge&logo=windows)](https://github.com/YOUR_USERNAME/YOUR_REPO/releases/download/v1.0/GoogleMapsScraper.exe)

> **File Size:** ~96 MB (includes all dependencies)  
> **Requirements:** Windows 10/11 + Chrome Browser

### 📋 Alternative: Python Source
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
pip install -r requirements.txt
python google_maps_scraper.py
```

## 🚀 Quick Start

1. **Download** the EXE file from the link above
2. **Double-click** `GoogleMapsScraper.exe` to launch
3. **Enter** your search details:
   - Business Type (e.g., "gym", "restaurant", "hospital")
   - Location (e.g., "Delhi", "Mumbai", "Bangalore")
   - Max Results (1-50)
4. **Click** "🚀 Extract & Create Files (One Click)"
5. **Wait** for extraction to complete
6. **Find** your files in the `extracted_results` folder

## 📊 Output Files

The scraper automatically creates:

- 📊 **Excel File** (`business_location_timestamp.xlsx`)
  - Professional formatting with colored headers
  - Auto-adjusted column widths
  - Complete business data

- 📄 **PDF Report** (`business_location_timestamp.pdf`)
  - Formatted business listings
  - Summary statistics
  - Professional layout

- 📁 **JSON Data** (for developers)

## 🎯 Extracted Data

For each business, the scraper extracts:

- 🏢 **Business Name**
- 📍 **Full Address**
- 📞 **Phone Number**
- ⭐ **Rating & Reviews**
- 🌐 **Website URL**
- 🕒 **Business Hours**
- 🏷️ **Business Type**
- 📅 **Extraction Date & Time**

## 🖼️ Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

### Extraction in Progress
![Extraction Progress](screenshots/extraction_progress.png)

### Results Display
![Results](screenshots/results_display.png)

## ⚙️ System Requirements

- **OS:** Windows 10/11
- **Browser:** Google Chrome (latest version)
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 200MB free space
- **Internet:** Stable connection required

## 🛠️ Technical Details

- **Language:** Python 3.13
- **GUI Framework:** Tkinter
- **Web Automation:** Selenium WebDriver
- **Export Libraries:** openpyxl, reportlab, pandas
- **Packaging:** PyInstaller (standalone EXE)

## 📝 Usage Examples

### Example 1: Find Gyms in Delhi
```
Keyword: gym
Location: Delhi
Max Results: 20
```

### Example 2: Find Restaurants in Mumbai
```
Keyword: restaurant
Location: Mumbai
Max Results: 50
```

### Example 3: Find Hospitals in Bangalore
```
Keyword: hospital
Location: Bangalore
Max Results: 30
```

## 🔧 Troubleshooting

### Common Issues:

**❌ Chrome not found**
- Install Google Chrome browser
- Ensure Chrome is updated to latest version

**❌ No results found**
- Check internet connection
- Try different keywords or locations
- Ensure location name is correct

**❌ Extraction fails**
- Close other Chrome instances
- Restart the application
- Check if Google Maps is accessible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please respect Google's Terms of Service and use responsibly. The developers are not responsible for any misuse of this tool.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report Bug](https://github.com/YOUR_USERNAME/YOUR_REPO/issues)
- 💡 [Request Feature](https://github.com/YOUR_USERNAME/YOUR_REPO/issues)
- 📧 Email: your.email@example.com

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ star!

---

**Made with ❤️ for the developer community**