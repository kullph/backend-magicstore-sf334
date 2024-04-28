from fastapi import APIRouter, Form, Depends
from model.storeModel import RawJSONData
from service.store import StoreService
import asyncpg
import os


router = APIRouter(
    prefix="/store",
    tags=["store"],
)

@router.get("/getAllShortend")
async def productGetNameAndID():
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    result = {}

    products = await conn.fetch(
        '''
        SELECT id, name FROM product;
        '''
        ,)
    
    for item in products:
        result[item['name']] = item['id']
    
    return {"status":True,"message":result}

@router.get("/productById/{id}")
async def productGetByID(id:int):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id)
    
    result = []
    for item in product:
        new_item = dict(item)
        img = await conn.fetch(
            '''
            SELECT img FROM img WHERE product_id = $1;
            '''
            ,item['id'])
        
        new_item['img'] = img
        result.append(new_item)
        

    return {"status":True,"message":result}

@router.get("/productsByElementId/{element_id}")
async def productGetByElemenIdt(element_id:int):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE Element_id = $1;
        '''
        ,element_id
        )
    
    temp  = []
    result = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])
        

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/productsByCategoryId/{category_id}")
async def productGetByCategoryId(category_id:int):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE Category_id = $1;
        '''
        ,category_id
        )
    
    temp  = []
    result = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/productsByElementName/{element_name}")
async def productGetByElementName(element_name:str):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )
    
    element_id = await conn.fetch(
        '''
        SELECT id FROM element WHERE name = $1;
        '''
        ,element_name
        )
    
    element_id = element_id[0]['id']

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE Element_id = $1;
        '''
        ,element_id
        )
    
    temp  = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])
        result = []

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/productsByCategoryName/{category_name}")
async def productGetByCategoryName(category_name:str):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )
    
    category_id = await conn.fetch(
        '''
        SELECT id FROM category WHERE name = $1;
        '''
        ,category_name
        )
    
    category_id = category_id[0]['id']

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE category_id = $1;
        '''
        ,category_id
        )
    
    temp  = []
    result = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])
        

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/productsByElementAndCategoryId/{element_id}/{category_id}")
async def productGetByElementAndCategory(element_id:int,category_id:int):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE Element_id = $1 AND category_id = $2;
        '''
        ,element_id, category_id
        )
    
    temp  = []
    result = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])
        

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/productsByElementOrCategoryId/{element_name}/{category_name}")
async def productGetByElementAndCategory(element_name:str,category_name:str):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )
    
    category_id = await conn.fetch(
        '''
        SELECT id FROM category WHERE name = $1;
        '''
        ,category_name
        )
    
    category_id = category_id[0]['id']

    element_id = await conn.fetch(
        '''
        SELECT id FROM element WHERE name = $1;
        '''
        ,element_name
        )
    
    element_id = element_id[0]['id']

    product_id = await conn.fetch(
        '''
        SELECT Product_id FROM search WHERE category_id = $1 AND element_id = $2;
        '''
        ,category_id,element_id
        )
    
    temp  = []
    result = []
    for id in product_id:
        product = await conn.fetch(
        '''
        SELECT * FROM product WHERE id = $1;
        '''
        ,id['product_id'])
        temp.append(product[0])
        

        for item in temp:
            img = await conn.fetch(
                '''
                SELECT img FROM img WHERE product_id = $1;
                '''
                ,item['id']
            )
            new_item = dict(item)
            new_item['img'] = img
            result.append(new_item)

    return {"status":True,"message":result}

@router.get("/reviewByProductId/{id}")
async def productGetReview(id:int):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    result = await conn.fetch(
        '''
            SELECT id, user_id, detail, score FROM review WHERE product_id = $1
        '''
        ,id
        )
    
    return {"status":True,"message":result}

@router.patch("/buy")
async def productGetReview(data:RawJSONData):
    conn = await asyncpg.connect(
        user='admin', 
        password='0000', 
        database='magic-store', 
        host='210.246.215.173',
        port='5432'
    )

    data=data.data

    for item in data:
        if not await StoreService.isHadById('product',item.product_id):
            return {"status":False,"message":"false product id"}
        
    for item in data:
        await conn.execute(
        '''
            UPDATE product SET sales_quantity = $1 WHERE id = $2;
        '''
        ,item.quantity, item.product_id
        )

    return {"status":True,"message":""}
