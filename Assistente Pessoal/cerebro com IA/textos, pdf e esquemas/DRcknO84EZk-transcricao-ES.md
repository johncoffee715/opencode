---
video_id: DRcknO84EZk
titulo: "Qwen en Claude Code: Programación LOCAL con IA y llama.cpp"
url: https://www.youtube.com/watch?v=DRcknO84EZk
canal: Nichonauta
etiquetas: [L-e, S-ca]
status: INGERIDA
origem: auto-subs ES via yt-dlp 2026.08.19 (EN 429 graceful)
data_ingestao: 2026-09-10
---

# DRcknO84EZk — Transcrição limpa (ES)

El día de hoy vamos a ver algo que ya hemos visto más de una ocasión, que es básicamente el desarrollo con modelos de lenguaje pequeñitos en nuestra PC, como lo pueden ser el modelo Qen 3.54B. Utilizamos dicho modelo porque la verdad es que funciona bastante bien y a pesar de que ya tiene varios meses que salió,

vemos que se sigue descargando demasiado y esto únicamente de su repositorio oficial dentro de Hugin Face, siendo que también está en Model Scope, que es de la misma gente de Alibaba Quen y que hay distintos tamaños de modelo. Este modelo lo vamos a probar el día de hoy con algo como P agent o cloud code. Y para ello,

pues simplemente lo que vamos a hacer es descargarlo. Solo antes de ello, recordar que Qen 3.54B es la versión más reciente de este tamaño, porque a pesar de que hay 3.6, no hay de este tamaño, 3.7 no hay de pesos abiertos y 3.8 no hay de este tamaño, solo unas versiones foneadas que

le ponen ese nombre, pero que no es original y que ya tenemos un directo probando todos ellos y funciona peor que el original. Entonces, dentro del tamaño 4B, este es el modelo más actual que tiene la gente de Quen. Es un modelo liberado bajo licencia APHE 2.0, que como entrada tiene imagen y texto, es

decir, es un modelo multimodal. Como salida solo texto es un modelo denso, no mezcla de expertos, con capacidad de activar o desactivar cadena de razonamiento, 262,144 tokens de ventana de contexto, 2011 idiomas, uso de herramientas y la ventana de contexto expandible hasta

1,10,000. Es un modelo bastante interesante que además cuenta con MTP predicción multitoken, incluido en el mismo modelo este modelo borrador para predecir más rápido los tokens siguientes, generando entonces más tokens por segundo. Vamos pues a descargarlo cuantizado para ser

ejecutado en llama CPP y lo descargaremos del agente de un slot. Tenemos por aquí Qen 3.54BT. Nos vamos a archivos y versiones y en esta ocasión yo voy a descargar el UDQ4 KXL, el cual el modelo pesa 2.99 GB, teniendo en cuenta que de todos modos aquí dentro está el MTP para la

predicción multitoken. Lo voy a descargar y también descargaré el mm Prog Bf16 para la visión pesando 676 MB. Esto claramente puede funcionar tanto en GPU como en CPU. en mismo llama CPP o cualquier programa. Y de hecho ya tenemos muchos tutoriales sobre llama CPP y sobre cómo funcionar únicamente

con CPU. Si nos vamos al model card y vemos por aquí la guía oficial que la gente de un slot tiene, vamos a ver que para ejecutarlo depende del tipo de uso que le queramos dar, se recomiendan unos parámetros de ese empleo u otros. Tareas generales de razonamiento son estos de por aquí, código preciso como por

ejemplo desarrollo web con razonamiento, esto de por aquí y luego seguimiento de instrucciones o bueno, en modo instructo razonamiento para targas generales y para razonamiento general. Tenemos todo esto y entonces lo que nosotros vamos a configurar es como esto de por aquí para desarrollo agéntico. Para ello, como en

nuestros videos que tenemos ya de llama CPP, vamos a hacer una carpeta en la que vamos a meter el modelo Qen 3.54B y aquí dentro pues metemos los dos archivos que acabamos de descargar ocupando en total 3.41 GB. Recordemos que este modelo en la actualidad es bastante más potente que lo top top que

