from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel, Field
from app.models.books import book
from app.db.base import get_db, engine
from sqlalchemy.orm import Session
from app.serializers.books.book import Book
from app.serializers.base import DataResponse
import io
import pandas as pd
app = FastAPI()
book.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(book.Books).all()


@app.post("/")
async def create_book(model_book: Book, db: Session = Depends(get_db)):
    book_model = book.Books()
    # print(model_book.title)
    book_model.title = model_book.title
    book_model.author = model_book.author
    book_model.description = model_book.description
    book_model.rating = model_book.rating

    db.add(book_model)
    db.commit()
    return await DataResponse().success_response(data=None, message="Create successful!", code=200)


@app.put("/{book_id}")
async def update_book(book_id: int, model_book: Book, db: Session = Depends(get_db)):
    book_model = db.query(book.Books).filter(book.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    book_model.title = model_book.title
    book_model.author = model_book.author
    book_model.description = model_book.description
    book_model.rating = model_book.rating

    db.add(book_model)
    db.commit()

    return await DataResponse().success_response(data=None, message="Update successful!", code=200)


@app.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(book.Books).filter(book.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    db.query(book.Books).filter(book.Books.id == book_id).delete()

    db.commit()
    return await DataResponse().success_response(data=None, message="Delete successful!", code=200)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    if file.filename.endswith('.xlsx'):
        # Read it, 'f' type is bytes
        f = await file.read()
        xlsx = io.BytesIO(f)
        dataframe1 = pd.read_excel(xlsx)
        for index, row in dataframe1.iterrows():
            book_model = book.Books()
            book_model.title = row["Title"]
            book_model.author = row["Author"]
            book_model.description = row["Description"]
            book_model.rating = row["Rating"]
            db.add(book_model)
            db.commit()
        return await DataResponse().success_response(data=None, message="Create successful!", code=200)
    else:
        return await DataResponse().error(data=None, message="You must choose the file in the correct format", code=404)

