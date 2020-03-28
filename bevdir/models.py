from django.db import models
from users.models import User



# BRANDNAMES = tuple([(spirit['brandname'], spirit['brandname']) for spirit in SPIRITS_LIST])

class Spirit(models.Model):
    brandname = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nc_code = models.CharField(max_length=10)
    supplier = models.CharField(max_length=100)
    proof = models.CharField(max_length=100)
    size = models.FloatField(default=0)
    mxb = models.FloatField(default=0)

    def __str__(self):
        return f'{self.brandname}'

    @property
    def price_per_oz(self):
        bottle_size_oz = float(self.size) * 33.814
        price_per_oz = round(float(self.mxb)/bottle_size_oz, 2)
        return price_per_oz



class MiscIngredient(models.Model):
    name = models.CharField(max_length=100)
    cost_per_unit = models.IntegerField(default=0)
    notes = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Rating(models.Model):
    stars = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    spirits = models.ForeignKey(Spirit, related_name='ratings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} {stars} stars'

class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_profit = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


    @property
    def total_cost(self):
        """
        cost per ounce=mxb_price/(size*33.814)
        cost per ounce* user input of volume = volume
        =total cost
        """
        total = 0
        for shot in self.shots.all():
            total += shot.cost
        # for portion in self.portions:
        #     total += portion.cost
        return total

    @property
    def recommended_price(self):
        """
        product of target_profit and total_cost
        """
        rec_price = self.total_cost/self.target_profit
        return rec_price

class Shot(models.Model):
    volume = models.FloatField(default=0)
    cocktail= models.ForeignKey(Cocktail, related_name='shots', on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirit, related_name='shots', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.volume} of {self.spirit.brandname} for {self.cocktail.name}'

    @property
    def cost(self):
        cost = self.volume * self.spirit.price_per_oz
        return cost

class Portion(models.Model):
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=10)
    price_per_unit = models.FloatField(default=0)
    cocktail= models.ForeignKey(Cocktail, related_name='portions', on_delete=models.CASCADE)
    misc_ingredient = models.ForeignKey(MiscIngredient, related_name='portions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.amount}{self.unit} of {self.misc_ingredient.name} for {self.cocktail.name}'

    @property
    def cost(self):
        cost = self.amount*self.price_per_unit
        return cost

#MANUALLY ENTER FOR NOW. EVENTUALLY POPULATE THIS DATA WITH A SCRAPE OR IMPORT FUNCTION:
# SPIRITS_LIST = [
#     {
#         'NC_Code':'00-005',
#         'collection':'Boutique Collection',
#         'category': 'bourbon',
#         'brandname':'Hookers house Bourbon',
#         'age':'NA',
#         'proof':'100',
#         'size':'0.75',
#         'unit':'L',
#         'mxb_price':'51.40',
#     },
#     {
#         'NC_Code':'00-810',
#         'collection':'Boutique Collection',
#         'category': 'Tequila & Mezcal',
#         'brandname':'Jose Cuervo Reserva de Familia',
#         'age':'NA',
#         'proof':'80',
#         'size':'0.75',
#         'unit':'L',
#         'mxb_price':'193.70',
#     },
#     {
#         'NC_Code':'42-916',
#         'collection':'Imported',
#         'category':'Gin',
#         'brandname':'Beefeater',
#         'age':'NA',
#         'proof':'94',
#         'size':'1.75',
#         'unit':'L',
#         'mxb_price':'$48.70',
#     },
#     {
#         'NC_Code':'43-251',
#         'collection':'Domestic',
#         'category': 'Vodka',
#         'brandname':'The Aperican Vodka',
#         'age':'NA',
#         'proof':'80',
#         'size':'1.75',
#         'unit':'L',
#         'mxb_price':'20.20',
#     },
#     {
#         'NC_Code':'56-784',
#         'collection':'Domestic',
#         'category': 'Cordials/ Liqueurs/ Specialties',
#         'brandname':'Hatfield & McCoy The Devil\'s Fire Moonshine',
#         'age':'NA',
#         'proof':'80',
#         'size':'.75',
#         'unit':'L',
#         'mxb_price':'31.70',
#     },
#     {
#         'NC_Code':'19-745',
#         'collection':'Special',
#         'category':'Special',
#         'brandname':'Cragganmore Distillers Edition 12Y',
#         'age':'12Y',
#         'proof':'80',
#         'size':'.75',
#         'unit':'L',
#         'mxb_price':'88.70',
#     },

# ]
