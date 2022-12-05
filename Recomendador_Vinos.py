
import pandas as pd
import re




def extract():
    # Se extraen los datos del csv
    df = pd.read_csv("wines_SPA.csv", sep=",", encoding="UTF-8")
    df.drop_duplicates(inplace=True)
    print(df)

    return df


def transform(df_original, df_filtrado, vino):
    df_filtrado_recurs = df_filtrado.copy()
    filtros = {'1': 'winery', '2': 'wine', '3': 'year', '4': 'rating',
               '5': 'region', '6': 'price', '7': 'type', '8': 'body', '9': 'acidity'}
    print("\nSe puede buscar recomendar un vino respecto a los siguientes filtros:")
    print("     1. winery")
    print("     2. wine")
    print("     3. year")
    print("     4. rating (0-5)")
    print("     5. region")
    print("     6. price (10 per cent range)")
    print("     7. type")
    print("     8. body (0-5)")
    print("     9. acidity (0-5)")
    
    # Se listan los filtros
    
    # Se pide el número de filtro al usuario
    
    filtro_num = input("\nPor qué quiere filtrar (número)? ")
    filtro = filtros[filtro_num]
    
    print("")
    
    while filtro_num != "No" or df_filtrado.empty:
        valor = df_original.at[vino, filtro]
        
        # Se busca el valor del filtro de nuestro vino inicial
        
        # Si es precio, se mira un rango de 10%. El resto si es igual
        if filtro == "price":
            df_filtrado = df_filtrado[df_filtrado[filtro]
                                      <= valor*1.1]
            df_filtrado = df_filtrado[df_filtrado[filtro] >= valor*0.9]
        else:
            df_filtrado = df_filtrado[df_filtrado[filtro] == valor]
            
        # Si en algún momnto me paso de filtrado, hay que volver a empezar de 0
        
        if df_filtrado.empty:
            print("Se han realizado demasiados filtros. Filtre de nuevo desde 0. ")
            df_filtrado = transform(df_original, df_filtrado_recurs, vino)
            return df_filtrado
        else:
            print(df_filtrado)
        filtro_num = input("Quiere añadir algún filtro más? ")
        # Se pregunta un filtro nuevo, ssalvo que no se quiera usar más
        if filtro_num != "No":
            filtro = filtros[filtro_num]

    # Return un vino recomendado
    return df_filtrado


if __name__ == "__main__":

    print("||| RECOMENDADOR DE VINOD |||\n")

    # Con espacio tras la coma

    df_original = extract()
    df = df_original.copy()

    df_año = pd.DataFrame()

    while df_año.empty:
        # Se pide el vino. Se puede añadir con o sin paréntesis, pero tiene que ser "," + "space"
        vino = input("\nIntroduzca vino (Bodega, Vino, Año): ")
        vino = (re.sub(r'[()]', '', vino)).split(', ')
        
        # Se va filtrando por bodega, vino, año
        df_bodega = df[df["winery"] == vino[0]]
        df_nombre = df_bodega[df_bodega["wine"] == vino[1]]
        df_año = df_nombre[df_nombre["year"] == vino[2]]

        if df_año.empty:
            # Si no encuentra nada, hay que meterlo otra vez o no está en la base de datos
            print("\nHa habido un error. Introduzca el vino correctamente. Si es correcto, el vino no está en la base de datos")

    print("\nEl vino seleccionado es alguno de los siguientes:")

    print(df_año)
    # Se pide qeu se seleccione el vino (suele haber filas duplicadas por vinos, pero algunas con valores Nan)
    # Hay vinos que aparecen con valores NaN pero se ha preferido para no perder datos
    indice_v = int(input(
        "\nIntroduzca el índice de su vino (el que no contenga NaN si duplicados): "))
    indice = list(df_año.index)

    df.drop(indice, inplace=True)

    vino_recomendado = transform(df_original, df, indice_v)

    print("\nSe recomienda alguno de los siguientes vinos:")
    print(vino_recomendado)
