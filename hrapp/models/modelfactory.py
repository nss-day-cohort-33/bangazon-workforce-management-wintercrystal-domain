import sqlite3

# Higher order function to create instances of models
# when performing single table queries
#Can't use model factory when there is a join in the table (book v. library)
def model_factory(model_type):
    def create(cursor, row):
        instance = model_type()
        smart_row = sqlite3.Row(cursor, row)
        for col in smart_row.keys():
            setattr(instance, col, smart_row[col])
        return instance
    return create