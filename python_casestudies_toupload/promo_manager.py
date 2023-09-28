import pandas as pd

class PromoManager:
    def __init__(self):
        self.promo_details = pd.DataFrame({'promo_code': ['DIGITALU', 'TTECDIGI', 'COOLGUYS', 'HYDBAD12'],
                                           'discount_fraction': [0.59, 0.47, 0.31, 0.17]})
    
    def get_discount(self, promo_code):
        promo_info = self.promo_details[self.promo_details['promo_code'] == promo_code]
        if not promo_info.empty:
            return promo_info.iloc[0]['discount_fraction']
        return None

