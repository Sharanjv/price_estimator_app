import os
import sqlalchemy
import pandas as pd

engine=sqlalchemy.create_engine(os.getenv('DB_URL_PRICE_EST'))


def get_listings(price, squareFootage, bedrooms, bathrooms):
    
    """this function queries listings table in AWS and returns a dataframe of the query result.
        If query result is empty, it returns an empty dataframe    
    """
    
    global engine
    
    raw_query="""select * 
                  from listings_pred 
                  where price>=:min_price 
                  and price<=:max_price
                  and "squareFootage">=:min_squareFootage
                  and "squareFootage"<=:max_squareFootage
                  and bedrooms>=:min_bedrooms
                  and bedrooms<=:max_bedrooms
                  and bathrooms>=:min_bathrooms
                  and bathrooms<=:max_bathrooms"""
    
    single_row_query="""select * 
                       from listings_pred
                       limit 1"""
    
    with engine.connect() as conn:
        query = sqlalchemy.text(raw_query)
        query1 = sqlalchemy.text(single_row_query)

        result=conn.execute(query, {'min_price': price[0], 'max_price': price[1], 
                                    'min_squareFootage': squareFootage[0], 'max_squareFootage': squareFootage[1], 
                                    'min_bedrooms': bedrooms[0], 'max_bedrooms': bedrooms[1], 
                                    'min_bathrooms': bathrooms[0], 'max_bathrooms': bathrooms[1]})
        
        result1 = conn.execute(query1)
        
        #check if result contains valid rows. if not return empty dataframe
        if result.fetchone():
            result=conn.execute(query, {'min_price': price[0], 'max_price': price[1], 
                                    'min_squareFootage': squareFootage[0], 'max_squareFootage': squareFootage[1], 
                                    'min_bedrooms': bedrooms[0], 'max_bedrooms': bedrooms[1], 
                                    'min_bathrooms': bathrooms[0], 'max_bathrooms': bathrooms[1]})
            return pd.DataFrame(result)
        else: 
             return pd.DataFrame(result1).iloc[0:0]
            
def get_price_groups ():
    
    """get list of unique price groups"""
    
    raw_query="""select distinct price_group_cd, price_group_desc from listings_pred"""
    global egine
    
    with engine.connect() as conn:
        query = sqlalchemy.text(raw_query)
        result = conn.execute(query)
    
    return pd.DataFrame(result).sort_values('price_group_cd')