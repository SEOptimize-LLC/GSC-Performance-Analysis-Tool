# Google Search Console Performance Analyzer

A comprehensive Streamlit application for analyzing Google Search Console performance data to identify optimization opportunities and insights.

## Features

### Query Analysis
- **Performance Metrics**: % of queries generating clicks, impressions, and their opposites
- **CTR Analysis**: Identify queries with high clicks/impressions but low CTR
- **Position Analysis**: Queries ranking in positions 4-10, 11-20, and 21+ with performance thresholds
- **Opportunity Identification**: Find queries with potential for improvement

### URL Analysis
- **URL Performance**: Same metrics as query analysis but from URL perspective
- **Performance Categorization**: Automatically categorize URLs into:
  - **Top URLs**: High-performing pages (configurable threshold)
  - **Good URLs**: Solid performers
  - **Weak URLs**: Underperforming pages
  - **Dead URLs**: No clicks generated
  - **Opportunity URLs**: Impressions but no clicks

### Insights & Recommendations
- **Actionable Insights**: AI-powered recommendations based on data patterns
- **Priority Actions**: Focus on high-impact opportunities
- **Performance Alerts**: Identify concerning trends

## Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
streamlit run app.py
```

### Uploading Data
1. Prepare your Google Search Console CSV export with these columns:
   - `query` or `keyword`
   - `page`, `url`, or `landing page`
   - `clicks`
   - `impressions`
   - `ctr` or `url ctr`
   - `position` or `avg. pos`

2. Upload the CSV file using the sidebar uploader
3. Configure URL performance thresholds:
   - Top URLs threshold (default: 1000 clicks)
   - Good URLs threshold (default: 100 clicks)
   - Weak URLs threshold (default: 10 clicks)

### Analysis Tabs

1. **Query Analysis**: Deep dive into query performance
2. **URL Analysis**: URL-level performance metrics
3. **URL Performance**: Visual categorization of URLs
4. **Insights**: Actionable recommendations
5. **Raw Data**: View and download processed data

## Key Insights Provided

### Query Opportunities
- Queries with 100+ clicks but <1% CTR
- Queries with 1000+ clicks but <1% CTR
- Queries ranking in positions 4-10 with 100+ clicks
- Queries ranking in positions 11-20 with 100+ clicks

### URL Opportunities
- URLs with impressions but zero clicks
- High-impression URLs with low CTR
- Underperforming content in good positions

### Performance Distribution
- Visual breakdown of URL performance categories
- Percentage distribution across performance tiers
- Identification of content gaps

## Customization

### Adjusting Thresholds
Modify the URL categorization thresholds in the sidebar:
- **Top URLs**: Adjust based on your site's traffic volume
- **Good URLs**: Set based on your average page performance
- **Weak URLs**: Define your minimum viable performance

### Data Processing
The analyzer automatically:
- Standardizes column names across different GSC export formats
- Handles CTR as both decimal (0.01) and percentage (1%)
- Removes duplicate query-URL combinations
- Calculates missing CTR values

## Sample Data Format

| query | page | clicks | impressions | ctr | position |
|-------|------|--------|-------------|-----|----------|
| best running shoes | /best-running-shoes | 150 | 12500 | 0.012 | 3.2 |
| running shoes | /running-shoes | 89 | 8900 | 0.010 | 4.1 |

## Troubleshooting

### Common Issues
1. **Missing columns**: Ensure your CSV has the required columns
2. **Data format**: Check that numeric columns don't contain text
3. **CTR format**: Values can be 0.01 (decimal) or 1 (percentage)

### Error Messages
- "Missing required columns": Check column names match expected format
- "Error processing file": Verify CSV format and data types

## Advanced Features

### Export Capabilities
- Download processed data as CSV
- Export insights and recommendations
- Save performance categorizations

### Visualizations
- Interactive pie charts for URL distribution
- Detailed data tables with sorting
- Real-time threshold adjustments

## Support

For issues or feature requests, please check:
1. CSV file format matches requirements
2. All required columns are present
3. Data types are correct (numeric for clicks, impressions, etc.)
