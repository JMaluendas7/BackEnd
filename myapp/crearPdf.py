import aspose.pdf as ap
import aspose.words as aw

# Inicializar objeto de documento
document = ap.Document()

# Añadir página
page = document.pages.add()

# Inicializar objeto fragmento de texto
text_fragment = ap.text.TextFragment("Hello,world!")

# Agregar fragmento de texto a la nueva página
page.paragraphs.add(text_fragment)

# Guardar PDF actualizado
document.save("../docs/output.pdf")

doc = aw.Document("index.html")
doc.save("../docs/Outputt.pdf")
