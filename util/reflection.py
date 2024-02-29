from flask import jsonify

def populate_object(obj, data_dictionary):

    for field in data_dictionary.keys():
        try:
            getattr(obj, field)
            setattr(obj, field, data_dictionary[field])
        except:
            return({"message":f"field{field} not in object"})