import pandas as pd

def get_county_data():
    
    pa_nj_county_data = {
    'County': [
        'Bucks', 'Delaware', 'Montgomery', 'Chester', 'Philadelphia', 'Atlantic', 'Bergen', 'Burlington', 
        'Camden', 'Cape May', 'Cumberland', 'Essex', 'Gloucester', 'Hudson', 'Hunterdon', 'Mercer', 
        'Middlesex', 'Monmouth', 'Morris', 'Ocean', 'Passaic', 'Salem', 'Somerset', 'Sussex', 
        'Union', 'Warren'
    ],
    'FIPS Code': [
        '42017', '42045', '42091', '42029', '42101', '34001', '34003', '34005', 
        '34007', '34009', '34011', '34013', '34015', '34017', '34019', '34021', 
        '34023', '34025', '34027', '34029', '34031', '34033', '34035', '34037', 
        '34039', '34041'
    ],
    'Latitude': [
        40.34, 39.92, 40.16, 39.97, 39.95, 39.48, 40.96, 39.83,
        39.80, 39.09, 39.35, 40.79, 39.77, 40.74, 40.57, 40.28,
        40.42, 40.29, 40.87, 39.85, 40.86, 39.57, 40.56, 41.13,
        40.65, 40.85
    ],
    'Longitude': [
        -75.13, -75.41, -75.36, -75.65, -75.16, -74.65, -74.03, -74.67,
        -75.10, -74.80, -75.18, -74.23, -75.13, -74.07, -74.92, -74.70,
        -74.41, -74.13, -74.54, -74.20, -74.29, -75.37, -74.64, -74.75,
        -74.26, -75.01
    ]
    }

    counties_df = pd.DataFrame(pa_nj_county_data)
    
    return counties_df


def get_greater_philly_fips():
    
    """FIPS codes for counties for greater Philly"""
    
    greater_philly = ['42029', '42045', '42101', '42091', '42017', '34015', '34005', '34033', '34007', '34005', '34011', 
                      '34001', '34029', '34025', '34021',  '34023', '34019', '34035', '34023', '34039']
    
    return greater_philly



    