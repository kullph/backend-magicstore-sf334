from fastapi import APIRouter, Form, Depends, FastAPI, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
import asyncpg
from datetime import timedelta, datetime
from service.mgmt import MgmtService
import os


router = APIRouter(
    prefix="/mgmt",
    tags=["store management"],
)

@router.get("/product")
async def productGetAll(
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    products = await conn.fetch(
    '''
    SELECT * FROM product;
    '''
    ,)

    result = []
    for e in products:
        new_e = dict(e)
        img = await conn.fetch(
            '''
            SELECT img FROM img WHERE product_id = $1;
            '''
            ,e['id'])
        new_e['img'] = img
        result.append(new_e)

    return {"status":True,"message":result}

@router.post("/product")
async def productCreate(
    name:str=Form(...),
    description:str=Form(...),
    price:float=Form(...),
    left_quantity:int=Form(...),
    file: list[UploadFile] = File(...),
    category_id:int=Form(...),
    element_id:int=Form(...)
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    if not await MgmtService.isHadById('element',element_id):
        return {"status":False,"message":"false element id"}
    if not await MgmtService.isHadById('category',category_id):
        return {"status":False,"message":"false category id"}

    pro_id = await conn.fetchval(
        '''
        INSERT INTO product(name, description, price, category_id, element_id, left_quantity, sales_quantity) VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING id;
        '''
        ,name,description,price,category_id,element_id,left_quantity,0
        )
    
    for img in file:
        file_path = os.path.join("./image", img.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await img.read())

        await conn.execute(
            '''
            INSERT INTO img(img, product_id) VALUES($2,$1)
            '''
            ,pro_id ,img.filename
            )
    
    await conn.execute(
            '''
            INSERT INTO search(product_id, category_id, element_id) VALUES($1, $2, $3)
            '''
            ,pro_id, category_id, element_id
            )

    return {"status":True,"message":""}

@router.put("/product")
async def productEdit(
    product_id:int=Form(...),
    name:str=Form(...),
    description:str=Form(...),
    price:float=Form(...),
    left_quantity:int=Form(...),
    file: list[UploadFile] = File(...),
    category_id:int=Form(...),
    element_id:int=Form(...)
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    if not await MgmtService.isHadById('element',element_id):
        return {"status":False,"message":"false element id"}
    if not await MgmtService.isHadById('category',category_id):
        return {"status":False,"message":"false category id"}

    pro_id = await conn.fetchval(
        '''
        INSERT INTO product(name, description, price, category_id, element_id, left_quantity, sales_quantity) VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING id;
        '''
        ,name,description,price,category_id,element_id,left_quantity,0
        )
    
    for img in file:
        file_path = os.path.join("./image", img.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await img.read())

        await conn.execute(
            '''
            INSERT INTO img(img, product_id) VALUES($2,$1)
            '''
            ,pro_id ,img.filename
            )
    
    await conn.execute(
            '''
            INSERT INTO search(product_id, category_id, element_id) VALUES($1, $2, $3)
            '''
            ,pro_id, category_id, element_id
            )

    return {"status":True,"message":""}

@router.delete("/product")
async def productDelete(
    product_id:str=Form(...)
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    await conn.execute(
        '''
        DELETE FROM product WHERE id = $1;
        '''
        ,int(product_id)
        )
    
    return {"status":True,"message":""}

@router.get("/category")
async def categoryGetAll(
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    result = await conn.fetch(
        '''
        SELECT * FROM category;
        '''
        ,
        )
    
    return {"status":True,"message":result}

@router.post("/category")
async def categoryPost(
    name:str=Form(...),
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    if not await MgmtService.isHadByName('category',name) :
        await conn.execute(
            '''
            INSERT INTO category(name) VALUES($1);
            '''
            ,name
            )
        return {"status":True,"message":""}
    else:
        return {"status":False,"message":"Category already has"}

@router.put("/category")
async def categoryPut(
    id:int=Form(...),
    name:str=Form(...)
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    await conn.execute(
        '''
        UPDATE category SET name = $1 WHERE id = $2
        '''
        ,name, id
        )
    
    return {"status":True,"message":""}

@router.delete("/category")
async def categoryDel(
    id:int=Form(...),
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    await conn.execute(
        '''
        DELETE FROM category WHERE id = $1;
        '''
        ,id
        )
    
    return {"status":True,"message":""}

@router.get("/element")
async def elementGetAll(
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    result = await conn.fetch(
        '''
        SELECT * FROM element;
        '''
        ,
        )
    
    return {"status":True,"message":result}

@router.post("/element")
async def elementPost(
    name:str=Form(...),
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    if not await MgmtService.isHadByName('element',name) :
        await conn.execute(
            '''
            INSERT INTO element(name) VALUES($1);
            '''
            ,name
            )
        return {"status":True,"message":""}
    else:
        return {"status":False,"message":"element already has"}

@router.put("/element")
async def elementPut(
     id:int=Form(...),
    name:str=Form(...)
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    await conn.execute(
        '''
        UPDATE element SET name = $1 WHERE id = $2
        '''
        ,name, id
        )
    
    return {"status":True,"message":""}

@router.delete("/element")
async def elementDel(
        id:int=Form(...),
    ):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='localhost',
        port='5432'
        )
    
    await conn.execute(
        '''
        DELETE FROM element WHERE id = $1;
        '''
        ,id
        )
    
    return {"status":True,"message":""}