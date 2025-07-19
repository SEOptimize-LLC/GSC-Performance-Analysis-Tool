import pandas as pd
import numpy as np
from typing import Dict
import warnings

warnings.filterwarnings('ignore')


class GSCAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """Initialize the GSC analyzer with a DataFrame."""
        self.df = df.copy()
        self.prepare_data()

    def prepare_data(self):
        """Clean and prepare the data for analysis."""
        # Standardize column names
        column_mapping = {
            'query': 'query',
            'keyword': 'query',
            'page': 'page',
            'landing page': 'page',
            'url': 'page',
            'address': 'page',
            'clicks': 'clicks',
            'impressions': 'impressions',
            'ctr': 'ctr',
            'url ctr': 'ctr',
            'position': 'position',
            'avg. pos': 'position'
        }

        # Convert column names to lowercase for matching
        self.df.columns = [col.lower() for col in self.df.columns]

        # Map columns to standard names
        rename_dict = {}
        for col in self.df.columns:
            for key, value in column_mapping.items():
                if key.lower() in col:
                    rename_dict[col] = value
                    break

        self.df = self.df.rename(columns=rename_dict)

        # Ensure required columns exist
        required_cols = ['query', 'page', 'clicks', 'impressions', 'ctr', 'position']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Convert data types
        self.df['clicks'] = pd.to_numeric(self.df['clicks'], errors='coerce').fillna(0)
        self.df['impressions'] = pd.to_numeric(self.df['impressions'], errors='coerce').fillna(0)
        self.df['position'] = pd.to_numeric(self.df['position'], errors='coerce').fillna(0)

        # Calculate CTR if not provided
        if 'ctr' not in self.df.columns or self.df['ctr'].isna().all():
            self.df['ctr'] = (self.df['clicks'] / self.df['impressions']).replace(
                [np.inf, -np.inf], 0
            ).fillna(0)
        else:
            self.df['ctr'] = pd.to_numeric(self.df['ctr'], errors='coerce').fillna(0)
            # Handle CTR as percentage
            if self.df['ctr'].max() > 1:
                self.df['ctr'] = self.df['ctr'] / 100

        # Remove duplicates
        self.df = self.df.drop_duplicates(subset=['query', 'page'])

    def query_analysis(self) -> Dict:
        """Perform query-based analysis."""
        query_stats = self.df.groupby('query').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'position': 'mean'
        }).reset_index()

        query_stats['ctr'] = (
            query_stats['clicks'] / query_stats['impressions']
        ).replace([np.inf, -np.inf], 0).fillna(0)

        total_queries = len(query_stats)

        results = {
            'total_queries': total_queries,
            'queries_with_clicks': len(query_stats[query_stats['clicks'] > 0]),
            'queries_with_impressions': len(query_stats[query_stats['impressions'] > 0]),
            'queries_without_clicks': len(query_stats[query_stats['clicks'] == 0]),
            'queries_without_impressions': len(query_stats[query_stats['impressions'] == 0]),
        }

        # Calculate percentages
        results['pct_queries_with_clicks'] = (
            results['queries_with_clicks'] / total_queries
        ) * 100
        results['pct_queries_with_impressions'] = (
            results['queries_with_impressions'] / total_queries
        ) * 100
        results['pct_queries_without_clicks'] = (
            results['queries_without_clicks'] / total_queries
        ) * 100
        results['pct_queries_without_impressions'] = (
            results['queries_without_impressions'] / total_queries
        ) * 100

        # CTR-based analysis
        results['queries_100clicks_1pct_ctr'] = len(
            query_stats[(query_stats['clicks'] >= 100) & (query_stats['ctr'] < 0.01)]
        )
        results['queries_1000clicks_1pct_ctr'] = len(
            query_stats[(query_stats['clicks'] >= 1000) & (query_stats['ctr'] < 0.01)]
        )
        results['queries_100impr_1pct_ctr'] = len(
            query_stats[(query_stats['impressions'] >= 100) & (query_stats['ctr'] < 0.01)]
        )
        results['queries_1000impr_1pct_ctr'] = len(
            query_stats[(query_stats['impressions'] >= 1000) & (query_stats['ctr'] < 0.01)]
        )

        # Position-based analysis for clicks
        results['queries_100clicks_pos_4_10'] = len(
            query_stats[
                (query_stats['clicks'] >= 100) &
                (query_stats['position'] >= 4) &
                (query_stats['position'] <= 10)
            ]
        )
        results['queries_100clicks_pos_11_20'] = len(
            query_stats[
                (query_stats['clicks'] >= 100) &
                (query_stats['position'] >= 11) &
                (query_stats['position'] <= 20)
            ]
        )
        results['queries_100clicks_pos_21_plus'] = len(
            query_stats[(query_stats['clicks'] >= 100) & (query_stats['position'] >= 21)]
        )

        results['queries_1000clicks_pos_4_10'] = len(
            query_stats[
                (query_stats['clicks'] >= 1000) &
                (query_stats['position'] >= 4) &
                (query_stats['position'] <= 10)
            ]
        )
        results['queries_1000clicks_pos_11_20'] = len(
            query_stats[
                (query_stats['clicks'] >= 1000) &
                (query_stats['position'] >= 11) &
                (query_stats['position'] <= 20)
            ]
        )
        results['queries_1000clicks_pos_21_plus'] = len(
            query_stats[(query_stats['clicks'] >= 1000) & (query_stats['position'] >= 21)]
        )

        # Position-based analysis for impressions
        results['queries_100impr_pos_4_10'] = len(
            query_stats[
                (query_stats['impressions'] >= 100) &
                (query_stats['position'] >= 4) &
                (query_stats['position'] <= 10)
            ]
        )
        results['queries_100impr_pos_11_20'] = len(
            query_stats[
                (query_stats['impressions'] >= 100) &
                (query_stats['position'] >= 11) &
                (query_stats['position'] <= 20)
            ]
        )
        results['queries_100impr_pos_21_plus'] = len(
            query_stats[(query_stats['impressions'] >= 100) & (query_stats['position'] >= 21)]
        )

        results['queries_1000impr_pos_4_10'] = len(
            query_stats[
                (query_stats['impressions'] >= 1000) &
                (query_stats['position'] >= 4) &
                (query_stats['position'] <= 10)
            ]
        )
        results['queries_1000impr_pos_11_20'] = len(
            query_stats[
                (query_stats['impressions'] >= 1000) &
                (query_stats['position'] >= 11) &
                (query_stats['position'] <= 20)
            ]
        )
        results['queries_1000impr_pos_21_plus'] = len(
            query_stats[(query_stats['impressions'] >= 1000) & (query_stats['position'] >= 21)]
        )

        # Convert counts to percentages
        for key in list(results.keys()):
            if key.startswith('queries_') and key != 'total_queries':
                pct_key = f'pct_{key}'
                results[pct_key] = (results[key] / total_queries) * 100

        return results

    def url_analysis(self) -> Dict:
        """Perform URL-based analysis."""
        url_stats = self.df.groupby('page').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'position': 'mean'
        }).reset_index()

        url_stats['ctr'] = (
            url_stats['clicks'] / url_stats['impressions']
        ).replace([np.inf, -np.inf], 0).fillna(0)

        total_urls = len(url_stats)

        results = {
            'total_urls': total_urls,
            'urls_with_clicks': len(url_stats[url_stats['clicks'] > 0]),
            'urls_with_impressions': len(url_stats[url_stats['impressions'] > 0]),
            'urls_without_clicks': len(url_stats[url_stats['clicks'] == 0]),
            'urls_without_impressions': len(url_stats[url_stats['impressions'] == 0]),
        }

        # Calculate percentages
        results['pct_urls_with_clicks'] = (
            results['urls_with_clicks'] / total_urls
        ) * 100
        results['pct_urls_with_impressions'] = (
            results['urls_with_impressions'] / total_urls
        ) * 100
        results['pct_urls_without_clicks'] = (
            results['urls_without_clicks'] / total_urls
        ) * 100
        results['pct_urls_without_impressions'] = (
            results['urls_without_impressions'] / total_urls
        ) * 100

        # CTR-based analysis
        results['urls_100clicks_1pct_ctr'] = len(
            url_stats[(url_stats['clicks'] >= 100) & (url_stats['ctr'] < 0.01)]
        )
        results['urls_1000clicks_1pct_ctr'] = len(
            url_stats[(url_stats['clicks'] >= 1000) & (url_stats['ctr'] < 0.01)]
        )
        results['urls_100impr_1pct_ctr'] = len(
            url_stats[(url_stats['impressions'] >= 100) & (url_stats['ctr'] < 0.01)]
        )
        results['urls_1000impr_1pct_ctr'] = len(
            url_stats[(url_stats['impressions'] >= 1000) & (url_stats['ctr'] < 0.01)]
        )

        # Position-based analysis for clicks
        results['urls_100clicks_pos_4_10'] = len(
            url_stats[
                (url_stats['clicks'] >= 100) &
                (url_stats['position'] >= 4) &
                (url_stats['position'] <= 10)
            ]
        )
        results['urls_100clicks_pos_11_20'] = len(
            url_stats[
                (url_stats['clicks'] >= 100) &
                (url_stats['position'] >= 11) &
                (url_stats['position'] <= 20)
            ]
        )
        results['urls_100clicks_pos_21_plus'] = len(
            url_stats[(url_stats['clicks'] >= 100) & (url_stats['position'] >= 21)]
        )

        results['urls_1000clicks_pos_4_10'] = len(
            url_stats[
                (url_stats['clicks'] >= 1000) &
                (url_stats['position'] >= 4) &
                (url_stats['position'] <= 10)
            ]
        )
        results['urls_1000clicks_pos_11_20'] = len(
            url_stats[
                (url_stats['clicks'] >= 1000) &
                (url_stats['position'] >= 11) &
                (url_stats['position'] <= 20)
            ]
        )
        results['urls_1000clicks_pos_21_plus'] = len(
            url_stats[(url_stats['clicks'] >= 1000) & (url_stats['position'] >= 21)]
        )

        # Position-based analysis for impressions
        results['urls_100impr_pos_4_10'] = len(
            url_stats[
                (url_stats['impressions'] >= 100) &
                (url_stats['position'] >= 4) &
                (url_stats['position'] <= 10)
            ]
        )
        results['urls_100impr_pos_11_20'] = len(
            url_stats[
                (url_stats['impressions'] >= 100) &
                (url_stats['position'] >= 11) &
                (url_stats['position'] <= 20)
            ]
        )
        results['urls_100impr_pos_21_plus'] = len(
            url_stats[(url_stats['impressions'] >= 100) & (url_stats['position'] >= 21)]
        )

        results['urls_1000impr_pos_4_10'] = len(
            url_stats[
                (url_stats['impressions'] >= 1000) &
                (url_stats['position'] >= 4) &
                (url_stats['position'] <= 10)
            ]
        )
        results['urls_1000impr_pos_11_20'] = len(
            url_stats[
                (url_stats['impressions'] >= 1000) &
                (url_stats['position'] >= 11) &
                (url_stats['position'] <= 20)
            ]
        )
        results['urls_1000impr_pos_21_plus'] = len(
            url_stats[(url_stats['impressions'] >= 1000) & (url_stats['position'] >= 21)]
        )

        # Convert counts to percentages
        for key in list(results.keys()):
            if key.startswith('urls_') and key != 'total_urls':
                pct_key = f'pct_{key}'
                results[pct_key] = (results[key] / total_urls) * 100

        return results

    def url_performance_analysis(self, thresholds: Dict = None) -> Dict:
        """Analyze URL performance based on clicks."""
        if thresholds is None:
            thresholds = {
                'top': 1000,
                'good': 100,
                'weak': 10
            }

        url_stats = self.df.groupby('page').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'position': 'mean'
        }).reset_index()

        total_urls = len(url_stats)

        # Categorize URLs
        top_urls = url_stats[url_stats['clicks'] >= thresholds['top']]
        good_urls = url_stats[
            (url_stats['clicks'] >= thresholds['good']) &
            (url_stats['clicks'] < thresholds['top'])
        ]
        weak_urls = url_stats[
            (url_stats['clicks'] >= thresholds['weak']) &
            (url_stats['clicks'] < thresholds['good'])
        ]
        dead_urls = url_stats[url_stats['clicks'] == 0]
        opportunity_urls = url_stats[
            (url_stats['clicks'] == 0) & (url_stats['impressions'] > 0)
        ]

        results = {
            'total_urls': total_urls,
            'top_urls_count': len(top_urls),
            'good_urls_count': len(good_urls),
            'weak_urls_count': len(weak_urls),
            'dead_urls_count': len(dead_urls),
            'opportunity_urls_count': len(opportunity_urls),
            'top_urls': top_urls,
            'good_urls': good_urls,
            'weak_urls': weak_urls,
            'dead_urls': dead_urls,
            'opportunity_urls': opportunity_urls
        }

        # Calculate percentages
        for category in ['top', 'good', 'weak', 'dead', 'opportunity']:
            results[f'pct_{category}_urls'] = (
                results[f'{category}_urls_count'] / total_urls
            ) * 100

        return results

    def generate_insights(self) -> Dict:
        """Generate actionable insights from the analysis."""
        query_results = self.query_analysis()
        url_results = self.url_analysis()
        performance_results = self.url_performance_analysis()

        insights = {
            'query_insights': {
                'high_potential_queries': query_results.get('queries_100impr_1pct_ctr', 0),
                'low_ctr_high_click_queries': query_results.get(
                    'queries_100clicks_1pct_ctr', 0
                ),
                'position_opportunities': {
                    'pos_4_10': query_results.get('queries_100clicks_pos_4_10', 0),
                    'pos_11_20': query_results.get('queries_100clicks_pos_11_20', 0),
                    'pos_21_plus': query_results.get('queries_100clicks_pos_21_plus', 0)
                }
            },
            'url_insights': {
                'performance_distribution': {
                    'top_urls': performance_results.get('pct_top_urls', 0),
                    'good_urls': performance_results.get('pct_good_urls', 0),
                    'weak_urls': performance_results.get('pct_weak_urls', 0),
                    'dead_urls': performance_results.get('pct_dead_urls', 0),
                    'opportunity_urls': performance_results.get('pct_opportunity_urls', 0)
                },
                'low_ctr_high_click_urls': url_results.get('urls_100clicks_1pct_ctr', 0)
            },
            'recommendations': []
        }

        # Generate recommendations
        if performance_results.get('pct_opportunity_urls', 0) > 10:
            insights['recommendations'].append(
                f"High opportunity: {performance_results.get('pct_opportunity_urls', 0):.1f}% "
                "of URLs have impressions but no clicks. Focus on improving CTR."
            )

        if query_results.get('queries_100clicks_1pct_ctr', 0) > 0:
            insights['recommendations'].append(
                f"Found {query_results.get('queries_100clicks_1pct_ctr', 0)} queries with "
                "100+ clicks but <1% CTR. Review meta titles and descriptions."
            )

        if performance_results.get('pct_dead_urls', 0) > 20:
            insights['recommendations'].append(
                f"{performance_results.get('pct_dead_urls', 0):.1f}% of URLs are dead. "
                "Consider content pruning or technical SEO improvements."
            )

        return insights
