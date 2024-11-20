# Proyecto de modelado multiagentes 2024-2

## Especificaciones del sistema modelado
El sistema modelado consiste en una red de agentes, cada uno controlado por un modelo LLM, con el objetivo de simular el comportamiento humano en términos de pensamiento lógico y emocional. Los agentes estarán diseñados para interactuar entre sí, utilizando varios estilos de toma de decisiones basados en aspectos psicológicos y cognitivos (e.g. necesidades básicas, razonamiento lógico matemático, interacciones interpersonales, respuestas emocionales, etc.) de tal forma que actúen como “jueces” y se decanten por una opción en conjunta a la hora de tomar decisiones.\
Cada agente consta de una “agenda” u objetivo interno que influirá en sus decisiones y comportamientos, de tal forma que al combinar estos agentes se obtenga un comportamiento de toma de decisiones cercano al humano. La idea es probar este sistema frente a entornos pre establecidos y documentar su comportamiento (e.g. ALFWorld, WebShop, ScienceWorld). 

## Importancia del sistema seleccionado
Entender el comportamiento humano en distintas situaciones es algo interesante e importante, ya que, comprender las consecuencias en la psique de una persona ante ciertas situaciones puede ayudar a enfrentarlas. Estudiar este tipo de efectos o comportamiento con personas reales es algo que está limitado por la ética, pero gracias a la validación de distintos artículos, es posible utilizar grandes modelos de lenguaje para simular estos comportamientos y observar uno similar al humano. 

## Motivación para tratar con ABMs
Los ABMs permiten modelar interacciones a nivel individual que al combinarse pueden generar dinámicas complejas a nivel de sistema, para este caso utilizar AMBs implica representar comportamientos en varios agentes diferentes, con perfiles distintos, de tal forma que se puedan estudiar las dinámicas emergentes de las diversas agendas en combinación para responder preguntas, explorar, superar pruebas de conocimiento, etc.
Es interesante pensar en las posibles combinaciones de agendas y cómo estas pueden variar el comportamiento general.

## Idea preliminar de los elementos a nivel microscópico
El o los agentes deben interactuar con el ambiente para resolver una situación o simplemente ver su respuesta a ellas. Un agente está compuesto por distintos mini-agentes cada uno representando una emoción, su objetivo es discutir entre sí para decidir qué hacer en un tiempo dado. Estos agentes (el principal y las emociones) interpretan e interactúan con el ambiente mediante lenguaje natural. Cada emoción se basará en el modelo Believe-Desire-Intention (BDI) para generar la discusión con sus contrapartes.

## Dinámicas macroscópicas deseables de reproducir
Existen dos opciones a probar:
- Toma de decisiones jerárquica: Cuando el Agente principal es quien finalmente decide que hacer luego de la discusión de sus emociones (mini-agentes).
- Toma de decisiones por iguales: Cuando las emociones no involucran al Agente principal tomando una decisión entre ellas, siendo éste simplemente una especie de vehículo.
Para ambas dinámicas se espera que el sistema pueda tomar decisiones respecto a los entornos establecidos, intentado minimizar problemas intrínsecos de los LLMs (sesgos, alucinaciones, rambling, etc).\

Cabe mencionar que en caso de que este sistema sea efectivo, se puede reducir el nivel de granularidad y convertir este sistema generado por múltiples agentes en un agente y así simular la interacción con pares (de forma similar a generative agents).

## Elementos de validación considerados
- Comparar con teorías psicológicas: (sentimientos, estados emocionales, composiciones de la personalidad) Comparación de los agentes respecto a modelos psicológicos establecidos (e.g. maslow, big five, contingencia) y si son capaces de acercarse a los comportamientos humanos en estas pruebas.
- Simulación de tareas reales: probar cómo los agentes resuelven tareas concretas en diferentes escenarios.
- Validación empírica: análisis comparativo entre comportamientos emergentes del sistema, probando diferentes combinaciones de agentes.
- Estabilidad y adaptabilidad del sistema: probar que tan sensible es el sistema a cambios de parámetros, personalidades y entornos.

## Tecnologías disponibles
NetLogo es la primera que se viene a la mente si se quiere optar por algo conocido y simple de implementar. Sin embargo hay que considerar un factor de escalabilidad en el caso de simular entornos más complejos, o si se piensa en algún momento utilizar muchos más agentes. Teniendo esto último en cuenta, las tecnologías más adecuadas sería Mason, que si bien es una herramienta desconocida para nosotros ofrece cubrir estos factores descritos previamente.
Por otro lado, para utilizar LLMs lo más común es hacer uso de python y bibliotecas contingentes como langhain.


science world requirements: 
sudo apt install default-jdk

wsl
venv
.env api key