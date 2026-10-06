from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Produto


Base.metadata.create_all(bind=engine)

app = FastAPI()


class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    categoria: str


@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    return produto


@app.post(
    "/produtos",
    status_code=status.HTTP_201_CREATED
)
def cadastrar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db)
):
    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        categoria=produto.categoria
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()

    return None
