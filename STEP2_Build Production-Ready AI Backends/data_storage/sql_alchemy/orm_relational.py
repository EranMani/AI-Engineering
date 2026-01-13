from sqlalchemy import create_engine, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

# 1. Standard Setup
class Base(DeclarativeBase):
    pass

# 2. The Parent Table (Brand)
class Brand(Base):
    __tablename__ = "brands"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    
    # THE MAGIC LINK 🔗
    # This tells Python: "I have a list of products."
    # back_populates means: "The Product class calls this link 'brand'"
    products: Mapped[list["Product"]] = relationship(back_populates="brand")

    def __repr__(self):
        return f"<Brand {self.name}>"

# 3. The Child Table (Product)
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column()
    
    # THE FOREIGN KEY (The actual database column)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    
    # THE MAGIC LINK 🔗
    # This tells Python: "This product belongs to one specific Brand object."
    brand: Mapped["Brand"] = relationship(back_populates="products")

    def __repr__(self):
        return f"<Product {self.name}>"

# 4. Create Tables
engine = create_engine("sqlite:///relational_store.db", echo=True)
Base.metadata.create_all(engine)
print("--- Tables Created ---")