import pandas as pd

ventas = {"descripción": ["Producto1", "Producto2", "Producto3"],
          "venta": ["3456", "5646", "7656"],
          }

dataframe = pd.DataFrame(ventas)
dataframe.to_excel('../docs/ventas.xlsx')
