from fastapi import  FastAPI, Request
from classes import *
import uvicorn
from fastapi.responses import JSONResponse

from fastapi.encoders import jsonable_encoder
from typing import List

app = FastAPI()

ID_GROUP = 1
ID_PARTICIPANT = 1

groups = []
participants =[]
participantsInGroups = []
recipients = []

def findInListByID(id: int, source: list):
    tmpActions = [item for item in source if item.id == id]
    if tmpActions == []:
        return -1
    else:
        return tmpActions[0]

def findGroupParticipantByID(id1: int, idperson: int):
    tmpActions = [item for item in participantsInGroups if item.ParticipantID == idperson and item.GroupID ==id1]
    if tmpActions == []:
        return -1
    else:
        return tmpActions[0]

@app.post("/group", status_code=202)
async def postPromo(request: Request):
    global ID_GROUP
    jsonbody = await request.json()
    name = jsonbody['name']
    description = jsonbody['description']
    item = Group(name=name, id=ID_GROUP, description=description)
    groups.append(item)
    ID_GROUP += 1
    return item.id

@app.get("/groups", response_model = List[Group], status_code=200)
async def getPromo():
    return groups

@app.get("/group/{id}")
async def getPromoID(id: int):
    global groups
    tmpAction = findInListByID(id, groups)
    if tmpAction == -1:
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=204)
    IDparticipants = [item.ParticipantID for item in participantsInGroups if item.GroupID == id]
    if IDparticipants != []:
        tmpparticipants = [item for item in participants if item.id in IDparticipants]
    else:
        tmpparticipants = []
    return {"id": tmpAction.id,
            "name": tmpAction.name,
            "description": tmpAction.description,
            "participants": tmpparticipants}

@app.put("/group/{id}")
async def getPromoID(id: int, request: Request):
    global groups
    jsonbody = await request.json()
    name = jsonbody['name']
    description = jsonbody['description']
    if name == '':
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=204)
    for i in range(len(groups)):
        if groups[i].id == id:
            groups[i].description = description
            groups[i].name = name 
            break
    return "OK"

@app.delete("/group/{id}", status_code=202)
async def deletePromo(id: int):
    global groups
    tmp = findInListByID(id, groups)
    groups.remove(tmp)

#-------------------------------
@app.post("/group/{id}/participant")
async def postParticipant(id: int, request: Request):
    global ID_PARTICIPANT, groups
    tmpAction = findInListByID(id, groups)
    if tmpAction == -1:
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=204)
    jsonbody = await request.json()
    name = jsonbody['name']
    wish = jsonbody['wish']
    item = Participant(id=ID_PARTICIPANT,name=name,wish=wish)
    ID_PARTICIPANT += 1
    participants.append(item)
    item2 = ParticipantsInGroups(ParticipantID=item.id, GroupID=id)
    participantsInGroups.append(item2)
    return item.id

@app.delete("/group/{id}/participant/{id2}")
async def postParticipant(id: int, id2: int):
    tmpAction = findInListByID(id, groups)
    if tmpAction == -1:
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=204)
    tmpPerson = findInListByID(id, participants)
    participants.remove(tmpPerson)
    tmppart = findGroupParticipantByID(id1=id, idperson=id2)
    participantsInGroups.remove(tmppart)


@app.post("/group/{id}/toss")
async def postRaffle(id: int):
    global groups
    tmpAction = findInListByID(id, groups)
    if tmpAction == -1:
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=204)
    IDparticipants = [item.ParticipantID for item in participantsInGroups if item.GroupID == id]

    if len(IDparticipants) < 3:
        return JSONResponse(content={"message": "Conflict"}, status_code=409)

    tmpparticipants = [item for item in participants if item.id in IDparticipants]
    listRes = []
    for i in range(len(tmpparticipants) - 1):
        item = Recipients(Person=tmpparticipants[i],Recipient=tmpparticipants[i+1])
        listRes.append(item)
        recipients.append(item)
    item = Recipients(Person=tmpparticipants[len(tmpparticipants)-1],Recipient=tmpparticipants[0])
    listRes.append(item)
    recipients.append(item)
    return(listRes)

@app.get("/group/{groupId}/participant/{participantId}/recipient")
async def getRecipient(groupId: int, participantId: int):
    tmpAction = findInListByID(participantId, participants)
    tmprez = [item for item in recipients if item.Person == tmpAction]
    return tmprez[0].Recipient


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)