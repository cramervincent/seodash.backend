from fastapi import APIRouter
from dependencies.dependencies import *
from models import models
from models import *
from functions.functions import scan_all_backlinks

from schemas.backlinks import *

router = APIRouter()


@router.get("/backlinks")
async def get_all_backlinks(db:Session = Depends(get_db)):
    result = db.query(models.Backlinks).all()
    return result

@router.get("/backlinks/scan")
async def get_all_backlinks(db:Session = Depends(get_db)):
    from datetime import date
    results = db.query(models.Backlinks).all()
    today = date.today().strftime('%m/%d/%Y')
    
    for result in results:  
        print(f"{result.id} / {len(results)}")
        entry = db.get(models.Backlinks, result.id)
        
        
        if await scan_all_backlinks(result.site, result.link) == False:
            entry.status = 'false'
                   
        else:
            entry.status = 'true'
            entry.last_check = today
            
        
        
    
        db.commit()
    
    return db.query(models.Backlinks).all()


@router.get("/backlinks/scan/{bId}")
async def get_all_backlinks(bId, db: Session = Depends(get_db)):
    from datetime import date
    results = db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()
    today = date.today().strftime('%m/%d/%Y')

    
        
    entry = db.get(models.Backlinks, bId)

    if await scan_all_backlinks(entry.site, entry.link) == False:
        entry.status = 'false'

    else:
        entry.status = 'true'
        entry.last_check = today

    db.commit()

    return db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()




@router.get("/backlinks/{bId}")
async def get_all_backlinks(bId, db:Session = Depends(get_db)):
    result = db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()
    if not result:
        raise HTTPException(status_code=404)
    return result

@router.post("/backlinks/")
async def create_new_backlink(data:backlink_schema, db:Session =  Depends(get_db)):
    new_backlink = models.Backlinks(
        link  = data.link,
        site  = data.site,
        status  = data.status,
        pa  = data.pa,
        da  = data.da,
        last_check = data.last_check,
    )
    db.add(new_backlink)
    db.commit()
    db.refresh(new_backlink)

    return new_backlink

@router.delete("/backlinks/{bId}")
async def delete_a_backlink(bId, db:Session =  Depends(get_db)):
    result = db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()
    if not result:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "Link verwijderd"

# @router.put("/backlinks/{bId}")
# async def edit_a_backlink():
#     return ["All backlinks"]    