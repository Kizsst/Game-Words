"""Haz un juego de pronunciacion de español a ingles para niños.
El juego debe tener varias categorias de palabras (frutas, animales, palabras comunes, palabras intermedias, palabras dificiles, comida, etc).
El juego debe mostrar una palabra, el niño debe repetirla y el juego debe evaluar la pronunciacion usando reconocimiento de voz y dar una puntuacion basada en la similitud entre lo que dijo el niño y la palabra correcta.
El juego debe ser divertido, con emojis y colores para hacerlo atractivo para los niños."""
import speech_recognition as sr
import pyttsx3
import os, sys
from difflib import SequenceMatcher
from colorama import Fore, Back, Style, init

init(autoreset=True)

CATEGORIAS = {
    "frutas_facil": {
        "emoji": "🍎",
        "dificultad": "Fácil",
        "palabras": [
            ("manzana", "apple"),
            ("plátano", "banana"),
            ("naranja", "orange"),
            ("fresa", "strawberry"),
            ("uva", "grape"),
            ("piña", "pineapple"),
            ("sandía", "watermelon"),
            ("durazno", "peach"),
            ("limón", "lemon"),
            ("cereza", "cherry"),
            ("mango", "mango"),
            ("papaya", "papaya"),
            ("kiwi", "kiwi"),
            ("frambuesa", "raspberry"),
            ("mora", "blackberry"),
            ("arándano", "blueberry"),
            ("coco", "coconut"),
            ("aguacate", "avocado"),
            ("pera", "pear"),
            ("dátil", "date"),
            ("higo", "fig"),
            ("melocotón", "peach"),
            ("albaricoque", "apricot"),
            ("ciruela", "plum"),
            ("açai", "acai"),
            ("carambola", "starfruit"),
            ("guanábana", "soursop"),
            ("maracuyá", "passion fruit"),
            ("lichi", "lychee"),
            ("tamarindo", "tamarind"),
        ]
    },
    "palabras_facil": {
        "emoji": "💬",
        "dificultad": "Fácil",
        "palabras": [
            ("hola", "hello"),
            ("gracias", "thank you"),
            ("por favor", "please"),
            ("adiós", "goodbye"),
            ("buenos días", "good morning"),
            ("de nada", "you are welcome"),
            ("perdón", "sorry"),
            ("ayuda", "help"),
            ("agua", "water"),
            ("comida", "food"),
            ("sí", "yes"),
            ("no", "no"),
            ("casa", "house"),
            ("coche", "car"),
            ("gato", "cat"),
            ("perro", "dog"),
            ("niño", "boy"),
            ("niña", "girl"),
            ("madre", "mother"),
            ("padre", "father"),
            ("hermano", "brother"),
            ("hermana", "sister"),
            ("amigo", "friend"),
            ("escuela", "school"),
            ("libro", "book"),
            ("pluma", "pen"),
            ("lápiz", "pencil"),
            ("mesa", "table"),
            ("silla", "chair"),
            ("puerta", "door"),
            ("ventana", "window"),
            ("luz", "light"),
            ("sol", "sun"),
            ("luna", "moon"),
            ("estrella", "star"),
            ("nube", "cloud"),
            ("lluvia", "rain"),
            ("nieve", "snow"),
            ("viento", "wind"),
            ("color", "color"),
            ("rojo", "red"),
            ("azul", "blue"),
            ("verde", "green"),
            ("amarillo", "yellow"),
            ("número", "number"),
            ("uno", "one"),
            ("dos", "two"),
            ("tres", "three"),
            ("cuatro", "four"),
            ("cinco", "five"),
            ("seis", "six"),
            ("siete", "seven"),
            ("ocho", "eight"),
            ("nueve", "nine"),
            ("diez", "ten"),
            ("cero", "zero"),
            ("tiempo", "time"),
            ("día", "day"),
            ("noche", "night"),
            ("mano", "hand"),
            ("pie", "foot"),
            ("cabeza", "head"),
            ("ojo", "eye"),
            ("oído", "ear"),
            ("nariz", "nose"),
            ("boca", "mouth"),
        ]
    },
    "palabras_intermedio": {
        "emoji": "📚",
        "dificultad": "Intermedio",
        "palabras": [
            ("paciencia", "patience"),
            ("curiosidad", "curiosity"),
            ("imaginación", "imagination"),
            ("dificultad", "difficulty"),
            ("velocidad", "speed"),
            ("generoso", "generous"),
            ("responsable", "responsible"),
            ("belleza", "beauty"),
            ("conocimiento", "knowledge"),
            ("experiencia", "experience"),
            ("inteligencia", "intelligence"),
            ("coraje", "courage"),
            ("amistad", "friendship"),
            ("honestidad", "honesty"),
            ("lealtad", "loyalty"),
            ("amabilidad", "kindness"),
            ("seguridad", "security"),
            ("libertad", "freedom"),
            ("justicia", "justice"),
            ("paz", "peace"),
            ("amor", "love"),
            ("alegría", "happiness"),
            ("tristeza", "sadness"),
            ("rabia", "anger"),
            ("miedo", "fear"),
            ("sorpresa", "surprise"),
            ("confianza", "confidence"),
            ("humildad", "humility"),
            ("orgullo", "pride"),
            ("vergüenza", "shame"),
            ("esperanza", "hope"),
            ("sueño", "dream"),
            ("deseo", "desire"),
            ("ambición", "ambition"),
            ("éxito", "success"),
            ("fracaso", "failure"),
            ("riesgo", "risk"),
            ("oportunidad", "opportunity"),
            ("desafío", "challenge"),
            ("victoria", "victory"),
            ("derrota", "defeat"),
            ("competencia", "competition"),
            ("cooperación", "cooperation"),
            ("conflicto", "conflict"),
            ("solución", "solution"),
            ("problema", "problem"),
            ("pregunta", "question"),
            ("respuesta", "answer"),
            ("idea", "idea"),
            ("pensamiento", "thought"),
            ("opinión", "opinion"),
            ("verdad", "truth"),
            ("mentira", "lie"),
            ("norma", "rule"),
            ("ley", "law"),
            ("derecho", "right"),
            ("deber", "duty"),
            ("obligación", "obligation"),
            ("promesa", "promise"),
            ("acuerdo", "agreement"),
            ("negocio", "business"),
            ("comercio", "commerce"),
            ("industria", "industry"),
            ("arte", "art"),
            ("música", "music"),
            ("danza", "dance"),
        ]
    },
    "oraciones_dificil": {
        "emoji": "🧠",
        "dificultad": "Difícil",
        "palabras": [
            ("Me gustaría aprender inglés", "I would like to learn English"),
            ("¿Cuál es tu nombre?", "What is your name?"),
            ("Tengo mucho que hacer hoy", "I have a lot to do today"),
            ("No entiendo lo que dices", "I do not understand what you are saying"),
            ("¿Dónde está la estación de tren?", "Where is the train station?"),
            ("Me encanta pasar tiempo con mis amigos", "I love spending time with my friends"),
            ("Necesito ayuda con mi tarea", "I need help with my homework"),
            ("¿Cuánto cuesta este libro?", "How much does this book cost?"),
            ("Mi nombre es Juan", "My name is Juan"),
            ("¿De dónde eres?", "Where are you from?"),
            ("Soy de España", "I am from Spain"),
            ("¿Cuántos años tienes?", "How old are you?"),
            ("Tengo diez años", "I am ten years old"),
            ("¿Cuál es tu comida favorita?", "What is your favorite food?"),
            ("Me gusta mucho la pizza", "I like pizza very much"),
            ("¿Qué haces en tu tiempo libre?", "What do you do in your free time?"),
            ("Leo libros y juego con mis amigos", "I read books and play with my friends"),
            ("¿Cuál es tu color favorito?", "What is your favorite color?"),
            ("Mi color favorito es azul", "My favorite color is blue"),
            ("¿Tienes mascotas en casa?", "Do you have pets at home?"),
            ("Sí, tengo un perro y un gato", "Yes, I have a dog and a cat"),
            ("Me gusta estudiar matemáticas", "I like studying mathematics"),
            ("¿A qué hora va a la escuela?", "What time do you go to school?"),
            ("Voy a la escuela a las ocho de la mañana", "I go to school at eight in the morning"),
            ("¿Cuál es tu asignatura favorita?", "What is your favorite subject?"),
            ("La ciencia es muy interesante", "Science is very interesting"),
            ("¿Qué quieres ser cuando crezcas?", "What do you want to be when you grow up?"),
            ("Quiero ser ingeniero", "I want to be an engineer"),
            ("¿Te gustaría viajar?", "Would you like to travel?"),
            ("Sí, me gustaría viajar por todo el mundo", "Yes, I would like to travel around the world"),
            ("¿Cuál es tu película favorita?", "What is your favorite movie?"),
            ("Me encanta la película de superhéroes", "I love superhero movies"),
            ("¿Qué hiciste el fin de semana?", "What did you do last weekend?"),
            ("Jugué fútbol con mis amigos en el parque", "I played football with my friends in the park"),
            ("¿Te gusta la música?", "Do you like music?"),
            ("Sí, me gusta mucho la música rock", "Yes, I like rock music very much"),
            ("¿Hablas otro idioma?", "Do you speak another language?"),
            ("Hablo español e inglés", "I speak Spanish and English"),
            ("¿Cuál es tu fruta favorita?", "What is your favorite fruit?"),
            ("Mi fruta favorita es la manzana", "My favorite fruit is the apple"),
            ("¿Desayunaste esta mañana?", "Did you have breakfast this morning?"),
            ("Sí, desayuné cereales y jugo de naranja", "Yes, I had cereal and orange juice"),
            ("¿Cuándo es tu cumpleaños?", "When is your birthday?"),
            ("Mi cumpleaños es en julio", "My birthday is in July"),
            ("¿Qué regalos recibiste en tu último cumpleaños?", "What gifts did you receive for your last birthday?"),
            ("Recibí una bicicleta y un videojuego", "I received a bicycle and a video game"),
            ("¿Cuál es el día de la semana que más te gusta?", "What is your favorite day of the week?"),
            ("Me gusta el sábado porque no hay escuela", "I like Saturday because there is no school"),
            ("¿Cómo fue tu día en la escuela?", "How was your day at school?"),
            ("Fue muy bueno, aprendí muchas cosas nuevas", "It was very good, I learned many new things"),
            ("¿Tienes hermanos o hermanas?", "Do you have brothers or sisters?"),
            ("Tengo un hermano y una hermana", "I have a brother and a sister"),
            ("¿Cuál es tu deporte favorito?", "What is your favorite sport?"),
            ("Me encanta jugar al baloncesto", "I love playing basketball"),
            ("¿Nunca has viajado en avión?", "Have you ever traveled by plane?"),
            ("Sí, una vez fui en avión a Francia", "Yes, I once flew to France"),
            ("¿Qué se te hace más difícil en la escuela?", "What is most difficult for you at school?"),
            ("Las matemáticas son bastante difíciles para mí", "Mathematics is quite difficult for me"),
        ]
    },
    "tecnologia_pro": {
        "emoji": "💻",
        "dificultad": "Intermedio",
        "palabras": [
            ("computadora", "computer"),
            ("teclado", "keyboard"),
            ("ratón", "mouse"),
            ("pantalla", "screen"),
            ("red", "network"),
            ("programación", "programming"),
        ]
    },
}

