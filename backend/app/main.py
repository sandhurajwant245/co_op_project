from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from app.models import Destination
import pprint
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection settings
MONGO_URL = "mongodb+srv://sandhurajwant245:RwE6aPviB0NAjKF8@cluster0.iktaex9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE = "travel_db"
COLLECTION = "destinations"

# MongoDB client
client = MongoClient(MONGO_URL)
db = client[DATABASE]
collection = db[COLLECTION]

data_to_insert = [
     {
        "country": "India",
        "popular": [
            {
                "name": "Niagara Falls",
                "imageUrl": "niagara_falls.png",
                "rating": 4.1,
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "CN Tower",
                "imageUrl": "cn_tower.png",
                "rating": 4.7,
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "Niagara Falls",
                "imageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRy2vAGuAI9t5lB3nCmgP0hXEAg0w7951MTmfm864gXXHNGZT91kM0ZA4wH9aKNVUDhjw&usqp=CAU",
                "rating": 4.1,
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "CN Tower",
                "imageUrl": "https://blog.businesstripfriend.com/upload/gallery/articles/1484694233_34131.jpg",
                "rating": 4.7,
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ],
        "recommended": [
            {
                "name": "Explore Niagara",
                "imageUrl": "https://cdn.aarp.net/content/dam/aarp/travel/destinations/2021/08/1140-journey-behind-the-falls.jpg",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "Adventure",
                "imageUrl": "https://www.news-herald.com/wp-content/uploads/2022/06/TNH-L-NIAGARAFALLS-WBOX-060922-09.jpg?w=466",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ],
        "location": [
            {
                "name": "Niagara Falls",
                "imageUrl": "niagara_falls.png",
                "description": "A breathtaking natural wonder located on the border of Ontario, Canada, and New York, USA.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "CN Tower",
                "imageUrl": "cn_tower.png",
                "description": "A 553.3 m-high concrete communications and observation tower located in Downtown Toronto.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ],
        "hotels": [
            {
                "name": "Home Stay Niagara",
                "imageUrl": "https://maplestakeinn.com/wp-content/uploads/2024/05/a63b7d13.jpg",
                "rating": 4.5,
                "description": "Cozy and comfortable home stays near Niagara Falls.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "Toronto Apartments",
                "imageUrl": "https://maplestakeinn.com/wp-content/uploads/2024/05/pool-chairs-umbrella-around-swimming-pool-with-coconut-palm-tree_1339-121645.jpg",
                "rating": 4.3,
                "description": "Modern apartments with a stunning view of the Toronto skyline.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ],
        "adventure": [
            {
                "name": "Niagara Jet Adventures",
                "imageUrl": "https://r1imghtlak.mmtcdn.com/95c55596d2d811ed97ff0a58a9feac02.webp?&downsize=900:675&output-format=jpg",
                "rating": 4.8,
                "description": "Experience the thrill of a lifetime with jet boat rides on the Niagara River.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "EdgeWalk at the CN Tower",
                "imageUrl": "https://r1imghtlak.mmtcdn.com/459d46e66d3211eaa38a0242ac110004.jpg?&downsize=900:675&crop=900:675;56,0&output-format=jpg",
                "rating": 4.9,
                "description": "A hands-free walk on the ledge of the CN Tower, 116 stories above the ground.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ],
        "food": [
            {
                "name": "Skylon Tower Revolving Dining Room",
                "imageUrl": "https://food-guide.canada.ca/sites/default/files/styles/slick_gallery_mobile/public/2024-04/chicken%20lettuce%20wrap-heroweb-ready.jpg",
                "rating": 4.6,
                "description": "Fine dining with a revolving view of Niagara Falls.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            },
            {
                "name": "360 Restaurant at the CN Tower",
                "imageUrl": "https://food-guide.canada.ca/sites/default/files/styles/slick_gallery_mobile/public/2020-07/grilled_salmon.jpg",
                "rating": 4.7,
                "description": "A dining experience with a panoramic view of Toronto from the top of the CN Tower.",
                "detail-facilities": " Department of Information Technology",
                "price": 100
            }
        ]
    },
]


# Function to insert data into MongoDB
def insert_data_into_db(data):
    try:
        for entry in data:
            country = entry.get("country")
            for category, items in entry.items():
                if category == "country":
                    continue
                for item in items:
                    # Insert each item into MongoDB collection
                    collection.insert_one({
                        "country": country,
                        "category": category,
                        **item  # Unpack item details into MongoDB document
                    })
        print("Data inserted successfully into MongoDB.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")


# Insert data into MongoDB when FastAPI starts
@app.post("/startup")
async def startup_event():
    insert_data_into_db(data_to_insert)

@app.get("/check_db")
async def check_db_status():
    try:
        db = client[DATABASE]
        collection_names = db.list_collection_names()
        if COLLECTION in collection_names:
            return {"message": "MongoDB and collection 'destinations' are running"}
        else:
            return {"message": f"Collection '{COLLECTION}' not found in database '{DATABASE}'"}
    except Exception as e:
        return {"message": f"Failed to connect to MongoDB: {str(e)}"}

@app.get("/ping")
async def ping_server():
    return {"message": "Server is running"}

# Routes
@app.post("startup")
async def startup_db_client():
    try:
        client.server_info()  # Check if the client is connected
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error.")

@app.post("/destination/", response_model=Destination)
async def create_destination(destination: Destination = Body(...)):
    destination_dict = destination.dict()
    inserted_result = collection.insert_one(destination_dict)
    destination.id = str(inserted_result.inserted_id)
    return destination

# Pydantic model for Destination
class Destination(BaseModel):
    name: str
    category: str
    country: str
    description: Optional[str]
    facilities: Optional[str]
    imageUrl: str
    price: float
    rating: float

@app.get("/by/{countryname}", response_model=dict)
async def read_destination(countryname: str):
    try:
        # Query MongoDB to find all documents for the specified country
        cursor = collection.find({"country": countryname})

        # Convert cursor to list of dictionaries (JSON-serializable format)
        destinations = []
        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            doc['_id'] = str(doc['_id'])
            destinations.append(doc)

        if not destinations:
            return {"message": f"No destinations found for country '{countryname}'"}

        # filler location,recommended,popular,hotels, adventure,food from destination
        location = [dest for dest in destinations if dest['category'] == 'location']
        recommended = [dest for dest in destinations if dest['category'] == 'recommended']
        popular = [dest for dest in destinations if dest['category'] == 'popular']
        hotels = [dest for dest in destinations if dest['category'] == 'hotels']
        adventure = [dest for dest in destinations if dest['category'] == 'adventure']
        food = [dest for dest in destinations if dest['category'] == 'food']

        # Prepare response format
        destinations_by_category = {
            "countryname": countryname,
            "location": location,
            "recommended": recommended,
            "popular": popular,
            "hotels": hotels,
            "adventure": adventure,
            "food": food
        }

        return destinations_by_category

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving destinations: {str(e)}")


@app.get("/destinations", response_model=List[Destination])
async def read_destinations():
    try:
        destinations = list(collection.find())
        return destinations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving destinations: {str(e)}")

# Run the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
