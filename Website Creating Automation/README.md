# Website Creating Automation

This project provides a suite of tools for automating website content creation and management, with a focus on converting content from various source formats (Excel, Word documents) to HTML templates. The automation handles various content transformations including formatting, structural elements, and metadata updates.

## Features

- **HTML Template Processing**: Update HTML templates with content from Excel spreadsheets
- **Word Document to HTML Conversion**: Convert DOCX files to HTML with proper formatting
- **Text Formatting Preservation**: Maintain formatting like bold text, headings, and lists
- **Marker-based Content Replacement**: Replace specific sections in HTML based on markers
- **Markdown to HTML Conversion**: Transform Markdown content into HTML
- **Metadata Tag Formatting**: Process and format meta tags from JSON strings

## Requirements

The script requires the following Python packages:
- pandas
- python-docx (docx)
- docx2python
- re (regular expressions)
- json

Install the required packages using:

```bash
pip install pandas python-docx docx2python
```

## Usage

The script provides two main functionalities that can be run separately:

### 1. HTML Template Processing

This functionality updates HTML templates with content from Excel spreadsheets. It's useful for batch updating website content across multiple pages.

```python
# Example usage for HTML template processing
python website_automation.py
# Then select option 1
```

This will:
1. Read data from specific cells in an Excel file
2. Load HTML templates
3. Replace specific sections in the templates with the Excel data
4. Save the updated HTML files

### 2. DOCX to HTML Conversion

This functionality converts Word documents to HTML, preserving formatting and structure.

```python
# Example usage for DOCX to HTML conversion
python website_automation.py
# Then select option 2
```

This will:
1. Preprocess the DOCX file to handle formatting (like bold text)
2. Convert the document to preliminary HTML
3. Process the HTML to apply proper formatting tags
4. Integrate the processed HTML into a template
5. Perform additional post-processing for specific formatting needs

## Core Functions

- `read_excel_data()`: Extracts data from specific cells in Excel files
- `load_html_template()`: Loads an HTML template file
- `replace_segment_in_html()`: Replaces sections in HTML based on markers
- `docx_to_html_with_docx2python()`: Converts DOCX files to HTML with formatting
- `markdown_to_html()`: Converts Markdown text to HTML
- `format_meta_tags()`: Formats JSON meta tags into HTML meta tag strings

## Advanced HTML Segment Manipulation

The toolkit provides powerful functions for precise HTML segment manipulation, which can be essential for website fixes, restructuring, and content migration.

### `replace_segment_in_html` Function

This function allows you to precisely target and replace sections of HTML content using marker-based identification:

```python
replace_segment_in_html(html_content, search_start_marker, search_end_marker, replacement_text,
                        start_occurrence=1, end_occurrence=1)
```

Key features:
- Finds the nth occurrence of the start and end markers in the HTML content
- Replaces everything between (and including) the markers with the replacement text
- Handles multiple occurrences of the same marker using the occurrence parameters
- Provides error handling for missing markers

This function is particularly useful for:

- **Updating JavaScript sections**: Replace outdated JavaScript code with newer versions without disrupting the surrounding HTML structure
- **Fixing broken markup**: Isolate and repair problematic HTML sections that cause rendering issues
- **Batch updating common elements**: Update navigation bars, footers, or other repeated elements across multiple pages with a single operation
- **Injecting third-party scripts**: Add analytics, chatbots, or other third-party code snippets into specific locations

### `get_segment_in_html` Function

This complementary function allows you to extract HTML segments for analysis, reuse, or relocation:

```python
get_segment_in_html(html_content, search_start_marker, search_end_marker, 
                    start_occurrence=1, end_occurrence=1)
```

Key features:
- Finds and extracts the HTML content between (and including) the specified markers
- Returns the segment as a string for further processing
- Can target specific occurrences of repeated markers
- Provides detailed error reporting for debugging

### Advanced Techniques: Combining Segment Operations

By combining `get_segment_in_html` and `replace_segment_in_html`, you can implement sophisticated HTML transformations:

#### Moving Content Between Sections

```python
# Extract content from one section
segment = get_segment_in_html(html_content, source_start_marker, source_end_marker)

# Insert it elsewhere
updated_html = replace_segment_in_html(html_content, target_start_marker, target_end_marker, segment)
```

#### Practical Website Fix Examples

