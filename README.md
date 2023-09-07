# Aplicación multiplataforma y multinube para la descarga de contenido multimedia
![image](https://github.com/zaulilloxone2/Analizador_Lexico/blob/280971c8b4e514785cf26e6cecf40f1f4175a0ed/udg%20logo.jpg) 
#### Alumnos: 
#### *Mendoza Morelos Martin Mathier 214798285
#### *Jesús Ángel Cota López 220790768
#### *Saul Ezequiel García Ramos 215465492
#### Carrera: INCO
#### CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS EN INGENIERÍAS CUCEI
### Proyecto Modular con folio: 4PM2023B

### Objetivo:
La preservación de las historietas japonesas y americanas en la era digital es muy compleja y se debe a que no se encuentra este tipo de materiales con facilidad en la red. Por esta razón, se ha propuesto la creación de una biblioteca en línea que permita a los usuarios acceder y descargar títulos de manera gratuita y sin fines de lucro.
Para lograr esto, se utilizó una combinación de herramientas de scrapping web y computación en la nube para recopilar una amplia variedad de mangas, novelas, libros, imágenes, viñetas y cómics. La aplicación cuenta con tecnología PWA, lo que significa que se puede utilizar en una amplia gama de dispositivos y sistemas operativos, incluyendo teléfonos móviles y computadoras.
Gracias a la nube, se pueden conservar los perfiles e historiales de descarga de los usuarios, lo que permite una experiencia personalizada y eficaz para los usuarios de la aplicación.
Palabras claves – Proyecto modular, Scrapper, API (interfaz de programación de aplicaciones), Manga, Inteligencia Artificial,Hot One Encoding, ML, Clústeres, AWS, Firebase.

### Justificación Módulo de Arquitectura y Programación de Sistemas:
La arquitectura y programación de sistemas que se ha elegido para el desarrollo de la aplicación PWA (Progressive Web App) es una elección acertada por varias razones. En primer lugar, se[a] ha utilizado el framework Angular para el desarrollo del front-end de la aplicación, lo que permite crear una interfaz de usuario dinámica y amigable para el usuario. Además, se ha hecho uso de CSS[d] y JavaScript[b] para el diseño y la programación de la aplicación, lo que proporciona una gran flexibilidad para crear una experiencia de usuario atractiva e interactiva.
En cuanto al back-end de la aplicación, se ha utilizado Python[g] y Go[f] para el desarrollo del servidor, lo que proporciona una gran estabilidad y seguridad para la aplicación. Estos lenguajes de programación son conocidos por su eficiencia y rendimiento, lo que hace que la aplicación sea rápida y escalable.
Además, se ha utilizado la metodología ágil SCRUM[h] para el desarrollo del proyecto, lo que permite una mayor flexibilidad y adaptación a los cambios en el proceso de desarrollo. SCRUM se centra en la colaboración y la comunicación constante entre los miembros del equipo, lo que permite una mayor eficiencia y productividad en el desarrollo de la aplicación.
Por último, el uso de estructuras de datos como archivos PDF y listas, es fundamental para el correcto funcionamiento de la aplicación, ya que permiten una gestión eficiente y organizada de los datos que maneja la aplicación. Estas estructuras de datos permiten la creación de una base de datos sólida y confiable, lo que se traduce en una mejor experiencia de usuario y una mayor eficiencia en el funcionamiento de la aplicación.
En resumen, la arquitectura y programación de sistemas que se ha utilizado para el desarrollo de la aplicación PWA es una elección acertada debido a su eficiencia, flexibilidad y capacidad para proporcionar una experiencia de usuario atractiva e interactiva. El uso de lenguajes de programación estables y seguros, la metodología ágil SCRUM y la utilización de estructuras de datos eficientes son elementos clave para el éxito del proyecto.

### Justificación Módulo de Sistemas Inteligentes:
La justificación de utilizar sistemas inteligentes basados en el aprendizaje automático y la inteligencia artificial, utilizando el algoritmo de clasificación one hot encoding, se basa en la capacidad de esta tecnología para hacer predicciones precisas y tomar decisiones basadas en grandes conjuntos de datos. La codificación en caliente, que es una técnica de transformación de datos, ayuda a convertir variables categóricas en una forma más fácilmente comprensible para los algoritmos de ML.
En este caso particular, se utilizará el análisis de las descargas previas de mangas o cómics para adquirir conocimientos y predecir las preferencias del usuario en cuanto a los gustos de manga o cómic. Esto se logra a través de la identificación de patrones en los datos y la creación de modelos predictivos que puedan ser utilizados para ofrecer recomendaciones personalizadas al usuario.
En conclusión, la utilización de sistemas inteligentes basados en inteligencia artificial y aprendizaje automático, y específicamente el algoritmo de clasificación one hot encoding, permite a las empresas analizar grandes conjuntos de datos y tomar decisiones más precisas y personalizadas basadas en patrones de comportamiento del usuario. Esto proporciona una experiencia de usuario más satisfactoria y puede mejorar la eficiencia y efectividad de las operaciones empresariales.

### Justificación Módulo de Sistemas Distribuidos:
Como parte de la implementación del módulo 3, se ha considerado que el proyecto sea capaz de alojar una amplia cantidad de usuarios y que, en el futuro, tenga una gran capacidad de escalabilidad. Además, se ha tenido en cuenta aspectos como la velocidad, el rendimiento y el volumen de información a procesar. Es por esta razón que se ha decidido distribuir el procesamiento del backend de manera dividida, con el fin de mitigar la alta demanda de recursos necesarios.
Por un lado, se han establecido dos bases de datos en Firebase [i] que almacenan dos tipos de información. La primera base de datos guarda los datos de los usuarios, como sus nombres, mangas visitados, contraseñas y todos los datos necesarios para iniciar sesión. La segunda base de datos almacena información sobre los mangas, como reseñas, géneros, artistas, editoriales, entre otros.
Con el objetivo de dividir las solicitudes, el procesamiento del scraper y la generación del archivo PDF[j] resultante, se ha optado por dividir el backend para optimizar estas tareas que consumen muchos recursos. En este sentido, el scraper se encuentra alojado en un servidor de AWS, y se controlan las solicitudes a través de unas funciones llamadas lambdas. Estas funciones ejecutan el código en una infraestructura de computación altamente disponible y se encargan de todas las tareas de administración de los recursos de computación, incluyendo el mantenimiento del servidor y del sistema operativo. Posteriormente, se comunica con el backend del scraper para procesar la solicitud, y el scraper envía la respuesta en forma de un enlace que contiene metadatos, encabezados e incluso imágenes.
El procesamiento del algoritmo de codificación One Hot encoding se realiza en tiempo real, utilizando un contenedor Docker[k] de pequeño tamaño. En este contenedor, el algoritmo codifica los datos generados por el usuario mientras ve los mangas en una matriz. Luego, se genera un historial de vistas para conocer los posibles gustos del usuario en base a lo que ha visto. Con esta información, el algoritmo genera una lista de 20 mangas diferentes que puede recomendar al usuario final.
La interpretación de la información obtenida por el scraper y la generación del archivo PDF recae en el cliente, es decir, en el usuario final. A través del frontend, el usuario final utiliza sus propios recursos computacionales para armar el archivo PDF. Esto incrementa considerablemente la eficiencia de la aplicación y ahorra recursos del servidor, manteniéndolo siempre disponible y evitando sobrecargas.

### Conclusiones:

