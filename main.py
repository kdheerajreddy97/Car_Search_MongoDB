from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.staticfiles import StaticFiles
from bson import ObjectId

app = FastAPI()
templates = Jinja2Templates(directory="static")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.mongodb = app.mongodb_client['Craiglist']

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()

@app.post("/search")
async def search(request: Request, search: str = Form(None), area: str = Form(None)):
    if search and area:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Please enter either the search field or the area field, not both."})
    elif search:
        # Handle search based on manufacturer
        projection = {"model": 1,"manufacturer": 1,"region": 1,"location": 1, "_id": 0}
        region_data = await app.mongodb["Cars"].find_one(
                {"region": area},
                projection=projection
            )
        if region_data:
            longitude = region_data["location"]["coordinates"][0]
            latitude = region_data["location"]["coordinates"][1]

        results = await app.mongodb["Cars"].find(
            {"$text": {"$search": search}},
            projection=projection
        ).to_list(length=1000)
        if results:
            formatted_results = [f"Model: {r['model']}, Manufacturer: {r['manufacturer']}, Region: {r['region']}" for r in results]
            return templates.TemplateResponse("result.html", {"request": request, "results": formatted_results})
        else:
            return templates.TemplateResponse("notfound.html", {"request": request})
    elif area:
            
            projection = {"location": 1, "_id": 0}
            region_data = await app.mongodb["Cars"].find_one(
                {"region": area},
                projection=projection
            )
            if region_data:
                longitude = region_data["location"]["coordinates"][0]
                latitude = region_data["location"]["coordinates"][1]

                # Calculate the radius for the $geoWithin query
                radius = 1000 / 6371  # 5km radius in radians (6371 is the approximate radius of the Earth)

                # Fetch all cars in the same region or within 5km distance
                cars = await app.mongodb["Cars"].find(
                    {
                        # "$or": [
                            # {"region": area},
                            # {
                            "location": {
                                '$near': {
                                    '$geometry': {
                                        'type':"Point",
                                        'coordinates':[longitude, latitude]
                                    },
                                    '$maxDistance': 5000
                                }
                            # }
                            }
                        # ]
                    }
                ).to_list(length=1000)

            # print(latitude, longitude)
            
                if cars:
                    formatted_results = [
                        f"Model: {car['model']}, Manufacturer: {car['manufacturer']}, Region: {car['region']}"
                        for car in cars
                    ]
                    return templates.TemplateResponse("result.html", {"request": request, "results": formatted_results})
                else:
                    return templates.TemplateResponse("notfound.html", {"request": request})
    else:
        return templates.TemplateResponse("notfound.html", {"request": request})

@app.get("/details/{index}")
async def car_details(request: Request, index: int):
    results = await app.mongodb["Cars"].find(
        {}
    ).to_list(length=1000)
    if index >= 0 and index < len(results):
        car = results[index]
        return templates.TemplateResponse("car_details.html", {"request": request, "car": car})
    else:
        return templates.TemplateResponse("notfound.html", {"request": request})
    
@app.post("/add_comment/{_id}")
async def thankyou(request: Request, _id: str, comment: str = Form(...)):
    print(_id)
    car_object_id = ObjectId(_id)
    car = await app.mongodb["Cars"].find_one({"_id": car_object_id})
    print(car_object_id)
    if car:
        await app.mongodb["Cars"].update_one({"_id": car_object_id}, {"$set": {"comment": comment}})
        print("Comment added successfully")
        print(car_object_id)
        return templates.TemplateResponse("thankyou.html", {"request": request})
    else:
        print("Comment not added")
        return templates.TemplateResponse("notfound.html", {"request": request})
    
@app.get("/thankyou")
async def thankyou(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})
    
@app.get("/")
async def main():
    return FileResponse('static/search.html')