1. **Fixing Script Loading Order Issues**:
   ```python
   # Extract script that needs to load earlier
   script_segment = get_segment_in_html(html_content, "<script id='analytics'>", "</script>")
   
   # Remove it from original location
   html_without_script = replace_segment_in_html(html_content, "<script id='analytics'>", "</script>", "")
   
   # Insert it in the head section
   fixed_html = replace_segment_in_html(html_without_script, "</title>", "</title>", script_segment)
   ```

2. **Relocating Content for Responsive Designs**:
   ```python
   # Extract sidebar content
   sidebar = get_segment_in_html(html_content, "<!-- sidebar-start -->", "<!-- sidebar-end -->")
   
   # Remove from original location
   html_without_sidebar = replace_segment_in_html(html_content, 
                                               "<!-- sidebar-start -->", 
                                               "<!-- sidebar-end -->", 
                                               "")
   
   # Insert at the bottom for mobile layouts
   mobile_optimized_html = replace_segment_in_html(html_without_sidebar, 
                                                "<!-- mobile-content-end -->", 
                                                "<!-- mobile-content-end -->", 
                                                sidebar)
   ```

3. **Fixing Duplicate Meta Tags**:
   ```python
   # Find all meta description tags
   pattern = r'<meta\s+name="description"\s+content="[^"]*"\s*/>'
   meta_tags = re.findall(pattern, html_content)
   
   if len(meta_tags) > 1:
       # Keep only the first one
       fixed_html = html_content
       for tag in meta_tags[1:]:
           fixed_html = fixed_html.replace(tag, "")
   ```

4. **Consolidating Fragmented JavaScript**:
   ```python
   # Extract scattered JS blocks
   js_blocks = []
   for i in range(1, 5):  # Assuming 4 JS blocks
       marker = f"<!-- js-block-{i} -->"
       end_marker = f"<!-- end-js-block-{i} -->"
       js_blocks.append(get_segment_in_html(html_content, marker, end_marker))
   
   # Remove original blocks
   cleaned_html = html_content
   for i in range(1, 5):
       marker = f"<!-- js-block-{i} -->"
       end_marker = f"<!-- end-js-block-{i} -->"
       cleaned_html = replace_segment_in_html(cleaned_html, marker, end_marker, "")
   
   # Combine and insert at the end of body
   combined_js = "\n".join(js_blocks)
   final_html = replace_segment_in_html(cleaned_html, "</body>", "</body>", combined_js + "</body>")
   ```

These segment manipulation functions provide surgical precision when working with HTML files, allowing for automated fixes to common website issues without manual editing.

## Configuration

The script uses configuration dictionaries to map:
- Excel cell locations to content variables
- HTML markers to content sections for replacement
- Formatting markers to HTML tags

## Logging

All operations are logged to a `processing_log.txt` file that records:
- Successful operations
- Error messages
- Warning messages

## Example Workflow

### HTML Template Processing

1. Define a list of HTML templates to process
2. Define corresponding Excel sheet names
3. Map the Excel cells to content variables
4. Configure the replacement markers in the HTML templates
5. Run the processing function for each template

### DOCX to HTML Conversion

1. Preprocess the DOCX file to add formatting markers
2. Define marker-to-tag mapping for HTML formatting
3. Convert DOCX to preliminary HTML
4. Process the HTML with proper formatting
5. Integrate into the final template
6. Perform additional formatting corrections

## Error Handling

The script includes robust error handling that:
- Validates input files exist
- Checks for empty cells in Excel data
- Verifies HTML markers are found
- Logs all errors with descriptive messages
- Terminates gracefully on critical errors

## Customization

The script is highly modular and can be extended or customized by:
- Modifying the cell mapping for different Excel structures
- Updating the marker configurations for different HTML templates
- Adding new marker types for additional formatting needs
- Creating new processing functions for different input formats

## Examples of Websites Created Using This Script

This automation script has been used to successfully create and manage the following pages:

- [NAO Medical Primary Care in Astoria](https://naomedical.com/primary-care/locations/astoria.html)
- [NAO Medical Nutritionist in Williamsburg](https://naomedical.com/nutritionist/locations/williamsburg.html)
- [Dr. Priti Practice Provider Page](https://naomedical.com/primary-care/provider/dr-priti-practice.html)

These pages showcase how the script can efficiently maintain consistent formatting and structure across different types of content while allowing for customization of specific page elements. The automation particularly shines when managing provider information, location details, and service descriptions that need to be updated regularly across multiple pages.