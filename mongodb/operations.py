import pymongo
from datetime import datetime
from bson.objectid import ObjectId

client = pymongo.MongoClient('mongodb+srv://<username>:<password>@cluster0.0d5fxsv.mongodb.net/test')

db = client['sample_mflix']

collections = db.list_collection_names()

comments = db.comments

# deleting
comments.find_one_and_delete({'name': 'Yara Greyjoy'})

# querying
comments.find_one({'name': 'Yara Greyjoy'})

# The web framework gets post_id from the URL and passes it as a string
def get_document_with_objectid(object_id):
    # Convert from string to ObjectId:
    return client.sample_mflix.comments.find_one({'_id': ObjectId(object_id)})

get_document_with_objectid('5a9427648b0beebeb6957b18')

# Create if not exists collection
#
# option 1 (require permissons to use validate_collection)
#ry:
#    db.validate_collection("test_collection")  # Try to validate a collection
#except pymongo.errors.OperationFailure:  # If the collection doesn't exist
#    print("This collection doesn't exist")
#    db.create_collection('test_collection')
#
# option 2
if not 'test_collection' in collections:
    db.create_collection('test_collection')

db.list_collection_names()

# Upsert mode
updates = [
    {
        '_id': ObjectId('5a9427648b0beebeb69579f5'), 
        'name': 'Yara Greyjoy', 
        'email': 'gemma_whelan@gameofthron.es', 
        'movie_id': ObjectId('573a1393f29313caabcde008'), 
        'text': 'Placeat minus at iure consectetur dolor animi veniam. Officiis eaque optio aliquam autem corporis repellat repellat sapiente. Repellat ratione fugit recusandae praesentium quae nam praesentium.', 
        'date': datetime(1997, 2, 22, 1, 54, 50)
    }
]

now = datetime.utcnow()
for document in updates:
    comments.update_one(
        filter={
            '_id': document['_id'],
        },
        update={
            '$setOnInsert': {
                'insertion_date': now,
            },
            '$set': {
                'last_update_date': now,
            },
        },
        upsert=True,
    )

comments.find_one({'_id': updates[0]['_id']})

print('asd')