teníamos de servicios en línea privados hace aproximadamente año y medio. Por ejemplo, si buscamos por aquí ese QEN 3.5, Qen 3.54B 54B nos aparece con una puntuación aproximada de 14, mientras que, por ejemplo, el O3 Mini o O3 Mini Higaban entre 13 y 10, siendo que estos modelos en su momento eran los más

inteligentes. Tiempo después salió el O3 Pro, que básicamente es el mismo modelo, 3 ejecutado múltiples veces, gastando más tokens para dar mayor calidad, cosa que es costosísima y lenta, pero pues eso mismo se puede hacer con cualquiera, no es un modelo en sí. Entonces, 10 o 13 de puntuación comparado contra 14.

200,000 tokens de ventana de contexto, 262,000 expandibles hasta 1,000ón sin multimodalidad, con visión de imágenes y videos. Estamos viendo entonces que no solo es que sea más inteligente de manera general, sino que también tiene más ventana de contexto y además

expandible hasta 1,10,000 y tiene capacidades multimodales, cosa que ese otro modelo no. Y en este caso lo podemos ejecutar con o sin cadena de razonamiento, mientras que los modelos O de Open AI pues son razonadores, no se puede desactivar el razonamiento. Así que vemos que tenemos un modelo

pequeñito, pero realmente bastante bastante bueno, no similar a lo que había a tope de gama hace año y medio. En general de modelos privados, en línea, lo que sea. El O3 Mini Higía, pues con esto tenemos algo mejor en absolutamente todo, no solo en inteligencia, sino en capacidad

multimodal. en ventana de contexto, en activar o desactivar cadena de razonamiento, etcétera. Vamos a crear un archivo punto bat ejecutarlo. Y dicho archivo punto bat, por ejemplo, nos va a ir quedando así para ser ejecutado con llama Server de Yama Cpp, el cual brinda tanto una interfaz web para utilizarlo

como un endpoint al estilo antropic y Open AI para conectarnos desde cualquier aplicación como lo puede ser Cloud Code Qen 3.54B 54B. Visión MTP para la predicción multitoken. Acelerar la generación de tokens 100% cargado en GPU. Estos son los hilos de mi procesador. Podemos

quitarlo si no queremos poner nada de eso. Cadena de razonamiento activa. Vamos a poner su ventana de contexto completa, 262,144 tokens. Los parámetros de ese ampleo voy a poner estos de por aquí, simplemente haciendo este cambio para evitar los bucles infinitos. Es un cambio que

recomienda tanto la gente de Quen como la gente de Unslot. No es 100% obligatorio, pero puede ayudar a evitar bucles infinitos. Después, por ejemplo, vamos a hacer que la KVK, la ventana de contexto esté cuantizada a 8 bits. Aún así, vamos a mantener bastante bien la calidad por la rotación de atención que

tiene Yama CPP al estilo Turbo Quant para una única respuesta a la vez, ver todos los logs de llama CPP en la consola y el parámetro que recomiendan para mejor visión. que pueda tomar en cuenta más cosas de la imagen a partir de que cada imagen de entrada consuma más tokens, como mínimo 1024. Con estos

ajustes, pues en este momento mi GPU está vacía y vamos a ver cuánto requiere una vez que esté en ejecución. Lo ejecutamos y nos está consumiendo 10.7 7 GB, teniendo en cuenta que buena parte de esto pues es la KV caché de la ventana de contexto completa tanto para el modelo como para el borrador y que

además lo tenemos cargado con todo y visión. La verdad es que está consumiendo, digamos, entre comillas, bastante memoria, pero porque tenemos el modelo a todo lo que da, hasta con MTP, visión, toda su ventana de contexto, etcétera. Si en este momento le hacemos alguna consulta, como por ejemplo, el

juego de Snake en HTML 5, vamos a ver qué velocidad nos da de generación de tokens. Y por aquí, luego de mil y tantos tokens, va en un promedio de 93 tokens por segundo. Generó en total 2,55 tokens. a un promedio de 93.06 tokens por segundo. Sigue ocupando lo mismo en la gráfica, eso no hay ningún

problema. Y pues vamos a previsualizar el código, pero así no es como lo queremos utilizar, así es como una especie de chat GPT. Nosotros lo que queremos es dentro de cloud code, chat GPT App similares, Open Code o qué s yo. Comúnmente lo hacemos funcionar en Pent

