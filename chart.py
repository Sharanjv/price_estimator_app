import geopandas as gpd
import altair as alt
import pandas as pd



def plot_background(counties_df, greater_philly):
    
    topojson_url = 'https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json'

    # Read topo json data into geo dataframe
    gdf = gpd.read_file(topojson_url)

    pa_nj_gdf = gdf[gdf['id'].isin(counties_df['FIPS Code']) & gdf['id'].isin(greater_philly)]


    # Pennsylvania and New Jersey background
    pa_nj_background = alt.Chart(alt.Data(values=pa_nj_gdf.to_json())).mark_geoshape(
        fill='lightgray',
        stroke='white', 
        dx=-2000, 
        tooltip=None
    ).properties(
        width=500,
        height=500
    ).project('albersUsa')
    
    return pa_nj_background


def labels_pointers(counties_df, greater_philly):
    
    county_labels = (alt.Chart(counties_df[counties_df['FIPS Code'].isin(greater_philly)])
                       .mark_text(align='left', baseline='middle', dx=5)
                       .encode(longitude='Longitude:Q',
                               latitude='Latitude:Q',
                               text='County:N', 
                               size=alt.condition(alt.datum.County=='Philadelphia', alt.value(18), alt.value(12))))
    
    return county_labels

 
def plot_viz(listings_predict, counties_df, greater_philly, price_groups):
    
    """plot points and selected point and plot final viz"""
    
    # color codes for points on map
    color_codes = ["#00695C", "#66CC00", "#FFD700", "#FFA500", "#E34234"]
    
    # format id (address) field
    listings_predict['id'] = listings_predict['id'].str.replace('-', ' ')

    # label expression mapping 
    label_expr = '{' + ', '.join([f'"{cd}": "{desc}"' for cd, desc in zip(price_groups['price_group_cd'], price_groups['price_group_desc'])]) + '}[datum.label]'
    
    price_grp_colors = (alt.Color('price_group_cd:O', 
                       scale=alt.Scale(domain = price_groups['price_group_cd'].to_list(), range=color_codes),
                       legend=alt.Legend(title='Price Estimate', labelExpr=label_expr)))
                      

    #get selection condition
    selection = alt.selection_point(fields=['longitude', 'latitude'], empty=False, on='click')
    
    #legend selection
    leg_sel = alt.selection_point(fields=['price_group_cd'], bind='legend')
    
    tooltip = [alt.Tooltip('price_group_desc:N', title='Price Estimate Group'),
               alt.Tooltip('price:Q', title='Listed Price ', format='$,.0f'),
               alt.Tooltip('price_est:Q', title='Estimated Price', format='$,.0f'),
               alt.Tooltip('squareFootage:Q', title='Square Footage', format=',d'),
               alt.Tooltip('id:N', title='Listing Address')]

    # Points on the map 
    points = (alt.Chart(listings_predict)
              .mark_circle(size=45)
              .encode(longitude='longitude:Q', latitude='latitude:Q', 
                      color = price_grp_colors,
                      tooltip=tooltip,
                      opacity=alt.condition(leg_sel, alt.value(0.5), alt.value(0.05)))
             .add_params(selection)
             .add_params(leg_sel)).properties(title='Select a listing to see additional details')
    
    selected_point = (alt.Chart(listings_predict)
                        .mark_circle(size=150, color='blue')
                        .encode(longitude='longitude:Q', latitude='latitude:Q')
                        .transform_filter(selection))
    
    
    # Base chart for information text
    base = (alt.Chart(listings_predict).transform_filter(selection))
    
    
    def infoWindowHeader(info_header, base_chart, size=14):
        """get info window headers"""

        header = (base_chart.mark_text(align='left', dx=-220, dy=40)
                            .encode(text=alt.value(info_header), color=alt.value('gray'), size=alt.value(size)))
        return header

    def infoWindowText(info_text, form,  base_chart, size=16, font_weight='normal', dx=-110, color=alt.value('black')):
        """get info window text"""

        text = (base_chart.mark_text(align='left', dx=dx, dy=40, fontWeight=font_weight)
                          .encode(text=alt.Text(info_text, format=form), color=color, size=alt.value(size)))
        return text

    
    
    colors = alt.Color('price_group_cd:O',
                        scale=alt.Scale(domain = price_groups['price_group_cd'].to_list(), range=color_codes),
                        legend=None)
    

    # Layer headers and text
    line0 = (alt.layer(infoWindowText('price_group_desc:N', '', base, size=22, dx=-220, color=colors))
               .properties(width=500, height=0.2))

    
    
    line1 = (alt.layer(infoWindowHeader('Listed Price:', base),  infoWindowText('price:N', '$0,.0f', base, size=18))
               .properties(width=500, height=0.2))

    line2 = (alt.layer(infoWindowHeader('Estimated Price:', base),  
                       infoWindowText('price_est:Q', '$0,.0f', base, size=18, font_weight='bold')).properties(
        width=500,
        height=1
    ))


    line3 = alt.layer(infoWindowHeader('Sq Ft:', base),  infoWindowText('squareFootage:Q', '0,.0f', base)).properties(
        width=500,
        height=1
    )

    line4 = alt.layer(infoWindowHeader('Bedrooms:', base),  infoWindowText('bedrooms:N', '0.0f', base)).properties(
        width=500,
        height=1
    )

    line5 = alt.layer(infoWindowHeader('Bathrooms:', base),  infoWindowText('bathrooms:Q', '0.1f', base)).properties(
        width=500,
        height=1
    )

    line6 = alt.layer(infoWindowHeader('Address:', base),  infoWindowText('id:N', '', base)).properties(
        width=500,
        height=1
    )

    line7 = alt.layer(infoWindowHeader('Year Built:', base),  infoWindowText('yearBuilt:N', '0.0f', base)).properties(
        width=500,
        height=1
    )

    line8 = alt.layer(infoWindowHeader('Days On Market:', base),  infoWindowText('daysOnMarket:N', '0.0f', base)).properties(
        width=500,
        height=1
    )

    line9 = alt.layer(infoWindowHeader('Lot Size:', base),  infoWindowText('lotSize:N', '0,.0f', base)).properties(
        width=500,
        height=1
    )
    

    line10 = alt.layer(infoWindowHeader('County:', base),  infoWindowText('county:N', '', base)).properties(
        width=500,
        height=1
    )
    
    
   # Combine the information texts vertically
    info_panel = alt.vconcat(line0, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10).properties(spacing=0.05)
    
    
    #layer all map elements     
    displayMap = ((plot_background(counties_df, greater_philly) 
                   + labels_pointers(counties_df, greater_philly) 
                   + points 
                   + selected_point)
                  .properties(width=400, height=450))
                 
    # display map + information panel
    
    viz = (alt.hconcat(displayMap, info_panel)
                .resolve_scale(color='independent')
                .properties(spacing=1))              
    
    
    

    return viz




                  

    
    
