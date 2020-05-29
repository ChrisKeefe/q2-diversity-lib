In bound_callable():

self.signature_order.items() contains all the stuff
while
user_input has dropped all args that are not passed explicitly

on line 224 of skd.action.bound_callable(), we call core.signature.check_types() on user_inputs.

check_types attempts to iterate over the things in the self.signature_order.items(), grabbing each item's name, and using it to index into the kwargs passed as user_inputs.
This fails (keyerror), because user_inputs is missing 'drop_undefined_samples'


user_inputs is missing information, because decorator.decorator in sdk.action._rewrite_wrapper_signature() is failing to preserve signature args.

######################################################3
decorator.decorator is being used to turn _bound_callable() into a wrapper function for the function we're turning into an Action. In other words, we use decorator.decorator to wrap function in bound_callable(), producing an action.

In order to replace this, we will need to wrap the function ourselves, preserving the signature. 

decorator.decorator has been superseded by decorator.decorate(reversed args). It is producing syntax errors for me, but this should be explored.

##################################################################
above not true. :(
decorator.decorator is just applying the new signature to the wrapper.