u Open Code. Sin embargo, el día de hoy pues vamos a probarlo en Cloud Code, cloud code CLI, que realmente funciona bastante bien y este modelo que puede usar tan bien herramientas pues debería de funcionar sin ningún problema. Entonces para ello voy a descargar Nodejs para mi sistema operativo porque

Cloud Code lo requiere y de hecho también voy a descargar Git. para programar como se debe con control de versiones y toda la cosa. Instalo Nodejs, instalo Git y ahora procedemos a buscar Cloud Code CLI. Aquí está el comando para instalarlo de las formas diferentes

que lo vayamos a hacer y nosotros, por ejemplo, lo vamos a instalar desde cmd en Windows. Así que copio el comando y en un cmd lo voy a pegar, presiono intro y aparentemente todo ya quedó instalado de forma correcta. Sin embargo, si lo abrimos en esta ocasión, pues se va a intentar conectar a una cuenta de cloud

y nosotros no queremos eso. Así que ahora, pues, tal como aquí nos puede decir en la guía de un slot o en cualquier lado, vamos a hacer que nos funcione en llama CPP. Para ello, en nuestro sistema operativo vamos a tener que agregar estas variables de entorno que van a indicar a cloud code hacia

dónde se tienen que conectar. Simplemente buscamos variables de entorno, entramos por aquí, le damos en nuevo, pego el nombre de cada una de las variables de entorno y ponemos la URL de hacia dónde se va a conectar. Mismo. Llama CPP ya incluye un endpo al estilo antropic, así que con esto debería de

funcionar. Simplemente tener en cuenta pues que debe de ser la URL correcta con todo y el puerto correcto. Le damos en aceptar. Ahora incluyo el siguiente valor, la siguiente variable de entorno y por último el modelo que vamos a utilizar. Una vez con estos ajustes le damos en aceptar a aceptar. Hay más

variables entorno para configurar más cosas, pero con esto ya funciona sin problema. Le damos en aceptar y ya la próxima vez que abramos un CMD debería de estar con las variables en torno actualizadas. Así que si escribimos cloud debería de funcionar. Para ello vamos a crear una carpeta en la que

vamos a probar lo que vamos a estar haciendo. Y si esquivo cloud y el flag para que no nos esté preguntando cada cosa, sino darle permisos ilimitados, cosa que tampoco es recomendable, pero para la prueba está bien. Vamos a lograr ejecutarlo y probarlo. Aquí nos hace la configuración inicial de el tema y demás

que queramos. Presiono intro, le doy en aceptar y ya estamos listos para utilizar Cloud Code con nuestro modelo Qen 3.54B. Reinicié. Llama CPP para ver que aquí está recién sin ninguna solicitud. Y ahora pues de hecho voy a separar esto simplemente para hacer lo siguiente y es

que vamos a hacer alguna consulta y vamos a ver si nos responde. Y si es que nos responde, asegurarnos de que quien nos está respondiendo pues es nuestro modelo en local, aunque lo vamos a notar por la calidad del mismo comparado contra Fable, por ejemplo, que pues claramente este es un modelo más simple,

pero igual funcional y también porque en llama CPP deberíamos de ver logs de que va generando tokens. Así que si en este momento le pregunto quién eres, presiono intro, vemos que en llama CPP rápidamente comienzan a suceder cosas y pues de este otro lado deberíamos de ver la respuesta. Y aquí está. Hola, soy

Cloud Code, el asistente oficial de programación en línea para cloud. Ya nos da información y demás y vemos que quién está funcionando, pues sí es nuestro modelo Qen 3.54B. Podemos buscar más a fondo todas las variables de entorno que existen para cloud code CLI para con ello pues lograr

configurar lo que nos haga falta. desde el tiempo de respuesta, la ventana de contexto, qué modelo va a funcionar para cada tipo de solicitud y demás. Y por aquí en la documentación oficial tenemos absolutamente todo, sin embargo, pues ya vemos que tampoco es que haga falta, pero de igual forma por aquí hay mucho

ajuste que se puede hacer simplemente agregando estas variables de entorno a nuestro sistema. Esto no es ningún truco, esto es algo oficial. Por eso Cloud Code pues lee dichas variables de entorno. En Cloud Code ni siquiera hicimos modificación, más bien Cloud Code busca estos valores. Voy a buscar

