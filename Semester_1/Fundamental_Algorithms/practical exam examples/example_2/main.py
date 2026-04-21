from repository.product_repository import ProductRepository
from service.product_service import ProductService
from domain.product import Product
from ui.console import Console

def main():
  filename = "products.txt"
  product_repository = ProductRepository(filename)
  product_service = ProductService(product_repository)
  console = Console(product_service)

  console.run()

if __name__ == "__main__":
  main()