class Juego:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        self.puntos = 0
        self.categoria = None
        
    def limpiar(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def titulo(self):
        print(f"\n{Back.CYAN}{Fore.BLACK}{'='*50}\n  🎤 PRONUNCIACIÓN EN INGLÉS 🎤\n{'='*50}{Style.RESET_ALL}\n")
    
    def hablar(self, texto):
        texto_limpio = texto.replace('_', ' ')
        self.tts.say(texto_limpio)
        self.tts.runAndWait()
    
    def escuchar(self):
        try:
            print(f"{Fore.YELLOW}🎤 Escuchando...{Style.RESET_ALL}")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
            try:
                return self.recognizer.recognize_google(audio, language='en-US').lower()
            except sr.UnknownValueError:
                return "TIMEOUT"
        except sr.WaitTimeoutError:
            return "TIMEOUT"
        except sr.RequestError:
            print(f"{Fore.RED}⚠️ Sin internet{Style.RESET_ALL}")
            return None
        except Exception as e:
            return "TIMEOUT"
    
    def similitud(self, p1, p2):
        p1 = p1.replace('_', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        p2 = p2.replace('_', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        return SequenceMatcher(None, p1, p2).ratio()
    
    def menu(self):
        self.limpiar()
        self.titulo()
        print(f"{Fore.GREEN}Elige una categoría:{Style.RESET_ALL}\n")
        
        cats = list(CATEGORIAS.items())
        for i, (nombre, data) in enumerate(cats, 1):
            print(f"  {Fore.CYAN}{i}{Style.RESET_ALL}. {data['emoji']} {nombre.upper()} ({data['dificultad']})")
        print(f"  {Fore.RED}0{Style.RESET_ALL}. Salir\n")
        
        while True:
            try:
                op = int(input(f"{Fore.YELLOW}Elige: {Style.RESET_ALL}"))
                if op == 0:
                    print(f"\n{Fore.MAGENTA}¡Hasta luego! 👋\n{Style.RESET_ALL}")
                    return "SALIR"
                elif 1 <= op <= len(cats):
                    self.categoria = cats[op-1][0]
                    return "OK"
            except:
                pass
    
    def menu_game_over(self):
        while True:
            self.limpiar()
            print(f"{Back.RED}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE}{'':>15}⏰ GAME OVER ⏰{'':>15}{Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
            print(f"\n{Fore.RED}😢 No escuché nada en el tiempo límite{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Puntos acumulados: {self.puntos}{Style.RESET_ALL}\n")
            print(f"{Back.RED}{Fore.WHITE}{'='*50}{Style.RESET_ALL}\n")
            
            print(f"{Fore.GREEN}¿Qué deseas hacer?{Style.RESET_ALL}\n")
            print(f"  {Fore.CYAN}1{Style.RESET_ALL}. Repetir esta categoría")
            print(f"  {Fore.CYAN}2{Style.RESET_ALL}. Cambiar de categoría")
            print(f"  {Fore.RED}3{Style.RESET_ALL}. Salir\n")
            
            try:
                op = int(input(f"{Fore.YELLOW}Elige: {Style.RESET_ALL}"))
                if op == 1:
                    return "REPETIR"
                elif op == 2:
                    return "CAMBIAR"
                elif op == 3:
                    print(f"\n{Fore.MAGENTA}¡Hasta luego! 👋\n{Style.RESET_ALL}")
                    return "SALIR"
            except:
                pass
    
    def game_over(self):
        return self.menu_game_over()
    
    def ronda(self, palabra_es, palabra_en, num, total):
        self.limpiar()
        self.titulo()
        cat_data = CATEGORIAS[self.categoria]
        print(f"{cat_data['emoji']} {Fore.CYAN}{self.categoria.upper()}{Style.RESET_ALL} - {Fore.YELLOW}{cat_data['dificultad']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Pregunta {num}/{total} | Puntos: {self.puntos}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}Pronuncia en INGLÉS:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{palabra_es.upper()}{Style.RESET_ALL}\n")
        
        respuesta = self.escuchar()
        if respuesta == "TIMEOUT":
            return "GAMEOVER"
        if not respuesta:
            return False
        
        sim = self.similitud(palabra_en, respuesta)
        print(f"\n{Fore.CYAN}Dijiste: {Fore.YELLOW}{respuesta.upper()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Esperado: {Fore.YELLOW}{palabra_en.upper()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Exactitud: {Fore.MAGENTA}{sim*100:.0f}%{Style.RESET_ALL}\n")
        
        if sim >= 0.85:
            print(f"{Fore.GREEN}🎉 ¡PERFECTO!{Style.RESET_ALL}")
            self.puntos += 10
            resultado = True
        elif sim >= 0.70:
            print(f"{Fore.GREEN}👍 ¡BIEN!{Style.RESET_ALL}")
            self.puntos += 7
            resultado = True
        elif sim >= 0.50:
            print(f"{Fore.YELLOW}😊 Aceptable{Style.RESET_ALL}")
            self.puntos += 3
            resultado = True
        else:
            print(f"{Fore.RED}❌ Incorrecto{Style.RESET_ALL}")
            resultado = False
        
        input(f"\n{Fore.CYAN}ENTER para continuar...{Style.RESET_ALL}")
        return resultado
    
    def jugar(self):
        cat_data = CATEGORIAS[self.categoria]
        palabras = cat_data["palabras"]
        emoji = cat_data["emoji"]
        correctas = 0
        
        for i, (palabra_es, palabra_en) in enumerate(palabras, 1):
            resultado = self.ronda(palabra_es, palabra_en, i, len(palabras))
            if resultado == "GAMEOVER":
                accion = self.game_over()
                if accion == "REPETIR":
                    self.puntos = 0
                    return self.jugar()
                elif accion == "CAMBIAR":
                    return "CAMBIAR"
                elif accion == "SALIR":
                    return "SALIR"
            elif resultado:
                correctas += 1
        
        self.limpiar()
        self.titulo()
        porcentaje = (correctas / len(palabras)) * 100
        
        print(f"{emoji} Categoría: {self.categoria.upper()}")
        print(f"{Fore.YELLOW}Correctas: {correctas}/{len(palabras)}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Puntos: {self.puntos}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Exactitud: {porcentaje:.0f}%{Style.RESET_ALL}\n")
        
        if porcentaje == 100:
            print(f"{Fore.GREEN}🏆 ¡CAMPEÓN!{Style.RESET_ALL}")
        elif porcentaje >= 80:
            print(f"{Fore.GREEN}🌟 ¡EXCELENTE!{Style.RESET_ALL}")
        elif porcentaje >= 60:
            print(f"{Fore.YELLOW}👏 ¡BIEN!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}💪 ¡Sigue practicando!{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}ENTER para continuar...{Style.RESET_ALL}")
    
    def run(self):
        while True:
            resultado = self.menu()
            if resultado == "SALIR":
                break
            self.puntos = 0
            resultado_juego = self.jugar()
            if resultado_juego == "SALIR":
                break

if __name__ == "__main__":
    try:
        juego = Juego()
        juego.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}¡Juego interrumpido!{Style.RESET_ALL}\n")
        sys.exit()