por ejemplo cómo instalar el MCP de Contex 7 en cloud code, presiono intro y pues aquí nos da una pequeña guía de cómo lo podemos hacer. De hecho, esta misma guía se la podemos pasar al modelo o podemos tener un documento. Voy a hacer un documento en la misma carpeta. dentro del mismo, pegué todo el manual y

a partir de ahí pues el mismo modelo puede encargarse de hacer las cosas, ni siquiera hace falta hacerlas nosotros. Simplemente aquí lo que quiero demostrar pues es que el modelo funciona y con todas las funcionalidades que puede ver aquí, incluido el agregar mps. Así que le voy a decir lee qué archivos tenemos

en la ruta actual. Presionamos intro, ahí comienza a ejecutar comandos y ya nos dice que lo que tenemos es contex 7.m. me dice, "¿Te gustaría que lea el contenido de este archivo?" Le voy a decir que sí. Lee el contenido y ahora nos va a responder. Ahí ya nos respondió y dice los pasos de cómo realizar estas

cosas. Y aquí entonces le voy a decir que lo implemente. Sí, impleméntalo en mi sistema. Claramente, comúnmente no hace falta estar viendo esto por acá, simplemente aquí es pues para demostrar que es con nuestro modelo de llama CPP. Aquí nos dice la herramienta está esperando tu selección. Tienes dos

opciones, MSP Server, CLI+ Skills. ¿Cuál opción prefieres? Voy a elegir la primera, por ejemplo, y vamos a ver si por sí solo logra seleccionar. Y aquí aparentemente ya todo funciona. Con Tex 7 MCP Server instalado exitosamente. Si en este momento nos vamos a MCPs, por aquí vemos que ya nos aparece este

context MSP. Voy a iniciar una nueva conversación y le voy a decir que consulte consulta en context MCP cómo hacer un label flotante en Bootstrap. No sé siquiera si eso existe, simplemente lo que queremos ver es que use la herramienta. Presionamos intro y aquí vemos que aparentemente está usando la

herramienta sin problemas. ya nos dio la información que consiguió en dicho MCP y dice, "Basado en mi conocimiento de Bootstrap y en documentación externa, aquí tienes cómo crear un label flotante usando Bootstrap." Ahí está. Realizó dos llamadas a context MCP, tal como estamos viendo, y con base en eso respondió.

Esto nos ayuda entonces a que si el modelo por sí solo no es muy potente, pues con las herramientas adecuadas lo podemos potenciar bastante. Ahora voy a intentar arrastrar una imagen directamente a la terminal y le voy a decir describe la imagen para ver si esto también está funcionando. En llama

CPP vemos que ocurren cosas y sí, funcionó sin problemas. También así puede entender las imágenes, describirlas simplemente arrastrándolas. ¿Y qué sucede si nosotros más bien le decimos, "Navega hasta la carpeta de imágenes de mi usuario y dime qué imágenes tengo." Y aquí luego de un rato

buscando hasta llegar a la carpeta de mi sistema, dice que en pictures, en mi carpeta de imágenes de mi usuario, únicamente tengo la imagen portada.jpg, que es la misma imagen que se mostró anteriormente, hasta se dio cuenta que es la misma. Así que vemos que en general bastante bien. Nunca ha fallado

el uso de una herramienta o algo así. Simplemente las habilidades totales del modelo pues van a depender no solo del modelo en sí y la cuantización en la que lo ejecutemos, sino de cómo le hacemos las peticiones, en qué arnés lo estemos ejecutando y también qué MCPs, qué skills, qué herramientas le tengamos

conectado, porque pues el modelo por sí solo a lo mejor no sabe de todo, ningún modelo sabe todo, pero a partir de los MCPs adecuados y todo ello, pues lo podemos hacer que hasta consulte en internet. Así que vemos que 100% es un modelo que se puede utilizar por aquí, puede usar herramientas, es en lo que

nunca falló y pues a partir de ahí puede ser una buena herramienta para trabajar, tanto para desarrollo o cualquier tipo de uso agéntico. Si quieres seguir viendo este tipo de videos, simplemente da like y suscríbete.
