import streamlit as st
import pandas as pd
import plotly.express as px
from gsc_analyzer import GSCAnalyzer

# Page configuration
st.set_page_config(
    page_title="GSC Performance Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📊 Google Search Console Performance Analyzer</div>', 
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📁 Data Upload")
    
    uploaded_file = st.file_uploader(
        "Upload your GSC CSV file",
        type=['csv'],
        help="Upload a CSV file with columns: query, page, clicks, impressions, ctr, position"
    )
    
    st.header("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        top_threshold = st.number_input("Top URLs threshold", value=1000, min_value=1)
        good_threshold = st.number_input("Good URLs threshold", value=100, min_value=1)
    with col2:
        weak_threshold = st.number_input("Weak URLs threshold", value=10, min_value=0)
    
    thresholds = {
        'top': top_threshold,
        'good': good_threshold,
        'weak': weak_threshold
    }

# Main content
if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        
        # Initialize analyzer
        analyzer = GSCAnalyzer(df)
        
        # Get all analyses
        query_results = analyzer.query_analysis()
        url_results = analyzer.url_analysis()
        performance_results = analyzer.url_performance_analysis(thresholds)
        insights = analyzer.generate_insights()
        
        # Summary metrics
        st.header("📈 Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Queries", f"{query_results['total_queries']:,}")
        with col2:
            st.metric("Total URLs", f"{url_results['total_urls']:,}")
        with col3:
            st.metric("Total Clicks", f"{df['clicks'].sum():,}")
        with col4:
            st.metric("Total Impressions", f"{df['impressions'].sum():,}")
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Query Analysis", 
            "URL Analysis", 
            "URL Performance", 
            "Insights",
            "Raw Data"
        ])
        
        with tab1:
            st.header("🔍 Query-Based Analysis")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Queries with Clicks", 
                    f"{query_results['queries_with_clicks']:,}",
                    f"{query_results['pct_queries_with_clicks']:.1f}%"
                )
            with col2:
                st.metric(
                    "Queries without Clicks",
                    f"{query_results['queries_without_clicks']:,}",
                    f"{query_results['pct_queries_without_clicks']:.1f}%"
                )
            with col3:
                st.metric(
                    "Queries with Impressions",
                    f"{query_results['queries_with_impressions']:,}",
                    f"{query_results['pct_queries_with_impressions']:.1f}%"
                )
            with col4:
                st.metric(
                    "Queries without Impressions",
                    f"{query_results['queries_without_impressions']:,}",
                    f"{query_results['pct_queries_without_impressions']:.1f}%"
                )
            
            # CTR Analysis
            st.subheader("CTR Analysis")
            ctr_data = {
                'Metric': [
                    '100+ Clicks, <1% CTR',
                    '1000+ Clicks, <1% CTR',
                    '100+ Impressions, <1% CTR',
                    '1000+ Impressions, <1% CTR'
                ],
                'Count': [
                    query_results['queries_100clicks_1pct_ctr'],
                    query_results['queries_1000clicks_1pct_ctr'],
                    query_results['queries_100impr_1pct_ctr'],
                    query_results['queries_1000impr_1pct_ctr']
                ],
                'Percentage': [
                    query_results['pct_queries_100clicks_1pct_ctr'],
                    query_results['pct_queries_1000clicks_1pct_ctr'],
                    query_results['pct_queries_100impr_1pct_ctr'],
                    query_results['pct_queries_1000impr_1pct_ctr']
                ]
            }
            ctr_df = pd.DataFrame(ctr_data)
            st.dataframe(ctr_df, use_container_width=True)
        
        with tab2:
            st.header("🔗 URL-Based Analysis")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "URLs with Clicks",
                    f"{url_results['urls_with_clicks']:,}",
                    f"{url_results['pct_urls_with_clicks']:.1f}%"
                )
            with col2:
                st.metric(
                    "URLs without Clicks",
                    f"{url_results['urls_without_clicks']:,}",
                    f"{url_results['pct_urls_without_clicks']:.1f}%"
                )
            with col3:
                st.metric(
                    "URLs with Impressions",
                    f"{url_results['urls_with_impressions']:,}",
                    f"{url_results['pct_urls_with_impressions']:.1f}%"
                )
            with col4:
                st.metric(
                    "URLs without Impressions",
                    f"{url_results['urls_without_impressions']:,}",
                    f"{url_results['pct_urls_without_impressions']:.1f}%"
                )
        
        with tab3:
            st.header("📊 URL Performance Analysis")
            
            # Performance distribution
            st.subheader("Performance Distribution")
            
            performance_data = {
                'Category': ['Top URLs', 'Good URLs', 'Weak URLs', 'Dead URLs', 'Opportunity URLs'],
                'Count': [
                    performance_results['top_urls_count'],
                    performance_results['good_urls_count'],
                    performance_results['weak_urls_count'],
                    performance_results['dead_urls_count'],
                    performance_results['opportunity_urls_count']
                ],
                'Percentage': [
                    performance_results['pct_top_urls'],
                    performance_results['pct_good_urls'],
                    performance_results['pct_weak_urls'],
                    performance_results['pct_dead_urls'],
                    performance_results['pct_opportunity_urls']
                ]
            }
            
            perf_df = pd.DataFrame(performance_data)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(perf_df, values='Count', names='Category', 
                            title='URL Performance Distribution')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(perf_df, use_container_width=True)
        
        with tab4:
            st.header("💡 Insights & Recommendations")
            
            # Display insights
            for insight in insights['recommendations']:
                st.markdown(f'<div class="insight-box">{insight}</div>', 
                           unsafe_allow_html=True)
        
        with tab5:
            st.header("📋 Raw Data")
            
            # Show data info
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Data Shape:**", df.shape)
                st.write("**Columns:**", list(df.columns))
            with col2:
                st.write("**Data Types:**")
                st.json(df.dtypes.to_dict())
            
            # Show sample data
            st.subheader("Sample Data")
            st.dataframe(df.head(100), use_container_width=True)
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.info("Please check that your CSV file has the required columns")
        
else:
    # Welcome screen
    st.info("""
    ## Welcome to GSC Performance Analyzer
    
    This tool helps you analyze Google Search Console performance data to identify:
    
    - **Query performance**: Which queries are driving traffic
    - **URL performance**: How individual pages are performing
    - **Opportunities**: URLs with impressions but no clicks
    - **CTR issues**: Queries/pages with low click-through rates
    - **Position opportunities**: Content ranking in positions 4-20
    
    ### How to use:
    1. Upload your GSC CSV file using the sidebar
    2. Configure thresholds for URL categorization
    3. Explore the different analysis tabs
    4. Download insights and recommendations
    
    ### Required CSV columns:
    - `query` or `keyword`
    - `page`, `url`, or `landing page`
    - `clicks`
    - `impressions`
    - `ctr` or `url ctr`
    - `position` or `avg. pos`
    """)
    
    # Sample data format
    st.subheader("Sample Data Format")
    sample_data = {
        'query': ['best running shoes', 'running shoes', 'athletic shoes'],
        'page': [
            'https://example.com/best-running-shoes',
            'https://example.com/running-shoes',
            'https://example.com/athletic-shoes'
        ],
        'clicks': [150, 89, 45],
        'impressions': [12500, 8900, 6700],
        'ctr': [0.012, 0.010, 0.0067],
        'position': [3.2, 4.1, 8.5]
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
