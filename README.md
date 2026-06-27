# VZLA_DEDUP
Limpiemos los registros en esta crisis

[Docs](https://docs.google.com/document/d/1RzTa_bjouoZrjoS-fo1ojqUxjaTYy_w5Fg6Ad3fX8TU/edit?usp=sharing)

# El problema

Hay miles de páginas, donde miles de personas suben datos relevantes, pero están todos descentralizados y no son accesibles. Esto hace que al querer crear una página nueva, proporcionemos datos duplicados, no verificados, obsoletos o irrelevantes. 

Este grupo se enfoca en arreglar este problema, a crear una base de datos centralizada y fiable. Esta BD la repartiremos mediante un API a las demás personas.

## Las etapas

Antes de hablar de una solución, entendamos a que nos enfrentamos

1. Recolección de datos: No podemos trabajar si no tenemos datos.
2. Serializar datos: Tendremos imágenes, texto y distintos formatos, necesitamos estandarizarlos.
3. Protección de datos: Los datos más sensibles como cédulas se tienen que hashear.
4. Depuración: Necesitamos eliminar duplicados y datos obsoletos. Esta es la etapa más peligrosa.
5. Almacenar: Guardamos los datos en una base de datos cifrada.
6. Verificación: Finalmente tenemos que corroborar si los datos corresponden con la realidad.

La recolección, serializar datos, protección y almacenamiento son las partes más simples. Scrapers, formaters y listo.

El problema es la depuración y verificación.

Para depurar, como determinamos que un dato esta duplicado? Que es obsoleto? Que no es relevante? El problema es que tratamos con información delicada, si descartamos información que era importante cometimos un error.

Verificar requiere contacto con la realidad física, aquí vamos a depender de páginas externas para que nos ayuden.

## Equipos

- Scrapers/Cleaners: Buscan data, la serializan, hashean y depuran.
- DB/API Managers: Manejan la bases de datos y su cifrado, crea los endpoints a los que se van a conectar los devs externos.
- Verification Team: Se encargan de hablar con páginas existentes, nos mandan datos relevantes y nos ayudan a entender como es que hay que hacer para verificar la data.

# Estructura Actual

```
.
├── api
│   ├── __init__.py
│   ├── auth.py
│   ├── main.py
│   └── routes
├── LICENSE
├── README.md
├── scrapers
│   ├── __init__.py
│   └── sources
├── shared
│   ├── __init__.py
│   ├── config.py
│   ├── hashing.py
│   └── storage.py
└── verification
    └── __init__.py
```

## Contribuciones

Estamos usando pull requests que solo se aceptan con verificación de una persona más.

1. Crea tus cambios, commit.
2. Crea una nueva rama `git checkout -b <nombre_de_tu_rama>`
3. Haz push
4. Ve a Github, crea el pull request, documenta y espera a que otro miembro del equipo lo acepte.


## Stack

Los frameworks que usamos
### Scrapping



### API/DB

- PSQL
- FastAPI - Python


### Validation