VISION_PREFIX = """
Genera un archivo JSON con la siguiente estructuctura y define los valores para los atributos respectivos. 
Si no se encuentra un valor para algun campo, el valor de dicho campo será 'NaN'. let's think step by step: 

Estructura base:
{
    "data":{
    "cliente":{
         "nombre":"",
         "direccion":""
         },
    "proveedor":{
        "nombre":"",
        "direccion":""
        },
    "factura":{
        "identificador":"",
        "total":""
        },
    "productos":[
       {"/agregar nombre de producto segun la factura/":{"cantidad":"", "precio":""}},
       {"/agregar nombre de producto segun la factura/":{"cantidad":"", "precio":""}},
       {"/agregar nombre de producto segun la factura/":{"cantidad":"", "precio":""}}
       ],
    "descripcion": "",
    "resumen": "",
    "sentimiento":"/clasificar en 'positivo' o 'negativo'; si no hay suficiente información, clasificar en 'neutral'/"
    }    
}

"""



PDF_PREFIX = """
Resume el contexto con la siguiente estructura.
"descripcion": "/brinda una breve descripcion del contexto/",
"resumen": "/menciona los puntos clave del contexto/",
"sentimiento":"/evalúa si se utilizan palabras negativas o positivas para determinar si hay un sentimiento positivo o negativo/"
"""


