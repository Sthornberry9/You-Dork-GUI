# You-Dork-GUI: AI Agent Instructions

## Project Overview
You-Dork is a Google Dorks generator tool for OSINT investigators. It scrapes the Exploit-DB Google Hacking Database (GHDB) and intelligently generates customized Google search queries based on user-provided information (names, emails, IPs, file types, CVEs, etc).

## Architecture

### Core Data Flow
1. **Database Layer** (`dork_database.json`): Maps 13+ categories to Google Dork templates (7,950+ exploits)
2. **CATEGORY_MAPPING dict**: Routes user input types → relevant dork categories (e.g., "email" → 3 applicable categories)
3. **Dork Generation Pipeline**:
   - User selects input types via interactive menu
   - `generate_dorks()` applies CATEGORY_MAPPING to select relevant database categories
   - `insert_smartly()` injects user values into dorks + ranks by keyword weights
   - Results displayed grouped by input_type → category hierarchy

### Key Components

**Selenium Web Scraping** ([lines 111-193](vscode-vfs://github/Sthornberry9/You-Dork-GUI/youdork.py#L111))
- Headless Chrome scrapes https://www.exploit-db.com/google-hacking-database
- Anti-bot bypass: masks webdriver detection
- Pagination loop iterates all GHDB pages until "Next" disabled
- Stores data in `dork_database.json` (init/update workflow)

**Smart Dork Injection** ([lines 296-329](vscode-vfs://github/Sthornberry9/You-Dork-GUI/youdork.py#L296))
- Detects dork operator patterns: `intext:`, `intitle:`, `site:`, `filetype:`, `ext:`, `inurl:`
- Injects user input at correct position (e.g., `intext:password` → `intext:"user input" password`)
- Ranking weights keyword scoring: "password"=10, "cve"=9, "exploit"=8 (see lines 305-307)
- Returns sorted list with highest-scoring dorks first

**Logging System** ([lines 331-345](vscode-vfs://github/Sthornberry9/You-Dork-GUI/youdork.py#L331))
- Date-based files: `logs/YYYY-MM-DD.txt`
- Manual opt-in per session + toggle for auto-logging

## Project Conventions

**Input Field Naming**: Use exact keys from `user_inputs` dict: `"name"`, `"username"`, `"email"`, `"phone"`, `"filetype"`, `"ip"`, `"domain"`, `"crypto"`, `"social"`, `"tech"`, `"address"`, `"cve"` (lines 226-227)

**Database Structure**: 
```json
{
  "Category Name": ["dork1", "dork2", ...],
  ...
}
```
Categories must be in `CATEGORY_MAPPING` values or they won't be selected.

**Dork Format Conventions**:
- Use Google search operators: `site:`, `intext:`, `intitle:`, `filetype:`, `inurl:`, `ext:`, `allintext:`
- Quote multi-word inputs: `insert_smartly()` handles this (line 315)
- No hardcoded user values in templates—always inject via `insert_smartly()`

**Color Output**: Custom ANSI codes (not colorama) for headers/results:
```python
GREEN = "\033[38;2;119;221;119m"
BLUE = "\033[38;2;136;209;241m"
RED = "\033[38;2;255;0;0m"
```

## Critical Workflows

**Database Update Workflow** (lines 196-213):
1. Checks if `dork_database.json` exists + non-empty
2. Prompts user to update if missing
3. Falls back to hardcoded dorks if scraping fails
4. Always validates JSON before using

**Troubleshooting Database Corruption** (lines 212-221):
- Catches `json.JSONDecodeError` → re-scrapes automatically
- Provides fallback dorks if re-scrape fails

**Environment Detection** (lines 83-99):
- Checks `CHROMEDRIVER_PATH` env var first
- Platform-specific paths: `chromedriver-win64/chromedriver.exe` (Windows), `chromedriver-linux64/chromedriver` (Linux)
- Falls back to system PATH via `shutil.which()`

## Dependencies
- **selenium**: Web scraping GHDB (requires ChromeDriver binary)
- **colorama**: Color terminal output (imported but custom ANSI codes preferred)

## Running & Testing
```bash
python youdork.py              # Main interactive menu
python youdork.py --help       # Show README from assets/README.txt
python youdork.py -h           # Same as --help
```

**Menu Options**: 1=Generate, 2=Toggle Logging, 3=Update DB, 4=Help, 5=Support, 0=Exit

## Important Notes for Agents
- **No CLI arguments for input**: All user interaction is interactive menu-driven
- **Global state**: `LOGGING` flag modified by `toggle_logging()` (line 348)
- **File paths are relative**: `dork_database.json`, `logs/`, `assets/` assumed in script directory
- **Windows/Linux agnostic**: Uses `os.name == 'nt'` for clear vs clear command
- **Slow operations**: Add 3-5 second delays around page loads in Selenium (lines 126, 171, 186)
