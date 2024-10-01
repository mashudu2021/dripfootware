from .cart import Cart

# create context processs our cart can work on every page
def cart(request):
    #Return the default data from our cart
    return{'cart': Cart(request)}