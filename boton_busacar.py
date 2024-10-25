def buscar_texto(pabra_para_buscar):
    import re
    pabra_para_buscar=input("ingrese el dato a buscar""\n")
    with open(archivo,"r") as f:
        lineas=f.readlines()
        buscador=re.escape(pabra_para_buscar)
        patas=re.compile(buscador)
        print("Resultado de la busqueda:""\n")
        for linea in lineas:
            if patas.search(linea):
                print(f"{linea.strip()}")
            else:
                print("No se encontraron resultados para la busqueda""\n""Imtemte con otro dato")
                input("\n""ingrese cialquier numero para continuar""\n")